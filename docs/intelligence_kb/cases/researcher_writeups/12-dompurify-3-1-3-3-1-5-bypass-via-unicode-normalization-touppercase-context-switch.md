---
type: case
vuln_class: DOMPurify
source_url: https://mizu.re/post/exploring-the-dompurify-library-bypasses-and-fixes
source_author: Kevin Mizu
source_date: 2024-11
collected_at: 2026-05-05
freshness: 2024
confidence: high
target_types:
  - client-side sanitizers
---

# DOMPurify 3.1.3-3.1.5 Bypass via Unicode Normalization + toUpperCase() Context Switch

## 链接

https://mizu.re/post/exploring-the-dompurify-library-bypasses-and-fixes

## 漏洞类型

DOMPurify

## 目标业务场景

client-side sanitizers

## 关键利用链摘要

": - /url: https://mizu.re/post/exploring-the-dompurify-library-bypasses-and-fixes§DOMPurify§ - text: <style>-like tag sanitized then uppercased to valid style after mutation

## 可迁移技法

Triggers mXSS in apps re-parsing output; fixed after researcher disclosure

## 为什么值得收藏

- 该案例可作为 `DOMPurify` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
