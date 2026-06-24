#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
PAPERS_FILE = ROOT / "data" / "papers.yaml"


def norm(text: str) -> str:
    return " ".join(text.lower().replace("−", "-").split())


def find_paper(papers: list[dict[str, Any]], paper_title: str) -> dict[str, Any]:
    wanted = norm(paper_title)
    for paper in papers:
        if norm(paper["title"]) == wanted:
            return paper
    raise KeyError(paper_title)


def update_paper(papers: list[dict[str, Any]], paper_title: str, **fields: Any) -> None:
    try:
        paper = find_paper(papers, paper_title)
    except KeyError:
        if "new_title" not in fields:
            raise
        paper = find_paper(papers, fields["new_title"])
    new_url = fields.get("url")
    if new_url and new_url != paper.get("url") and "arxiv.org" in paper.get("url", ""):
        fields.setdefault("preprint_url", paper["url"])
    if "new_title" in fields:
        paper["title"] = fields.pop("new_title")
    paper.update({key: value for key, value in fields.items() if value is not None})


def add_paper(papers: list[dict[str, Any]], item: dict[str, Any]) -> None:
    titles = {norm(paper["title"]) for paper in papers}
    if norm(item["title"]) not in titles:
        papers.append(item)


def main() -> None:
    data = yaml.safe_load(PAPERS_FILE.read_text(encoding="utf-8"))
    papers: list[dict[str, Any]] = data["papers"]

    semantic_scholar = ["sources/semantic_scholar_arxiv_batch_2026-06-12.json"]
    openalex = ["sources/openalex_multi_agent_top_venue_lookup_2026-06-12.json"]
    openreview = ["sources/openreview_multi_agent_search_2026-06-12.json"]
    dblp = ["sources/dblp_multi_agent_top_venue_lookup_2026-06-12.json"]
    acl_xml = ["sources/acl_anthology_xml_checks_2026-06-12.md"]

    verified_updates: list[tuple[str, dict[str, Any]]] = [
        (
            "Learning Multiagent Communication with Backpropagation",
            {
                "url": "https://proceedings.neurips.cc/paper/2016/hash/55b1927fdafef39c48e5b73b5d61ea60-Abstract.html",
                "source_type": "neurips",
                "venue": "NeurIPS 2016",
                "evidence_sources": dblp + semantic_scholar,
            },
        ),
        (
            "Learning to Communicate with Deep Multi-Agent Reinforcement Learning",
            {
                "url": "https://proceedings.neurips.cc/paper/2016/hash/c7635bfd99248a2cdef8249ef7bfbef4-Abstract.html",
                "source_type": "neurips",
                "venue": "NeurIPS 2016",
                "evidence_sources": dblp + semantic_scholar,
            },
        ),
        (
            "TarMAC: Targeted Multi-Agent Communication",
            {
                "url": "https://proceedings.mlr.press/v97/das19a.html",
                "source_type": "pmlr",
                "venue": "ICML 2019",
                "evidence_sources": dblp + semantic_scholar,
            },
        ),
        (
            "Learning when to Communicate at Scale in Multiagent Cooperative and Competitive Tasks",
            {"venue": "ICLR 2019", "evidence_sources": semantic_scholar},
        ),
        (
            "AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors",
            {
                "new_title": "AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors in Agents",
                "url": "https://openreview.net/forum?id=EHg5GDnyq1",
                "source_type": "openreview",
                "venue": "ICLR 2024 Poster",
                "evidence_sources": openreview + semantic_scholar,
            },
        ),
        (
            "Theory of Mind for Multi-Agent Collaboration via Large Language Models",
            {
                "url": "https://aclanthology.org/2023.emnlp-main.13/",
                "source_type": "acl",
                "venue": "EMNLP 2023",
                "doi": "10.18653/v1/2023.emnlp-main.13",
                "evidence_sources": openalex + semantic_scholar + acl_xml,
            },
        ),
        (
            "Scaling Large Language Model-based Multi-Agent Collaboration",
            {
                "url": "https://openreview.net/forum?id=K3n5jPkrU6",
                "source_type": "openreview",
                "venue": "ICLR 2025 Poster",
                "evidence_sources": openreview + semantic_scholar,
            },
        ),
        (
            "Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate",
            {
                "url": "https://aclanthology.org/2024.emnlp-main.992/",
                "source_type": "acl",
                "venue": "EMNLP 2024",
                "doi": "10.18653/v1/2024.emnlp-main.992",
                "evidence_sources": openalex + semantic_scholar + acl_xml,
            },
        ),
        (
            "ReConcile: Round-Table Conference Improves Reasoning via Consensus among Diverse LLMs",
            {
                "url": "https://aclanthology.org/2024.acl-long.381/",
                "source_type": "acl",
                "venue": "ACL 2024",
                "doi": "10.18653/v1/2024.acl-long.381",
                "evidence_sources": openalex + semantic_scholar + acl_xml,
            },
        ),
        (
            "More Agents Is All You Need",
            {
                "url": "https://openreview.net/forum?id=bgzUSZ8aeg",
                "source_type": "openreview",
                "venue": "TMLR 2024",
                "evidence_sources": semantic_scholar,
            },
        ),
        (
            "Mixture-of-Agents Enhances Large Language Model Capabilities",
            {
                "url": "https://openreview.net/forum?id=h0ZfDIrj7T",
                "source_type": "openreview",
                "venue": "ICLR 2025 Spotlight",
                "evidence_sources": openreview + semantic_scholar,
            },
        ),
        (
            'CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society',
            {"venue": "NeurIPS 2023", "doi": "10.52202/075280-2264", "evidence_sources": openalex + semantic_scholar},
        ),
        (
            "Generative Agents: Interactive Simulacra of Human Behavior",
            {
                "url": "https://dl.acm.org/doi/10.1145/3586183.3606763",
                "source_type": "acm",
                "venue": "UIST 2023",
                "doi": "10.1145/3586183.3606763",
                "evidence_sources": openalex + semantic_scholar,
            },
        ),
        (
            "SOTOPIA: Interactive Evaluation for Social Intelligence in Language Agents",
            {
                "url": "https://openreview.net/forum?id=mM7VurbA4r",
                "source_type": "openreview",
                "venue": "ICLR 2024 Spotlight",
                "evidence_sources": openreview + semantic_scholar,
            },
        ),
        (
            "Communicative Agents for Software Development",
            {
                "new_title": "ChatDev: Communicative Agents for Software Development",
                "url": "https://aclanthology.org/2024.acl-long.810/",
                "source_type": "acl",
                "venue": "ACL 2024",
                "doi": "10.18653/v1/2024.acl-long.810",
                "evidence_sources": openalex + semantic_scholar,
            },
        ),
        (
            "On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents",
            {
                "url": "https://openreview.net/forum?id=bkiM54QftZ",
                "source_type": "openreview",
                "venue": "ICML 2025 Poster",
                "evidence_sources": semantic_scholar,
            },
        ),
        (
            "Language Agents as Optimizable Graphs",
            {
                "new_title": "GPTSwarm: Language Agents as Optimizable Graphs",
                "url": "https://openreview.net/forum?id=uTC9AFXIhg",
                "source_type": "openreview",
                "venue": "ICML 2024 Oral",
                "evidence_sources": openreview + semantic_scholar,
            },
        ),
        (
            "AFlow: Automating Agentic Workflow Generation",
            {
                "url": "https://openreview.net/forum?id=z5uVAKwmjf",
                "source_type": "openreview",
                "venue": "ICLR 2025 Oral",
                "evidence_sources": openreview + semantic_scholar,
            },
        ),
        (
            "EvoAgent: Towards Automatic Multi-Agent Generation via Evolutionary Algorithms",
            {
                "url": "https://aclanthology.org/2025.naacl-long.315/",
                "source_type": "acl",
                "venue": "NAACL 2025",
                "doi": "10.18653/v1/2025.naacl-long.315",
                "evidence_sources": openalex + semantic_scholar,
            },
        ),
        (
            "Reflexion: Language Agents with Verbal Reinforcement Learning",
            {"venue": "NeurIPS 2023", "doi": "10.52202/075280-0377", "evidence_sources": openalex + semantic_scholar},
        ),
        (
            "Voyager: An Open-Ended Embodied Agent with Large Language Models",
            {
                "url": "https://openreview.net/forum?id=ehfRiF0R3a",
                "source_type": "openreview",
                "venue": "TMLR 2024",
                "evidence_sources": semantic_scholar,
            },
        ),
        (
            "AgentBench: Evaluating LLMs as Agents",
            {
                "url": "https://openreview.net/forum?id=zAdUB0aCTQ",
                "source_type": "openreview",
                "venue": "ICLR 2024 Poster",
                "evidence_sources": semantic_scholar,
            },
        ),
        (
            "GAIA: a benchmark for General AI Assistants",
            {
                "url": "https://openreview.net/forum?id=fibxvahvs3",
                "source_type": "openreview",
                "venue": "ICLR 2024 Poster",
                "evidence_sources": semantic_scholar,
            },
        ),
        (
            "SWE-bench: Can Language Models Resolve Real-World GitHub Issues?",
            {
                "url": "https://openreview.net/forum?id=VTF8yNQM66",
                "source_type": "openreview",
                "venue": "ICLR 2024 Oral",
                "evidence_sources": openreview + semantic_scholar,
            },
        ),
        (
            "Agent-as-a-Judge: Evaluate Agents with Agents",
            {
                "url": "https://openreview.net/forum?id=Nn9POI9Ekt",
                "source_type": "openreview",
                "venue": "ICML 2025 Poster",
                "evidence_sources": semantic_scholar,
            },
        ),
        (
            "MedAide: Information Fusion and Anatomy of Medical Intents via LLM-based Agent Collaboration",
            {
                "url": "https://doi.org/10.1016/j.inffus.2025.103743",
                "source_type": "journal",
                "venue": "Information Fusion 2025",
                "doi": "10.1016/j.inffus.2025.103743",
                "evidence_sources": semantic_scholar,
            },
        ),
        (
            "Towards Engineering Multi-Agent LLMs: A Protocol-Driven Approach",
            {
                "url": "https://doi.org/10.1109/APSEC66846.2025.00100",
                "source_type": "ieee",
                "venue": "APSEC 2025",
                "doi": "10.1109/APSEC66846.2025.00100",
                "evidence_sources": semantic_scholar,
            },
        ),
        ("SMoA: Improving Multi-agent Large Language Models with Sparse Mixture-of-Agents", {"venue": "PAKDD 2025", "evidence_sources": semantic_scholar}),
        ("Stay Focused: Problem Drift in Multi-Agent Debate", {"venue": "EACL 2025", "evidence_sources": semantic_scholar}),
        (
            "Enhancing Multi-Agent Debate System Performance via Confidence Expression",
            {"venue": "EMNLP 2025", "evidence_sources": semantic_scholar},
        ),
        ("iMAD: Intelligent Multi-Agent Debate for Efficient and Accurate LLM Inference", {"venue": "AAAI 2026", "evidence_sources": semantic_scholar}),
        (
            "Shadows in the Code: Exploring the Risks and Defenses of LLM-based Multi-Agent Software Development Systems",
            {"venue": "AAAI 2026", "evidence_sources": semantic_scholar},
        ),
    ]

    for paper_title, fields in verified_updates:
        update_paper(papers, paper_title, **fields)

    additions: list[dict[str, Any]] = [
        {
            "title": "Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments",
            "year": 2017,
            "category": "Task-Oriented Collaboration & Dynamic Teaming",
            "url": "https://proceedings.neurips.cc/paper/2017/hash/68a9750337a418a86fe06c1991a1d64c-Abstract.html",
            "source_type": "neurips",
            "venue": "NeurIPS 2017",
            "preprint_url": "https://arxiv.org/abs/1706.02275",
            "tags": ["marl", "actor-critic", "mixed-cooperative-competitive", "collaboration"],
            "summary_zh": "提出 MADDPG，用集中式训练和分散式执行处理混合合作-竞争环境中的多智能体策略学习。",
            "relevance_zh": "是多智能体协作/竞争学习的重要基础论文，可作为 LLM agent 团队协作前的 MARL 基线背景。",
            "status": "important",
            "evidence_sources": semantic_scholar,
        },
        {
            "title": "QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning",
            "year": 2018,
            "category": "Task-Oriented Collaboration & Dynamic Teaming",
            "url": "https://proceedings.mlr.press/v80/rashid18a.html",
            "source_type": "pmlr",
            "venue": "ICML 2018",
            "preprint_url": "https://arxiv.org/abs/1803.11485",
            "tags": ["marl", "value-factorization", "team-reward", "cooperation"],
            "summary_zh": "提出 QMIX，通过单调值函数分解把团队回报分配到各 agent 的局部动作价值。",
            "relevance_zh": "补齐协作任务中 team reward 和 credit assignment 的基础方法，有助于定义多 agent 协作评测指标。",
            "status": "important",
            "evidence_sources": openalex + semantic_scholar,
        },
        {
            "title": "Counterfactual Multi-Agent Policy Gradients",
            "year": 2018,
            "category": "Task-Oriented Collaboration & Dynamic Teaming",
            "url": "https://doi.org/10.1609/aaai.v32i1.11794",
            "source_type": "aaai",
            "venue": "AAAI 2018",
            "doi": "10.1609/aaai.v32i1.11794",
            "preprint_url": "https://arxiv.org/abs/1705.08926",
            "tags": ["marl", "credit-assignment", "counterfactual-baseline", "cooperation"],
            "summary_zh": "提出 COMA，用 counterfactual baseline 缓解多智能体合作中的信用分配问题。",
            "relevance_zh": "为多 agent 协作中的责任归因、失败归因和团队级优化提供基础算法背景。",
            "status": "important",
            "evidence_sources": openalex + semantic_scholar,
        },
        {
            "title": "Actor-Attention-Critic for Multi-Agent Reinforcement Learning",
            "year": 2019,
            "category": "Task-Oriented Collaboration & Dynamic Teaming",
            "url": "https://proceedings.mlr.press/v97/iqbal19a.html",
            "source_type": "pmlr",
            "venue": "ICML 2019",
            "preprint_url": "https://arxiv.org/abs/1810.02912",
            "tags": ["marl", "attention", "actor-critic", "collaboration"],
            "summary_zh": "提出 MAAC，用 attention critic 在训练时选择性聚合其他 agent 信息。",
            "relevance_zh": "与 LLM 多 agent 中“只关注相关 agent 输出”的思想一致，可作为协作注意力机制的基础参考。",
            "status": "important",
            "evidence_sources": semantic_scholar,
        },
        {
            "title": "Learning Attentional Communication for Multi-Agent Cooperation",
            "year": 2018,
            "category": "Communication & Routing",
            "url": "https://proceedings.neurips.cc/paper/2018/hash/6a8018b3a00b69c008601b8becae392b-Abstract.html",
            "source_type": "neurips",
            "venue": "NeurIPS 2018",
            "preprint_url": "https://arxiv.org/abs/1805.07733",
            "tags": ["attentional-communication", "marl", "message-routing", "cooperation"],
            "summary_zh": "提出 ATOC，用注意力机制动态形成通信组，使 agent 在需要时选择性通信。",
            "relevance_zh": "是“通信不是全连接广播，而是按需要形成通信组”的早期顶会基础论文。",
            "status": "important",
            "evidence_sources": semantic_scholar,
        },
        {
            "title": "Learning Multi-Agent Communication from Graph Modeling Perspective",
            "year": 2024,
            "category": "Communication & Routing",
            "url": "https://openreview.net/forum?id=Qox9rO0kN0",
            "source_type": "openreview",
            "venue": "ICLR 2024 Poster",
            "tags": ["learnable-graph", "communication-topology", "marl", "graph-modeling"],
            "summary_zh": "把多智能体通信结构建模为可学习图，通过双层优化同时学习通信图和策略参数。",
            "relevance_zh": "直接支撑通信拓扑可学习这一方向，可与 LLM 动态通信拓扑论文形成传统 MARL 到 LLM-MAS 的脉络。",
            "status": "important",
            "evidence_sources": ["sources/openreview_marl_foundations_search_2026-06-12.json"],
        },
        {
            "title": "Efficient Multi-Agent Communication via Shapley Message Value",
            "year": 2022,
            "category": "Communication & Routing",
            "url": "https://www.ijcai.org/proceedings/2022/82",
            "source_type": "ijcai",
            "venue": "IJCAI 2022",
            "doi": "10.24963/ijcai.2022/82",
            "tags": ["message-value", "shapley-value", "communication-efficiency", "marl"],
            "summary_zh": "用 Shapley message value 估计消息贡献，减少多智能体通信中的冗余消息。",
            "relevance_zh": "为“哪些消息值得发”提供可解释价值估计思路，适合连接 token budget 和通信收益评估。",
            "status": "important",
            "evidence_sources": ["sources/openalex_additional_multi_agent_candidates_2026-06-12.json"],
        },
        {
            "title": "Can ChatGPT Defend its Belief in Truth? Evaluating LLM Reasoning via Debate",
            "year": 2023,
            "category": "Debate, Consensus & Verification",
            "url": "https://aclanthology.org/2023.findings-emnlp.795/",
            "source_type": "acl",
            "venue": "Findings of EMNLP 2023",
            "doi": "10.18653/v1/2023.findings-emnlp.795",
            "tags": ["debate", "reasoning-evaluation", "belief-defense", "verification"],
            "summary_zh": "通过 debate 形式评测 LLM 是否能在对抗式讨论中维护或修正自己的信念。",
            "relevance_zh": "补充多 agent 辩论的评测视角，可用于分析共识形成是否真正提升事实性和推理。",
            "status": "important",
            "evidence_sources": openalex,
        },
        {
            "title": "ExpeL: LLM Agents Are Experiential Learners",
            "year": 2024,
            "category": "Evolution & Optimization",
            "url": "https://doi.org/10.1609/aaai.v38i17.29936",
            "source_type": "aaai",
            "venue": "AAAI 2024",
            "doi": "10.1609/aaai.v38i17.29936",
            "preprint_url": "https://arxiv.org/abs/2308.10144",
            "tags": ["experiential-learning", "memory", "reflection", "agent-learning"],
            "summary_zh": "提出 ExpeL，让语言 agent 从训练任务经历中抽取自然语言经验，并在推理时检索使用。",
            "relevance_zh": "虽然不是多 agent 专用，但为“从执行轨迹中积累经验并改进行为”的进化闭环提供关键基线。",
            "status": "important",
            "evidence_sources": ["sources/openalex_additional_multi_agent_candidates_2026-06-12.json"],
        },
        {
            "title": "SwarmAgentic: Towards Fully Automated Agentic System Generation via Swarm Intelligence",
            "year": 2025,
            "category": "Evolution & Optimization",
            "url": "https://aclanthology.org/2025.emnlp-main.93/",
            "source_type": "acl",
            "venue": "EMNLP 2025",
            "doi": "10.18653/v1/2025.emnlp-main.93",
            "preprint_url": "https://arxiv.org/abs/2506.15672",
            "tags": ["agentic-system-generation", "swarm-intelligence", "automated-design", "evolution"],
            "summary_zh": "使用群体智能自动生成 agentic system，关注系统结构、角色和流程的自动化设计。",
            "relevance_zh": "直接补充多 agent 系统自动生成与进化方向，适合与 AFlow/GPTSwarm/EvoAgent 放在同一脉络。",
            "status": "important",
            "evidence_sources": ["sources/openalex_additional_multi_agent_candidates_2026-06-12.json"],
        },
        {
            "title": "Experiential Co-Learning of Software-Developing Agents",
            "year": 2024,
            "category": "Evolution & Optimization",
            "url": "https://aclanthology.org/2024.acl-long.305/",
            "source_type": "acl",
            "venue": "ACL 2024",
            "doi": "10.18653/v1/2024.acl-long.305",
            "tags": ["experiential-learning", "software-agents", "co-learning", "trajectory-memory"],
            "summary_zh": "提出 Experiential Co-Learning，让软件开发中的 instructor/assistant agents 从历史轨迹中提取 shortcut-oriented experiences，并用于后续任务。",
            "relevance_zh": "直接连接多 agent 软件协作和经验驱动进化，可作为 ChatDev 类系统如何从失败和轨迹中持续改进的核心参考。",
            "status": "important",
            "evidence_sources": acl_xml,
        },
        {
            "title": "A Survey of Multi-Agent Deep Reinforcement Learning with Communication",
            "year": 2024,
            "category": "Surveys & Taxonomies",
            "url": "https://doi.org/10.1007/s10458-023-09633-6",
            "source_type": "journal",
            "venue": "Autonomous Agents and Multi-Agent Systems 2024",
            "doi": "10.1007/s10458-023-09633-6",
            "tags": ["survey", "marl", "communication", "protocols"],
            "summary_zh": "系统综述多智能体深度强化学习中的通信机制，覆盖显式通信、隐式通信和通信效率问题。",
            "relevance_zh": "为 LLM 多 agent 通信研究提供前 LLM 时代的系统背景，帮助区分学到的通信协议与提示式通信。",
            "status": "important",
            "evidence_sources": openalex,
        },
    ]

    for item in additions:
        add_paper(papers, item)

    data["catalog"]["last_verified"] = "2026-06-12"
    PAPERS_FILE.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=140), encoding="utf-8")
    print(f"papers={len(papers)}")


if __name__ == "__main__":
    main()
