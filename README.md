# 徐峰 · AI 交互原型、评测体系与质量工程工作记录

这里放的是我平时做 AI 玩法原型、评测校准、概率仿真和游戏质量工程（2020 至今）的工作记录与可运行脚本。按主题分好了入口，挑感兴趣的地方看就行。

[![Portfolio CI](https://github.com/feng46430-cloud/ai-engineering-portfolio/actions/workflows/verify.yml/badge.svg)](https://github.com/feng46430-cloud/ai-engineering-portfolio/actions/workflows/verify.yml)
[![Starlight CI](https://github.com/feng46430-cloud/starlight-market-ai-npc-blueprint/actions/workflows/verify.yml/badge.svg)](https://github.com/feng46430-cloud/starlight-market-ai-npc-blueprint/actions/workflows/verify.yml)

![星海交易局 — Unity 6 URP 3D AI-NPC 实验原型](./assets/starlight-3d-theater.png)

---

## 想看什么？从这里进去

- **AI 评测（Eval）与概率仿真**：看 [**AI 评测校准与止损记录**](./03-deterministic-guardrails/human-vs-ai-sparring-playbook.md)（修正 `98%` 虚高通过率、拆开“注入率 ≠ 表达率”）和 [**02 · 评测、5-Gate 与概率仿真**](./02-ai-eval-and-simulation/)（5,000 盒抽卡防摸包与期望守恒脚本）。
- **AI 玩法与智能 NPC 原型**：看 [**《星海交易局》3D AI-NPC 实验原型**](https://github.com/feng46430-cloud/starlight-market-ai-npc-blueprint)（前台藏底牌盲测博弈 + 规则层隔离账本与机密）和 [**01 · 多 Agent 编排工作台演变**](./01-multi-agent-orchestrator/)。
- **游戏 QA、延迟拆解与底层排障**：看 [**04 · 4 段延迟拆解与根因排障**](./04-systems-benchmark-and-governance/)（TCP/UDP 抓包、Profiler A/B 对照、Windows 原子写并发与跨平台哈希排查）和 [**02 · 5-Gate 文档×源码核验流程**](./02-ai-eval-and-simulation/)。

---

## 5 块主要记录（均附实机图、原始日志或可运行脚本）

### 1. AI 评测校准与 3D AI-NPC 规则隔离原型（[独立原型仓](https://github.com/feng46430-cloud/starlight-market-ai-npc-blueprint)）
- **评测口径校准**：早期批测报告 `98%+` 通过率，复盘发现三个口子：8B 替考 4B、底线合规占加分、并发排队掩盖单玩家延迟。改成 **Gate 0 零加分否决 + 空载单玩家耗时（`concurrency=1`）+ 100 分体验重权** 后，基线落回 `31.2 (F)`，同种子下一轮把 Top-3 开场白复读从 `36.4%` 压到 `5.3%`。
- **注入率 ≠ 表达率与负向选型**：Run 03 里旧监控记跨轮记忆 `24/24`，翻对话原文发现实际 `0/4` 体现记忆，遂拆开“检索注入”与“对话表达”两套指标；实测 `bge-reranker` 在“梭哈/死叉”处距误杀仅差 `0.0356`，记录后放弃了用通用检索精排替代安全拦截的想法。
- **当前进度**：Unity 6 URP 原型含 2 名对手 NPC，本机 RX 7900 GRE 16 GiB 实测 4 模型专用显存 `9.30 GiB`。云端 `L4 BF16` 批跑最新 Run 04（`v4.5.5`，`52.0 / 100`）已把 Contested 拉到 `8/8`、人设拉到 `74.2`，但角色开场白口癖（`"哎哟，这"×44次`）造成新复读回退，仍在迭代中。

---

### 2. 卡池概率 QA：5,000 盒五层卡池防摸包与期望守恒仿真（[`02`](./02-ai-eval-and-simulation/)）
- 用 Python 零依赖仿真对照三种抽卡实现：**朴素随机**（31.3% 空盒且 `1/1` 唯一卡超发 63 张）vs **尾包死保底**（尾包出货占比飙升至 `28.6%` 引发摸包漏洞，并带来 `+28.7%` 隐性期望通胀）vs **整盒保底 + Fisher-Yates 均匀洗牌 + 基础掉率补偿守恒 + `1/1` 全局耗尽锁**（空盒 `0%`、期望守恒 `1.10`、尾包占比回归 `8.26%`、`mulberry32` 确定性复现）。
- 同目录包含 **5-Gate 文档×源码核验流程**（拆离当前可测 / 未落地预留 / 跨文档冲突，前台白话与后台排查锚点分离）及多策略成长曲线校准脚本。

---

### 3. 系统级 QA：4 段端到端延迟拆解与底层根因排障（[`04`](./04-systems-benchmark-and-governance/)）
- **4 段控变量延迟拆解**：把跨采集、重建软件、网络传输与引擎后处理的延迟黑盒拆成 4 段独立测量（8 ms 高速逐帧 + 激光标定 + 双 VM 对照 + Unity Profile Analyzer A/B 排除后处理嫌疑），抓包定位原始 UDP 跳过握手导致的魔数 `actorId` 映射失效。
- **底层根因排障集**：覆盖 Windows `tmp+rename` 原子写与文件锁冲突触发的 `1/12` 偶发 `EPERM`、Git `core.autocrlf=true` 导致的 60 文件哈希误报、以及 9 周多分支验收防返工流程；跨模型网关（Claude→Gemini）`assistant_prefill` 与 `reasoning_effort` 兼容排查另记在 [`02/token-economics-audit.md`](./02-ai-eval-and-simulation/token-economics-audit.md)。

---

### 4. 产品交互减法：废弃已完成的节点连线画布（[`01`](./01-multi-agent-orchestrator/)）
- 多 Agent 工作台连线画布已完成坐标防冲突与曲线渲染，但实测高频调优拉线繁琐、改顺序易断链，遂推倒改为有序步骤列表 + 缩进子 Agent + 拖拽级联更新；同期因 V1 `867` 条绿测暗藏 7 处假接线，重做核心引擎至 `v4.16.1`，核心单测收敛为 **`306/306 <1s`**。

| 废弃前：节点连线画布 | 重构后：有序步骤列表 + 缩进子 Agent |
| :---: | :---: |
| ![废弃前节点连线画布](./assets/ui-evolution-canvas-before.png) | ![重构后有序步骤列表](./assets/ui-evolution-list-after.png) |

---

### 5. 长对话上下文误触修复与防劣化记录（[`05`](./05-rp-narrative-and-ablation/) + [`03`](./03-deterministic-guardrails/)）
- **标签误触降噪实测（201 轮单存档 · `N=3` 对照）**：修复历史思考块与状态标签误触 31 条无关知识库的 Bug，单轮 Prompt 从异常膨胀的 `133k` 回归 `15k` 基线（`-88.7%`），S3 点名旧条目正常召回（[原始 JSON](./05-rp-narrative-and-ablation/real-ablation-results.json)）。
- **独立只读复审与行为变更防劣化**：在 1.7 万行前端启动优化的 4 轮独立只读复审中，拦下异步懒加载覆写用户开关点击态的竞态 Bug；在私有引擎仓落地行为变更指纹校验（`changelog check`），防止调优期静默改坏阈值或默认提示词。

![201 轮长对话上下文对照](./assets/ablation-3way-chart.svg)

---

## 本地零依赖复现与目录索引

<details>
<summary><strong>展开查看：30 秒本地零依赖验证命令（Python 3 / Node.js）</strong></summary>

```bash
git clone https://github.com/feng46430-cloud/ai-engineering-portfolio.git
cd ai-engineering-portfolio

# 1) 5,000 盒五层卡池防摸包、期望守恒与 1/1 全局唯一锁仿真
python 02-ai-eval-and-simulation/demo-simulation/run_gacha_box_sim.py

# 2) 长周期数值曲线校准与单维阈值重叠反例脚本
python 02-ai-eval-and-simulation/demo-simulation/run_sim.py

# 3) 01 模块内存态校验演示单测（人工原话审批 + 写入前旧值防覆盖校验 HITL CAS，14/14）
node --test 01-multi-agent-orchestrator/mve/mve.test.mjs

# 4) 核验《星海交易局》脱敏诊断 JSON（75% 权重重算 + 分档审计）
git clone https://github.com/feng46430-cloud/starlight-market-ai-npc-blueprint.git
python starlight-market-ai-npc-blueprint/repro/verify_scorecard.py
```

</details>

<details>
<summary><strong>展开查看：01–05 完整目录索引</strong></summary>

- [**01 · 多 Agent 编排工作台与 6 份架构决策记录（ADR）**](./01-multi-agent-orchestrator/)
- [**02 · AI 评测、5-Gate 核验流程、Token 审计与概率仿真**](./02-ai-eval-and-simulation/)
- [**03 · AI 评测校准、产品止损记录与双 Agent 只读复审**](./03-deterministic-guardrails/)
- [**04 · 4 段延迟控变量拆解、分支治理与 5 大根因排障**](./04-systems-benchmark-and-governance/)
- [**05 · 长对话标签误触降噪与 CoT 瘦身实测数据**](./05-rp-narrative-and-ablation/)

</details>

---

*注：本仓库记录的问题拆解、评测设计与脚本由个人在业余或脱敏抽象场景下整理，协同 AI Coding 工具实现，不含前/现任职企业 NDA 资产或受版权保护语料。文档采用 CC BY-NC-SA 4.0，脚本采用 MIT 协议。*
