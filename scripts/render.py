#!/usr/bin/env python3
from __future__ import annotations

from collections import OrderedDict, defaultdict
from pathlib import Path
from typing import Any
from urllib.parse import urlparse

import yaml

ROOT = Path(__file__).resolve().parents[1]
PAPERS_FILE = ROOT / "data" / "papers.yaml"
PROJECTS_FILE = ROOT / "data" / "projects.yaml"
README = ROOT / "README.md"
README_ZH = ROOT / "README_zh.md"
SURVEY_ZH = ROOT / "survey_zh.md"

TECHNICAL_READINGS_CATEGORY = "Technical Docs, Blogs & Field Reports"
TECHNICAL_READING_GROUPS = [
    "Anthropic Official Engineering Articles",
    "OpenAI Official Engineering Articles and Docs",
    "Multi-Agent Framework Documentation",
    "Protocol Documentation",
    "Evaluation, Runtime, and Engineering Blogs",
    "High-Quality Personal and Community Blogs",
]
FEATURED_READING_NAMES = [
    "Anthropic - How we built our multi-agent research system",
    "Anthropic - Building multi-agent systems",
    "Anthropic - Multi-agent coordination patterns",
    "Anthropic - Building Effective AI Agents",
    "OpenAI Agents SDK - Orchestrating Multiple Agents",
    "OpenAI Cookbook - Orchestrating Agents",
    "OpenAI - Harness engineering",
    "OpenAI - Building more helpful agents with a new evaluation framework",
    "LangChain - How and when to build multi-agent systems",
    "AutoGen Documentation - Multi-agent Design Patterns",
    "LangGraph Documentation - Multi-agent Systems",
    "Google A2A Protocol Documentation",
    "Model Context Protocol Documentation",
]


def load_yaml(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict):
        raise ValueError(f"{path} must contain a mapping")
    return data


def esc(text: Any) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ").strip()


def paper_source_label(paper: dict[str, Any]) -> str:
    return esc(paper.get("venue") or paper.get("source_type", ""))


def paper_source_stats(papers: list[dict[str, Any]]) -> dict[str, int]:
    stats: dict[str, int] = defaultdict(int)
    for paper in papers:
        stats[str(paper.get("source_type", "unknown"))] += 1
    return dict(sorted(stats.items(), key=lambda item: (-item[1], item[0])))


def official_paper_count(papers: list[dict[str, Any]]) -> int:
    return len([paper for paper in papers if "arxiv.org" not in str(paper.get("url", ""))])


def featured_readings(projects: list[dict[str, Any]]) -> list[dict[str, Any]]:
    priority = {name.lower(): idx for idx, name in enumerate(FEATURED_READING_NAMES)}
    rows = [p for p in projects if p.get("category") == TECHNICAL_READINGS_CATEGORY]
    rows.sort(key=lambda p: (priority.get(str(p.get("name", "")).lower(), 999), str(p.get("name", "")).lower()))
    return rows


def is_github_url(url: Any) -> bool:
    return urlparse(str(url)).netloc.lower() == "github.com"


def split_project_catalog(projects: list[dict[str, Any]]) -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    technical_readings = [p for p in projects if p.get("category") == TECHNICAL_READINGS_CATEGORY]
    github_projects = [
        p for p in projects
        if p.get("category") != TECHNICAL_READINGS_CATEGORY and is_github_url(p.get("repo_url", ""))
    ]
    other_project_refs = [
        p for p in projects
        if p.get("category") != TECHNICAL_READINGS_CATEGORY and not is_github_url(p.get("repo_url", ""))
    ]
    return github_projects, technical_readings, other_project_refs


def technical_reading_group(item: dict[str, Any]) -> str:
    name = str(item.get("name", ""))
    tags = {str(tag).lower() for tag in item.get("tags", [])}
    if name.startswith("Anthropic - "):
        return "Anthropic Official Engineering Articles"
    if name.startswith("OpenAI") or name.startswith("OpenAI Developers"):
        return "OpenAI Official Engineering Articles and Docs"
    if "documentation" in tags or name.endswith("Documentation") or "Agents SDK" in name or "Cookbook" in name:
        if "protocol" in tags or "a2a" in tags or "mcp" in tags:
            return "Protocol Documentation"
        return "Multi-Agent Framework Documentation"
    if "protocolbench" in tags or "protocol" in tags or "a2a" in tags or "mcp" in tags:
        return "Protocol Documentation"
    if any(token in tags for token in ("agent-overview", "agent-definition", "multi-agent-evaluation", "agentic-design-patterns")):
        return "High-Quality Personal and Community Blogs"
    return "Evaluation, Runtime, and Engineering Blogs"


def group_technical_readings(items: list[dict[str, Any]]) -> OrderedDict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        grouped[technical_reading_group(item)].append(item)
    out: OrderedDict[str, list[dict[str, Any]]] = OrderedDict()
    for group in TECHNICAL_READING_GROUPS:
        rows = grouped.get(group, [])
        rows.sort(key=lambda x: str(x.get("name", "")).lower())
        out[group] = rows
    return out


def category_order(data: dict[str, Any]) -> list[str]:
    return [c["name_en"] for c in data["categories"]]


def group_by_category(items: list[dict[str, Any]], order: list[str]) -> OrderedDict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for item in items:
        grouped[item["category"]].append(item)
    out: OrderedDict[str, list[dict[str, Any]]] = OrderedDict()
    for category in order:
        rows = grouped.get(category, [])
        rows.sort(key=lambda x: (int(x.get("year", 9999)) if "year" in x else 9999, str(x.get("title", x.get("name", ""))).lower()))
        out[category] = rows
    return out


def render_readme_en(papers_data: dict[str, Any], projects_data: dict[str, Any]) -> str:
    papers = papers_data["papers"]
    projects = projects_data["projects"]
    core_papers = [p for p in papers if p.get("status") == "core"]
    github_projects, technical_readings, other_project_refs = split_project_catalog(projects)
    core_github_projects = [p for p in github_projects if p.get("status") == "core"]
    core_technical_readings = [p for p in technical_readings if p.get("status") == "core"]
    core_other_project_refs = [p for p in other_project_refs if p.get("status") == "core"]
    paper_order = category_order(papers_data)
    project_order = category_order(projects_data)
    papers_by_cat = group_by_category(papers, paper_order)
    github_projects_by_cat = group_by_category(github_projects, project_order)
    other_project_refs_by_cat = group_by_category(other_project_refs, project_order)
    technical_readings_by_group = group_technical_readings(technical_readings)

    lines: list[str] = []
    lines.append("# Awesome Multi-Agent Communication, Collaboration, and Evolution")
    lines.append("")
    lines.append("A curated and updateable repository for research on **multi-agent communication, collaboration, robustness, and evolution**, focused on LLM-based multi-agent systems and long-tail task assistants.")
    lines.append("")
    lines.append(f"- Papers: **{len(papers)}**")
    lines.append(f"- GitHub projects and systems: **{len(github_projects)}**")
    lines.append(f"- Technical docs, blogs, and field reports: **{len(technical_readings)}**")
    lines.append(f"- Non-GitHub project/reference rows: **{len(other_project_refs)}**")
    lines.append(f"- Core papers: **{len(core_papers)}**")
    lines.append(f"- Core GitHub projects/systems: **{len(core_github_projects)}**")
    lines.append(f"- Core technical readings: **{len(core_technical_readings)}**")
    lines.append(f"- Core non-GitHub references: **{len(core_other_project_refs)}**")
    lines.append(f"- Papers with non-arXiv primary source: **{official_paper_count(papers)}**")
    lines.append(f"- Papers with verified venue metadata: **{len([p for p in papers if p.get('venue')])}**")
    lines.append(f"- Last verified: **{papers_data['catalog']['last_verified']}**")
    lines.append("- Language: [English](./README.md) | [中文](./README_zh.md)")
    lines.append("")
    featured = featured_readings(projects)
    if featured:
        lines.append("<a id=\"featured-technical-readings\"></a>")
        lines.append("## Featured Technical Readings")
        lines.append("")
        for p in featured[:10]:
            lines.append(f"- [{esc(p['name'])}]({p['repo_url']}): {esc(p['summary_zh'])}")
        lines.append("")
    lines.append("## Contents")
    lines.append("")
    lines.append("- [Scope](#scope)")
    if featured:
        lines.append("- [Featured Technical Readings](#featured-technical-readings)")
    lines.append("- [Main Documents](#main-documents)")
    lines.append("- [Category Overview](#category-overview)")
    lines.append("- [Source Coverage](#source-coverage)")
    lines.append("- [Core Papers](#core-papers)")
    lines.append("- [Core GitHub Projects and Systems](#core-github-projects-and-systems)")
    lines.append("- [Core Technical Readings](#core-technical-readings)")
    lines.append("- [Core Non-GitHub References](#core-non-github-references)")
    lines.append("- [Complete Paper Catalog](#complete-paper-catalog)")
    lines.append("- [GitHub Project Catalog](#github-project-catalog)")
    lines.append("- [Technical Docs, Blogs, and Field Reports](#technical-docs-blogs-and-field-reports)")
    lines.append("- [Non-GitHub Project and Benchmark References](#non-github-project-and-benchmark-references)")
    lines.append("- [Maintenance](#maintenance)")
    lines.append("")
    lines.append("## Scope")
    lines.append("")
    lines.append("This repository is intentionally narrower than generic agent-framework lists. It tracks work that helps answer three questions:")
    lines.append("")
    lines.append("1. **Communication:** who should receive what information, when, and under what token budget?")
    lines.append("2. **Collaboration:** how should agents form teams, coordinate, verify, and recover from failures?")
    lines.append("3. **Evolution:** how can traces and feedback improve prompts, roles, tools, edges, topologies, and workflows?")
    lines.append("")
    lines.append("## Main Documents")
    lines.append("")
    lines.append("- [Chinese survey draft](./survey_zh.md)")
    lines.append("- [Curation policy](./docs/curation_policy.md)")
    lines.append("- [Search strategy](./docs/search_strategy.md)")
    lines.append("- [Research questions](./docs/research_questions.md)")
    lines.append("")
    lines.append("## Category Overview")
    lines.append("")
    lines.append("| Catalog | Category | Entries |")
    lines.append("| --- | --- | ---: |")
    for category, rows in papers_by_cat.items():
        lines.append(f"| Papers | {esc(category)} | {len(rows)} |")
    for category, rows in github_projects_by_cat.items():
        if rows:
            lines.append(f"| GitHub projects | {esc(category)} | {len(rows)} |")
    for group, rows in technical_readings_by_group.items():
        if rows:
            lines.append(f"| Technical docs/blogs | {esc(group)} | {len(rows)} |")
    for category, rows in other_project_refs_by_cat.items():
        if rows:
            lines.append(f"| Non-GitHub references | {esc(category)} | {len(rows)} |")
    lines.append("")
    lines.append("## Source Coverage")
    lines.append("")
    lines.append("| Primary source | Papers |")
    lines.append("| --- | ---: |")
    for source, count in paper_source_stats(papers).items():
        lines.append(f"| {esc(source)} | {count} |")
    lines.append("")
    lines.append("## Core Papers")
    lines.append("")
    lines.append("| Area | Paper | Year | Venue / source | Why it matters |")
    lines.append("| --- | --- | ---: | --- | --- |")
    for p in core_papers:
        lines.append(f"| {esc(p['category'])} | [{esc(p['title'])}]({p['url']}) | {p['year']} | {paper_source_label(p)} | {esc(p['relevance_zh'])} |")
    lines.append("")
    lines.append("## Core GitHub Projects and Systems")
    lines.append("")
    lines.append("| Area | Project | Why it matters |")
    lines.append("| --- | --- | --- |")
    for p in core_github_projects:
        lines.append(f"| {esc(p['category'])} | [{esc(p['name'])}]({p['repo_url']}) | {esc(p['relevance_zh'])} |")
    lines.append("")
    lines.append("## Core Technical Readings")
    lines.append("")
    lines.append("| Group | Reading | Why it matters |")
    lines.append("| --- | --- | --- |")
    for p in core_technical_readings:
        lines.append(f"| {esc(technical_reading_group(p))} | [{esc(p['name'])}]({p['repo_url']}) | {esc(p['relevance_zh'])} |")
    lines.append("")
    lines.append("## Core Non-GitHub References")
    lines.append("")
    if core_other_project_refs:
        lines.append("| Area | Reference | Why it matters |")
        lines.append("| --- | --- | --- |")
        for p in core_other_project_refs:
            lines.append(f"| {esc(p['category'])} | [{esc(p['name'])}]({p['repo_url']}) | {esc(p['relevance_zh'])} |")
    else:
        lines.append("- None")
    lines.append("")
    lines.append("## Complete Paper Catalog")
    lines.append("")
    for category, rows in papers_by_cat.items():
        lines.append(f"### {category}")
        lines.append("")
        lines.append("| Paper | Year | Venue / source | Status | Tags | Why it matters |")
        lines.append("| --- | ---: | --- | --- | --- | --- |")
        for p in rows:
            tags = ", ".join(p.get("tags", []))
            lines.append(
                f"| [{esc(p['title'])}]({p['url']}) | {p['year']} | {paper_source_label(p)} | "
                f"{esc(p.get('status', ''))} | {esc(tags)} | {esc(p['relevance_zh'])} |"
            )
        lines.append("")
    lines.append("## GitHub Project Catalog")
    lines.append("")
    for category, rows in github_projects_by_cat.items():
        if not rows:
            continue
        lines.append(f"### {category}")
        lines.append("")
        lines.append("| Project | Status | Tags | Why it matters |")
        lines.append("| --- | --- | --- | --- |")
        for p in rows:
            tags = ", ".join(p.get("tags", []))
            lines.append(
                f"| [{esc(p['name'])}]({p['repo_url']}) | {esc(p.get('status', ''))} | "
                f"{esc(tags)} | {esc(p['relevance_zh'])} |"
            )
        lines.append("")
    lines.append("## Technical Docs, Blogs, and Field Reports")
    lines.append("")
    for group, rows in technical_readings_by_group.items():
        if not rows:
            continue
        lines.append(f"### {group}")
        lines.append("")
        lines.append("| Reading | Status | Tags | Why it matters |")
        lines.append("| --- | --- | --- | --- |")
        for p in rows:
            tags = ", ".join(p.get("tags", []))
            lines.append(
                f"| [{esc(p['name'])}]({p['repo_url']}) | {esc(p.get('status', ''))} | "
                f"{esc(tags)} | {esc(p['relevance_zh'])} |"
            )
        lines.append("")
    lines.append("## Non-GitHub Project and Benchmark References")
    lines.append("")
    for category, rows in other_project_refs_by_cat.items():
        if not rows:
            continue
        lines.append(f"### {category}")
        lines.append("")
        lines.append("| Reference | Status | Tags | Why it matters |")
        lines.append("| --- | --- | --- | --- |")
        for p in rows:
            tags = ", ".join(p.get("tags", []))
            lines.append(
                f"| [{esc(p['name'])}]({p['repo_url']}) | {esc(p.get('status', ''))} | "
                f"{esc(tags)} | {esc(p['relevance_zh'])} |"
            )
        lines.append("")
    lines.append("## Maintenance")
    lines.append("")
    lines.append("Source of truth:")
    lines.append("")
    lines.append("- `data/papers.yaml`")
    lines.append("- `data/projects.yaml`")
    lines.append("")
    lines.append("Regenerate generated files:")
    lines.append("")
    lines.append("```bash")
    lines.append("python3 scripts/render.py")
    lines.append("```")
    lines.append("")
    lines.append("Validate schema and links:")
    lines.append("")
    lines.append("```bash")
    lines.append("python3 scripts/verify.py")
    lines.append("```")
    lines.append("")
    lines.append("Verify GitHub-backed project entries with GitHub CLI:")
    lines.append("")
    lines.append("```bash")
    lines.append("python3 scripts/verify_github_projects.py")
    lines.append("```")
    lines.append("")
    return "\n".join(lines) + "\n"


def render_readme_zh(papers_data: dict[str, Any], projects_data: dict[str, Any]) -> str:
    papers = papers_data["papers"]
    projects = projects_data["projects"]
    github_projects, technical_readings, other_project_refs = split_project_catalog(projects)
    core_github_projects = [p for p in github_projects if p.get("status") == "core"]
    core_technical_readings = [p for p in technical_readings if p.get("status") == "core"]
    core_other_project_refs = [p for p in other_project_refs if p.get("status") == "core"]
    paper_order = category_order(papers_data)
    project_order = category_order(projects_data)
    papers_by_cat = group_by_category(papers, paper_order)
    github_projects_by_cat = group_by_category(github_projects, project_order)
    other_project_refs_by_cat = group_by_category(other_project_refs, project_order)
    technical_readings_by_group = group_technical_readings(technical_readings)

    lines: list[str] = []
    lines.append("# 多智能体通信、协作与进化综述仓库")
    lines.append("")
    lines.append("这是一个可持续更新的综述仓库，聚焦 **LLM 多智能体通信、协作、鲁棒性与群体进化**，目标是支撑“高效、低成本、可自进化的多智能体协作系统”研究。")
    lines.append("")
    lines.append(f"- 论文条目: **{len(papers)}**")
    lines.append(f"- GitHub 项目/系统条目: **{len(github_projects)}**")
    lines.append(f"- 技术文档/博客/工程复盘: **{len(technical_readings)}**")
    lines.append(f"- 非 GitHub 项目/基准参考: **{len(other_project_refs)}**")
    lines.append(f"- 核心论文: **{len([p for p in papers if p.get('status') == 'core'])}**")
    lines.append(f"- 核心 GitHub 项目/系统: **{len(core_github_projects)}**")
    lines.append(f"- 核心技术阅读: **{len(core_technical_readings)}**")
    lines.append(f"- 核心非 GitHub 参考: **{len(core_other_project_refs)}**")
    lines.append(f"- 非 arXiv 主来源论文: **{official_paper_count(papers)}**")
    lines.append(f"- 已核验 venue 元数据论文: **{len([p for p in papers if p.get('venue')])}**")
    lines.append(f"- 最近核验: **{papers_data['catalog']['last_verified']}**")
    lines.append("- 语言: [English](./README.md) | [中文](./README_zh.md)")
    lines.append("")
    featured = featured_readings(projects)
    if featured:
        lines.append("<a id=\"featured-technical-readings\"></a>")
        lines.append("## 精选技术阅读")
        lines.append("")
        for p in featured[:10]:
            lines.append(f"- [{esc(p['name'])}]({p['repo_url']}): {esc(p['summary_zh'])}")
        lines.append("")
    lines.append("## 目录")
    lines.append("")
    lines.append("- [核心定位](#核心定位)")
    if featured:
        lines.append("- [精选技术阅读](#featured-technical-readings)")
    lines.append("- [主要文档](#主要文档)")
    lines.append("- [来源覆盖](#来源覆盖)")
    lines.append("- [论文目录](#论文目录)")
    lines.append("- [GitHub 项目目录](#github-项目目录)")
    lines.append("- [技术文档、博客与工程复盘](#技术文档博客与工程复盘)")
    lines.append("- [非 GitHub 项目与基准参考](#非-github-项目与基准参考)")
    lines.append("- [维护方式](#维护方式)")
    lines.append("")
    lines.append("## 核心定位")
    lines.append("")
    lines.append("本仓库不是泛 agent 框架清单，而是围绕三个研究问题组织：")
    lines.append("")
    lines.append("1. **通信**：谁接收什么信息、什么时候接收、在多大 token budget 下接收。")
    lines.append("2. **协作**：如何动态组队、分工、验证、恢复和处理错误 agent。")
    lines.append("3. **进化**：如何从执行轨迹和反馈中优化 prompt、role、tool、边连接、拓扑和 workflow。")
    lines.append("")
    lines.append("## 主要文档")
    lines.append("")
    lines.append("- [中文综述初稿](./survey_zh.md)")
    lines.append("- [收录规则](./docs/curation_policy.md)")
    lines.append("- [检索策略](./docs/search_strategy.md)")
    lines.append("- [研究问题](./docs/research_questions.md)")
    lines.append("")
    lines.append("## 来源覆盖")
    lines.append("")
    lines.append("| 主来源 | 论文数 |")
    lines.append("| --- | ---: |")
    for source, count in paper_source_stats(papers).items():
        lines.append(f"| {esc(source)} | {count} |")
    lines.append("")
    lines.append("## 论文目录")
    lines.append("")
    for category, rows in papers_by_cat.items():
        lines.append(f"### {category}")
        lines.append("")
        lines.append("| 论文 | 年份 | Venue / 来源 | 标签 | 贴合理由 |")
        lines.append("| --- | ---: | --- | --- | --- |")
        for p in rows:
            tags = ", ".join(p.get("tags", []))
            lines.append(f"| [{esc(p['title'])}]({p['url']}) | {p['year']} | {paper_source_label(p)} | {esc(tags)} | {esc(p['relevance_zh'])} |")
        lines.append("")
    lines.append("## GitHub 项目目录")
    lines.append("")
    for category, rows in github_projects_by_cat.items():
        if not rows:
            continue
        lines.append(f"### {category}")
        lines.append("")
        lines.append("| 项目 | 标签 | 贴合理由 |")
        lines.append("| --- | --- | --- |")
        for p in rows:
            tags = ", ".join(p.get("tags", []))
            lines.append(f"| [{esc(p['name'])}]({p['repo_url']}) | {esc(tags)} | {esc(p['relevance_zh'])} |")
        lines.append("")
    lines.append("## 技术文档、博客与工程复盘")
    lines.append("")
    for group, rows in technical_readings_by_group.items():
        if not rows:
            continue
        lines.append(f"### {group}")
        lines.append("")
        lines.append("| 阅读材料 | 标签 | 贴合理由 |")
        lines.append("| --- | --- | --- |")
        for p in rows:
            tags = ", ".join(p.get("tags", []))
            lines.append(f"| [{esc(p['name'])}]({p['repo_url']}) | {esc(tags)} | {esc(p['relevance_zh'])} |")
        lines.append("")
    lines.append("## 非 GitHub 项目与基准参考")
    lines.append("")
    for category, rows in other_project_refs_by_cat.items():
        if not rows:
            continue
        lines.append(f"### {category}")
        lines.append("")
        lines.append("| 条目 | 标签 | 贴合理由 |")
        lines.append("| --- | --- | --- |")
        for p in rows:
            tags = ", ".join(p.get("tags", []))
            lines.append(f"| [{esc(p['name'])}]({p['repo_url']}) | {esc(tags)} | {esc(p['relevance_zh'])} |")
        lines.append("")
    lines.append("## 维护方式")
    lines.append("")
    lines.append("单一数据源：")
    lines.append("")
    lines.append("- `data/papers.yaml`")
    lines.append("- `data/projects.yaml`")
    lines.append("")
    lines.append("更新后运行：")
    lines.append("")
    lines.append("```bash")
    lines.append("python3 scripts/render.py")
    lines.append("python3 scripts/verify.py --skip-links")
    lines.append("python3 scripts/verify_github_projects.py")
    lines.append("```")
    lines.append("")
    return "\n".join(lines) + "\n"


def render_survey_zh(papers_data: dict[str, Any], projects_data: dict[str, Any]) -> str:
    papers = papers_data["papers"]
    projects = projects_data["projects"]
    github_projects, technical_readings, other_project_refs = split_project_catalog(projects)
    paper_order = category_order(papers_data)
    project_order = category_order(projects_data)
    papers_by_cat = group_by_category(papers, paper_order)
    github_projects_by_cat = group_by_category(github_projects, project_order)
    other_project_refs_by_cat = group_by_category(other_project_refs, project_order)
    technical_readings_by_group = group_technical_readings(technical_readings)

    def core_titles(category: str) -> list[dict[str, Any]]:
        return [p for p in papers_by_cat.get(category, []) if p.get("status") == "core"]

    lines: list[str] = []
    lines.append("# 多智能体通信、协作与进化综述初稿")
    lines.append("")
    lines.append(f"更新日期：{papers_data['catalog']['last_verified']}")
    lines.append("")
    lines.append("## 摘要")
    lines.append("")
    lines.append("面向复杂长尾任务的 LLM 多智能体系统正在从“多个 agent 简单并行”走向基础设施化：系统必须在通信成本、协作鲁棒性和持续进化之间取得平衡。本文围绕通信、协作、进化三条主线整理相关论文、开源项目、技术文档和工程博客，并把综述正文、论文库、项目库和验证流程放在同一个可持续更新的仓库中。")
    lines.append("")
    lines.append("## 主题分类图")
    lines.append("")
    lines.append("```mermaid")
    lines.append("flowchart TD")
    lines.append("    accTitle: Multi-Agent Review Map")
    lines.append("    accDescr: The survey organizes multi-agent research into communication, collaboration, evolution, and evaluation infrastructure.")
    lines.append("    goal[低成本、鲁棒、可进化的多智能体协作系统]")
    lines.append("    comm[通信: routing, topology, token budget]")
    lines.append("    collab[协作: teaming, orchestration, verification]")
    lines.append("    evo[进化: traces, feedback, graph/workflow optimization]")
    lines.append("    eval[评测: success, cost, latency, robustness, evolution gain]")
    lines.append("    harness[工程底座: runtime, protocol, observability, governance]")
    lines.append("    goal --> comm")
    lines.append("    goal --> collab")
    lines.append("    goal --> evo")
    lines.append("    comm --> eval")
    lines.append("    collab --> eval")
    lines.append("    evo --> eval")
    lines.append("    harness --> comm")
    lines.append("    harness --> collab")
    lines.append("    harness --> evo")
    lines.append("```")
    lines.append("")
    lines.append("## 1. 引言")
    lines.append("")
    lines.append("单一 agent 在复杂长尾任务中会遇到上下文污染、工具选择困难、探索宽度不足和长期状态漂移等问题。多智能体系统的价值不在于简单堆叠 agent，而在于把任务拆解、信息压缩、角色专长、互相验证和持续改进组织成可控的系统。")
    lines.append("")
    lines.append("从项目目标看，综述需要围绕三个问题展开：")
    lines.append("")
    lines.append("1. 通信层如何避免全局广播和 token 浪费，同时保证关键信息不丢失。")
    lines.append("2. 协作层如何在 agent 能力波动、上下线、错误输出和工具失败时保持整体稳定。")
    lines.append("3. 进化层如何把执行轨迹转化为 prompt、role、tool、topology 和 workflow 的可验证改进。")
    lines.append("")
    lines.append("## 2. 方法：如何维护这个综述仓库")
    lines.append("")
    lines.append("本仓库采用数据驱动维护方式：用结构化 YAML 作为单一数据源，用脚本生成 README 和综述正文，用验证脚本检查 schema、重复项、URL、GitHub 仓库状态和论文来源报告。这样综述不是一次性文档，而是可持续更新的研究资产。")
    lines.append("")
    lines.append("## 3. 通信：从全局广播到预算约束路由")
    lines.append("")
    lines.append("多智能体通信的核心矛盾是：通信越多，信息越充分，但 token、延迟和噪声越高；通信越少，成本降低，但关键事实可能无法到达正确 agent。")
    lines.append("")
    lines.append("### 3.1 核心论文")
    lines.append("")
    lines.append("| 论文 | 年份 | Venue / 来源 | 机制 | 对项目的价值 |")
    lines.append("| --- | ---: | --- | --- | --- |")
    for p in papers_by_cat["Communication & Routing"]:
        lines.append(f"| [{esc(p['title'])}]({p['url']}) | {p['year']} | {paper_source_label(p)} | {esc(', '.join(p['tags']))} | {esc(p['relevance_zh'])} |")
    lines.append("")
    lines.append("### 3.2 设计结论")
    lines.append("")
    lines.append("通信模块建议采用四级 baseline：full broadcast、role-based routing、budgeted semantic routing、dynamic topology routing。full broadcast 只作为对照，不应作为目标方案。真正值得研究的是在 token budget 下同时优化通信 precision 和 recall。")
    lines.append("")
    lines.append("## 4. 协作：从固定流程到动态组队和鲁棒协作")
    lines.append("")
    lines.append("协作层要解决的不是“有几个 agent”，而是 agent 之间的任务边界、信息边界、责任边界和验证边界。")
    lines.append("")
    lines.append("### 4.1 核心论文")
    lines.append("")
    lines.append("| 论文 | 年份 | Venue / 来源 | 机制 | 对项目的价值 |")
    lines.append("| --- | ---: | --- | --- | --- |")
    collaboration_categories = (
        "Task-Oriented Collaboration & Dynamic Teaming",
        "Debate, Consensus & Verification",
        "Role-Playing, Agent Society & Simulation",
        "Software Engineering Multi-Agent Collaboration",
        "Robustness & Reliability",
    )
    for category in collaboration_categories:
        for p in papers_by_cat[category]:
            lines.append(f"| [{esc(p['title'])}]({p['url']}) | {p['year']} | {paper_source_label(p)} | {esc(', '.join(p['tags']))} | {esc(p['relevance_zh'])} |")
    lines.append("")
    lines.append("### 4.2 工程模式")
    lines.append("")
    lines.append("| 模式 | 适合场景 | 风险 |")
    lines.append("| --- | --- | --- |")
    lines.append("| Orchestrator-Subagent | 子任务短、边界清晰、需要总控合成 | 总控成为信息瓶颈，handoff 损失细节 |")
    lines.append("| Generator-Verifier | 输出质量关键且验收标准明确 | verifier 标准弱会橡皮图章 |")
    lines.append("| Agent Teams | 长任务分区独立，worker 需要积累上下文 | 共享资源冲突和完成检测困难 |")
    lines.append("| Message Bus | 事件驱动、agent 类型持续增长 | 路由错误和 trace 调试更难 |")
    lines.append("| Shared State | 多 agent 需要互相复用发现 | 容易重复工作、反应循环和终止条件不清 |")
    lines.append("")
    lines.append("## 5. 进化：从单次 prompt 到团队级自优化")
    lines.append("")
    lines.append("进化层要避免两个极端：一是只做人工 prompt 调参，难以规模化；二是让系统在线任意改代码，风险过高。更可行的路线是在结构化配置空间中优化 prompt、role、tool、edge、topology 和 verifier policy，并通过离线 replay + regression test 控制风险。")
    lines.append("")
    lines.append("### 5.1 核心论文")
    lines.append("")
    lines.append("| 论文 | 年份 | Venue / 来源 | 机制 | 对项目的价值 |")
    lines.append("| --- | ---: | --- | --- | --- |")
    for p in papers_by_cat["Evolution & Optimization"]:
        lines.append(f"| [{esc(p['title'])}]({p['url']}) | {p['year']} | {paper_source_label(p)} | {esc(', '.join(p['tags']))} | {esc(p['relevance_zh'])} |")
    lines.append("")
    lines.append("### 5.2 推荐进化闭环")
    lines.append("")
    lines.append("```mermaid")
    lines.append("flowchart LR")
    lines.append("    accTitle: Trace Guided Evolution Loop")
    lines.append("    accDescr: A safe multi-agent evolution loop starts from traces, attributes failures, proposes configuration changes, evaluates them offline, and only then deploys them.")
    lines.append("    trace[执行轨迹]")
    lines.append("    attr[失败归因]")
    lines.append("    propose[候选改动: prompt/role/tool/edge/topology]")
    lines.append("    replay[离线回放评测]")
    lines.append("    regress[回归测试]")
    lines.append("    deploy[灰度上线]")
    lines.append("    trace --> attr --> propose --> replay --> regress --> deploy")
    lines.append("    deploy --> trace")
    lines.append("```")
    lines.append("")
    lines.append("## 6. 评测：不要只看最终分数")
    lines.append("")
    lines.append("多智能体系统的评测必须是 harness-aware 的：报告的不是模型能力本身，而是 model + routing + topology + tools + memory + verifier + runtime 的组合能力。")
    lines.append("")
    lines.append("| 指标 | 含义 |")
    lines.append("| --- | --- |")
    lines.append("| End-to-end success rate | 最终任务是否可交付 |")
    lines.append("| Long-tail success rate | 复杂长尾任务成功率 |")
    lines.append("| Token cost | 总 token、通信 token、重复上下文 token |")
    lines.append("| Latency | 端到端耗时和 critical path 耗时 |")
    lines.append("| Robustness drop | 注入 faulty agent 后性能下降幅度 |")
    lines.append("| Recovery rate | agent/tool/context failure 后恢复比例 |")
    lines.append("| Evolution gain | 同类任务多轮出现后的成功率或成本改善 |")
    lines.append("")
    lines.append("### 6.1 相关 benchmark")
    lines.append("")
    lines.append("| 论文 | 年份 | Venue / 来源 | 对项目的价值 |")
    lines.append("| --- | ---: | --- | --- |")
    for p in papers_by_cat["Evaluation & Benchmarks"]:
        lines.append(f"| [{esc(p['title'])}]({p['url']}) | {p['year']} | {paper_source_label(p)} | {esc(p['relevance_zh'])} |")
    lines.append("")
    lines.append("## 7. GitHub 项目与工程底座")
    lines.append("")
    for idx, category in enumerate(project_order, start=1):
        rows = github_projects_by_cat[category]
        if not rows:
            continue
        lines.append(f"### 7.{idx} {category}")
        lines.append("")
        lines.append("| 项目 | 标签 | 对项目的价值 |")
        lines.append("| --- | --- | --- |")
        for p in rows:
            lines.append(f"| [{esc(p['name'])}]({p['repo_url']}) | {esc(', '.join(p['tags']))} | {esc(p['relevance_zh'])} |")
        lines.append("")
    lines.append("## 8. 技术文档、博客与工程复盘")
    lines.append("")
    for idx, (group, rows) in enumerate(technical_readings_by_group.items(), start=1):
        if not rows:
            continue
        lines.append(f"### 8.{idx} {group}")
        lines.append("")
        lines.append("| 阅读材料 | 标签 | 对项目的价值 |")
        lines.append("| --- | --- | --- |")
        for p in rows:
            lines.append(f"| [{esc(p['name'])}]({p['repo_url']}) | {esc(', '.join(p['tags']))} | {esc(p['relevance_zh'])} |")
        lines.append("")
    lines.append("## 9. 非 GitHub 项目与基准参考")
    lines.append("")
    for idx, category in enumerate(project_order, start=1):
        rows = other_project_refs_by_cat[category]
        if not rows:
            continue
        lines.append(f"### 9.{idx} {category}")
        lines.append("")
        lines.append("| 条目 | 标签 | 对项目的价值 |")
        lines.append("| --- | --- | --- |")
        for p in rows:
            lines.append(f"| [{esc(p['name'])}]({p['repo_url']}) | {esc(', '.join(p['tags']))} | {esc(p['relevance_zh'])} |")
        lines.append("")
    lines.append("## 10. 建议研究路线")
    lines.append("")
    lines.append("### 10.1 论文方向 A：预算约束上下文路由")
    lines.append("")
    lines.append("以 RCR-Router、Sparse Communication Topology 和动态拓扑生成为主线，研究在 token budget 下如何把结构化任务记忆发送给最需要的 agent。")
    lines.append("")
    lines.append("### 10.2 论文方向 B：鲁棒动态协作")
    lines.append("")
    lines.append("以 MAS-Resilience、RAPS 和 disagreement/self-repair 为主线，研究 agent 能力波动、故障、知识冲突和恶意消息下的协作稳定性。")
    lines.append("")
    lines.append("### 10.3 论文方向 C：基于轨迹的群体进化")
    lines.append("")
    lines.append("以 GPTSwarm、AFlow、EvoAgent、EvoMAS、Meta-Team 为主线，研究如何从 trace 和 failure attribution 中自动改进多 agent 协作图。")
    lines.append("")
    lines.append("## 11. 结论")
    lines.append("")
    lines.append("多智能体通信、协作和进化应被视为一个统一的系统问题：通信决定信息效率，协作决定任务稳定性，进化决定系统能否持续改善。最可行的研究路线不是再造一个普通 agent 框架，而是构建可观测、可评测、可回放、可优化的多智能体协作基础设施。")
    lines.append("")
    lines.append("## 参考论文索引")
    lines.append("")
    for p in papers:
        venue = f", {p['venue']}" if p.get("venue") else ""
        lines.append(f"- {p['title']} ({p['year']}{venue}): {p['url']}")
    lines.append("")
    return "\n".join(lines) + "\n"


def main() -> None:
    papers = load_yaml(PAPERS_FILE)
    projects = load_yaml(PROJECTS_FILE)
    README.write_text(render_readme_en(papers, projects), encoding="utf-8")
    README_ZH.write_text(render_readme_zh(papers, projects), encoding="utf-8")
    SURVEY_ZH.write_text(render_survey_zh(papers, projects), encoding="utf-8")
    print(f"Rendered {README}")
    print(f"Rendered {README_ZH}")
    print(f"Rendered {SURVEY_ZH}")


if __name__ == "__main__":
    main()
