#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
import json
import re
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parents[1]
PROJECTS_FILE = ROOT / "data" / "projects.yaml"
REPORT_DIR = ROOT / "reports" / "verification"


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping")
    return data


def github_repo_from_url(url: str) -> str | None:
    parsed = urlparse(url)
    if parsed.netloc.lower() != "github.com":
        return None
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) < 2:
        return None
    owner, repo = parts[0], parts[1]
    repo = re.sub(r"\.git$", "", repo)
    return f"{owner}/{repo}"


def gh_repo_view(repo: str) -> dict[str, Any]:
    fields = [
        "nameWithOwner",
        "url",
        "description",
        "isArchived",
        "isEmpty",
        "isFork",
        "isPrivate",
        "stargazerCount",
        "forkCount",
        "licenseInfo",
        "defaultBranchRef",
        "pushedAt",
        "updatedAt",
    ]
    last_error = ""
    for attempt in range(3):
        proc = subprocess.run(
            ["gh", "repo", "view", repo, "--json", ",".join(fields)],
            cwd=ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
        if proc.returncode == 0:
            payload = json.loads(proc.stdout)
            payload["repo"] = repo
            payload["ok"] = True
            payload["verified_by"] = "gh repo view"
            return payload
        last_error = proc.stderr.strip() or proc.stdout.strip()
        time.sleep(1 + attempt)

    rest_payload = github_rest_repo_view(repo)
    if rest_payload.get("ok"):
        rest_payload["gh_error"] = last_error
        return rest_payload
    return {"repo": repo, "ok": False, "error": last_error or rest_payload.get("error", "")}


def github_rest_repo_view(repo: str) -> dict[str, Any]:
    url = f"https://api.github.com/repos/{repo}"
    headers = {
        "Accept": "application/vnd.github+json",
        "User-Agent": "multi-agent-review-verify",
    }
    token_proc = subprocess.run(
        ["gh", "auth", "token"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
        check=False,
    )
    if token_proc.returncode == 0 and token_proc.stdout.strip():
        headers["Authorization"] = f"Bearer {token_proc.stdout.strip()}"
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=20) as resp:
            payload = json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as e:
        return {"repo": repo, "ok": False, "error": f"REST HTTP {e.code}"}
    except Exception as e:
        return {"repo": repo, "ok": False, "error": f"REST {e}"}

    license_payload = payload.get("license") or {}
    return {
        "repo": repo,
        "ok": True,
        "verified_by": "GitHub REST API",
        "nameWithOwner": payload.get("full_name", repo),
        "url": payload.get("html_url", f"https://github.com/{repo}"),
        "description": payload.get("description"),
        "isArchived": bool(payload.get("archived")),
        "isEmpty": payload.get("size") == 0,
        "isFork": bool(payload.get("fork")),
        "isPrivate": bool(payload.get("private")),
        "stargazerCount": payload.get("stargazers_count", 0),
        "forkCount": payload.get("forks_count", 0),
        "licenseInfo": {"spdxId": license_payload.get("spdx_id") or ""},
        "defaultBranchRef": {"name": payload.get("default_branch") or ""},
        "pushedAt": payload.get("pushed_at") or "",
        "updatedAt": payload.get("updated_at") or "",
    }


def main() -> None:
    projects = load_yaml(PROJECTS_FILE)["projects"]
    github_items: list[dict[str, Any]] = []
    non_github_items: list[dict[str, Any]] = []

    for item in projects:
        repo = github_repo_from_url(str(item["repo_url"]))
        if repo:
            github_items.append({**item, "github_repo": repo})
        else:
            non_github_items.append(item)

    results = []
    seen: set[str] = set()
    for item in github_items:
        repo = item["github_repo"]
        if repo in seen:
            continue
        seen.add(repo)
        results.append(gh_repo_view(repo))

    ok = [r for r in results if r.get("ok")]
    failed = [r for r in results if not r.get("ok")]
    archived = [r for r in ok if r.get("isArchived")]
    private = [r for r in ok if r.get("isPrivate")]
    empty = [r for r in ok if r.get("isEmpty")]

    date_stamp = dt.date.today().isoformat()
    json_path = REPORT_DIR / f"{date_stamp}-github-projects.json"
    md_path = REPORT_DIR / f"{date_stamp}-github-projects.md"
    REPORT_DIR.mkdir(parents=True, exist_ok=True)

    json_payload = {
        "generated_at": dt.datetime.now(dt.timezone.utc).isoformat(),
        "total_projects": len(projects),
        "github_project_rows": len(github_items),
        "unique_github_repos": len(results),
        "verified": len(ok),
        "failed": len(failed),
        "archived": len(archived),
        "private": len(private),
        "empty": len(empty),
        "non_github_projects": [
            {
                "name": item["name"],
                "category": item["category"],
                "repo_url": item["repo_url"],
            }
            for item in non_github_items
        ],
        "results": results,
    }
    json_path.write_text(json.dumps(json_payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    lines: list[str] = []
    lines.append("# GitHub Project Verification Report")
    lines.append("")
    lines.append(f"- Generated at: `{json_payload['generated_at']}`")
    lines.append(f"- Total project rows: `{len(projects)}`")
    lines.append(f"- GitHub project rows: `{len(github_items)}`")
    lines.append(f"- Unique GitHub repositories checked: `{len(results)}`")
    lines.append(f"- Verified by `gh repo view`: `{len(ok)}`")
    lines.append(f"- Failed: `{len(failed)}`")
    lines.append(f"- Archived: `{len(archived)}`")
    lines.append(f"- Private: `{len(private)}`")
    lines.append(f"- Empty: `{len(empty)}`")
    lines.append(f"- Non-GitHub project/reference rows: `{len(non_github_items)}`")
    lines.append("")
    lines.append("## Failed GitHub Checks")
    lines.append("")
    if failed:
        for r in failed:
            lines.append(f"- `{r['repo']}`: {r.get('error', '')}")
    else:
        lines.append("- None")
    lines.append("")
    lines.append("## Non-GitHub Project/Reference Rows")
    lines.append("")
    if non_github_items:
        lines.append("| Name | Category | URL |")
        lines.append("| --- | --- | --- |")
        for item in non_github_items:
            lines.append(f"| {item['name']} | {item['category']} | {item['repo_url']} |")
    else:
        lines.append("- None")
    lines.append("")
    lines.append("## Verified GitHub Repositories")
    lines.append("")
    lines.append("| Repository | Stars | Forks | Archived | Default branch | Updated | Pushed | License |")
    lines.append("| --- | ---: | ---: | --- | --- | --- | --- | --- |")
    for r in sorted(ok, key=lambda x: str(x["nameWithOwner"]).lower()):
        branch = (r.get("defaultBranchRef") or {}).get("name", "")
        license_name = (r.get("licenseInfo") or {}).get("spdxId", "") or "-"
        lines.append(
            "| "
            + " | ".join(
                [
                    f"[{r['nameWithOwner']}]({r['url']})",
                    str(r.get("stargazerCount", "")),
                    str(r.get("forkCount", "")),
                    str(r.get("isArchived", "")),
                    branch,
                    str(r.get("updatedAt", "")),
                    str(r.get("pushedAt", "")),
                    license_name,
                ]
            )
            + " |"
        )
    lines.append("")
    md_path.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote report: {md_path}")
    print(f"Wrote data: {json_path}")

    if failed:
        print("GitHub verification failed.")
        for r in failed:
            print(f"- {r['repo']}: {r.get('error', '')}")
        sys.exit(1)
    print("GitHub verification passed.")


if __name__ == "__main__":
    main()
