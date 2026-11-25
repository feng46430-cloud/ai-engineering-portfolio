<div align="center">

# Feng Xu (徐峰)

**AI Evaluation & Deterministic Harness Practitioner · Technical AI Workflow Architect · 6-Year Game/XR QA Lead**

*Turning stochastic LLM capabilities into deterministic, verifiable, production-grade workflows.*  
*用需求拆解、确定性护栏、控变量评测与质量门禁，把 AI 系统从 60 分 Demo 稳定交付到 95 分生产工具。*

<p>
  <img src="https://img.shields.io/badge/Focus-AI%20Eval%20%26%20Guardrails-1d4ed8?style=flat-square" alt="AI Eval" />
  <img src="https://img.shields.io/badge/Architecture-Multi--Agent%20Orchestration-0f172a?style=flat-square" alt="Multi-Agent" />
  <img src="https://img.shields.io/badge/Methodology-Spec--Driven%20%26%20Deterministic%20Harness-334155?style=flat-square" alt="Spec-Driven" />
  <img src="https://img.shields.io/badge/Domain-Game%20%26%20XR%20Systems%20QA%20(6%20Yrs)-475569?style=flat-square" alt="Systems QA" />
  <img src="https://img.shields.io/badge/Base-Shanghai%20%7C%20Remote-0369a1?style=flat-square" alt="Location" />
</p>

</div>

---

### Verified Engineering Highlights（核心量化实证）

| Dimension | Verified Proof |
| :--- | :--- |
| **Multi-Agent Architecture** | Led V1 (`23,908` LOC / `867` tests / `52` routes) → V2–V4 (`5,290` LOC / `284` tests, **-79% complexity**) refactor with **6 formal ADRs** & Hybrid RAG (`Exact → Vector → Rerank`) |
| **AI Eval & Simulation** | Built **5-Gate Doc × Source-Code Anti-Hallucination QA Pipeline** + **500-turn dynamic state-machine simulator** catching **11 systemic defects** pre-launch |
| **Deterministic Guardrails** | Shipped true-random anti-cheating injector (`crypto.getRandomValues`), nested macro lexer/repairer, 2-tier memory compaction agent & **Builder × Read-Only Reviewer** dual-agent audit gates |
| **Systems Benchmarking** | Designed **4-stage VR/Mocap latency decomposition** (fixed third-party Unity SDK UDP protocol bug) & **3-architecture × 6-device × 7-dimension** benchmark driving final hardware selection |
| **Quality & Ownership** | 3 consecutive lead/founding-QA roles (Outsource QA Leader → 0→1 Esports QA Lead → 0→1 Founding QA); cut smoke testing from **3×30 min → 1×5–10 min**; built **36 green automated test suites** |

---

### Featured Portfolio（精选公开作品 — 建议从第一项读起）

#### 1. [`ai-engineering-portfolio`](https://github.com/feng46430-cloud/ai-engineering-portfolio) — *30 秒速览 AI 架构、评测与确定性护栏展示仓*
> 零废话、去娱乐化、含 Mermaid 架构图、脱敏 ADR 与可一键运行的零依赖 Python Demo：
- [**01 · Multi-Agent Orchestrator**](https://github.com/feng46430-cloud/ai-engineering-portfolio/tree/main/01-multi-agent-orchestrator) — 配置驱动多 Agent 编排引擎（V1→V4 演进、控制面/上下文面分离 ADR、废弃画布改有序列表产品复盘）
- [**02 · AI Eval & Simulation**](https://github.com/feng46430-cloud/ai-engineering-portfolio/tree/main/02-ai-eval-and-simulation) — 5-Gate 文档×源码防幻觉 SOP、Token 经济学审计与 **可运行 Python 500 轮仿真 / RFC-4180 校验 Demo**
- [**03 · Deterministic Guardrails**](https://github.com/feng46430-cloud/ai-engineering-portfolio/tree/main/03-deterministic-guardrails) — “让模型读而非算”护栏模式集、双 Agent 交叉复审工作流与 13 维红队评审框架
- [**04 · Systems Benchmark & Postmortems**](https://github.com/feng46430-cloud/ai-engineering-portfolio/tree/main/04-systems-benchmark-and-governance) — 软硬件全链路控变量评测、9 周分支发布治理与 5 大底层排障实录

#### 2. [`chat-autobackup`](https://github.com/feng46430-cloud/chat-autobackup) — *源码级根因修复的独立 JavaScript 扩展*
> 深入核查宿主渲染源码（`redisplayChat` / `mesid` / `is_system`）根治隐藏楼层计数偏移 Bug，实现分卡/分会话独立计数与目录自动备份。

#### 3. [Public Engineering & Hardware Eval PDFs（飞书免登录原件）](https://jcn3qpi51ul0.feishu.cn/drive/folder/Lj6cfpcyzluJ6Bd5zq1cfjw0nTd)
> 收录 23 页全链路硬件延迟测试方案、16 页 6 设备横评总结、9 周研发分支治理图、2 份内部测试工具 PRD 与游戏系统策划探索文档。

---

### Operating Principles（工程信条）

1. **Mechanism First, Zero Band-Aids（先定机制，拒绝补丁叠补丁）** — Trace failures to architecture, contracts, or data flow rather than stacking defensive prompt rules or downstream hacks.
2. **Let Models Read, Not Compute（机制保确定性，让模型读而非算）** — Delegate state, randomness, schema enforcement, and boundary gating to deterministic code; let LLMs focus on reasoning and synthesis.
3. **Zero-Cost Gates Before Paid Calls（零成本门禁优先）** — Run static validation, unit tests, doc gates, and fake-model stability sweeps first; trigger paid LLM evaluation only after deterministic baselines are 100% green.

---

### Capability Stack（能力图谱）

| Domain | Capabilities & Tooling |
| :--- | :--- |
| **AI Agent & Context Engineering** | Multi-Agent DAG Orchestration · Hybrid RAG (`Exact + Vector + Rerank`) · Context Compression & U-Curve Attention Audit · MCP · Anthropic & OpenAI API Protocol Debugging · Local SearXNG |
| **AI Evaluation & Guardrails** | 5-Gate Doc×Code Anti-Hallucination SOP · Dynamic State-Machine Simulation · Anti-Goodhart Bidirectional Critic · Lexical/Regex Guardrails · Dual-Agent Independent Code Review |
| **Spec-Driven Delivery & Tooling** | Technical PRD & Architecture Spec (ADR) · Spec-Driven AI-Assisted Tooling (Python / Node.js / Electron / CDP) · `node --test` Automated Regression · RFC-4180 / SHA-256 Validation |
| **Game, XR & Systems QA (6 Yrs)** | Unreal Engine / Unity Profiling (`Unity Profile Analyzer` / `PerfDog`) · VR & Mocap Hardware Latency Benchmarking · Release Branch Governance · Cross-Timezone English Collaboration |

---

<div align="center">
  <sub>Open to opportunities in <b>AI Evaluation (AI Eval)</b> · <b>Technical AI PM</b> · <b>AI Workflow & Efficiency Engineering</b> · <b>AI-Native QA Architecture</b></sub>
</div>
