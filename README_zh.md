# 多智能体通信、协作与进化综述仓库

这是一个可持续更新的综述仓库，聚焦 **LLM 多智能体通信、协作、鲁棒性与群体进化**，目标是支撑“高效、低成本、可自进化的多智能体协作系统”研究。

- 论文条目: **108**
- GitHub 项目/系统条目: **79**
- 技术文档/博客/工程复盘: **47**
- 非 GitHub 项目/基准参考: **4**
- 核心论文: **42**
- 核心 GitHub 项目/系统: **17**
- 核心技术阅读: **7**
- 核心非 GitHub 参考: **1**
- 非 arXiv 主来源论文: **41**
- 已核验 venue 元数据论文: **53**
- 最近核验: **2026-06-13**
- 语言: [English](./README.md) | [中文](./README_zh.md)

<a id="featured-technical-readings"></a>
## 精选技术阅读

- [Anthropic - How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system): Anthropic 对生产级 research multi-agent system 的工程复盘，包含 lead agent、并行 subagents、任务分解、trace 和 citation 验证经验。
- [Anthropic - Building multi-agent systems](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them): 讨论什么时候值得使用多 agent，以及 context protection、parallelization、specialization 三类收益和高额 token 成本之间的取舍。
- [Anthropic - Multi-agent coordination patterns](https://claude.com/blog/multi-agent-coordination-patterns): 总结 generator-verifier、orchestrator-subagent、agent teams、message bus、shared state 五类常见协作模式及适用条件。
- [Anthropic - Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents): Anthropic 对 workflows 与 autonomous agents 的实用区分，并总结 prompt chaining、routing、parallelization、orchestrator-workers、evaluator-optimizer 等模式。
- [OpenAI Agents SDK - Orchestrating Multiple Agents](https://openai.github.io/openai-agents-python/multi_agent/): OpenAI Agents SDK 官方多 agent 编排文档，覆盖 agents-as-tools、handoffs 和 manager 模式。
- [OpenAI Cookbook - Orchestrating Agents](https://cookbook.openai.com/examples/orchestrating_agents): OpenAI Cookbook 示例，展示如何用 routines、handoffs 和工具组织多个 agents。
- [OpenAI - Harness engineering](https://openai.com/index/harness-engineering/): OpenAI 对 harness engineering 的实践总结，强调通过约束、验证和工具环境让 agent-first 软件更可靠。
- [OpenAI - Building more helpful agents with a new evaluation framework](https://openai.com/index/building-more-helpful-agents-with-a-new-evaluation-framework/): OpenAI 发布 BrowseComp，用难以搜索定位的问题评估 agent 深度检索和信息整合能力。
- [LangChain - How and when to build multi-agent systems](https://blog.langchain.com/how-and-when-to-build-multi-agent-systems/): LangChain 对 multi-agent supervisor、handoff、subagent 工具化等模式的实践建议。
- [AutoGen Documentation - Multi-agent Design Patterns](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-patterns/intro.html): AutoGen 官方文档中的多 agent 设计模式入口，覆盖 Core runtime 下的协作组织方式。

## 目录

- [核心定位](#核心定位)
- [精选技术阅读](#featured-technical-readings)
- [主要文档](#主要文档)
- [来源覆盖](#来源覆盖)
- [论文目录](#论文目录)
- [GitHub 项目目录](#github-项目目录)
- [技术文档、博客与工程复盘](#技术文档博客与工程复盘)
- [非 GitHub 项目与基准参考](#非-github-项目与基准参考)
- [维护方式](#维护方式)

## 核心定位

本仓库不是泛 agent 框架清单，而是围绕三个研究问题组织：

1. **通信**：谁接收什么信息、什么时候接收、在多大 token budget 下接收。
2. **协作**：如何动态组队、分工、验证、恢复和处理错误 agent。
3. **进化**：如何从执行轨迹和反馈中优化 prompt、role、tool、边连接、拓扑和 workflow。

## 主要文档

- [中文综述初稿](./survey_zh.md)
- [收录规则](./docs/curation_policy.md)
- [检索策略](./docs/search_strategy.md)
- [研究问题](./docs/research_questions.md)

## 来源覆盖

| 主来源 | 论文数 |
| --- | ---: |
| arxiv | 67 |
| openreview | 16 |
| acl | 10 |
| neurips | 4 |
| pmlr | 4 |
| aaai | 2 |
| journal | 2 |
| acm | 1 |
| ieee | 1 |
| ijcai | 1 |

## 论文目录

### Communication & Routing

| 论文 | 年份 | Venue / 来源 | 标签 | 贴合理由 |
| --- | ---: | --- | --- | --- |
| [Learning Multiagent Communication with Backpropagation](https://proceedings.neurips.cc/paper/2016/hash/55b1927fdafef39c48e5b73b5d61ea60-Abstract.html) | 2016 | NeurIPS 2016 | commnet, differentiable-communication, marl | 是“通信可以被学习”的基础论文，可作为 LLM 多 agent 路由学习的理论背景。 |
| [Learning to Communicate with Deep Multi-Agent Reinforcement Learning](https://proceedings.neurips.cc/paper/2016/hash/c7635bfd99248a2cdef8249ef7bfbef4-Abstract.html) | 2016 | NeurIPS 2016 | rial, dial, communication-learning, marl | 支撑“通信协议可通过环境反馈优化”的理论基础。 |
| [Learning Attentional Communication for Multi-Agent Cooperation](https://proceedings.neurips.cc/paper/2018/hash/6a8018b3a00b69c008601b8becae392b-Abstract.html) | 2018 | NeurIPS 2018 | attentional-communication, marl, message-routing, cooperation | 是“通信不是全连接广播，而是按需要形成通信组”的早期顶会基础论文。 |
| [Learning when to Communicate at Scale in Multiagent Cooperative and Competitive Tasks](https://arxiv.org/abs/1812.09755) | 2018 | ICLR 2019 | ic3net, communication-gating, scalable-marl | 可借鉴为 LLM agent 通信开关、预算门控和 token 节省机制。 |
| [TarMAC: Targeted Multi-Agent Communication](https://proceedings.mlr.press/v97/das19a.html) | 2018 | ICML 2019 | targeted-communication, attention, marl | 与项目中的“高效信息路由机制”高度同构。 |
| [Efficient Multi-Agent Communication via Shapley Message Value](https://www.ijcai.org/proceedings/2022/82) | 2022 | IJCAI 2022 | message-value, shapley-value, communication-efficiency, marl | 为“哪些消息值得发”提供可解释价值估计思路，适合连接 token budget 和通信收益评估。 |
| [Exchange-of-Thought: Enhancing Large Language Model Capabilities through Cross-Model Communication](https://arxiv.org/abs/2312.01823) | 2023 | arxiv | cross-model-communication, relay, debate, memory | 适合整理多 agent 通信协议设计空间。 |
| [A Scalable Communication Protocol for Networks of Large Language Models](https://arxiv.org/abs/2410.11905) | 2024 | arxiv | communication-protocol, llm-networks, scalability, message-passing | 为 A2A/ANP/ACP 等工程协议之外的学术协议设计提供参考，适合补齐协议层文献。 |
| [Improving Multi-Agent Debate with Sparse Communication Topology](https://arxiv.org/abs/2406.11776) | 2024 | arxiv | sparse-topology, debate, communication-cost | 支撑“不是所有 agent 都应该互相通信”的设计假设，适合做全连接通信的对照实验。 |
| [Learning Multi-Agent Communication from Graph Modeling Perspective](https://openreview.net/forum?id=Qox9rO0kN0) | 2024 | ICLR 2024 Poster | learnable-graph, communication-topology, marl, graph-modeling | 直接支撑通信拓扑可学习这一方向，可与 LLM 动态通信拓扑论文形成传统 MARL 到 LLM-MAS 的脉络。 |
| [SMoA: Improving Multi-agent Large Language Models with Sparse Mixture-of-Agents](https://arxiv.org/abs/2411.03284) | 2024 | PAKDD 2025 | sparse-mixture-of-agents, response-selection, early-stopping, role-diversity | 是 MoA 类系统从全连接通信走向稀疏通信的直接参考，适合做成本受限多 agent 推理 baseline。 |
| [Cut the Crap: An Economical Communication Pipeline for LLM-based Multi-Agent Systems](https://openreview.net/forum?id=LkzuPorQ5L) | 2025 | ICLR 2025 | agentprune, communication-pruning, token-efficiency, adversarial-robustness | 直接命中“协作不能显著增加 token/成本”的工程边界，是通信剪枝和经济型协作拓扑的关键顶会论文。 |
| [Dynamic Generation of Multi-LLM Agents Communication Topologies with Graph Diffusion Models](https://arxiv.org/abs/2510.07799) | 2025 | arxiv | topology-generation, graph-diffusion, cost-quality-robustness | 适合支撑“动态 agent 组队 + 动态通信网络”的算法路线。 |
| [G-Designer: Architecting Multi-agent Communication Topologies via Graph Neural Networks](https://proceedings.mlr.press/v267/zhang25cu.html) | 2025 | ICML 2025 | topology-design, graph-neural-network, task-adaptive-routing, token-efficiency | 与动态通信网络、任务自适应路由和低成本协作高度相关，可与 GPTSwarm、AgentPrune、MasRouter 形成拓扑优化主线。 |
| [MasRouter: Learning to Route LLMs for Multi-Agent Systems](https://aclanthology.org/2025.acl-long.757/) | 2025 | ACL 2025 | routing, llm-selection, multi-agent-systems, inference-efficiency | 直接服务“谁该参与、何时参与、以什么成本参与”的路由问题，是多 agent 通信与动态组队的关键 ACL 论文。 |
| [RCR-Router: Efficient Role-Aware Context Routing for Multi-Agent LLM Systems with Structured Memory](https://arxiv.org/abs/2508.04903) | 2025 | arxiv | context-routing, role-aware, structured-memory, token-budget | 直接命中项目“通信代价大、关键信息传不准”的问题，可作为预算约束上下文路由主 baseline。 |
| [Differentiable Mixture-of-Agents Incentivizes Swarm Intelligence of Large Language Models](https://arxiv.org/abs/2605.15706) | 2026 | arxiv | differentiable-routing, sparse-activation, test-time-adaptation, swarm-intelligence | 连接“动态通信拓扑”和“在线自适应”，适合作为可学习路由和群体智能方向的前沿参考。 |
| [RADAR: Redundancy-Aware Diffusion for Multi-Agent Communication Structure Generation](https://arxiv.org/abs/2605.09907) | 2026 | arxiv | redundancy-aware, diffusion, communication-structure-generation, topology-generation | 补强 G-Designer、ARG-Designer 之后的通信结构生成路线，适合跟踪 2026 年前沿拓扑生成方法。 |
| [RouteMoA: Dynamic Routing without Pre-Inference Boosts Efficient Mixture-of-Agents](https://arxiv.org/abs/2601.18130) | 2026 | arxiv | mixture-of-agents, dynamic-routing, model-selection, cost-latency | 对“协作不能显著增加 token 和耗时”的约束非常关键，可支撑预推理前的 agent/model 路由。 |
| [TCAndon-Router: Adaptive Reasoning Router for Multi-Agent Collaboration](https://arxiv.org/abs/2601.04544) | 2026 | arxiv | adaptive-routing, reasoning-router, collaboration, dynamic-selection | 与 MasRouter、RCR-Router、ARMOR-MAD 共同构成动态路由方向，可作为后续候选 baseline。 |
| [The Five Ws of Multi-Agent Communication: Who Talks to Whom, When, What, and Why -- A Survey from MARL to Emergent Language and LLMs](https://arxiv.org/abs/2602.11583) | 2026 | TMLR 2026 | survey, communication, marl, emergent-language, llm-agents | 是本仓库通信章节的高质量分类法补充，可帮助把传统可学习通信和 LLM 自然语言通信放到同一脉络。 |
| [Towards Adaptive, Scalable, and Robust Coordination of LLM Agents: A Dynamic Ad-Hoc Networking Perspective](https://arxiv.org/abs/2602.08009) | 2026 | arxiv | publish-subscribe, reputation, dynamic-networking, intent-routing | 同时覆盖通信路由、动态协作和鲁棒性，是项目基础设施设计的强相关论文。 |

### Task-Oriented Collaboration & Dynamic Teaming

| 论文 | 年份 | Venue / 来源 | 标签 | 贴合理由 |
| --- | ---: | --- | --- | --- |
| [Multi-Agent Actor-Critic for Mixed Cooperative-Competitive Environments](https://proceedings.neurips.cc/paper/2017/hash/68a9750337a418a86fe06c1991a1d64c-Abstract.html) | 2017 | NeurIPS 2017 | marl, actor-critic, mixed-cooperative-competitive, collaboration | 是多智能体协作/竞争学习的重要基础论文，可作为 LLM agent 团队协作前的 MARL 基线背景。 |
| [Counterfactual Multi-Agent Policy Gradients](https://doi.org/10.1609/aaai.v32i1.11794) | 2018 | AAAI 2018 | marl, credit-assignment, counterfactual-baseline, cooperation | 为多 agent 协作中的责任归因、失败归因和团队级优化提供基础算法背景。 |
| [QMIX: Monotonic Value Function Factorisation for Deep Multi-Agent Reinforcement Learning](https://proceedings.mlr.press/v80/rashid18a.html) | 2018 | ICML 2018 | marl, value-factorization, team-reward, cooperation | 补齐协作任务中 team reward 和 credit assignment 的基础方法，有助于定义多 agent 协作评测指标。 |
| [Actor-Attention-Critic for Multi-Agent Reinforcement Learning](https://proceedings.mlr.press/v97/iqbal19a.html) | 2019 | ICML 2019 | marl, attention, actor-critic, collaboration | 与 LLM 多 agent 中“只关注相关 agent 输出”的思想一致，可作为协作注意力机制的基础参考。 |
| [A Dynamic LLM-Powered Agent Network for Task-Oriented Agent Collaboration](https://arxiv.org/abs/2310.02170) | 2023 | arxiv | dynamic-agent-network, agent-selection, collaboration | 可作为动态组队和 agent 选择机制的早期 baseline。 |
| [AgentVerse: Facilitating Multi-Agent Collaboration and Exploring Emergent Behaviors in Agents](https://openreview.net/forum?id=EHg5GDnyq1) | 2023 | ICLR 2024 Poster | agentverse, dynamic-composition, emergent-behavior, collaboration | 补齐早期通用 LLM 多 agent 协作框架，对动态组队和正负涌现行为分析有参考价值。 |
| [AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation](https://arxiv.org/abs/2308.08155) | 2023 | arxiv | autogen, multi-agent-conversation, tool-use, human-in-the-loop | 是 LLM 多 agent conversation framework 的基础论文，应作为协作运行时和对话协议 baseline。 |
| [Theory of Mind for Multi-Agent Collaboration via Large Language Models](https://aclanthology.org/2023.emnlp-main.13/) | 2023 | EMNLP 2023 | theory-of-mind, belief-state, cooperative-game, collaboration | 适合支撑“agent 之间需要理解彼此状态和意图”的协作机制章节。 |
| [Adaptive In-conversation Team Building for Language Model Agents](https://arxiv.org/abs/2405.19425) | 2024 | arxiv | captainagent, team-building, agent-selection, in-conversation | 补齐动态组队中“对话中途扩队/换队”的机制，可作为 AgentVerse、Dynamic Agent Network 之后的关键候选。 |
| [AgentCoord: Visually Exploring Coordination Strategy for LLM-based Multi-Agent Collaboration](https://arxiv.org/abs/2404.11943) | 2024 | arxiv | coordination-strategy, visual-exploration, structured-representation, human-in-the-loop | 适合支撑“协作协议/拓扑如何设计和调试”的工具化方向。 |
| [Magentic-One: A Generalist Multi-Agent System for Solving Complex Tasks](https://arxiv.org/abs/2411.04468) | 2024 | arxiv | orchestrator, specialist-agents, replanning, autogenbench | 是 orchestrator-specialist 架构的强参考系统，也提供 AutoGenBench 这类可隔离评测工具。 |
| [MedAide: Information Fusion and Anatomy of Medical Intents via LLM-based Agent Collaboration](https://doi.org/10.1016/j.inffus.2025.103743) | 2024 | Information Fusion 2025 | medical, intent-aware, role-rotation, information-fusion | 应用较窄，但 intent-aware fusion 和 role rotation 对通用协作框架有借鉴价值。 |
| [Multi-Agent Collaboration in Incident Response with Large Language Models](https://arxiv.org/abs/2412.00652) | 2024 | arxiv | incident-response, cybersecurity, centralized, decentralized, hybrid | 可作为动态协作结构和高压任务响应的应用案例。 |
| [Scaling Large Language Model-based Multi-Agent Collaboration](https://openreview.net/forum?id=K3n5jPkrU6) | 2024 | ICLR 2025 Poster | macnet, scaling-law, dag-topology, thousand-agents | 是协作规模化和拓扑组织的重要论文，直接支撑“多个开源榜单 SOTA”和大规模协作框架目标。 |
| [Towards Effective GenAI Multi-Agent Collaboration: Design and Evaluation for Enterprise Applications](https://arxiv.org/abs/2412.05449) | 2024 | arxiv | enterprise, coordination-mode, routing-mode, payload-reference | 与项目落地到任务助手和企业级复杂任务高度贴合，尤其适合作端到端可用率与成本指标参考。 |
| [Assemble Your Crew: Automatic Multi-agent Communication Topology Design via Autoregressive Graph Generation](https://arxiv.org/abs/2507.18224) | 2025 | AAAI 2026 Oral | arg-designer, autoregressive-graph-generation, topology-design, role-selection | 直接补强自动组队与通信拓扑生成，是从固定团队走向按任务生成团队的高质量前沿工作。 |
| [Collaborating Action by Action: A Multi-agent LLM Framework for Embodied Reasoning](https://arxiv.org/abs/2504.17950) | 2025 | arxiv | mindcraft, minecollab, embodied-agents, communication-efficiency | 是“多 agent 通信并不总是越多越好”的重要负面证据，直接支撑通信压缩、意图路由和协作成本控制。 |
| [Collaborative Belief Reasoning with LLMs for Efficient Multi-Agent Collaboration](https://arxiv.org/abs/2509.21981) | 2025 | arxiv | belief-modeling, intent-inference, embodied-collaboration, communication-efficiency | 直接补强“协作者意图理解 + 低通信成本协作”，适合和 Theory of Mind、belief state 类工作放在同一协作脉络。 |
| [Mediator-Guided Multi-Agent Collaboration among Open-Source Models for Medical Decision-Making](https://arxiv.org/abs/2508.05996) | 2025 | arxiv | mediator-agent, heterogeneous-models, medical-vqa, multimodal | 适合借鉴 mediator-guided collaboration 和异构模型协作机制。 |
| [Talk Structurally, Act Hierarchically: A Collaborative Framework for LLM Multi-Agent Systems](https://arxiv.org/abs/2502.11098) | 2025 | arxiv | structured-communication, hierarchical-refinement, talkhier, collaboration | 直接补强“通信协议 + 分层协作”的设计路线，可作为动态团队协作的强 baseline。 |
| [Tiered Agentic Oversight: A Hierarchical Multi-Agent System for Healthcare Safety](https://arxiv.org/abs/2506.12482) | 2025 | arxiv | hierarchical-oversight, safety, routing, healthcare | 对项目的 hierarchical routing、error absorption、human-in-the-loop 协作有参考价值。 |
| [ConSensus: Efficient Multi-Agent Collaboration for Multimodal Sensing](https://arxiv.org/abs/2601.06453) | 2026 | arxiv | multimodal, consensus, hybrid-fusion, token-efficient | 是“专业 agent + 低成本融合”的好例子，适合任务助手多源信息整合场景。 |

### Debate, Consensus & Verification

| 论文 | 年份 | Venue / 来源 | 标签 | 贴合理由 |
| --- | ---: | --- | --- | --- |
| [Can ChatGPT Defend its Belief in Truth? Evaluating LLM Reasoning via Debate](https://aclanthology.org/2023.findings-emnlp.795/) | 2023 | Findings of EMNLP 2023 | debate, reasoning-evaluation, belief-defense, verification | 补充多 agent 辩论的评测视角，可用于分析共识形成是否真正提升事实性和推理。 |
| [ChatEval: Towards Better LLM-based Evaluators through Multi-Agent Debate](https://arxiv.org/abs/2308.07201) | 2023 | arxiv | multi-agent-evaluation, debate, llm-as-judge | 可用于项目中的结果验证和 agent-as-judge 设计。 |
| [Encouraging Divergent Thinking in Large Language Models through Multi-Agent Debate](https://aclanthology.org/2024.emnlp-main.992/) | 2023 | EMNLP 2024 | mad, divergent-thinking, judge, reasoning | 是 debate/verification 协作主线的基础论文，已有条目保留为核心协作机制。 |
| [Improving Factuality and Reasoning in Language Models through Multiagent Debate](https://arxiv.org/abs/2305.14325) | 2023 | arxiv | multiagent-debate, factuality, reasoning, society-of-minds | 是 LLM multiagent debate 的代表性基础工作，应作为 debate 协作机制和 factuality 改进 baseline。 |
| [ReConcile: Round-Table Conference Improves Reasoning via Consensus among Diverse LLMs](https://aclanthology.org/2024.acl-long.381/) | 2023 | ACL 2024 | round-table, consensus, diverse-llms, confidence-weighted-voting | 对异构 agent 的 consensus 机制、置信度字段和投票聚合策略很有参考价值。 |
| [GroupDebate: Enhancing the Efficiency of Multi-Agent Debate Using Group Discussion](https://arxiv.org/abs/2409.14051) | 2024 | arxiv | group-debate, token-efficient, debate-groups | 直接对应项目“协作不能增加 token/耗时”的成本约束。 |
| [Mixture-of-Agents Enhances Large Language Model Capabilities](https://openreview.net/forum?id=h0ZfDIrj7T) | 2024 | ICLR 2025 Spotlight | mixture-of-agents, layered-aggregation, multi-model-collaboration, ensemble | 是多模型/多 agent 层级聚合的关键 baseline，也暴露了后续稀疏路由和成本控制需求。 |
| [More Agents Is All You Need](https://openreview.net/forum?id=bgzUSZ8aeg) | 2024 | TMLR 2024 | agent-forest, sampling-and-voting, scaling-agents, ensemble | 提供“更多 agent 是否值得”的基础 scaling 对照，可作为复杂协作机制的低成本 baseline。 |
| [Enhancing Multi-Agent Debate System Performance via Confidence Expression](https://arxiv.org/abs/2509.14034) | 2025 | EMNLP 2025 | confidence-expression, debate-dynamics, calibration | 可用于设计 agent 消息协议中的 confidence 字段和动态仲裁机制。 |
| [iMAD: Intelligent Multi-Agent Debate for Efficient and Accurate LLM Inference](https://arxiv.org/abs/2511.11306) | 2025 | AAAI 2026 | selective-debate, trigger-policy, token-efficient, confidence | 非常贴合“按需协作”和“成本不增”的产品目标。 |
| [Stay Focused: Problem Drift in Multi-Agent Debate](https://arxiv.org/abs/2502.19559) | 2025 | EACL 2025 | problem-drift, debate-failure, driftjudge, driftpolicy | 重要负面结果，提醒协作轮次越多不一定越好，必须有终止和聚焦机制。 |
| [ARMOR-MAD: Adaptive Routing for Heterogeneous Multi-Agent Debate in Large Language Model Reasoning](https://arxiv.org/abs/2606.13197) | 2026 | arxiv | adaptive-routing, heterogeneous-agents, debate | 与项目的“能力波动、动态路由、成本控制”高度相关。 |
| [Courtroom-Style Multi-Agent Debate with Progressive RAG and Role-Switching for Controversial Claim Verification](https://arxiv.org/abs/2603.28488) | 2026 | arxiv | courtroom-debate, progressive-rag, role-switching, claim-verification | 对结构化 adversarial collaboration 和证据扩展机制有参考价值。 |
| [DynaDebate: Breaking Homogeneity in Multi-Agent Debate with Dynamic Path Generation](https://arxiv.org/abs/2601.05746) | 2026 | arxiv | dynamic-path-generation, process-centric-debate, verification-agent | 对“动态角色/路径分配 + verifier 触发机制”很有参考价值。 |
| [Multi-Agent Debate with Memory Masking](https://arxiv.org/abs/2603.20215) | 2026 | arxiv | memory-masking, debate-robustness, erroneous-memory | 直接支撑“关键信息传不准/错误信息传播”的上下文治理机制。 |
| [Tool-MAD: A Multi-Agent Debate Framework for Fact Verification with Diverse Tool Augmentation and Adaptive Retrieval](https://arxiv.org/abs/2601.04742) | 2026 | arxiv | tool-augmented-debate, adaptive-retrieval, fact-verification | 适合任务助手中的事实核验、工具专长协作和 evidence-aware debate。 |

### Role-Playing, Agent Society & Simulation

| 论文 | 年份 | Venue / 来源 | 标签 | 贴合理由 |
| --- | ---: | --- | --- | --- |
| [CAMEL: Communicative Agents for "Mind" Exploration of Large Language Model Society](https://arxiv.org/abs/2303.17760) | 2023 | NeurIPS 2023 | camel, role-playing, inception-prompting, agent-society | 是 LLM 多 agent 角色协作和 agent society 的基础论文，应作为后续 CAMEL/role-playing 工作源头。 |
| [Generative Agents: Interactive Simulacra of Human Behavior](https://dl.acm.org/doi/10.1145/3586183.3606763) | 2023 | UIST 2023 | generative-agents, memory, reflection, social-simulation | 对长期记忆、反思和群体涌现行为建模有基础价值，可支撑“协作系统如何积累经验”的背景。 |
| [SOTOPIA: Interactive Evaluation for Social Intelligence in Language Agents](https://openreview.net/forum?id=mM7VurbA4r) | 2023 | ICLR 2024 Spotlight | social-intelligence, role-play, interaction-evaluation, sotopia | 可补足多 agent 协作评测中“社会智能、策略沟通、角色互动”这类非代码任务维度。 |
| [LLM Harmony: Multi-Agent Communication for Problem Solving](https://arxiv.org/abs/2401.01312) | 2024 | arxiv | role-playing, personas, communication, problem-solving | 可作为早期 role-playing collaboration baseline。 |

### Software Engineering Multi-Agent Collaboration

| 论文 | 年份 | Venue / 来源 | 标签 | 贴合理由 |
| --- | ---: | --- | --- | --- |
| [ChatDev: Communicative Agents for Software Development](https://aclanthology.org/2024.acl-long.810/) | 2023 | ACL 2024 | chatdev, chat-chain, communicative-dehallucination, software-development | 是软件工程多 agent 协作的代表性工作，应作为固定流程和语言通信协作 baseline。 |
| [MetaGPT: Meta Programming for A Multi-Agent Collaborative Framework](https://arxiv.org/abs/2308.00352) | 2023 | arxiv | sop, role-specialization, software-agents | 适合作固定 SOP 协作 baseline，用于对比动态拓扑和自进化方法。 |
| [AgentMesh: A Cooperative Multi-Agent Generative AI Framework for Software Development Automation](https://arxiv.org/abs/2507.19902) | 2025 | arxiv | planner, coder, debugger, reviewer, software | 是经典角色分工流水线 baseline，适合和动态/进化式协作比较。 |
| [Co-Saving: Resource Aware Multi-Agent Collaboration for Software Development](https://arxiv.org/abs/2505.21898) | 2025 | arxiv | resource-aware, shortcuts, experiential-knowledge, token-reduction | 直接服务项目“成本不增”和“从历史轨迹进化”的目标。 |
| [DocAgent: A Multi-Agent System for Automated Code Documentation Generation](https://arxiv.org/abs/2504.08725) | 2025 | arxiv | documentation, topological-code-processing, verifier, orchestrator | 适合参考“上下文拓扑排序 + 专业 agent + verifier”的协作结构。 |
| [Optimizing LLM-Based Multi-Agent System with Textual Feedback: A Case Study on Software Development](https://arxiv.org/abs/2505.16086) | 2025 | arxiv | textual-feedback, prompt-optimization, group-optimization, software | 是“根据失败解释优化多 agent 角色/prompt”的直接相关论文。 |
| [Shadows in the Code: Exploring the Risks and Defenses of LLM-based Multi-Agent Software Development Systems](https://arxiv.org/abs/2511.18467) | 2025 | AAAI 2026 | security, malicious-agent, software-development, defense | 说明多 agent 协作系统必须有分角色安全和关键 agent 防护。 |
| [Towards Engineering Multi-Agent LLMs: A Protocol-Driven Approach](https://doi.org/10.1109/APSEC66846.2025.00100) | 2025 | APSEC 2025 | protocol, structured-messaging, lifecycle, a2a, semap | 与“通用协作框架”和 A2A/MCP 风格协议化设计高度贴合。 |
| [Self-Organizing Multi-Agent Systems for Continuous Software Development](https://arxiv.org/abs/2603.25928) | 2026 | arxiv | self-organizing, continuous-development, manager-agents, hire-fire | 强相关于动态 agent 组队、长期任务和自组织协作。 |

### Robustness & Reliability

| 论文 | 年份 | Venue / 来源 | 标签 | 贴合理由 |
| --- | ---: | --- | --- | --- |
| [On the Resilience of LLM-Based Multi-Agent Collaboration with Faulty Agents](https://openreview.net/forum?id=bkiM54QftZ) | 2024 | ICML 2025 Poster | faulty-agents, resilience, challenge, reviewer | 直接对应项目“agent 上下线、能力波动、整体任务执行不稳定”的痛点。 |
| [Amplified Vulnerabilities: Structured Jailbreak Attacks on LLM-based Multi-Agent Debate](https://arxiv.org/abs/2504.16489) | 2025 | arxiv | jailbreak, multi-agent-debate, security, attack | 说明多 agent 协作不天然更安全，必须把消息安全、角色安全和验证机制纳入设计。 |
| [Disagreements Can Help: A Self-Repair Approach to LLM Agents' Robustness in Knowledge Conflicts](https://arxiv.org/abs/2502.15153) | 2025 | arxiv | knowledge-conflict, self-repair, disagreement | 可用于设计冲突检测、互相质疑和自修复协作机制。 |
| [GUARDIAN: Safeguarding LLM Multi-Agent Collaborations with Temporal Graph Modeling](https://arxiv.org/abs/2505.19234) | 2025 | arxiv | temporal-graph, safety, hallucination-propagation, anomaly-detection | 直接服务于“关键信息传不准”和错误跨 agent 放大的安全问题，可作为 trace graph 防御方向。 |
| [Maris: A Formally Verifiable Privacy Policy Enforcement Paradigm for Multi-Agent Collaboration Systems](https://arxiv.org/abs/2505.04799) | 2025 | arxiv | privacy-policy, message-flow-control, reference-monitor, prompt-injection | 直接补强多 agent 通信的治理层，适合支撑敏感信息跨 agent 泄露和权限边界设计。 |
| [VerifyMAS: Hypothesis Verification for Failure Attribution in LLM Multi-Agent Systems](https://arxiv.org/abs/2605.17467) | 2026 | arxiv | failure-attribution, trace-analysis, verification | 自进化系统必须先知道失败来自分解、路由、执行、合成还是验证，故强相关。 |
| [When Embedding-Based Defenses Fail: Rethinking Safety in LLM-Based Multi-Agent Systems](https://arxiv.org/abs/2605.01133) | 2026 | arxiv | safety, malicious-agent, message-defense | 适合支撑多 agent 消息污染、防御和可信通信子方向。 |

### Evolution & Optimization

| 论文 | 年份 | Venue / 来源 | 标签 | 贴合理由 |
| --- | ---: | --- | --- | --- |
| [Reflexion: Language Agents with Verbal Reinforcement Learning](https://arxiv.org/abs/2303.11366) | 2023 | NeurIPS 2023 | self-reflection, verbal-rl, episodic-memory | 是自进化机制的单 agent 基础，可扩展到团队级经验沉淀。 |
| [Self-Taught Optimizer (STOP): Recursively Self-Improving Code Generation](https://arxiv.org/abs/2310.02304) | 2023 | arxiv | self-improvement, scaffold-optimization, code-generation | 可作为自动改 prompt/tool/workflow 的思想背景。 |
| [Voyager: An Open-Ended Embodied Agent with Large Language Models](https://openreview.net/forum?id=ehfRiF0R3a) | 2023 | TMLR 2024 | lifelong-learning, skill-library, self-verification | 支撑“技能库/经验库”式长期进化，但本身不是多 agent 主线。 |
| [AFlow: Automating Agentic Workflow Generation](https://openreview.net/forum?id=z5uVAKwmjf) | 2024 | ICLR 2025 Oral | workflow-search, mcts, agentic-workflow | 适合作离线 workflow 自动优化器，对项目“可自进化协作系统”非常关键。 |
| [EvoAgent: Towards Automatic Multi-Agent Generation via Evolutionary Algorithms](https://aclanthology.org/2025.naacl-long.315/) | 2024 | NAACL 2025 | evolutionary-algorithm, multi-agent-generation, mutation, crossover | 与项目“群体进化”命名和目标直接对齐。 |
| [ExpeL: LLM Agents Are Experiential Learners](https://doi.org/10.1609/aaai.v38i17.29936) | 2024 | AAAI 2024 | experiential-learning, memory, reflection, agent-learning | 虽然不是多 agent 专用，但为“从执行轨迹中积累经验并改进行为”的进化闭环提供关键基线。 |
| [Experiential Co-Learning of Software-Developing Agents](https://aclanthology.org/2024.acl-long.305/) | 2024 | ACL 2024 | experiential-learning, software-agents, co-learning, trajectory-memory | 直接连接多 agent 软件协作和经验驱动进化，可作为 ChatDev 类系统如何从失败和轨迹中持续改进的核心参考。 |
| [GPTSwarm: Language Agents as Optimizable Graphs](https://openreview.net/forum?id=uTC9AFXIhg) | 2024 | ICML 2024 Oral | gptswarm, graph-optimization, prompt-optimization, edge-optimization | 几乎直接对应“多 agent 反馈链路如何优化”，可作为群体进化主 baseline。 |
| [AgentNet: Decentralized Evolutionary Coordination for LLM-based Multi-Agent Systems](https://arxiv.org/abs/2504.00587) | 2025 | arxiv | decentralized-coordination, agent-evolution, rag, dynamic-routing | 补齐去中心化协作进化路线，与 centralized orchestrator/manager 架构形成重要对照。 |
| [Cross-Task Experiential Learning on LLM-based Multi-Agent Collaboration](https://arxiv.org/abs/2505.23187) | 2025 | arxiv | mael, cross-task-experience, graph-collaboration, reward-pool | 直接补强“跨任务经验积累”和“协作系统进化”方向。 |
| [MAS-GPT: Training LLMs to Build LLM-based Multi-Agent Systems](https://openreview.net/forum?id=3CiSpY3QdZ) | 2025 | ICML 2025 Poster | mas-generation, query-adaptive, executable-code, system-design | 直接面向“根据任务自动生成协作系统”的进化方向，可与 AFlow、SwarmAgentic、ARG-Designer 共同构成自动化设计主线。 |
| [Multi-Agent Collaboration via Evolving Orchestration](https://arxiv.org/abs/2505.19591) | 2025 | NeurIPS 2025 | evolving-orchestration, puppeteer, reinforcement-learning, dynamic-sequencing | 直接补齐“协作编排本身可进化”的顶会工作，适合和 GPTSwarm、AFlow、EvoAgent、EvoMAS 共同作为进化主线 baseline。 |
| [SwarmAgentic: Towards Fully Automated Agentic System Generation via Swarm Intelligence](https://aclanthology.org/2025.emnlp-main.93/) | 2025 | EMNLP 2025 | agentic-system-generation, swarm-intelligence, automated-design, evolution | 直接补充多 agent 系统自动生成与进化方向，适合与 AFlow/GPTSwarm/EvoAgent 放在同一脉络。 |
| [Evolutionary Generation of Multi-Agent Systems](https://arxiv.org/abs/2602.06511) | 2026 | arxiv | evomas, configuration-space, evolutionary-generation | 对工程落地尤其重要，因为配置空间进化比任意代码进化更可控。 |
| [Evolve as a Team: Collaborative Self-Evolution for LLM-based Multi-Agent Systems](https://arxiv.org/abs/2605.29790) | 2026 | arxiv | team-evolution, collaborative-self-evolution, post-task-communication | 最贴合“多 agent 之间互相影响的复杂反馈链路”的研究问题。 |
| [Swarm Skills: A Portable, Self-Evolving Multi-Agent System Specification](https://arxiv.org/abs/2605.10052) | 2026 | arxiv | swarm-skills, portable-specification, self-evolving | 对“通用协作框架、可迁移到其他智能体产品线”非常贴合。 |

### Evaluation & Benchmarks

| 论文 | 年份 | Venue / 来源 | 标签 | 贴合理由 |
| --- | ---: | --- | --- | --- |
| [AgentBench: Evaluating LLMs as Agents](https://openreview.net/forum?id=zAdUB0aCTQ) | 2023 | ICLR 2024 Poster | agent-benchmark, interactive-environment, evaluation | 可作为任务助手多 agent 系统的公共能力评测参考。 |
| [GAIA: a benchmark for General AI Assistants](https://openreview.net/forum?id=fibxvahvs3) | 2023 | ICLR 2024 Poster | general-assistant, web, tool-use, benchmark | 适合作“多步骤信息搜集+整合”公共评测集。 |
| [SWE-bench: Can Language Models Resolve Real-World GitHub Issues?](https://openreview.net/forum?id=VTF8yNQM66) | 2023 | ICLR 2024 Oral | software-engineering, long-horizon, benchmark | 适合测长上下文、多步骤协作和可恢复执行，但需补充非代码长尾任务。 |
| [Agent-as-a-Judge: Evaluate Agents with Agents](https://openreview.net/forum?id=Nn9POI9Ekt) | 2024 | ICML 2025 Poster | agent-evaluation, process-feedback, llm-judge | 自进化需要 reward/critic，该论文可支撑反馈信号设计。 |
| [VillagerAgent: A Graph-Based Multi-Agent Framework for Coordinating Complex Task Dependencies in Minecraft](https://arxiv.org/abs/2406.05720) | 2024 | arxiv | villagerbench, minecraft, dag-coordination, complex-dependencies | 适合作为复杂依赖、多 agent 分工、同步和动态适应能力的协作评测场景。 |
| [MALLM: Multi-Agent Large Language Models Framework](https://arxiv.org/abs/2509.11656) | 2025 | EMNLP 2025 Demo | multi-agent-debate, framework, configuration, evaluation-pipeline | 适合系统比较 debate、relay、memory、voting、consensus 等多 agent 策略，补齐“实验框架/可复现评测”维度。 |
| [MultiAgentBench: Evaluating the Collaboration and Competition of LLM agents](https://aclanthology.org/2025.acl-long.421/) | 2025 | ACL 2025 | benchmark, collaboration, competition, coordination-protocols | 是当前多 agent 协作评测的重要 ACL 基准，可用于验证通信拓扑和协作策略是否真正提升任务完成与协作质量。 |
| [MARBLE: Multi-Agent Reasoning for Bioinformatics Learning and Evolution](https://arxiv.org/abs/2601.14349) | 2026 | arxiv | bioinformatics, multi-agent-reasoning, learning, evolution | 虽是垂直领域，但对“领域复杂任务 + 多 agent 学习/进化”有参考价值，适合作补充性 benchmark。 |

### Surveys & Taxonomies

| 论文 | 年份 | Venue / 来源 | 标签 | 贴合理由 |
| --- | ---: | --- | --- | --- |
| [A Survey of Multi-Agent Deep Reinforcement Learning with Communication](https://doi.org/10.1007/s10458-023-09633-6) | 2024 | Autonomous Agents and Multi-Agent Systems 2024 | survey, marl, communication, protocols | 为 LLM 多 agent 通信研究提供前 LLM 时代的系统背景，帮助区分学到的通信协议与提示式通信。 |
| [The Landscape of Emerging AI Agent Architectures for Reasoning, Planning, and Tool Calling](https://arxiv.org/abs/2404.11584) | 2024 | arxiv | survey, agent-architecture, planning, tool-use | 适合作 agent architecture 背景章节。 |
| [Multi-Agent Collaboration Mechanisms: A Survey of LLMs](https://arxiv.org/abs/2501.06322) | 2025 | arxiv | survey, collaboration, coordination-protocols | 适合作本综述的分类法参考。 |
| [Multi-Agent Coordination across Diverse Applications: A Survey](https://arxiv.org/abs/2502.14743) | 2025 | arxiv | survey, coordination, scalability, heterogeneity | 适合支撑“协作”的理论定义和跨领域背景。 |

## GitHub 项目目录

### Frameworks & Runtimes

| 项目 | 标签 | 贴合理由 |
| --- | --- | --- |
| [AG2](https://github.com/ag2ai/ag2) | autogen-fork, agentos, groupchat, multi-agent | 适合与 Microsoft AutoGen 对比，观察社区版多 agent 框架如何演进。 |
| [Agent Squad](https://github.com/2FastLabs/agent-squad) | routing, multi-agent, specialist-agents, context | 与项目“任务助手多专业 agent 联合执行”和 request routing 高度相关。 |
| [AgentScope](https://github.com/agentscope-ai/agentscope) | multi-agent-platform, message-exchange, fault-tolerance, distributed | 与“通用协作框架 + 动态协作 + 鲁棒部署”高度贴合。 |
| [AgentVerse](https://github.com/OpenBMB/AgentVerse) | multi-agent, framework, simulation, collaboration | 可作为早期通用多 agent 协作框架和仿真实验平台参考。 |
| [Agno](https://github.com/agno-agi/agno) | agent-platform, teams, memory, runtime | 适合参考多 agent team 在生产平台中的运行、管理和观测抽象。 |
| [AutoGen](https://github.com/microsoft/autogen) | multi-agent, event-driven, agentchat, runtime | 适合参考多 agent conversation、事件驱动通信和分布式 agent runtime。 |
| [BeeAI Framework](https://github.com/i-am-bee/beeai-framework) | python, typescript, workflows, production-agents | 可作为企业级多 agent 运行时、工具接入和协议生态的补充参考。 |
| [CAMEL](https://github.com/camel-ai/camel) | agent-society, multi-agent, memory, benchmarks | 适合做多 agent 实验平台和 agent society baseline。 |
| [ChatDev](https://github.com/OpenBMB/ChatDev) | software-company, chat-chain, multi-agent, macnet | 是软件工程多 agent 协作和协作 scaling law 的核心参考实现。 |
| [CrewAI](https://github.com/crewAIInc/crewAI) | crews, flows, role-based, business-workflows | 可作为业务流程协作 baseline，但研究创新不应停留在框架调用。 |
| [deepagents](https://github.com/langchain-ai/deepagents) | long-running, subagents, planning, langgraph | 适合参考长尾复杂任务中 subagent 编排、任务持久化和工作状态管理。 |
| [Google ADK](https://github.com/google/adk-python) | agent-development-kit, multi-agent, evaluation, deployment | 可作为多 agent 产品化 SDK、评测和部署路径的强参考。 |
| [LangGraph](https://github.com/langchain-ai/langgraph) | graph-runtime, stateful, durable-execution, multi-agent | 适合做多 agent 协作运行时和 traceable workflow baseline。 |
| [LlamaIndex](https://github.com/run-llama/llama_index) | agent-workflows, retrieval, tools, multi-agent | 对“多 agent + 检索/文档/数据任务”的任务助手落地很重要，适合作为 RAG-heavy 协作基线。 |
| [Mastra](https://github.com/mastra-ai/mastra) | typescript, workflows, agents, memory | 对前端/Node 生态中多 agent workflow 与产品化部署很有参考价值。 |
| [MetaGPT](https://github.com/FoundationAgents/MetaGPT) | sop, role-specialization, software-company | 适合做固定角色/固定流程协作 baseline。 |
| [Microsoft Agent Framework](https://github.com/microsoft/agent-framework) | multi-agent, workflows, orchestration, observability | 适合跟踪 AutoGen 之后的生产级多 agent 编排方向。 |
| [NeMo Agent Toolkit](https://github.com/NVIDIA/NeMo-Agent-Toolkit) | agent-toolkit, multi-agent, optimization, nvidia | 与“多 agent 协作优化”和企业级 agent team 运行效率直接相关。 |
| [Open Multi-Agent](https://github.com/open-multi-agent/open-multi-agent) | dag, tracing, typescript, multi-agent | 适合作任务 DAG、并行协作和可观测执行 baseline。 |
| [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) | agents, handoffs, tracing, guardrails, mcp | 适合借鉴 handoff、manager-style orchestration 和 tracing 的简洁抽象。 |
| [OpenAI Swarm](https://github.com/openai/swarm) | educational, handoffs, routines, multi-agent-orchestration | 虽非生产框架，但对理解 handoff、agent-as-tool 和轻量编排模式非常有参考价值。 |
| [PraisonAI](https://github.com/MervinPraison/PraisonAI) | multi-agent, workforce, self-improving, rag | 可作为业务流程中“多角色 agent workforce”落地方式的对照项目。 |
| [Pydantic AI](https://github.com/pydantic/pydantic-ai) | typed-agents, structured-output, graph, production | 多 agent 协作需要强 schema、可验证状态和清晰工具契约，Pydantic AI 是重要工程参考。 |
| [Semantic Kernel](https://github.com/microsoft/semantic-kernel) | enterprise, orchestration, plugins, multi-agent | 适合作企业场景中多 agent 编排、工具接入和结构化插件契约的工程参考。 |
| [smolagents](https://github.com/huggingface/smolagents) | code-agents, managed-agents, tools, lightweight | 对“简洁 agent loop + managed subagents”的最小实现有参考价值，可作为复杂框架的低开销对照。 |
| [Strands Agents](https://github.com/strands-agents/sdk-python) | sdk, multi-agent, mcp, production | 对“通用协作框架 + 跨模型/跨工具生态”有参考价值。 |

### Protocols & Interoperability

| 项目 | 标签 | 贴合理由 |
| --- | --- | --- |
| [Agent Client Protocol](https://github.com/agentclientprotocol/agent-client-protocol) | acp, editor-agent, protocol, sessions | 对跨宿主 agent 协作、agent handoff 和可迁移会话协议有参考价值。 |
| [Agent Communication Protocol](https://github.com/i-am-bee/acp) | acp, agent-protocol, interoperability, archived | 与 A2A、ANP、MCP 一起构成跨 agent 通信协议调研边界，应在协议对比中说明其归档状态。 |
| [Agent Network Protocol](https://github.com/agent-network-protocol/AgentNetworkProtocol) | anp, agent-network, interoperability, decentralized | 补齐 A2A/MCP 之外的协议路线，适合研究跨组织 agent 发现和协作网络。 |
| [Agent2Agent Protocol](https://github.com/a2aproject/A2A) | a2a, agent-interop, task-delegation, agent-cards | 与“通用协作框架”和跨产品线 agent 协作高度相关。 |
| [Agora Protocol](https://github.com/agora-protocol/python) | agora, protocol, python-sdk, collaboration | 可作为 ProtocolBench 类协议评测中的协议生态补充，不作为核心工程框架。 |
| [mcp-agent](https://github.com/lastmile-ai/mcp-agent) | mcp, workflow, multi-server, agent-framework | 适合参考如何把多个工具服务器聚合进 agent 协作流程。 |
| [Model Context Protocol](https://github.com/modelcontextprotocol/modelcontextprotocol) | mcp, tools, resources, prompts, interoperability | 多智能体框架若要跨产品线复用，工具/上下文接入层建议兼容 MCP。 |

### Benchmarks & Evaluation

| 项目 | 标签 | 贴合理由 |
| --- | --- | --- |
| [AgentBench](https://github.com/THUDM/AgentBench) | agent-benchmark, environments, reasoning, decision-making | 适合测基础 agent 执行能力，但需补充多 agent 通信和进化指标。 |
| [ChatEval](https://github.com/thunlp/ChatEval) | multi-agent-evaluator, debate, llm-as-judge | 可作为多 agent verifier/judge 组件和评价方法 baseline。 |
| [Collaborative Gym](https://github.com/SALT-NLP/collaborative-gym) | collaborative-agents, human-agent-collaboration, evaluation, environments | 补齐 human-agent/team collaboration 评测维度，有助于评估多 agent 与人类协同的真实可用性。 |
| [DeepEval](https://github.com/confident-ai/deepeval) | evaluation, llm-judge, testing | 可作为自建 Qianwen-LongTail-MAS-Bench 的评测基础设施参考。 |
| [E2EDev](https://github.com/SCUNLP/E2EDev) | end-to-end-software-development, bdd, multi-agent-annotation, benchmark | 适合评估多 agent 从需求到交付的完整长任务能力。 |
| [M-MAD](https://github.com/SU-JIAYUAN/M-MAD) | multi-agent-debate, machine-translation-evaluation, llm-as-judge | 适合参考如何把复杂评价标准拆成多个 specialist judges。 |
| [MARBLE / MultiAgentBench](https://github.com/ulab-uiuc/MARBLE) | multiagentbench, marble, acl-2025, collaboration, competition | 对验证多 agent 通信拓扑、协作协议和竞争/协作行为质量非常关键。 |
| [Multi-Agents-Debate](https://github.com/Skytliang/Multi-Agents-Debate) | multi-agent-debate, reasoning, judge | 是 debate 协作机制的核心 baseline。 |
| [Promptfoo](https://github.com/promptfoo/promptfoo) | eval, red-team, ci, regression | 适合做多 agent 变更后的回归测试和安全测试。 |
| [SWE-bench](https://github.com/SWE-bench/SWE-bench) | software-engineering, long-horizon, benchmark | 可测长任务执行、上下文管理、验证和恢复能力。 |
| [SWE-Dev](https://github.com/DorothyDUUU/SWE-Dev) | feature-development, software-engineering, benchmark, rl | 适合补充 SWE-bench 对“新增功能/端到端开发”的覆盖。 |
| [tau2-bench](https://github.com/sierra-research/tau2-bench) | tool-agent-user, benchmark, multi-turn, real-world-domains | 适合评估多 agent 任务助手在真实工具和用户反馈循环中的协作表现。 |
| [Terminal-Bench](https://github.com/harbor-framework/terminal-bench) | terminal, benchmark, long-horizon, verification | 可用于测试多 agent 在代码、命令行、文件系统任务中的长程协作和恢复能力。 |
| [TheAgentCompany](https://github.com/TheAgentCompany/TheAgentCompany) | workplace, simulated-company, benchmark, long-horizon | 与多 agent 任务助手和软件团队协作评测高度相关。 |
| [WebArena](https://github.com/web-arena-x/webarena) | web-agent, benchmark, realistic-environment, tool-use | 可作为任务助手“多步骤信息搜集+执行”的公共环境基准。 |
| [WorkArena](https://github.com/ServiceNow/WorkArena) | enterprise, web-agent, service-workflows, benchmark | 适合补充企业长尾任务、流程系统和真实业务操作场景的评测。 |

### Observability & Operations

| 项目 | 标签 | 贴合理由 |
| --- | --- | --- |
| [AgentOps](https://github.com/AgentOps-AI/agentops) | agent-monitoring, tracing, cost, benchmarks | 多 agent 通信、成本和失败归因需要统一轨迹与成本观测，AgentOps 是强工程参考。 |
| [Arize Phoenix](https://github.com/Arize-ai/phoenix) | observability, eval, tracing, llmops | 可作为 trace + evaluation + failure analysis 工程参考。 |
| [GUARDIAN](https://github.com/JialongZhou666/GUARDIAN) | temporal-graph, safety, anomaly-detection, multi-agent | 适合把多 agent 消息 trace 转成图并做错误传播/异常检测。 |
| [Langfuse](https://github.com/langfuse/langfuse) | observability, traces, cost, prompts | 适合记录多 agent 消息、成本、失败轨迹和进化前后对比。 |
| [LangSmith](https://github.com/langchain-ai/langsmith-sdk) | observability, tracing, eval, debugging | 多 agent 通信/进化需要 trace-native evaluation，LangSmith 可作工程参考。 |
| [LangWatch](https://github.com/langwatch/langwatch) | evaluations, simulations, agent-testing, observability | 适合作多 agent 变更后的离线仿真、回归评测和线上质量监控。 |
| [Weave](https://github.com/wandb/weave) | tracing, evaluations, llmops, wandb | 可用于多 agent 轨迹回放、成本/质量对比和进化前后评估。 |

### Research Implementations & Baselines

| 项目 | 标签 | 贴合理由 |
| --- | --- | --- |
| [AgentForest](https://github.com/MoreAgentsIsAllYouNeed/AgentForest) | sampling-and-voting, agent-scaling, ensemble-baseline | 适合作为最简单但必须比较的多 agent scaling baseline。 |
| [AgentNet](https://github.com/zoe-yyx/AgentNet) | decentralized, evolutionary-coordination, rag, dynamic-routing | 与中心化 orchestrator 架构形成对照，适合研究去中心化协作和进化机制。 |
| [AgentPrune](https://github.com/yanweiyue/AgentPrune) | communication-pruning, token-efficiency, iclr-2025, robustness | 是低成本通信和通信鲁棒性实验的重要 baseline，适合直接纳入复现实验。 |
| [ARG-Designer](https://github.com/Shiy-Li/ARG-Designer) | aaai-2026, topology-generation, role-selection, graph-generation | 对自动组队、自动拓扑设计和低成本协作非常关键，适合作为前沿 baseline。 |
| [Dr. MAS](https://github.com/langfengQ/DrMAS) | reinforcement-learning, co-training, heterogeneous-llms, multi-agent | 对群体进化和多 agent 学习机制有参考价值，适合作为训练型 MAS baseline。 |
| [Generative Agents](https://github.com/joonspk-research/generative_agents) | agent-society, memory, reflection, simulation | 适合作为长期记忆、经验沉淀和 agent society 章节的经典参考实现。 |
| [GPTSwarm](https://github.com/metauto-ai/GPTSwarm) | optimizable-graphs, prompt-optimization, edge-optimization, evolution | 是群体进化和“多 agent 反馈链路优化”的核心实现，应作为主 baseline。 |
| [MALLM](https://github.com/Multi-Agent-LLMs/mallm) | multi-agent-llms, consensus, debate, framework | 适合快速搭建 debate、投票、共识类 baseline，并记录多 agent 实验配置。 |
| [MARTI](https://github.com/TsinghuaC3I/MARTI) | reinforced-training, inference, multi-agent-llm, optimization | 补齐“多 agent 不只推理编排，也可训练/强化优化”的工程路线。 |
| [MAS-GPT](https://github.com/MASWorks/MAS-GPT) | mas-generation, icml-2025, executable-code, auto-design | 是自动化多 agent 系统生成和进化方向的重要实现。 |
| [MasRouter](https://github.com/yanweiyue/masrouter) | routing, acl-2025, llm-selection, multi-agent | 是动态路由、低成本协作和模型选择实验的核心 baseline。 |
| [RADAR](https://github.com/cszhangzhen/RADAR) | communication-structure, diffusion, redundancy-aware, topology-generation | 作为 2026 通信结构生成候选 baseline，可与 G-Designer、ARG-Designer 对比。 |
| [ReConcile](https://github.com/dinobby/ReConcile) | round-table, consensus, confidence-weighted-voting, diverse-models | 可作为异构 agent 共识、置信度表达和投票聚合的基础实现。 |
| [RMoA](https://github.com/mindhunter01/RMoA) | residual-mixture-of-agents, diversity-selection, adaptive-termination | 可作为 MoA 家族中“信息保真 + 成本控制”的重要对照。 |
| [SMoA](https://github.com/David-Li0406/SMoA) | sparse-mixture-of-agents, response-selection, early-stopping | 适合研究多 agent 聚合如何在保持效果的同时降低成本。 |
| [SOTOPIA](https://github.com/sotopia-lab/sotopia) | social-intelligence, role-play, interaction-evaluation | 可补充非代码长尾任务中的协作、沟通和社会目标评测。 |
| [TalkHier](https://github.com/sony/talkhier) | structured-communication, hierarchical-refinement, llm-multi-agent | 适合做“结构化消息协议 + 分层协作修正”的核心 baseline。 |
| [VillagerAgent](https://github.com/cnsdqd-dyb/VillagerAgent-Minecraft-multiagent-framework) | minecraft, villagerbench, dag-coordination, complex-dependencies | 适合构造任务依赖、同步、动态适应和 hallucination 控制的协作评测。 |

### Reference Systems & Case Studies

| 项目 | 标签 | 贴合理由 |
| --- | --- | --- |
| [DocAgent](https://github.com/facebookresearch/DocAgent) | documentation, verifier, orchestrator, code-understanding | 是“专业 agent + topological context + verifier”的清晰参考系统。 |
| [Magentic-One](https://github.com/microsoft/autogen/tree/main/python/packages/autogen-magentic-one) | orchestrator, specialist-agents, autogenbench, replanning | 是 orchestrator-subagent 架构、错误恢复和隔离评测的高价值参考系统。 |
| [OpenHands](https://github.com/OpenHands/OpenHands) | software-agent, coding, benchmark, runtime | 虽不是纯多 agent 框架，但可作为长任务执行、工具使用和软件任务评测的重要 baseline。 |
| [SWE-agent](https://github.com/SWE-agent/SWE-agent) | software-agent, swe-bench, execution, repair | 可作为单/多 agent 软件任务对比基线，帮助衡量多 agent 协作是否真正带来收益。 |
| [Symphony](https://github.com/openai/symphony) | orchestration, issue-driven, isolated-runs, coding-agents | 虽偏编码 agent，但对“任务分解、隔离执行、编排控制面和回收结果”非常有参考价值。 |

## 技术文档、博客与工程复盘

### Anthropic Official Engineering Articles

| 阅读材料 | 标签 | 贴合理由 |
| --- | --- | --- |
| [Anthropic - Building Effective AI Agents](https://www.anthropic.com/engineering/building-effective-agents) | engineering-guide, workflows, agents, patterns | 是多 agent 协作模式选择的基础阅读，能防止把所有任务都错误地做成复杂多 agent。 |
| [Anthropic - Building multi-agent systems](https://claude.com/blog/building-multi-agent-systems-when-and-how-to-use-them) | field-report, context-protection, specialization, token-cost | 直接约束本项目“token 消耗和端到端耗时维持不增”的工程边界。 |
| [Anthropic - Claude Code auto mode](https://www.anthropic.com/engineering/claude-code-auto-mode) | permissions, autonomy, classifier, coding-agents | 对多 agent 中 human-in-the-loop、权限门控和自动化边界设计有启发。 |
| [Anthropic - Claude Code sandboxing](https://www.anthropic.com/engineering/claude-code-sandboxing) | sandboxing, security, autonomy, coding-agents | 多 agent 协作会放大工具调用和文件系统风险，沙箱边界是基础治理机制。 |
| [Anthropic - Code execution with MCP](https://www.anthropic.com/engineering/code-execution-with-mcp) | mcp, code-execution, sandbox, tool-boundaries | 多 agent 系统需要清晰工具边界和执行隔离，MCP 是关键互操作层。 |
| [Anthropic - Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) | agent-evals, nondeterminism, trajectories, evaluation | 自进化多 agent 必须有可靠 eval/reward，这篇补齐评测方法论。 |
| [Anthropic - Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents) | context-engineering, memory, working-state, token-budget | 多 agent 通信路由本质上依赖上下文预算和信息选择，这篇可直接支撑通信层设计。 |
| [Anthropic - Effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents) | long-running-agents, state, resumability, harness | 任务助手长尾复杂任务通常是长时任务，多 agent 协作运行时必须处理恢复和状态漂移。 |
| [Anthropic - Harness design for long-running application development](https://www.anthropic.com/engineering/harness-design-long-running-apps) | long-running, app-development, harness, reliability | 可为软件工程多 agent 协作和持续开发任务提供工程约束。 |
| [Anthropic - How we built our multi-agent research system](https://www.anthropic.com/engineering/multi-agent-research-system) | field-report, lead-agent, parallel-subagents, research | 是“多步骤信息搜集+整合”场景最直接的公开工程案例，应作为系统设计和成本评估的必读材料。 |
| [Anthropic - Multi-agent coordination patterns](https://claude.com/blog/multi-agent-coordination-patterns) | patterns, generator-verifier, orchestrator-subagent, message-bus, shared-state | 可作为本仓库协作分类和系统架构章节的工程模式骨架。 |
| [Anthropic - Quantifying infrastructure noise in agentic coding evals](https://www.anthropic.com/engineering/infrastructure-noise) | evaluation, infrastructure-noise, coding-agents, reproducibility | 多 agent 系统评测更容易受环境和基础设施波动影响，这篇适合指导评测治理。 |
| [Anthropic - Scaling Managed Agents](https://www.anthropic.com/engineering/managed-agents) | managed-agents, session-logs, sandbox, architecture | 对多 agent 运行时边界、隔离执行和状态回放设计很有参考价值。 |
| [Anthropic - Writing effective tools for AI agents](https://www.anthropic.com/engineering/writing-tools-for-agents) | tool-design, schemas, agent-tools, reliability | 多 agent 框架中的 specialist agents 常以工具形式互相调用，工具契约质量直接影响协作可靠性。 |

### OpenAI Official Engineering Articles and Docs

| 阅读材料 | 标签 | 贴合理由 |
| --- | --- | --- |
| [OpenAI - Building more helpful agents with a new evaluation framework](https://openai.com/index/building-more-helpful-agents-with-a-new-evaluation-framework/) | field-report, browsecomp, evaluation, hard-to-find-information | 适合支撑“多步骤信息搜集+整合”类任务助手评测，尤其是高难检索和证据链质量。 |
| [OpenAI - Harness engineering](https://openai.com/index/harness-engineering/) | harness-engineering, verification, reliability, agent-first-software | 为多 agent 工程化提供 harness、验证和可靠性约束，是系统落地的重要方法论。 |
| [OpenAI - Symphony orchestration](https://openai.com/index/open-source-codex-orchestration-symphony/) | orchestration, codex, issue-driven, control-plane | 可借鉴到多 agent 任务助手的任务队列、隔离执行和结果合并流程。 |
| [OpenAI - The next evolution of the Agents SDK](https://openai.com/index/the-next-evolution-of-the-agents-sdk/) | agents-sdk, sandbox, manifests, memory, tools | 对生产级 agent SDK 如何标准化工具、记忆和执行环境有参考价值。 |
| [OpenAI - Unrolling the Codex agent loop](https://openai.com/index/unrolling-the-codex-agent-loop/) | agent-loop, tool-replay, stateless-calls, codex | 多 agent 系统同样需要处理轨迹回放、上下文增长和工具调用状态，这篇能支撑运行时设计。 |
| [OpenAI Agents SDK - Orchestrating Multiple Agents](https://openai.github.io/openai-agents-python/multi_agent/) | documentation, agents-sdk, handoffs, orchestration | 对用 OpenAI Agents SDK 复现 supervisor/manager/handoff 协作模式非常关键。 |
| [OpenAI Cookbook - Orchestrating Agents](https://cookbook.openai.com/examples/orchestrating_agents) | cookbook, handoffs, routines, orchestration | 是 OpenAI 生态中最直接的多 agent 编排实践示例，应和 Swarm/Agents SDK 一起参考。 |
| [OpenAI Developers - Testing Agent Skills Systematically with Evals](https://developers.openai.com/blog/eval-skills) | skills, evals, traces, regression | 自进化多 agent 系统需要 regression-safe 的技能/协作模式评测闭环。 |

### Multi-Agent Framework Documentation

| 阅读材料 | 标签 | 贴合理由 |
| --- | --- | --- |
| [AG2 Documentation - Multi-agent Chat](https://docs.ag2.ai/latest/docs/user-guide/advanced-concepts/orchestration/group-chat/introduction/) | documentation, ag2, groupchat, multi-agent | 适合与 AutoGen 官方模式对照，观察 group chat 协作抽象的演进。 |
| [AutoGen Documentation - Multi-agent Design Patterns](https://microsoft.github.io/autogen/stable/user-guide/core-user-guide/design-patterns/intro.html) | documentation, autogen, design-patterns, runtime | 适合把 AutoGen 论文和 Magentic-One 系统落到可复现实验配置。 |
| [Hugging Face smolagents - Multi-agent Systems](https://github.com/huggingface/smolagents/blob/main/docs/source/en/examples/multiagents.md) | documentation, smolagents, managed-agents, code-agents | 适合用最小 agent 框架验证“manager + specialist”的协作开销和效果。 |
| [LangGraph Documentation - Multi-agent Systems](https://docs.langchain.com/oss/python/langgraph/workflows-agents) | documentation, langgraph, supervisor, swarm | 是构建 traceable multi-agent workflow baseline 的直接工程参考。 |
| [LlamaIndex Documentation - Multi-agent Workflows](https://docs.llamaindex.ai/en/stable/understanding/agent/multi_agent/) | documentation, llamaindex, workflows, retrieval-agents | 对多 agent 任务助手中的数据检索、工具调用和 workflow 组合有直接工程价值。 |
| [Mastra Documentation - Agent Networks](https://mastra.ai/docs/agents/networks) | documentation, mastra, agent-network, typescript | 补齐 Node/TypeScript 生态下多 agent network 工程实践。 |
| [Pydantic AI Documentation - Multi-agent Applications](https://ai.pydantic.dev/multi-agent-applications/) | documentation, pydantic-ai, typed-agents, applications | 对要求高可靠 schema、工具参数和状态校验的多 agent 系统尤其有价值。 |

### Protocol Documentation

| 阅读材料 | 标签 | 贴合理由 |
| --- | --- | --- |
| [Google A2A Protocol Documentation](https://a2a-protocol.org/latest/specification/) | documentation, a2a, interoperability, agent-cards | 对“通用协作框架”和跨产品线 agent 协作协议设计高度相关。 |
| [Model Context Protocol Documentation](https://github.com/modelcontextprotocol/modelcontextprotocol/tree/main/docs) | documentation, mcp, tools, context | 多 agent 系统若要可迁移和可扩展，工具/上下文层应优先兼容 MCP。 |
| [ProtocolBench - Which LLM Multi-Agent Protocol to Choose?](https://openreview.net/forum?id=lqNqKUG2dn) | protocolbench, protocolrouter, a2a, anp, acp, mcp | 虽未作为正式顶会论文收录，但对协议选型、协议评测指标和 hybrid protocol routing 很有参考价值。 |

### Evaluation, Runtime, and Engineering Blogs

| 阅读材料 | 标签 | 贴合理由 |
| --- | --- | --- |
| [Cognition - Don't Build Multi-Agents](https://cognition.ai/blog/dont-build-multi-agents) | anti-patterns, agent-design, reliability, single-agent-baseline | 是重要负面/约束性阅读，可帮助判断什么时候不该上多 agent，防止复杂度和成本无谓膨胀。 |
| [Cognition - What We Learned Building Cloud Agents](https://cognition.ai/blog/what-we-learned-building-cloud-agents) | cloud-agents, vm-isolation, snapshots, governance | 对多 agent 长任务运行环境、隔离执行和企业落地非常有参考价值。 |
| [HumanLayer - 12 Factor Agents](https://www.humanlayer.dev/blog/12-factor-agents) | production-agents, principles, operations, reliability | 适合作多 agent 任务助手工程化 checklist。 |
| [HumanLayer - Skill Issue: Harness Engineering for Coding Agents](https://www.humanlayer.dev/blog/skill-issue-harness-engineering-for-coding-agents) | harness-engineering, coding-agents, skills, operations | 可迁移到多 agent 中 skill/workflow/tool 描述的系统化管理。 |
| [Inngest - Your Agent Needs a Harness, Not a Framework](https://www.inngest.com/blog/your-agent-needs-a-harness-not-a-framework) | harness-first, reliability, orchestration, production | 对多 agent 系统的队列、重试、状态和事件驱动 orchestration 很有启发。 |
| [LangChain - Agent frameworks, runtimes, and harnesses](https://blog.langchain.com/agent-frameworks-runtimes-and-harnesses-oh-my/) | architecture, framework, runtime, harness | 有助于把多 agent 通信/协作算法和底层 harness 工程职责分离。 |
| [LangChain - Evaluating Deep Agents](https://blog.langchain.com/evaluating-deep-agents-our-learnings/) | deep-agents, evaluation, long-horizon, stateful-agents | 适合设计多 agent 长尾任务评测、错误分类和回归测试。 |
| [LangChain - How and when to build multi-agent systems](https://blog.langchain.com/how-and-when-to-build-multi-agent-systems/) | engineering-guide, supervisor, handoff, multi-agent | 可帮助把论文中的协作模式映射到 LangGraph/LangChain 工程实现。 |
| [LangChain - Improving Deep Agents with harness engineering](https://blog.langchain.com/improving-deep-agents-with-harness-engineering/) | deep-agents, harness-engineering, benchmark, iteration | 支撑“自进化不一定先改模型，可以先优化 harness/workflow”的研究路线。 |
| [LangChain - The Anatomy of an Agent Harness](https://blog.langchain.com/the-anatomy-of-an-agent-harness/) | harness, architecture, components, reliability | 是把多 agent 框架落成可维护工程系统的架构参考。 |
| [Martin Fowler - Harness Engineering](https://martinfowler.com/articles/exploring-gen-ai/harness-engineering.html) | architecture, harness-engineering, entropy, gen-ai | 为多 agent 系统边界、治理和工程复杂度控制提供高质量架构视角。 |

### High-Quality Personal and Community Blogs

| 阅读材料 | 标签 | 贴合理由 |
| --- | --- | --- |
| [DeepLearning.AI - Four AI Agent Strategies](https://www.deeplearning.ai/the-batch/how-agents-can-improve-llm-performance) | agentic-design-patterns, multi-agent-collaboration, reflection, planning | 是工业界传播最广的 agentic pattern 框架之一，适合放在多 agent 协作模式章节作为概念入口。 |
| [LessWrong - Survey of Multi-agent LLM Evaluations](https://www.lesswrong.com/posts/tGcLA596E8g3KnphE/survey-of-multi-agent-llm-evaluations) | multi-agent-evaluation, risks, miscoordination, collusion | 补齐多 agent 评测不只看任务分数，还要看协作失败、串谋和安全风险的视角。 |
| [Lilian Weng - LLM Powered Autonomous Agents](https://lilianweng.github.io/posts/2023-06-23-agent/) | agent-overview, planning, memory, tool-use, reflection | 虽不是多 agent 专文，但为理解多 agent 中每个 agent 的能力边界和自我改进机制提供基础。 |
| [Simon Willison - Agent Definition](https://simonwillison.net/2025/Sep/18/agents/) | agent-definition, tool-loop, terminology, multi-agent | 有助于统一“agent”和“multi-agent system”的工程术语，避免把普通 workflow 误称为多 agent。 |

## 非 GitHub 项目与基准参考

### Protocols & Interoperability

| 条目 | 标签 | 贴合理由 |
| --- | --- | --- |
| [SEMAP](https://arxiv.org/abs/2510.12120) | protocol, structured-messaging, a2a, software-engineering | 虽主要是论文方案，但非常适合作为多 agent 协作协议设计参考。 |

### Benchmarks & Evaluation

| 条目 | 标签 | 贴合理由 |
| --- | --- | --- |
| [GAIA](https://arxiv.org/abs/2311.12983) | general-assistant, web, tool-use, benchmark | 适合任务助手信息搜集、整合和工具使用评测。 |

### Observability & Operations

| 条目 | 标签 | 贴合理由 |
| --- | --- | --- |
| [AgentCoord](https://arxiv.org/abs/2404.11943) | coordination-visualization, strategy-design, human-in-the-loop | 适合作协作拓扑、任务依赖和 agent 关系的调试工具参考。 |

### Research Implementations & Baselines

| 条目 | 标签 | 贴合理由 |
| --- | --- | --- |
| [MINDCraft / MineCollab](https://mindcraft-minecollab.github.io/) | minecraft, communication-efficiency, embodied-agents, collaboration-benchmark | 可作为 embodied multi-agent 场景下“通信越多是否越好”和“协作是否真正带来收益”的强评测补充。 |

## 维护方式

单一数据源：

- `data/papers.yaml`
- `data/projects.yaml`

更新后运行：

```bash
python3 scripts/render.py
python3 scripts/verify.py --skip-links
python3 scripts/verify_github_projects.py
```

