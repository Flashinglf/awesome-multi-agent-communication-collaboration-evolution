# Research Questions

This repository is organized around one practical research goal:

> Build a low-cost, robust, self-evolving multi-agent collaboration infrastructure for long-tail task assistants.

## RQ1: Communication

How should a multi-agent system decide **who receives what information, when, and under what token budget**?

Subquestions:

- How much quality is lost when replacing full broadcast with sparse routing?
- Can role-aware context routing improve communication precision while preserving recall?
- Can dynamic topologies outperform fixed star, chain, hierarchy, or fully connected structures?
- How should communication be evaluated beyond final answer accuracy?

Suggested metrics:

- total token cost
- inter-agent communication tokens
- communication precision
- communication recall
- answer quality
- latency

## RQ2: Collaboration

How should a system dynamically assign roles, route subtasks, and recover from weak or failed agents?

Subquestions:

- Which collaboration structures are robust under faulty agents?
- When should the system use orchestrator-subagent, message bus, shared state, or agent teams?
- How should challengers, reviewers, and verifiers be inserted without exploding cost?
- How should agent reputation or health be estimated from traces?

Suggested metrics:

- end-to-end success rate
- long-tail task success rate
- robustness drop under injected faulty agents
- recovery rate
- verifier false accept / false reject rate

## RQ3: Evolution

How can multi-agent teams improve from execution feedback without unsafe online self-modification?

Subquestions:

- Which parts should be optimized: prompts, roles, tools, edges, topology, memory policy, or verifier policy?
- Can failure attribution turn traces into targeted workflow updates?
- Should evolution operate on code, configuration, or declarative coordination skills?
- How can regression evaluation prevent benchmark overfitting and behavior regressions?

Suggested metrics:

- evolution gain across repeated task families
- regression pass rate
- cost-quality-latency frontier improvement
- transfer performance on unseen long-tail tasks
- safety violation rate after evolution
