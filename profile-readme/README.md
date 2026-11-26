<div align="center">

# Feng Xu (徐峰)

**AI Interactive Systems & Role Play Designer · AI Eval Practitioner · 6-Year Game QA Lead**

*Turning stochastic LLM capabilities into controllable, verifiable interactive worlds and production workflows.*  
*用机制设计、确定性护栏、控变量评测与严苛实机验收，把 AI 交互叙事与多 Agent 工作流从 60 分 Demo 稳定做到 95 分可用体验。*

<p>
  <img src="https://img.shields.io/badge/Focus-AI%20Interactive%20%26%20Role%20Play-1d4ed8?style=flat-square" alt="AI Interactive & Role Play" />
  <img src="https://img.shields.io/badge/Practice-AI%20Eval%20%26%20Simulation-0f172a?style=flat-square" alt="AI Eval & Simulation" />
  <img src="https://img.shields.io/badge/Architecture-Multi--Agent%20Workflow-334155?style=flat-square" alt="Multi-Agent" />
  <img src="https://img.shields.io/badge/Domain-Game%20Systems%20%26%20QA%20Lead%20(6%20Yrs)-475569?style=flat-square" alt="Game Systems QA" />
  <img src="https://img.shields.io/badge/Base-Shanghai%20%7C%20Remote-0369a1?style=flat-square" alt="Location" />
</p>

</div>

---

### Core Track Record（核心实证 · STAR 摘要）

> *Engineering prototypes and automation scripts below are spec-led, designed, and strictly verified by me in collaboration with AI Coding tools.*

| Dimension | Verified Result |
| :--- | :--- |
| **Role Play & AI World Simulation** | **~30,000 deduplicated turns** (~15K AI replies, max **4,046 turns** in a single thread) across 6 original interactive worlds; built decentralized NPC simulation, anti-sycophancy/anti-hostility calibration & **~40% CoT token compression** without losing adherence |
| **Multi-Agent Orchestration** | Led zero-base V1 → V2–V4 refactor (**-79% system complexity**), authored **6 formal ADRs**, replaced node canvas with ordered step lists, and shipped Hybrid RAG + independent judge gating (`v4.16.1`) |
| **AI Eval & Anti-Hallucination QA** | Established **5-Gate Doc × Source-Code QA SOP** (surfaced **400+** spec gaps, lifted Test Gym coverage **70.0% → 98.6%**, P0 **100%**) + **500-turn dynamic simulator** catching **11 systemic defects** pre-launch |
| **Deterministic Guardrails** | Shipped true-random anti-cheating gate, nested syntax auto-repair, 2-tier preference memory compression & **Builder × Read-Only Reviewer** audit SOP; led open-source secondary-dev consolidation (**-54% assets, 36 green test suites**) |
| **Systems Benchmarking & QA Lead** | Designed **4-stage VR/Mocap latency decomposition** & **3-architecture × 6-device** benchmark driving 5-node hardware selection; cut smoke testing from **3×30 min → 1×5–10 min** across 3 consecutive lead/founding-QA roles |

---

### Featured Portfolio（精选公开作品 — 单层清爽导航，直达真实原件与脚本）

#### 1. [`ai-engineering-portfolio`](https://github.com/feng46430-cloud/ai-engineering-portfolio) — *5 大 STAR 实证模块 + 真实预设原件与可运行脚本*
- [**01 · Multi-Agent Orchestrator**](https://github.com/feng46430-cloud/ai-engineering-portfolio/tree/main/01-multi-agent-orchestrator) — V1→V4 归零重构复盘（-79%）、6 份 ADR、废弃画布改有序列表的产品决策
- [**02 · AI Eval & Simulation**](https://github.com/feng46430-cloud/ai-engineering-portfolio/tree/main/02-ai-eval-and-simulation) — 5-Gate 文档×源码防幻觉 SOP、商业脱敏实证与 **可运行 500 轮仿真 / CSV 门禁 Python 脚本**
- [**03 · Deterministic Guardrails**](https://github.com/feng46430-cloud/ai-engineering-portfolio/tree/main/03-deterministic-guardrails) — “让模型读而非算”护栏体系、开源二次开发收敛复盘与双 Agent 复审 / 13 维红队框架
- [**04 · Systems Benchmark & Governance**](https://github.com/feng46430-cloud/ai-engineering-portfolio/tree/main/04-systems-benchmark-and-governance) — VR 动捕 4 段延迟拆解、6 设备横评、9 周分支发布治理与 5 大根因排障实录
- [**05 · RP Narrative Preset & 201-Turn Fair Ablation**](https://github.com/feng46430-cloud/ai-engineering-portfolio/tree/main/05-rp-narrative-and-ablation) — 自研重构叙事预设纯文本原件（`55,890→12,170` 字 `-78.2%`）+ 201 楼真实原卡 `N=3` 多场景 3-Way 公平消融（均值 Prompt Token `-88.7%`、CoT 遵循 `0/3→3/3`、点名旧曲精准召回不误杀）

#### 2. [`chat-autobackup`](https://github.com/feng46430-cloud/chat-autobackup) — *源码级根因修复的独立扩展*
> 核查宿主渲染逻辑根治隐藏楼层计数偏移 Bug，实现分卡/分会话独立计数与自动备份。

#### 3. [Public Engineering & Hardware Eval PDFs（飞书免登录原件）](https://jcn3qpi51ul0.feishu.cn/drive/folder/Lj6cfpcyzluJ6Bd5zq1cfjw0nTd)
> 收录 23 页全链路硬件延迟测试方案、16 页 6 设备横评总结、9 周研发分支治理图、2 份内部测试工具 PRD 与游戏系统策划文档。

---

### Operating Principles（工作信条）

1. **Root Cause Over Band-Aids（先追根因，拒绝补丁叠补丁）** — Fix underlying mechanisms, contracts, or premises rather than stacking defensive prompt rules or downstream workarounds.
2. **Let Models Read, Not Compute（机制保确定性，让模型读而非算）** — Delegate randomness, state boundaries, format validation, and access control to deterministic rules; let LLMs focus on reasoning and narrative quality.
3. **Zero-Cost Gates Before Paid Calls（零成本门禁优先）** — Run static checks, unit tests, and offline simulation sweeps first; never trust an agent's self-reported "done" without independent verification.

---

<div align="center">
  <sub>Open to opportunities in <b>AI Interactive Systems & Role Play</b> · <b>AI Evaluation (AI Eval)</b> · <b>Technical AI PM</b> · <b>Game / AI-Native QA Lead</b></sub>
</div>
