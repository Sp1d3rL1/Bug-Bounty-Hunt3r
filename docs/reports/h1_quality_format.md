# HackerOne Quality Report Format

> Bilingual / 双语：HackerOne 2025-01 字段对齐版（含 H1 强制字段 + recommended fields）。
> 通用模板见 `english_report_template.md`。本文件聚焦"如何让 H1 triager 第一眼判断为 quality report"。

---

## H1 Required Fields Cheat-Sheet

| Field | H1 status | 必须填写要点 |
|---|---|---|
| Title | required | ≤ 70 chars，包含 weakness type + endpoint/feature |
| Severity | required | None / Low / Medium / High / Critical（基于 H1 自家 severity 标准 + CVSS 3.1） |
| State | auto | 你提交时不用填；triager 会改 |
| Asset | required | 必须从 program 的 in-scope assets 列表里选；自由文本会被退回 |
| Weakness | required | 选 H1 提供的标准 weakness（映射到 CWE） |
| Bounty | optional | 不要主动写期望金额；H1 triager 决定 |
| Disclosure | recommended | 在报告底部声明你的 disclosure 偏好 |

## Quality Report 锚点 (H1 Quality Report Standards 2024)

H1 把以下视为 "Critical Information" — 缺一个就会被退回 Need More Info：

1. ✅ Clear, concise summary of the issue
2. ✅ Steps to reproduce — 必须独立可执行，不依赖外部状态
3. ✅ Proof of concept (HTTP request/response, code, video) — 至少一种
4. ✅ Impact statement — 不要写 "this could be critical"，要写 "an attacker can do X to Y, leading to Z"
5. ✅ Suggested mitigations — 给至少 1 条具体建议（不要"应使用最佳实践"这种空话）

---

## Title

`<weakness> in <endpoint or feature> allows <attacker role> to <impact>`

## Summary

3-5 sentences. 必须能让 triager 在不展开 PoC 的情况下决定 priority。

## Steps to Reproduce

1. 完全独立的步骤；不要假设 triager 已经登录或有特定的 session
2. 给具体值（用占位符标记 `<TOKEN_A>`，但其余写死）
3. 第一步必须是"create a fresh account at https://program.com/signup"，让 triager 能从零开始

## Proof of Concept

### HTTP Request
```http
POST /api/... HTTP/2
Host: target.com
...
```

### HTTP Response
```http
HTTP/2 200 OK
{"sensitive_data": "..."}
```

### Video PoC
- ≤ 3 min
- 显示完整流程：注册 A → 注册 B → 触发漏洞 → 验证
- password-protected; 在报告里附密码

## Impact

> H1 看 impact 是按"who can do what to what scale"评分

- **Affected users**: <例 "All registered users in EU region (~ 3M users per public statement)">
- **Attacker prerequisites**: <例 "Any free-tier user with valid email">
- **Required victim interaction**: <例 "None" / "Click a crafted link" / "Open shared document">
- **Confidentiality / Integrity / Availability impact**: 列具体哪个被影响

## Severity Justification

CVSS 3.1: `<vector>` (X.X)
- Attack Vector (AV): Network / Adjacent / Local / Physical
- Attack Complexity (AC): Low / High
- Privileges Required (PR): None / Low / High
- User Interaction (UI): None / Required
- Scope (S): Unchanged / Changed
- Confidentiality / Integrity / Availability (CIA): None / Low / High

> 解释每个轴的选择，不要只贴 vector

## Suggested Mitigations

1. <具体的代码层 fix — 给伪代码或具体 patch 思路>
2. <架构层 fix — 例 add WAF rule / centralised auth middleware>
3. <检测层 fix — 例 log + alert on cross-tenant access>

## Disclosure Preference

- [ ] Default H1 disclosure timeline (90 days after fix)
- [ ] Public disclosure once fixed
- [ ] Private disclosure (no public CVE)

## Bounty / Recognition

> 不主动喊价；如果 program 表里有金额就引用

- Per program scope page: `<Critical: $X / High: $Y>`

---

## 中文要点提示

- H1 triager 一天看几十份报告，**前 3 行决定他的态度**：title 精炼 + 一句话 summary + 立即看到 PoC
- "Severity Justification" 是新手最容易省的一节，但写了之后 triager 直接接受你打的分概率高很多
- Suggested Mitigations 不要泛泛 — 给具体可读的代码层建议（哪怕只是一句"在 ResolveInvoice 里改成按 user_id 过滤"），triager 会觉得你"懂这事"
- 视频 PoC 加密码很重要；H1 默认所有附件可被任意 staff 看，加密码降低意外泄露风险
- 不要把多个漏洞打包在一份报告里；H1 一份报告 = 一个漏洞，否则会被拆分扣分
