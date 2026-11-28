# 跨项目架构决策索引（ADR Index · 共 18 条）

> 本页汇总分散在 3 个公开仓库里的全部核心架构决策（Architecture Decision Records），按工程主题归类，只保留**痛点 → 取舍 → 实证结果**精炼摘要，并单向索引回原项目完整文档与对应踩坑复盘（单一事实源，避免多处复制产生漂移）。

- **出处项目**：[`starlight-market-ai-npc-blueprint`](https://github.com/feng46430-cloud/starlight-market-ai-npc-blueprint)（9 条）｜[`ai-engineering-portfolio`](./README.md)（8 条）｜[`thinking-regex-shield`](https://github.com/feng46430-cloud/thinking-regex-shield)（1 条）
- **配套踩坑复盘**：[`ai-field-notes`（16 篇人机协作排雷笔记）](https://github.com/feng46430-cloud/ai-field-notes)

---

## 一、确定性规则边界与防泄漏隔离（5 条）

| 编号 | 决策主题 | 核心取舍与实证 | 出处项目原文 | 关联踩坑 |
| :--- | :--- | :--- | :--- | :--- |
| **SL-ADR-01** | 把机密隔离与账本移出 Prompt | 股价盈亏收归 `MarketEngine`；`S3 DisclosureBudget=0` 时机密物理不入上下文，`S6` 拦野生 `%` 与姓氏错乱 | [`starlight / ARCHITECTURE-BLUEPRINT`（ADR-01）](https://github.com/feng46430-cloud/starlight-market-ai-npc-blueprint/blob/main/docs/ARCHITECTURE-BLUEPRINT.md) | — |
| **SL-ADR-05** | 拆除业务死词表，改互斥三桶语义门禁 | 废弃 5 张 `S1` 业务词表与易触发 Yes-Bias 的二元布尔，改用 `chat \| ask_conclusion \| verify_detail`（`temperature=0` + `cache_prompt: false`）回填状态机与跨 NPC 传话 | [`starlight / ARCHITECTURE-BLUEPRINT`（ADR-05）](https://github.com/feng46430-cloud/starlight-market-ai-npc-blueprint/blob/main/docs/ARCHITECTURE-BLUEPRINT.md) | [Note 15](https://github.com/feng46430-cloud/ai-field-notes/blob/main/notes/15-npc-dialogue-six-live-playtest-pitfalls.md) / [Note 16](https://github.com/feng46430-cloud/ai-field-notes/blob/main/notes/16-when-ai-fixes-create-silent-regressions.md) |
| **SL-ADR-06** | 动态新颖片段重合防偷漏 | 删除源码硬编码机密词表与误杀高频词的 3-bigram，改为仅对 `UnderwaterFact` 判定连续 4 字新颖片段或 `≥5` 新颖中文 2-gram（豁免玩家原话） | [`starlight / ARCHITECTURE-BLUEPRINT`（ADR-06）](https://github.com/feng46430-cloud/starlight-market-ai-npc-blueprint/blob/main/docs/ARCHITECTURE-BLUEPRINT.md) | [Note 15](https://github.com/feng46430-cloud/ai-field-notes/blob/main/notes/15-npc-dialogue-six-live-playtest-pitfalls.md) / [Note 16](https://github.com/feng46430-cloud/ai-field-notes/blob/main/notes/16-when-ai-fixes-create-silent-regressions.md) |
| **MA-ADR-001** | 控制平面与上下文平面彻底分离 | 确定性代码掌控调度、门禁与回滚；各 Agent 仅看白名单裁剪后的局部视图，否决同模型自生成自审 | [`01 / adr-highlights`（ADR-001）](./01-multi-agent-orchestrator/adr-highlights.md) | — |
| **TRS-ADR-01** | 双钩子“留壳藏芯”物理隔离思考块 | `BEFORE_REGEX` 抽芯保留 `<thinking>` 外壳、`AFTER_MARKDOWN` 还原并按 `<textarea>` 内外分治换行；覆盖闭合 / Prefill / 流式三态 + `stash > 32` 上限（`82/82` 单测） | [`thinking-regex-shield / README`](https://github.com/feng46430-cloud/thinking-regex-shield) | [Note 09](https://github.com/feng46430-cloud/ai-field-notes/blob/main/notes/09-thinking-block-streaming-isolation.md) |

---

## 二、记忆、世界拓扑与自由涌现（3 条）

| 编号 | 决策主题 | 核心取舍与实证 | 出处项目原文 | 关联踩坑 |
| :--- | :--- | :--- | :--- | :--- |
| **SL-ADR-04** | 3 行极简物理容器壳 + 全量动作/情绪涌现 | 删除 350+ 字反应处方并解锁 `action(5)×emotion(6)`；同机 A/B/C 对照达 `8/8`、`P50=678ms`（优于重规则 `7/8` 粉红大象泄漏） | [`starlight / ARCHITECTURE-BLUEPRINT`（ADR-04）](https://github.com/feng46430-cloud/starlight-market-ai-npc-blueprint/blob/main/docs/ARCHITECTURE-BLUEPRINT.md) | — |
| **SL-ADR-07** | 双层记忆与世界拓扑涌现闭环 | `MarketTopologyStore` 五重机制：原子事实 + `evidenceQuote` + 精确边 1-Hop；**母节点有界扇出（`≤ 4`）+ 子节点动态晋升分枝 + 冷节点 LRU 淘汰**（`N = 100` 轮浸泡最大直接子节点 `23 → 4`、动态晋升 `19` 枝、单轮注入 `~293 tok`）；`LockedFloor` / `BiasedDoubt` / VIP `PromotedSlots` / `Contested`；Delta-Only `[ROLLING_SUMMARIES]` 热窗口 + `ForeshadowingSlot` | [`starlight / ARCHITECTURE-BLUEPRINT`（ADR-07）](https://github.com/feng46430-cloud/starlight-market-ai-npc-blueprint/blob/main/docs/ARCHITECTURE-BLUEPRINT.md) | — |
| **SL-ADR-08** | 显式玩家身份与双向禁教导演技契约 | 开局独立玩家姓名阻断匿名吸附，门禁拦截正/反向演技处方；**已标明阶段性边界**：剧情真匿名态后续直接收编进 `MarketTopologyStore`（`player` 一等节点 + `OwnerEntityId` 渲染分栏 + `Relationship` 边知情态），不新造身份系统 | [`starlight / ARCHITECTURE-BLUEPRINT`（ADR-08）](https://github.com/feng46430-cloud/starlight-market-ai-npc-blueprint/blob/main/docs/ARCHITECTURE-BLUEPRINT.md) | [Note 15](https://github.com/feng46430-cloud/ai-field-notes/blob/main/notes/15-npc-dialogue-six-live-playtest-pitfalls.md) |

---

## 三、算力、延迟与缓存经济学（3 条）

| 编号 | 决策主题 | 核心取舍与实证 | 出处项目原文 | 关联踩坑 |
| :--- | :--- | :--- | :--- | :--- |
| **SL-ADR-02** | 4 端口 GPU 同驻 → 单 `Qwen3-8B` 按需分层 | RX 7900 GRE 实测 `Qwen3-8B` 比 `Qwen3.5-4B` 快 **4.7 倍**；切 `-Profile lean` 单主脑后显存 `9.30 → 5.22 GiB`，前台 `P50=825.5ms`，3 日整局折算 **`¥0.0055/局`** | [`starlight / ARCHITECTURE-BLUEPRINT`（ADR-02）](https://github.com/feng46430-cloud/starlight-market-ai-npc-blueprint/blob/main/docs/ARCHITECTURE-BLUEPRINT.md) | — |
| **SL-ADR-03** | **负向选型**：放弃复用检索精排做安全拦截 | `N=10` 实机探针中 `bge-reranker-v2-m3` 对股市黑话“死叉/梭哈”距误杀线仅差 `0.0356` logit，遂放弃复用，线上改用专用安全分类器 | [`starlight / ARCHITECTURE-BLUEPRINT`（ADR-03）](https://github.com/feng46430-cloud/starlight-market-ai-npc-blueprint/blob/main/docs/ARCHITECTURE-BLUEPRINT.md) | [Note 03](https://github.com/feng46430-cloud/ai-field-notes/blob/main/notes/03-anti-sycophancy-and-search-before-build.md) |
| **MA-ADR-004** | 静动分层 Prefix Cache 与无偏差 U 型注意力 | 静态规则前移 + 动态状态贴尾 + 固定字典键序保护 KV Cache 与 Thinking Signature；剥离 `data.tools` 单独统计防挤偏注意力区间 | [`01 / adr-highlights`（ADR-004）](./01-multi-agent-orchestrator/adr-highlights.md) | [Note 10](https://github.com/feng46430-cloud/ai-field-notes/blob/main/notes/10-multi-agent-writing-four-antipatterns.md) |

---

## 四、AI 评测校准、防 Goodhart 与概率守恒（3 条）

| 编号 | 决策主题 | 核心取舍与实证 | 出处项目原文 | 关联踩坑 |
| :--- | :--- | :--- | :--- | :--- |
| **MA-ADR-003** | 滑动窗口趋势评估 + 双向漂移检查 | 废弃单轮刚性配额（防 Goodhart 机械化），改用 3–5 轮滑动窗口并同步监控过度附和与过度对抗双端漂移 | [`01 / adr-highlights`（ADR-003）](./01-multi-agent-orchestrator/adr-highlights.md) | [Note 07](https://github.com/feng46430-cloud/ai-field-notes/blob/main/notes/07-over-mechanized-checklist-backfire.md) |
| **EV-ADR-01** | AI 评测口径校准与注入/表达拆轨 | 拆解早期 `98%+` 虚高通过率（替考/合规灌水/并发掩盖延迟），确立 Gate 0 零加分否决、空载单玩家延迟与“记忆注入率 ≠ 对话表达率”双轨核算 | [`03 / human-vs-ai-sparring-playbook`](./03-deterministic-guardrails/human-vs-ai-sparring-playbook.md) | [Note 01](https://github.com/feng46430-cloud/ai-field-notes/blob/main/notes/01-fake-98pct-eval-and-injection-vs-expression.md) |
| **EV-ADR-02** | 五层卡池整盒保底、期望守恒与 `1/1` 唯一锁 | 废弃引发 `28.6%` 尾包摸包与 `+28.7%` 期望通胀的尾包死保底，改用整盒保底 + Fisher-Yates 洗牌 + 掉率补偿 + 全局耗尽锁（5,000 盒验证：空盒 `0%`、期望 `1.10`、尾包 `8.26%`） | [`02 / README`](./02-ai-eval-and-simulation/README.md) · [`run_gacha_box_sim.py`](./02-ai-eval-and-simulation/demo-simulation/run_gacha_box_sim.py) | — |

---

## 五、工程安全、交互减法与并发容错（4 条）

| 编号 | 决策主题 | 核心取舍与实证 | 出处项目原文 | 关联踩坑 |
| :--- | :--- | :--- | :--- | :--- |
| **MA-ADR-002** | 声明式配置 + 静态 AST 解析，禁执行外部脚本 | 以 YAML/JSON + 静态解析器（`zod.mjs`）替代可执行业务脚本，消除任意代码执行风险并支持毫秒级快照回滚 | [`01 / adr-highlights`（ADR-002）](./01-multi-agent-orchestrator/adr-highlights.md) | — |
| **MA-ADR-005** | **产品减法**：废弃节点连线画布改有序列表 | 推倒已实现的曲线防冲突连线画布，改为有序步骤列表 + 缩进子 Agent + 拖拽引用自愈与单/多 Agent 无损切换 | [`01 / adr-highlights`（ADR-005）](./01-multi-agent-orchestrator/adr-highlights.md) | — |
| **MA-ADR-006** | 宽容输出解析与跨代写盘安全演进 | 四态宽容分块免无谓重跑 + `readVerdict` 否定优先；写盘从 V1 `409` 乐观锁演进为 V2–V4 HITL 原话提案逐条 CAS + `WAL` 崩溃幂等恢复（`15/15` 单测，含 `concurrency = 64 × 10` 轮抢写每轮严格 1 胜 / 63 冲突零脏写） | [`01 / adr-highlights`（ADR-006）](./01-multi-agent-orchestrator/adr-highlights.md) | [Note 11](https://github.com/feng46430-cloud/ai-field-notes/blob/main/notes/11-llm-state-and-judge-five-pitfalls.md) / [Note 12](https://github.com/feng46430-cloud/ai-field-notes/blob/main/notes/12-dont-blame-the-model-config-split-brain.md) |
| **SL-ADR-09** | 三层原子快照回滚 + 离线无锁 Roslyn 编译门禁 | 状态机、记忆索引与拓扑图谱三层同步 `CaptureSnapshot/RollbackSnapshot` + `stateEpoch` 乐观锁；契约门禁直调 Unity Roslyn 零锁工程完成 5 程序集离线编译验真 | [`starlight / ARCHITECTURE-BLUEPRINT`（ADR-09）](https://github.com/feng46430-cloud/starlight-market-ai-npc-blueprint/blob/main/docs/ARCHITECTURE-BLUEPRINT.md) | [Note 15](https://github.com/feng46430-cloud/ai-field-notes/blob/main/notes/15-npc-dialogue-six-live-playtest-pitfalls.md) |
