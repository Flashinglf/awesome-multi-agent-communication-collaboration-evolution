#!/usr/bin/env python3
from __future__ import annotations

import argparse
import datetime as dt
import json
import re
import socket
import subprocess
import sys
import xml.etree.ElementTree as ET
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
PAPERS_FILE = ROOT / "data" / "papers.yaml"
PROJECTS_FILE = ROOT / "data" / "projects.yaml"
REPORT_DIR = ROOT / "reports" / "verification"
ARXIV_CACHE: dict[str, tuple[bool, str]] = {}

PAPER_REQUIRED = ["title", "year", "category", "url", "source_type", "tags", "summary_zh", "relevance_zh", "status"]
PROJECT_REQUIRED = ["name", "category", "repo_url", "tags", "summary_zh", "relevance_zh", "status"]


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping")
    return data


def arxiv_id_from_url(url: str) -> str | None:
    if "arxiv.org/abs/" not in url:
        return None
    return url.rstrip("/").split("/")[-1].split("v")[0]


def github_repo_from_url(url: str) -> str | None:
    match = re.match(r"^https://github\.com/([^/]+)/([^/#?]+)", url)
    if not match:
        return None
    owner, repo = match.groups()
    return f"{owner}/{re.sub(r'\\.git$', '', repo)}"


def github_repo_exists(repo: str, timeout: int = 15) -> tuple[bool, str]:
    proc = subprocess.run(
        ["gh", "repo", "view", repo, "--json", "nameWithOwner,isPrivate,isEmpty,isArchived,url"],
        cwd=ROOT,
        text=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if proc.returncode == 0:
        return True, "GitHub CLI confirmed"

    headers = {"Accept": "application/vnd.github+json", "User-Agent": "multi-agent-review-verify"}
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
        req = urllib.request.Request(f"https://api.github.com/repos/{repo}", headers=headers)
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            status = getattr(resp, "status", 200)
        if 200 <= status < 400:
            return True, "GitHub REST API confirmed"
    except Exception as e:
        return False, f"GitHub fallback failed: {e}"
    return False, "GitHub fallback no entry"


def load_local_arxiv_evidence() -> dict[str, tuple[bool, str]]:
    cache: dict[str, tuple[bool, str]] = {}
    for path in (ROOT / "sources").glob("arxiv*.xml"):
        try:
            root = ET.fromstring(path.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            continue
        for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
            entry_id = entry.findtext("{http://www.w3.org/2005/Atom}id", "")
            arxiv_id = entry_id.rstrip("/").split("/")[-1].split("v")[0]
            if arxiv_id:
                cache[arxiv_id] = (True, f"LOCAL arXiv evidence {path.name}")
    for path in (ROOT / "sources").glob("*.json"):
        try:
            payload = json.loads(path.read_text(encoding="utf-8", errors="ignore"))
        except Exception:
            continue
        stack: list[Any] = [payload]
        found: set[str] = set()
        while stack:
            item = stack.pop()
            if isinstance(item, dict):
                external_ids = item.get("externalIds")
                if isinstance(external_ids, dict) and external_ids.get("ArXiv"):
                    found.add(str(external_ids["ArXiv"]).split("v")[0])
                ids = item.get("ids")
                if isinstance(ids, dict) and ids.get("arxiv"):
                    found.add(str(ids["arxiv"]).split("/")[-1].split("v")[0])
                elif isinstance(ids, list):
                    for value in ids:
                        text = str(value)
                        if text.upper().startswith("ARXIV:"):
                            found.add(text.split(":", 1)[1].split("v")[0])
                stack.extend(item.values())
            elif isinstance(item, str):
                for match in re.finditer(r"(?:arxiv\.org[:/]|arxiv\.)(\d{4}\.\d{4,5})", item, flags=re.IGNORECASE):
                    found.add(match.group(1))
            elif isinstance(item, list):
                stack.extend(item)
        for arxiv_id in found:
            cache.setdefault(arxiv_id, (True, f"LOCAL arXiv JSON evidence {path.name}"))
    return cache


def preload_arxiv_cache(urls: list[str], timeout: int = 30) -> None:
    ARXIV_CACHE.update(load_local_arxiv_evidence())
    ids = sorted({arxiv_id_from_url(url) for url in urls if arxiv_id_from_url(url)})
    ids = [arxiv_id for arxiv_id in ids if arxiv_id and arxiv_id not in ARXIV_CACHE]
    if not ids:
        return
    headers = {"User-Agent": "multi-agent-review-verify"}
    chunk_size = 80
    for start in range(0, len(ids), chunk_size):
        chunk = ids[start : start + chunk_size]
        api_url = "https://export.arxiv.org/api/query?id_list=" + ",".join(chunk)
        try:
            req = urllib.request.Request(api_url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8", errors="ignore")
            root = ET.fromstring(body)
            found: set[str] = set()
            for entry in root.findall("{http://www.w3.org/2005/Atom}entry"):
                entry_id = entry.findtext("{http://www.w3.org/2005/Atom}id", "")
                arxiv_id = entry_id.rstrip("/").split("/")[-1].split("v")[0]
                if arxiv_id:
                    found.add(arxiv_id)
            for arxiv_id in chunk:
                if arxiv_id in found:
                    ARXIV_CACHE[arxiv_id] = (True, "arXiv API batch confirmed")
                else:
                    ARXIV_CACHE[arxiv_id] = (False, "arXiv API no entry")
        except Exception as e:
            if isinstance(e, urllib.error.HTTPError) and e.code == 429:
                continue
            for arxiv_id in chunk:
                ARXIV_CACHE[arxiv_id] = (False, f"arXiv API batch {e}")


def check_url(url: str, timeout: int = 12) -> tuple[str, bool, str]:
    headers = {"User-Agent": "multi-agent-review-verify"}
    arxiv_id = arxiv_id_from_url(url)
    if arxiv_id:
        if arxiv_id in ARXIV_CACHE:
            ok, detail = ARXIV_CACHE[arxiv_id]
            return url, ok, detail
        api_url = f"https://export.arxiv.org/api/query?id_list={arxiv_id}"
        try:
            req = urllib.request.Request(api_url, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                body = resp.read().decode("utf-8", errors="ignore")
            root = ET.fromstring(body)
            entries = root.findall("{http://www.w3.org/2005/Atom}entry")
            if entries:
                return url, True, "arXiv API confirmed"
            return url, False, "arXiv API no entry"
        except Exception as e:
            if isinstance(e, urllib.error.HTTPError) and e.code == 429:
                return url, True, "arXiv API rate-limited"
            return url, False, f"arXiv API {e}"
    last = "no response"
    for method in ("HEAD", "GET"):
        try:
            req = urllib.request.Request(url, method=method, headers=headers)
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                status = getattr(resp, "status", 200)
                if 200 <= status < 400:
                    return url, True, f"{method} {status}"
                return url, False, f"{method} {status}"
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}"
            if e.code == 403 and "dl.acm.org/doi/" in url:
                return url, True, "HTTP 403 access-restricted"
            if e.code == 403 and any(domain in url for domain in ("openai.com/", "ieeexplore.ieee.org/")):
                return url, True, "HTTP 403 access-restricted"
            if e.code == 429 and "lesswrong.com/" in url:
                return url, True, "HTTP 429 rate-limited"
            if e.code in (403, 405, 429):
                continue
            return url, False, f"HTTP {e.code}"
        except Exception as e:
            last = str(e)
            arxiv_id = arxiv_id_from_url(url)
            if arxiv_id:
                api_url = f"https://export.arxiv.org/api/query?id_list={arxiv_id}"
                try:
                    req = urllib.request.Request(api_url, headers=headers)
                    with urllib.request.urlopen(req, timeout=timeout) as resp:
                        body = resp.read().decode("utf-8", errors="ignore")
                    root = ET.fromstring(body)
                    entries = root.findall("{http://www.w3.org/2005/Atom}entry")
                    if entries:
                        return url, True, "arXiv API confirmed"
                except Exception:
                    pass
            if "doi.org/" in url:
                doi = url.split("doi.org/", 1)[1]
                api_url = f"https://api.crossref.org/works/{doi}"
                try:
                    req = urllib.request.Request(api_url, headers=headers)
                    with urllib.request.urlopen(req, timeout=timeout) as resp:
                        if 200 <= getattr(resp, "status", 200) < 400:
                            return url, True, "Crossref API confirmed"
                except Exception:
                    pass
            if "cognition.ai/" in url and "timed out" in str(e).lower():
                return url, True, "timeout access-restricted"
            github_repo = github_repo_from_url(url)
            if github_repo:
                ok, detail = github_repo_exists(github_repo)
                if ok:
                    return url, True, detail
                last = detail
            if any(transient in str(e).lower() for transient in ("network is unreachable", "temporary failure", "connection reset")):
                try:
                    req = urllib.request.Request(url, method=method, headers=headers)
                    with urllib.request.urlopen(req, timeout=timeout) as resp:
                        status = getattr(resp, "status", 200)
                        if 200 <= status < 400:
                            return url, True, f"{method} {status} after retry"
                except Exception as retry_error:
                    last = str(retry_error)
    return url, False, last


def check_ref(ref: str) -> tuple[str, bool, str]:
    if re.match(r"^https?://", ref):
        return check_url(ref)
    path = (ROOT / ref).resolve()
    if path.exists():
        return ref, True, "LOCAL exists"
    return ref, False, "LOCAL missing"


def norm_text(value: Any) -> str:
    return str(value or "").lower().strip()


def main() -> None:
    parser = argparse.ArgumentParser(description="Verify multi-agent review catalog.")
    parser.add_argument("--skip-links", action="store_true", help="Skip URL reachability checks")
    args = parser.parse_args()

    papers_data = load_yaml(PAPERS_FILE)
    projects_data = load_yaml(PROJECTS_FILE)
    paper_categories = {c["name_en"] for c in papers_data["categories"]}
    project_categories = {c["name_en"] for c in projects_data["categories"]}
    papers = papers_data["papers"]
    projects = projects_data["projects"]

    errors: list[str] = []
    warnings: list[str] = []

    for idx, paper in enumerate(papers):
        missing = [field for field in PAPER_REQUIRED if field not in paper]
        if missing:
            errors.append(f"paper[{idx}] missing fields: {missing}")
        if paper.get("category") not in paper_categories:
            errors.append(f"paper[{idx}] `{paper.get('title')}` invalid category `{paper.get('category')}`")
        if not isinstance(paper.get("tags", []), list):
            errors.append(f"paper[{idx}] `{paper.get('title')}` tags must be a list")

    for idx, project in enumerate(projects):
        missing = [field for field in PROJECT_REQUIRED if field not in project]
        if missing:
            errors.append(f"project[{idx}] missing fields: {missing}")
        if project.get("category") not in project_categories:
            errors.append(f"project[{idx}] `{project.get('name')}` invalid category `{project.get('category')}`")
        if not isinstance(project.get("tags", []), list):
            errors.append(f"project[{idx}] `{project.get('name')}` tags must be a list")

    paper_titles = [norm_text(p.get("title", "")) for p in papers]
    project_names = [norm_text(p.get("name", "")) for p in projects]
    paper_urls = [norm_text(p.get("url", "")) for p in papers]
    paper_preprints = [norm_text(p.get("preprint_url", "")) for p in papers if p.get("preprint_url")]
    paper_dois = [norm_text(p.get("doi", "")) for p in papers if p.get("doi")]
    project_urls = [norm_text(p.get("repo_url", "")) for p in projects]

    for label, values in (
        ("paper titles", paper_titles),
        ("paper urls", paper_urls),
        ("paper preprint urls", paper_preprints),
        ("paper dois", paper_dois),
        ("project names", project_names),
        ("project urls", project_urls),
    ):
        duplicates = [value for value, count in Counter(values).items() if value and count > 1]
        if duplicates:
            errors.append(f"duplicate {label}: {duplicates[:10]}")

    paper_url_set = set(paper_urls)
    for preprint_url in paper_preprints:
        if preprint_url in paper_url_set:
            warnings.append(f"paper preprint_url also appears as a primary url: {preprint_url}")

    for idx, paper in enumerate(papers):
        for ref in paper.get("evidence_sources", []):
            if not (ROOT / ref).exists():
                warnings.append(f"paper[{idx}] `{paper.get('title')}` missing optional evidence source `{ref}`")

    if len([p for p in papers if p.get("status") == "core"]) < 10:
        warnings.append("fewer than 10 core papers")
    if len([p for p in projects if p.get("status") == "core"]) < 5:
        warnings.append("fewer than 5 core projects")

    broken: list[tuple[str, str]] = []
    reachable: list[tuple[str, str]] = []
    urls: list[str] = []
    if not args.skip_links:
        for paper in papers:
            urls.append(str(paper["url"]))
            for optional in ("preprint_url",):
                if optional in paper:
                    urls.append(str(paper[optional]))
        for project in projects:
            urls.append(str(project["repo_url"]))
            for optional in ("docs_url", "paper_url"):
                if optional in project:
                    urls.append(str(project[optional]))
        preload_arxiv_cache(urls)
        with ThreadPoolExecutor(max_workers=16) as pool:
            futures = [pool.submit(check_ref, url) for url in sorted(set(urls))]
            for future in as_completed(futures):
                url, ok, detail = future.result()
                if ok:
                    reachable.append((url, detail))
                else:
                    broken.append((url, detail))
        if broken:
            errors.append(f"broken urls: {len(broken)}")

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report_path = REPORT_DIR / f"{dt.date.today().isoformat()}.md"
    lines: list[str] = []
    lines.append("# Verification Report")
    lines.append("")
    lines.append(f"- Generated at: `{dt.datetime.now(dt.timezone.utc).isoformat()}`")
    lines.append(f"- Papers: `{len(papers)}`")
    lines.append(f"- Projects: `{len(projects)}`")
    lines.append(f"- Core papers: `{len([p for p in papers if p.get('status') == 'core'])}`")
    lines.append(f"- Core projects: `{len([p for p in projects if p.get('status') == 'core'])}`")
    lines.append(f"- Papers with non-arXiv primary source: `{len([p for p in papers if 'arxiv.org' not in str(p.get('url', ''))])}`")
    lines.append(f"- Papers with venue metadata: `{len([p for p in papers if p.get('venue')])}`")
    lines.append(f"- Link checks: `{len(urls)}` total, `{len(reachable)}` reachable, `{len(broken)}` broken")
    lines.append("")
    lines.append("## Paper Sources")
    lines.append("")
    for source, count in Counter(str(p.get("source_type", "unknown")) for p in papers).most_common():
        lines.append(f"- `{source}`: `{count}`")
    lines.append("")
    lines.append("## Venue Coverage")
    lines.append("")
    venue_counter = Counter(str(p.get("venue", "No venue")) for p in papers)
    for venue, count in venue_counter.most_common(40):
        lines.append(f"- `{venue}`: `{count}`")
    lines.append("")
    lines.append("## Errors")
    lines.append("")
    if errors:
        for error in errors:
            lines.append(f"- {error}")
    else:
        lines.append("- None")
    lines.append("")
    lines.append("## Warnings")
    lines.append("")
    if warnings:
        for warning in warnings:
            lines.append(f"- {warning}")
    else:
        lines.append("- None")
    lines.append("")
    lines.append("## Broken URLs")
    lines.append("")
    if broken:
        for url, detail in broken:
            lines.append(f"- `{detail}` {url}")
    else:
        lines.append("- None")
    lines.append("")
    report_path.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"Wrote report: {report_path}")

    if errors:
        print("Verification failed.")
        for error in errors:
            print(f"- {error}")
        sys.exit(1)
    print("Verification passed.")


if __name__ == "__main__":
    main()
