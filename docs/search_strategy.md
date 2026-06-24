# Search Strategy

Search date: 2026-06-13

## Core Queries

Use these recurring query groups when refreshing the repository.

### Communication

- `"multi-agent" "LLM" communication routing token cost`
- `"Five Ws" "multi-agent communication" MARL emergent language LLMs`
- `"role-aware context routing" multi-agent LLM`
- `"sparse communication topology" multi-agent debate`
- `"dynamic communication topology" "LLM agents"`
- `"AgentPrune" "Cut the Crap" "multi-agent" communication pruning`
- `"G-Designer" "multi-agent communication topologies"`
- `"MasRouter" "Learning to Route LLMs" "Multi-Agent Systems"`
- `"RADAR" "Multi-Agent Communication Structure Generation"`
- `"publish-subscribe" "LLM agents" "reputation"`
- `"targeted multi-agent communication" TarMAC`
- `"Mixture-of-Agents" sparse routing cost latency`
- `"dynamic routing" "Mixture-of-Agents"`
- `"differentiable mixture-of-agents" sparse activation`

### Collaboration

- `"LLM-based multi-agent collaboration" coordination protocol`
- `"dynamic LLM agent network" task-oriented collaboration`
- `"collaborative belief reasoning" "efficient multi-agent collaboration"`
- `"MINDCraft" "MineCollab" "multi-agent LLM"`
- `"multi-agent orchestration patterns" generator verifier message bus shared state`
- `"multi-agent debate" "large language models"`
- `"faulty agents" "LLM-based multi-agent collaboration"`
- `"AutoGen" "multi-agent conversation"`
- `"AgentVerse" "emergent behaviors"`
- `"Talk Structurally" "Act Hierarchically"`
- `"Magentic-One" "generalist multi-agent system"`
- `"ARG-Designer" automatic multi-agent communication topology design`
- `"Adaptive In-conversation Team Building" language model agents`

### Evolution

- `"language agents as optimizable graphs"`
- `"agentic workflow generation" MCTS`
- `"automatic multi-agent generation" evolutionary algorithm`
- `"multi-agent collaboration via evolving orchestration"`
- `"collaborative self-evolution" "LLM-based multi-agent"`
- `"self-evolving multi-agent system specification"`
- `"trace-guided" "multi-agent" evolution`
- `"MAS-GPT" "Training LLMs to Build LLM-based Multi-Agent Systems"`
- `"AgentNet" "Decentralized Evolutionary Coordination" "multi-agent"`

### Debate, Consensus, and Agent Society

- `"Improving Factuality and Reasoning" "Multiagent Debate"`
- `"ReConcile" "Round-Table Conference" consensus LLMs`
- `"More Agents Is All You Need"`
- `"CAMEL" "Communicative Agents" "Large Language Model Society"`
- `"Generative Agents" "Interactive Simulacra"`
- `"SOTOPIA" "social intelligence" "language agents"`

### Evaluation

- `"Agent-as-a-Judge" evaluate agents with agents`
- `"MALLM" "Multi-Agent Large Language Models Framework"`
- `"LLM agent benchmark" "interactive environments"`
- `"GAIA benchmark" "general AI assistants"`
- `"SWE-bench" "language models resolve GitHub issues"`
- `"multi-agent systems" "failure attribution"`
- `"VillagerBench" "multi-agent collaboration"`
- `"AutoGenBench" "agentic evaluation"`
- `"multi-agent collaboration systems" privacy policy enforcement`
- `"MultiAgentBench" "Evaluating the Collaboration and Competition" "LLM agents"`
- `"MARBLE" "Multi-Agent Reasoning" "Learning and Evolution"`

### Projects, Protocols, and Technical Readings

- `"OpenAI Swarm" routines handoffs multi-agent`
- `"OpenAI Agents SDK" "orchestrating multiple agents" handoffs`
- `"OpenAI Cookbook" "orchestrating agents" handoffs routines`
- `"LlamaIndex" multi-agent workflows agent documentation`
- `"Hugging Face smolagents" multi-agent managed agents`
- `"Pydantic AI" multi-agent applications`
- `"Mastra" agent network multi-agent`
- `"BeeAI Framework" multi-agent workflow`
- `"Agent Communication Protocol" ACP agent protocol`
- `"Agent Network Protocol" ANP agent communication`
- `"ProtocolBench" "Which LLM Multi-Agent Protocol to Choose"`
- `"Andrew Ng" "multi-agent collaboration" agentic design patterns`
- `"Lilian Weng" "LLM Powered Autonomous Agents"`
- `"Simon Willison" agent definition multi-agent system`
- `"Survey of Multi-agent LLM Evaluations" miscoordination collusion`
- `"Cognition" "Don't Build Multi-Agents"`

## Refresh Procedure

1. Search papers in arXiv, Semantic Scholar, OpenAlex, Crossref, DBLP, OpenReview, ACL Anthology, ACM, IEEE, PMLR, NeurIPS proceedings, AAAI, IJCAI, AAMAS, and journal platforms.
2. Search implementation projects on GitHub with topic keywords: `multi-agent`, `agent-framework`, `agent-runtime`, `mcp`, `a2a`, `agent-evaluation`, `agent-observability`.
3. Search technical documentation and field reports from official engineering sources and framework docs, especially Anthropic, OpenAI, Microsoft/AutoGen, LangChain/LangGraph, MCP, and A2A. Keep these in `Technical Docs, Blogs & Field Reports` rather than mixing them with GitHub projects.
4. Deduplicate by normalized title, DOI, primary URL, and arXiv/preprint URL before adding a new row.
5. Prefer the official venue page as primary `url` for accepted/published papers, and move the arXiv page to `preprint_url`.
6. Add candidates to YAML with `status: candidate` first.
7. Promote to `important` or `core` only after checking the source and confirming project fit.
8. Run:

```bash
python3 scripts/render.py
python3 scripts/verify.py --skip-links
python3 scripts/audit_paper_sources.py
```

9. Run full link verification when network is available:

```bash
python3 scripts/verify.py
```

10. Run GitHub API verification for GitHub-backed projects:

```bash
python3 scripts/verify_github_projects.py
```

## Venue and Platform Priority

Use this priority order when the same work appears on multiple platforms:

1. Official conference/journal landing page: ACL Anthology, OpenReview accepted page, PMLR, NeurIPS proceedings, ACM DL, AAAI OJS, IJCAI proceedings, IEEE, Springer/journal DOI page.
2. Stable DOI resolver when the venue page is DOI-first.
3. arXiv preprint, saved as `preprint_url` if a formal page exists.
4. Repository/project page, saved under `data/projects.yaml`, not as a duplicate paper row.

Never count an arXiv preprint and its accepted conference version as two separate papers.

## Evidence Files

Raw search evidence should be kept in `sources/`:

- `sources/arxiv_verified_additions_2026-06-12.xml`: AutoGen, AgentVerse, Mixture-of-Agents, ReConcile, More Agents, TalkHier, SMoA, RouteMoA, DMoA.
- `sources/arxiv_verified_additions_security_benchmarks_2026-06-12.xml`: Maris, VillagerAgent, RMoA.
- `sources/arxiv_camel_verified_2026-06-12.xml`: CAMEL.
- `sources/arxiv_agent_society_magentic_verified_2026-06-12.xml`: Generative Agents, SOTOPIA, Magentic-One.
- `sources/dblp_multi_agent_top_venue_lookup_2026-06-12.json`: DBLP title lookups for NeurIPS/ICML foundational communication papers; DBLP rate-limited the later queries.
- `sources/openalex_multi_agent_top_venue_lookup_2026-06-12.json`: OpenAlex title lookups for ACL/EMNLP/ACM/AAAI/PMLR/DOI venue enrichment.
- `sources/semantic_scholar_arxiv_batch_2026-06-12.json`: Semantic Scholar batch enrichment from current arXiv IDs to venues, DOIs, and S2 records.
- `sources/openreview_multi_agent_search_2026-06-12.json`: OpenReview searches for ICLR/ICML/TMLR official pages.
- `sources/openreview_marl_foundations_search_2026-06-12.json`: OpenReview checks for MARL communication foundations and CommFormer.
- `sources/openalex_additional_multi_agent_candidates_2026-06-12.json`: Additional OpenAlex candidate search for AAAI/IJCAI/EMNLP evolution and communication papers.
- `sources/arxiv_new_gap_candidates_2026-06-12.xml`: arXiv API verification for Five Ws communication survey, Evolving Orchestration, MALLM, CoBel-World, and MINDCraft/MineCollab additions.
- `sources/arxiv_gap_additions_2026-06-13.xml`: arXiv API verification for AgentPrune, G-Designer, MAS-GPT, MultiAgentBench, ARG-Designer, CaptainAgent, AgentNet, TCAndon-Router, and MARBLE additions.
- `sources/arxiv_protocol_and_router_gap_2026-06-13.xml`: arXiv API verification for RADAR and protocol/router follow-up checks.
- `sources/acl_2025_masrouter_2026-06-13.bib` and `sources/acl_2025_masrouter_2026-06-13.html`: ACL Anthology evidence for MasRouter.
- `sources/acl_2025_multiagentbench_2026-06-13.bib` and `sources/acl_2025_multiagentbench_2026-06-13.html`: ACL Anthology evidence for MultiAgentBench.
- `sources/pmlr_gdesigner_2026-06-13.html`: PMLR evidence for G-Designer at ICML 2025.
- `sources/openreview_agentprune_2026-06-13.html`: OpenReview evidence for AgentPrune at ICLR 2025.
- `sources/openreview_masgpt_2026-06-13.html`: OpenReview evidence for MAS-GPT at ICML 2025.
- `sources/openreview_protocolbench_2026-06-13.html`: OpenReview evidence for ProtocolBench; kept as technical reading because the page indicates an ICLR 2026 rejected submission.
- `sources/github_gap_project_metadata_2026-06-13.jsonl`: GitHub metadata evidence for added frameworks, protocols, benchmarks, and research implementations.
- `sources/technical_blog_gap_evidence_2026-06-13.md`: Search evidence for Andrew Ng/DeepLearning.AI, Lilian Weng, Simon Willison, LessWrong, and Cognition technical readings.
