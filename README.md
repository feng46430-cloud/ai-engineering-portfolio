# AI Interactive Systems, Evaluation & Deterministic Harness Portfolio

> **定位**：2020 年入行游戏质量工程、连续担纲项目质量体系搭建与 QA Lead 的 **AI 交互叙事与世界模拟设计者 / AI 评测（Eval）与上下文策略实践者 / 技术向 Agent 工作流设计者**。  
> **分工与展示说明（Spec-First & Live-Demo Ready）**：本仓库所有工程原型与工具均由 **本人主导问题定义、Spec 规则与架构决策、异常边界约束及严苛实机验收，协同 AI Coding 工具落地**。本仓库完整公开 **6 份正式架构决策记录（ADR-001 ~ ADR-006）、可直接本地复现的零依赖仿真/门禁脚本、脱敏实采消融 JSON 及实机运行工作台高清界面**；涉及防自动化抓取的全量业务预设与完整工作台支持于业务面试中**现场屏幕共享 Live Demo 与任意极端 Case 实时压测**。

> [!NOTE]
> **合规与净室声明（Clean-Room Disclaimer）**：本仓库中所有个人独立作品（`01` / `03` / `05` 及 `02` 中的离线仿真）均为作者业余原创实践；`02`（防幻觉核验规范）与 `04`（系统评测与治理框架）所载规范、方法论及示例数据均为基于公开/虚构示例独立撰写的通用工程抽象（Clean-room abstraction），**不包含任何过往及现任职企业的内部业务数据、未公开项目信息、私有代码、商业硬件测试原表或受 NDA 保护资产**。

---

## 一、按目标岗位直接看哪块（30 秒直达核心实证）

| 你正在招的岗位方向 | 优先看这 2 个目录 | 核心真证据（Spec 思路 + 真实对照 + 可运行脚本） |
| :--- | :--- | :--- |
| **智能 NPC / AI 玩法策划 / AI 互动叙事** | **[05 · 叙事 Spec 与真实重 Roll 对照](./05-rp-narrative-and-ablation/)** · **[01 · 多 Agent 编排](./01-multi-agent-orchestrator/)** | 4 组真实存档废弃重 Roll / 硬骰受挫 vs 定稿对照 · Spec 架构蓝图 · 完整 6 份 ADR（含废弃画布改有序列表复盘） |
| **AI 内容策略 PM / 大模型评测（AI Eval）** | **[05 · 201 楼 3-Way 公平消融](./05-rp-narrative-and-ablation/)** · **[02 · AI 评测与仿真](./02-ai-eval-and-simulation/)** | 同存档 3 场景实测 Prompt 由 `~13.3 万` 压回 `~1.5 万` Token（`-88.7%`）· 13 艺人秩相关与 `1,860` 周仿真脚本 · 5-Gate 防幻觉框架 |
| **AI 应用 PM / 工作流与 UGC 工具产品** | **[01 · 多 Agent 编排工作台](./01-multi-agent-orchestrator/)** · **[03 · 确定性护栏治理](./03-deterministic-guardrails/)** | V1→V4 归零重构 · 有序步骤列表 + 单/多 Agent 无损切换 · 三级宽容解析免重跑与三问归属法 |
| **游戏测试经理 / QA 效能** | **[02 · 5-Gate 防幻觉框架](./02-ai-eval-and-simulation/)** · **[04 · 系统评测与治理](./04-systems-benchmark-and-governance/)** | 5-Gate 文档×源码防幻觉通用规范 · Gate 5 校验脚本 · 4 段延迟拆解 & 分支治理通用方法论 |

### 30 秒本地零依赖复现（Python 3 标准库直跑）

```bash
git clone https://github.com/feng46430-cloud/ai-engineering-portfolio.git
cd ai-engineering-portfolio

# 1) 13 位真实艺人秩相关审计（57/61 = 93.4%）+ 多策略 1,860 模拟周世界经济防通胀仿真
python 02-ai-eval-and-simulation/demo-simulation/run_sim.py

# 2) 5,000 盒五层卡池整盒保底、Fisher-Yates 防摸包、掉率补偿守恒（消除 +28.7% 保底通胀）与 1/1 全局锁校验
python 02-ai-eval-and-simulation/demo-simulation/run_gacha_box_sim.py

# 3) Gate 5 双层测试用例 RFC-4180 结构、防重与乱码确定性门禁校验
python 02-ai-eval-and-simulation/demo-simulation/validate_csv.py
```

---

## 二、五大模块 STAR 一览

| 模块 | S / T（解决的真问题） | A（本人主导的关键动作） | R（可验证结果） |
| :--- | :--- | :--- | :--- |
| **[01 · 多 Agent 编排与审校工作台](./01-multi-agent-orchestrator/)** | 单轮长 Prompt 注意力稀释、自审失效、V1 过度耦合难维护 | 主导归零重构并沉淀完整 **[6 份 ADR](./01-multi-agent-orchestrator/adr-highlights.md)**；确立引擎领域无关 + 白名单隔离 + 独立判官打回；实测砍掉低效连线画布改有序列表 | 核心架构瘦身 `~79%`，`284` 项单测秒级全绿，持续迭代发版至 `v4.16.1` |
| **[02 · AI 评测、防幻觉规范与动态仿真](./02-ai-eval-and-simulation/)** | AI 照着过期文档编造假用例；长周期多变量规则上线后易死锁失衡 | 抽象 **5-Gate 文档×源码核验通用 SOP** 与 Gate 5 校验脚本（Clean-room）；设计多策略 **`1,860` 模拟周离线数值仿真**、`5,000` 盒卡池概率校验与 Token 审计 | 仿真上线前拦截 **11** 项系统失衡缺陷；3 套零依赖 Python 仿真与门禁脚本可直接本地复现 |
| **[03 · 确定性护栏与质量治理体系](./03-deterministic-guardrails/)** | 模型不擅长公平随机与格式闭合；黑名单禁令越堆越失效 | 确立「让模型读而非算」，落地真随机防作弊、嵌套语法修复、两级偏好压缩、7 套渐进式 Agent Skills 与双 Agent 交叉复审 | `862` 字散乱补丁精简为 3 条公理；开源二次开发 **5 套管线合一**、启动模块 `8→4`、跨双仓 **39** 套单测全绿 |
| **[04 · 软硬件系统评测与研发治理（通用框架）](./04-systems-benchmark-and-governance/)** | 端到端体感延迟黑盒难定位、多分支开发过早结单返工、多端联动冒烟耗人耗时 | 抽象 **4 段延迟拆解**与多架构 7 维控变量选型框架、多分支主干统一验收治理范式及 5 大通用根因排障实录（Clean-room） | 沉淀可复用的分段归因标尺、引擎直测提效思路与 5 大跨层工程排障复盘 |
| **[05 · 叙事架构 Spec、真实重 Roll 对照与 201 楼消融](./05-rp-narrative-and-ablation/)** | 长程互动上下文动辄 13 万 Token 烧钱且丢指令，缺多场景公平实测 | 重构现役提示词规则库（`270→70` 条，全库 `-78%` / 常驻负载 `-40%`）；在 201 条消息真实原卡覆盖 3 类场景做 3-Way 公平消融 | 3 场景实测 Prompt 由 `~13.3 万` 压回至 **`~1.5 万` Token（`-88.7%`）**，思考指令 `3/3` 全按规执行且点名旧曲精准召回不误杀 |

---

## 三、实测消融数据与自研工作台实机界面（已脱敏）

### 1. 201 条消息真实长程存档 · 3-Way 公平消融实测（数据源：[`real-ablation-results.json`](./05-rp-narrative-and-ablation/real-ablation-results.json)）

![201 条消息 3-Way 公平消融实测对比](./assets/ablation-3way-chart.svg)

### 2. 自研工作台实机运行截屏（零拼接假图，仅对接口与别名做最小脱敏）

| 全局 U 型注意力透视与实时 X 光（本轮折叠 31 项 / 省 6,899 字） | 世界书扫描护目镜（自动识别 41 个标签 / 实机拦截误触明细） |
| :---: | :---: |
| ![全局 U 型注意力分布与实时 X 光](./assets/ui-xray-ucurve.png) | ![世界书扫描护目镜与拦截明细](./assets/ui-worldbook-goggles.png) |

> 更多高清实机截屏（有序步骤 CoT 拖拽编排与自动结构化执行流、独立 API 隔音室防从众辩论、副 AI 审校判官与 `see` 最小视野白名单、22 位真实大师剧组与范文仿写库）分别嵌在 **[01](./01-multi-agent-orchestrator/)** 与 **[05](./05-rp-narrative-and-ablation/)** 模块中。

---

## 四、可直接检验的原件与脚本索引

| 类型 | 入口链接 | 说明 |
| :--- | :--- | :--- |
| **6 份完整架构决策记录（ADR）** | [`adr-highlights.md`](./01-multi-agent-orchestrator/adr-highlights.md) · [`patterns.md`](./01-multi-agent-orchestrator/patterns.md) | 完整公开 `ADR-001` ~ `ADR-006`（控制面分离、静态 AST 解析、双向漂移、Prefix Cache 静动分层、废弃画布改有序列表、三级宽容契约与 `CAS 409` 乐观锁） |
| **叙事预设与世界模拟 Spec 蓝图** | [`narrative-preset-core-modules.md`](./05-rp-narrative-and-ablation/narrative-preset-core-modules.md) · [`world-simulation-rules.md`](./05-rp-narrative-and-ablation/world-simulation-rules.md) | 现役预设瘦身与 CoT 因果链 Spec 蓝图 + 六档三支柱门禁/硬阈值裁定/多水流世界架构（保护成品源码，重解题思路） |
| **真实重 Roll 对照与 201 楼消融** | [`05-rp-narrative-and-ablation/README.md`](./05-rp-narrative-and-ablation/README.md) · [`real-ablation-results.json`](./05-rp-narrative-and-ablation/real-ablation-results.json) | 4 组真实游玩存档废弃重 Roll / 硬骰受挫 vs 定稿对照 + 201 条消息真实原卡 3 场景消融实测 JSON + 实验态→商业实时态快慢双脑裁剪表 |
| **可运行多策略与概率仿真 Demo** | [`run_sim.py`](./02-ai-eval-and-simulation/demo-simulation/run_sim.py) · [`run_gacha_box_sim.py`](./02-ai-eval-and-simulation/demo-simulation/run_gacha_box_sim.py) | 零依赖 Python 3：① 13 位真实艺人跨档样本秩相关审计（单维粉丝一致度 `57/61 = 93.4%`，定位 4,000 万重叠盲区以反推三支柱门禁）+ 多策略 `1,860` 模拟周成长仿真；② 五层卡池整盒保底 + Fisher-Yates 防摸包洗牌 + 基础掉率补偿守恒（消除 `+28.7%` 保底通胀）+ 全局 `1/1` 库存锁 |
| **可运行 Gate 5 校验器** | [`validate_csv.py`](./02-ai-eval-and-simulation/demo-simulation/validate_csv.py) · [`sample_testcases.csv`](./02-ai-eval-and-simulation/demo-simulation/sample_testcases.csv) | 零依赖 Python 3 脚本：前后台分离双层用例样表 + 编码/防重/乱码确定性门禁 |
| **成本、Skills 与评审规范** | [`token-economics-audit.md`](./02-ai-eval-and-simulation/token-economics-audit.md) · [`agent-skills-and-mcp-governance.md`](./03-deterministic-guardrails/agent-skills-and-mcp-governance.md) · [`dual-agent-review-sop.md`](./03-deterministic-guardrails/dual-agent-review-sop.md) · [`13-dim-redteam-rubric.md`](./03-deterministic-guardrails/13-dim-redteam-rubric.md) · [`engineering-postmortems.md`](./04-systems-benchmark-and-governance/engineering-postmortems.md) | Token 经济核算、7 套渐进式 Agent Skills 与按需 MCP 准入、Builder × Reviewer 双盲复审 SOP、13 维红队记分与 5 大根因排障 |
| **外部公开扩展源码** | [`thinking-regex-shield`（GitHub）](https://github.com/feng46430-cloud/thinking-regex-shield) · [`chat-autobackup`（GitHub）](https://github.com/feng46430-cloud/chat-autobackup) | 2 套独立发布的开源扩展源码（双钩子物理隔离思维链与正文渲染 `82/82` 全绿；源码级修复隐藏系统消息计数偏移与 JSONL 表头往返对齐） |

---

## License

Released under the [MIT License](./LICENSE). 本仓库所有案例、数据与脚本均已彻底脱敏，不含任何公司专有代码、商业机密、密钥或第三方受版权保护素材；涉及第三方开源项目二次开发的案例均已明确标注来源。
