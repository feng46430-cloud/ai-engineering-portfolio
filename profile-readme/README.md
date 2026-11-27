<div align="center">

# Feng Xu (徐峰)

**AI Interactive Systems & Role Play Designer · AI Eval Practitioner · Game QA Lead (Since 2020)**

*Turning stochastic LLM capabilities into controllable, verifiable interactive worlds and production workflows.*  
*用机制设计、确定性护栏、控变量评测与严苛实机验收，把 AI 交互叙事与多 Agent 工作流从 60 分 Demo 稳定做到 95 分可用体验。*

<p>
  <img src="https://img.shields.io/badge/Focus-AI%20Interactive%20%26%20Role%20Play-1d4ed8?style=flat-square" alt="AI Interactive & Role Play" />
  <img src="https://img.shields.io/badge/Practice-AI%20Eval%20%26%20Simulation-0f172a?style=flat-square" alt="AI Eval & Simulation" />
  <img src="https://img.shields.io/badge/Architecture-Multi--Agent%20Workflow-334155?style=flat-square" alt="Multi-Agent" />
  <img src="https://img.shields.io/badge/Domain-Game%20Systems%20%26%20QA%20Lead-475569?style=flat-square" alt="Game Systems QA" />
  <img src="https://img.shields.io/badge/Base-Shanghai%20%7C%20Remote-0369a1?style=flat-square" alt="Location" />
</p>

</div>

---

### Core Track Record（核心实证 · STAR 摘要）

> *Spec-First Disclosure: Engineering prototypes and automation scripts below are spec-led, designed, and strictly verified by me in collaboration with AI Coding tools. To protect original creative/prompt IP, this public portfolio focuses on architecture Specs, ADRs, generalized real Before/After evidence, and minimal runnable demos rather than copy-pasteable production prompt source. All generalized QA/governance frameworks (`02` / `04`) are clean-room abstractions using public/fictional examples only, with zero proprietary employer data or NDA-protected assets.*

| Dimension | Verified Result |
| :--- | :--- |
| **Role Play & AI World Simulation** | **~15,000 AI generation tests** (max **4,046 messages** in a single thread) across 6 interactive worlds & 5 model families; built decentralized NPC simulation, anti-sycophancy/anti-hostility calibration & CoT causal decision chain |
| **Multi-Agent Orchestration** | Led zero-base V1 → V2–V4 refactor, authored **6 formal ADRs**, replaced node canvas with ordered step lists, and shipped Hybrid RAG + independent judge gating (`v4.16.1`) |
| **AI Eval & Dynamic Simulation** | Audited **13 real-world artists** (`57/61 = 93.4%` single-metric rank concordance exposing 40M overlap blind spots to derive a 3-pillar promotion gate) and built a **multi-strategy 2–12yr (`1,860`-week) offline dynamic simulator** catching **11 systemic defects** pre-launch, **5,000-box gacha/card-break simulator** (`0` pity violations, anti-pack-searching shuffle, EV-conserved odds eliminating `+28.7%` pity inflation & `0` global `1/1` over-issues), 201-message 3-probe context ablation (`~133k → ~15k` prompt tokens), plus Clean-Room **5-Gate Doc × Source-Code QA Framework** |
| **Deterministic Guardrails & Skills** | Shipped true-random anti-cheating gate, nested syntax auto-repair, 2-tier preference memory compression, **7 progressive-disclosure Agent Skills**, `mcp-on-demand` 4-tier safety routing & **Builder × Read-Only Reviewer** audit SOP; led open-source secondary-dev consolidation (**5 pipelines → 1, startup modules 8 → 4, 39 green test suites across 2 repos**) |
| **Systems Benchmarking & Governance** | Clean-Room abstractions for **4-stage motion-to-photon latency decomposition**, multi-architecture hardware evaluation, branch release governance & **5 root-cause engineering postmortems** |

---

### Featured Portfolio（精选公开作品 — 单层清爽导航，直达真实原件与脚本）

#### 1. [`ai-engineering-portfolio`](https://github.com/feng46430-cloud/ai-engineering-portfolio) — *5 大 STAR 实证模块 + 架构 Spec 蓝图、脱敏实采数据与可运行脚本*
- [**01 · Multi-Agent Orchestrator**](https://github.com/feng46430-cloud/ai-engineering-portfolio/tree/main/01-multi-agent-orchestrator) — V1→V4 归零重构复盘、6 份 ADR、三问归属法与废弃画布改有序列表的产品决策
- [**02 · AI Eval & Simulation**](https://github.com/feng46430-cloud/ai-engineering-portfolio/tree/main/02-ai-eval-and-simulation) — 5-Gate 文档×源码防幻觉通用框架（Clean-Room）与 **可运行 `1,860` 周多策略仿真 / `5,000` 盒卡池校验 / CSV 门禁 Python 脚本**
- [**03 · Deterministic Guardrails**](https://github.com/feng46430-cloud/ai-engineering-portfolio/tree/main/03-deterministic-guardrails) — “让模型读而非算”护栏体系、开源二次开发收敛复盘与双 Agent 复审 / 13 维红队框架
- [**04 · Systems Benchmark & Governance**](https://github.com/feng46430-cloud/ai-engineering-portfolio/tree/main/04-systems-benchmark-and-governance) — 4 段体感延迟拆解通用方法论（Clean-Room）、研发分支治理范式与 5 大根因排障实录
- [**05 · RP Narrative Spec, Reroll Evidence & 201-Turn Ablation**](https://github.com/feng46430-cloud/ai-engineering-portfolio/tree/main/05-rp-narrative-and-ablation) — Spec 架构蓝图（不暴露可直接照抄的成品提示词源码）+ 真实存档废弃重 Roll vs 定稿对照 + 201 条消息真实存档 3 场景 3-Way 公平消融（Prompt `~13.3 万 → ~1.5 万` Token、思考指令全按规执行且点名旧曲精准召回）

#### 2. [`thinking-regex-shield`](https://github.com/feng46430-cloud/thinking-regex-shield) — *双钩子物理隔离思维链与正文渲染的独立扩展（`82/82` 全绿）*
> 采用“留壳藏芯”占位与 `<textarea>` 内外分治还原，根治全局/角色正则误伤 `<thinking>` 内部文本及流式未闭合态 HTML 击穿问题。

#### 3. [`chat-autobackup`](https://github.com/feng46430-cloud/chat-autobackup) — *源码级根因修复的独立扩展*
> 核查宿主渲染逻辑根治隐藏楼层计数偏移 Bug，实现分卡/分会话独立计数与自动备份。

---

### Operating Principles（工作信条）

1. **Root Cause Over Band-Aids（先追根因，拒绝补丁叠补丁）** — Fix underlying mechanisms, contracts, or premises rather than stacking defensive prompt rules or downstream workarounds.
2. **Let Models Read, Not Compute（机制保确定性，让模型读而非算）** — Delegate randomness, state boundaries, format validation, and access control to deterministic rules; let LLMs focus on reasoning and narrative quality.
3. **Zero-Cost Gates Before Paid Calls（零成本门禁优先）** — Run static checks, unit tests, and offline simulation sweeps first; never trust an agent's self-reported "done" without independent verification.

---

<div align="center">
  <sub>Open to opportunities in <b>AI Interactive Systems & Role Play</b> · <b>AI Evaluation (AI Eval)</b> · <b>Technical AI PM</b> · <b>Game / AI-Native QA Lead</b></sub>
</div>
