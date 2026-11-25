# AI Engineering, Evaluation & Deterministic Harness Portfolio

> **定位**：6 年复杂系统 QA & 0→1 QA Lead 背景的 **AI 系统评测（AI Eval）/ 技术向 AI 产品与工作流架构师 / AI-Native 质量效能负责人**。  
> **核心理念**：不靠“玄学调 Prompt”，而是通过 **「需求拆解 → 确定性机制约束（让模型读而非算）→ 源码对齐与仿真压测 → 独立交叉验收」**，把不稳定的大模型能力工程化地稳定交付到真实业务工作流。

---

## 30 秒看懂这份作品集（核心实证一览）

| 模块 | 代表项目 / 体系 | 关键架构与量化实证 | 对应目标岗位能力 |
| :--- | :--- | :--- | :--- |
| **[01 · 多 Agent 编排引擎](./01-multi-agent-orchestrator/)** | 配置驱动型多 Agent 编排与审校工作台（V1 → V2~V4 `v4.16.1`） | • **V1 (23,908 行 / 867 单测 / 52 路由) → 复盘归零重构 V2~V4 (5,290 行 / 284 单测)，代码瘦身 79%**<br>• **6 份正式 ADR** + 3 条架构铁律 + 混合 RAG（精确命中 → 向量粗筛 → 精排 Rerank）<br>• 产品决策：实测废弃低效节点画布，改用有序步骤列表 + 单/内部多 Agent 无损切换 | AI Agent 架构<br>技术向 AI PM<br>AI 工作流工程 |
| **[02 · AI 评测与仿真体系](./02-ai-eval-and-simulation/)** | 5-Gate 文档×源码防幻觉审计 SOP + 500 轮动态仿真压测 & Token 经济学 | • **5-Gate 源码交叉核验管线**：分离现网可测 / 未实现预留 / 跨文档冲突 + RFC-4180 校验<br>• **500 轮数值/状态机仿真**：上线前拦截 **11 项系统缺陷**（冷启动死锁、衰减误差、竞态）<br>• **含可一键运行 Python Demo**：`python 02-ai-eval-and-simulation/demo-simulation/run_sim.py` | AI Eval 评测工程<br>AI-Native 测开<br>质量架构设计 |
| **[03 · 确定性护栏武器库](./03-deterministic-guardrails/)** | Deterministic Harness 护栏模式集 + 双 Agent 交叉复审 + 13 维红队评审 | • **4 大确定性护栏**：真随机防 LLM 挑数 / 嵌套语法词法检测修复 / 两级记忆压缩 / 换轴判据<br>• **Builder × 独立只读 Reviewer 双 Agent 四轮复审门禁**（拦截异步竞态、死卡独立回滚）<br>• **大型遗留前端改造复盘**：1.7 万行单文件审计 + 5 管线合一 + 资源省 54% + **36 套单测全绿** | Agent 稳定性与安全<br>AI 工程治理<br>自动化质量门禁 |
| **[04 · 软硬件系统评测与治理](./04-systems-benchmark-and-governance/)** | VR 动捕全链路控变量 Benchmark + 研发分支治理 + 真实排障集 | • **4 段端到端延迟拆解** + 定位第三方 Unity SDK **UDP 协议初始化 Bug**<br>• **3 架构 6 设备 7 维横评** + 强磁 5 分钟累积误差压测 → 拍板核心 5 节点穿戴式方案<br>• **9 周分支合并与验收流重构** + 656 条四域用例体系 + 2 份内部工具 PRD | 控变量实验设计<br>底层根因排障<br>研发效能与流程治理 |

---

## 我的工作方式（为什么能把 AI 从 60 分稳定做到 95 分）

1. **Spec 驱动与架构优先（先定机制与判据，绝不盲改）**  
   先拆清需求边界、数据契约、状态机与失败路径，再以规格驱动（Spec-Driven）协同 AI Coding 工具高效实现；拒绝“打地鼠式叠补丁”，所有规则回归单一真源（Single Source of Truth）。
2. **控制面与上下文面分离（让模型读而非算）**  
   确定性代码管状态、随机源、格式契约、权限隔离和机械校验；LLM 只做其擅长的推理与生成，并通过**双向漂移审稿（防过度附和 / 防过度敌意）**替代易诱发 Goodhart 效应的死板配额。
3. **零成本门禁优先 + 端到端强证据验收**  
   凡可离线验证的只读检查、静态解析、单测、假模型稳定性压测与 400/404 异常路径必须先跑全绿，严控 Token 成本；不轻信模型自称“已完成”，通过独立只读 Agent 复审与真实环境验证闭环。

---

## 快速体验可运行 Demo（零外部依赖，Python 3 直接跑）

```bash
# 1. 运行 500 轮状态机与非线性增长仿真对比（演示如何上线前拦出冷启动死锁与衰减误差）
python 02-ai-eval-and-simulation/demo-simulation/run_sim.py

# 2. 运行 RFC-4180 CSV + UTF-8 BOM + 防重ID/空字段确定性门禁校验器
python 02-ai-eval-and-simulation/demo-simulation/validate_csv.py
```

---

## 扩展阅读与公开原件

- **公开扩展源码**：[feng46430-cloud/chat-autobackup](https://github.com/feng46430-cloud/chat-autobackup)（通读宿主渲染源码根治隐藏楼层索引偏移 Bug）
- **完整硬件评测 / 工具 PRD / 流程治理 PDF 原件**：[飞书公开作品集《测试文档》](https://jcn3qpi51ul0.feishu.cn/drive/folder/Lj6cfpcyzluJ6Bd5zq1cfjw0nTd)（免登录可读）

> **边界与声明**：本仓库所有工程复盘、ADR、数据与 Demo 均已彻底脱敏，不含任何公司专有代码、商业机密、密钥或第三方受版权保护源码；其中涉及第三方开源项目二次开发的案例，均已明确标注“基于开源二次开发”且仅展示本人主导的架构分析与测试工程数据。
