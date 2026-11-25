# 双 Agent 交叉复审工作流（Builder × Independent Read-Only Reviewer）

> **核心问题**：AI Coding 时代最大的质量风险，不是 AI 写不出代码，而是 **“同一个 Agent 既写代码又自测自夸，把异步竞态、破坏性回归和不可回滚改动悄无声息地塞进主干”**。

---

## 工作流架构（三权分立门禁）

```mermaid
flowchart LR
    H["架构与规格负责人 (Human)<br/>定义 Spec / 边界 / 回滚硬条款"] --> B["Builder Agent<br/>按 Spec 编码实现 + 跑基础单测"]
    B --> R["Independent Read-Only Reviewer Agent<br/>严禁改文件 · 逐行核对 Diff 与竞态"]
    R -- "FAIL：列出 file:line 级缺陷" --> B
    R -- "PASS：全条款达标" --> V["零成本门禁 + 端到端真机验收"]
```

---

## 实战案例：1.7 万行前端启动性能优化（P0 三刀重构 · 4 轮交叉复审）

- **改造目标**：将应用启动核心模块加载数从 **`8 → 4`**（Prompt / TTS / Image / Worldbook 全部改造为 `ensure*Manager` 懒加载 + 缓存）。
- **设立的硬性验收条款**：
  1. 绝不破坏既有公共 API getter；
  2. 所有异步懒加载回调不得引入用户交互竞态；
  3. 每一项优化必须保留可独立回滚快照。
- **4 轮独立只读复审（Codex Reviewer）真实拦出的高危缺陷**：
  - **Round 1（拦截 4 处 FAIL）**：暴露出公开 getter 导出缺失与初始化顺序依赖；
  - **Round 2（拦截 3 处 P2）**：在 `calendar-view.js` 抓出**开关回调竞态 Bug**——用户快速切换开关时，异步 `ensureWorldbookManager` 完成后的初绘回调会覆盖用户刚刚的点击状态 → 通过在 `change` 回调首行打标 `e.target.dataset.userTouched='1'` 并在初绘补绘前校验彻底根治；
  - **Round 3–4（技术裁决）**：审计出三刀缝在同一文件导致“每刀独立回滚”条款未严格闭环，明确留痕整目录基线校验点（MD5 锁定）与风险边界后才放行合并。

---

## 零成本门禁优先准则（Cost-Aware Verification）

为了避免频繁调付费大模型烧预算，每次迭代严格执行 **两级验证顺序**：
1. **Tier 1（零 Token 成本，必须 100% 全绿）**：静态语法检查、Schema/Manifest 契约校验、单元测试、文档门禁（`check-docs`）、假模型稳定性压测（`smoke --fake`）、400/404 异常边界、提示词组装预览；
2. **Tier 2（产生模型费用，仅在 Tier 1 全绿后按需触发）**：真实 LLM 端到端冒烟与主观质量抽检。
