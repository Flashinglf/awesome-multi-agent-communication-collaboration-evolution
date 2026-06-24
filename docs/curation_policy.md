# Curation Policy

## Scope

This repository tracks papers and projects for **multi-agent communication, collaboration, and evolution**, with emphasis on LLM-based multi-agent systems and implementation paths for long-tail task assistants.

The scope is intentionally narrower than generic agent frameworks:

- Communication: context routing, message routing, topology generation, publish-subscribe, learned communication, token-budgeted information exchange.
- Collaboration: role assignment, orchestration patterns, dynamic teaming, shared state, verification, conflict handling.
- Evolution: self-improvement, workflow search, graph optimization, team-level learning, failure-attribution-driven updates.
- Evaluation: benchmarks and harnesses that can measure quality, cost, latency, robustness, and evolution gain.

## Inclusion Criteria

For papers:

- Directly relevant to at least one of communication, collaboration, robustness, evolution, or multi-agent evaluation.
- Prefer primary papers, surveys, and papers with reusable algorithms or benchmarks.
- Include older MARL communication papers only when they provide foundational mechanisms such as gating, targeting, or learned protocols.
- Prefer the official venue page as the primary `url` when a paper is accepted or published in ACL Anthology, OpenReview, PMLR, NeurIPS proceedings, ACM DL, AAAI, IJCAI, IEEE, or a journal.
- Keep arXiv as `preprint_url` when an official venue page exists; do not add a second duplicate paper row for the same work.
- For accepted papers, add `venue`; add `doi` when a stable DOI is available.
- Add `evidence_sources` pointing to raw search/API evidence under a local `sources/` archive when a venue or official URL is enriched from external indexes. The archive is optional and is not tracked in the public repository.

For projects:

- Public and usable as an implementation reference, framework, protocol, benchmark, observability layer, or production case study.
- Must have a clear relationship to multi-agent communication/collaboration/evolution infrastructure.
- Generic single-agent apps are excluded unless they supply reusable evaluation, tracing, or workflow mechanisms.

## Category Design

Paper categories:

1. Communication & Routing
2. Task-Oriented Collaboration & Dynamic Teaming
3. Debate, Consensus & Verification
4. Role-Playing, Agent Society & Simulation
5. Software Engineering Multi-Agent Collaboration
6. Robustness & Reliability
7. Evolution & Optimization
8. Evaluation & Benchmarks
9. Surveys & Taxonomies

Project categories:

1. Frameworks & Runtimes
2. Protocols & Interoperability
3. Benchmarks & Evaluation
4. Observability & Operations
5. Research Implementations & Baselines
6. Reference Systems & Case Studies
7. Technical Docs, Blogs & Field Reports

The technical reading category is reserved for high-signal public engineering posts, official documentation, protocol specifications, and local PDF field reports that directly inform multi-agent communication, collaboration, evaluation, or evolution design. It is not a generic blogroll.

## Data Contract

Source of truth:

- `data/papers.yaml`
- `data/projects.yaml`

Required paper fields:

`title | year | category | url | source_type | tags | summary_zh | relevance_zh | status`

Recommended paper fields:

`venue | doi | preprint_url | evidence_sources`

Required project fields:

`name | category | repo_url | tags | summary_zh | relevance_zh | status`

Recommended project fields:

`docs_url | paper_url`

## Maintenance Rules

- Update YAML first.
- Regenerate generated markdown files with `python3 scripts/render.py`.
- Validate schema and URL reachability with `python3 scripts/verify.py`.
- Validate GitHub-backed project entries with `python3 scripts/verify_github_projects.py`; this requires `gh auth status` to be valid.
- Audit paper source coverage with `python3 scripts/audit_paper_sources.py`.
- Keep generated README files and `survey_zh.md` in sync with YAML.
- Record verification reports under `reports/verification/YYYY-MM-DD.md`.
- Keep candidate evidence in a local `sources/` archive, preferably raw arXiv API XML or search-result JSON, so later updates can audit why an entry was added. The public repository may omit this archive to keep the repository lightweight.
- Avoid duplicate paper titles, primary URLs, preprint URLs, and DOIs. If a benchmark/tool is described inside a system paper, place the tool under `data/projects.yaml` instead of adding a second paper row with the same arXiv URL.
