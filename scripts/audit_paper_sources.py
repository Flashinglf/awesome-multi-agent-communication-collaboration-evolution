#!/usr/bin/env python3
from __future__ import annotations

import datetime as dt
from collections import Counter
from pathlib import Path
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parents[1]
PAPERS_FILE = ROOT / "data" / "papers.yaml"
REPORT_DIR = ROOT / "reports" / "verification"


def main() -> None:
    data = yaml.safe_load(PAPERS_FILE.read_text(encoding="utf-8"))
    papers = data["papers"]
    source_counts = Counter(str(paper.get("source_type", "unknown")) for paper in papers)
    domain_counts = Counter(urlparse(str(paper.get("url", ""))).netloc for paper in papers)
    venue_counts = Counter(str(paper.get("venue", "No venue")) for paper in papers)
    arxiv_only = [
        paper for paper in papers
        if paper.get("source_type") == "arxiv" and not paper.get("venue") and not paper.get("doi")
    ]
    official = [paper for paper in papers if "arxiv.org" not in str(paper.get("url", ""))]

    REPORT_DIR.mkdir(parents=True, exist_ok=True)
    report = REPORT_DIR / f"{dt.date.today().isoformat()}-paper-sources.md"
    lines: list[str] = []
    lines.append("# Paper Source Audit")
    lines.append("")
    lines.append(f"- Generated at: `{dt.datetime.now(dt.timezone.utc).isoformat()}`")
    lines.append(f"- Papers: `{len(papers)}`")
    lines.append(f"- Non-arXiv primary-source papers: `{len(official)}`")
    lines.append(f"- Papers with venue metadata: `{len([p for p in papers if p.get('venue')])}`")
    lines.append(f"- arXiv-only papers without venue/DOI metadata: `{len(arxiv_only)}`")
    lines.append("")
    lines.append("## Primary Source Types")
    lines.append("")
    for source, count in source_counts.most_common():
        lines.append(f"- `{source}`: `{count}`")
    lines.append("")
    lines.append("## Primary URL Domains")
    lines.append("")
    for domain, count in domain_counts.most_common():
        lines.append(f"- `{domain}`: `{count}`")
    lines.append("")
    lines.append("## Venue Metadata")
    lines.append("")
    for venue, count in venue_counts.most_common():
        lines.append(f"- `{venue}`: `{count}`")
    lines.append("")
    lines.append("## arXiv-only Follow-up Queue")
    lines.append("")
    if arxiv_only:
        for paper in sorted(arxiv_only, key=lambda p: (p.get("year", 9999), p["title"])):
            lines.append(f"- `{paper['year']}` {paper['title']} - {paper['url']}")
    else:
        lines.append("- None")
    lines.append("")
    report.write_text("\n".join(lines), encoding="utf-8")
    print(f"Wrote report: {report}")


if __name__ == "__main__":
    main()
