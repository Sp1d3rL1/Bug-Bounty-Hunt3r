<!-- GROK_API_SCAFFOLD_START -->
---
type: technique
title: "DOM XSS Using Web Messages and Javascript URL"
vuln_class: "postMessage DOM XSS"
source_url: "https://infosecwriteups.com/dom-xss-using-web-messages-and-javascript-url-window-postmessage-innerhtml-sink-e5db2a0f1bfe"
source_author: "Aditya Bhatt"
source_date: "2025-12-26"
confidence: "high"
risk_level: "low"
freshness: "2026-05"
target_types:
  - "Web apps with cross-origin messaging"
---

# DOM XSS Using Web Messages and Javascript URL

## 核心思路
Unsafe postMessage listener + innerHTML sink without origin check leads to DOM XSS via javascript: URL.

## 前置条件
仅适用于授权 Bug Bounty scope、Lab 或自有环境；使用测试账号、合成数据和最小影响验证。

## 完整技法细节
见下方 Grok API 扩展补充与 Evidence；缺少可核查来源的细节保持 needs_review。

## 适用目标画像
Web apps with cross-origin messaging

## 为什么有效
围绕 postMessage DOM XSS 的真实公开来源提炼可迁移条件，重点关注认证、授权、状态机、集成边界或客户端信任边界。

## 手工验证流程
在授权范围内以只读或最小影响方式验证：确认前置条件、构造合成数据/测试账号、观察授权边界或状态差异、记录证据并停止在安全影响证明处。

## 可自动化部分
可自动化收集公开入口、参数、JS/API schema、配置差异和变更信号；实际漏洞确认保留人工复核。

## 误报/失败条件
目标无对应功能、权限模型不同、补丁已生效、测试账号权限不足、来源无法复核或影响无法用最小证明表达。

## 授权边界
不访问非授权目标；不导出真实敏感数据；不进行破坏性、DoS、爆破、认证批量尝试或真实支付损害测试。

## 报告 impact 角度
说明可影响的资产、权限边界、业务状态、数据类别、可复现前置条件和最小影响证据。

## 相关案例链接
- https://infosecwriteups.com/dom-xss-using-web-messages-and-javascript-url-window-postmessage-innerhtml-sink-e5db2a0f1bfe
<!-- GROK_API_SCAFFOLD_END -->

<!-- GROK_API_EXPANSION_START -->

## Grok API 扩展补充

## 核心思路
Unsafe postMessage listener + innerHTML sink without origin check leads to DOM XSS via javascript: URL.

## 前置条件
Web app with cross-origin postMessage listener that injects received data directly into innerHTML without origin validation or sanitization.

## 完整技法细节
Use iframe to send crafted postMessage containing <img onerror> or javascript: URL 测试载荷. Trigger execution via innerHTML sink.

## 适用目标画像
Web apps with cross-origin messaging

## 为什么有效
No origin check + direct innerHTML assignment allows arbitrary JS execution.

## 手工验证流程（授权 / Lab only）
Lab-style POC in BurpSuite / GitHub repo for safe client-side postMessage DOM XSS validation.

## 可自动化部分
BurpSuite extension or custom script for postMessage interception and 测试载荷 testing.

## 误报/失败条件
Origin checks present or sanitization applied.

## 授权边界
Authorized scope, Lab only, synthetic data, test accounts

## 报告 impact 角度
2025 writeup with lab-style POC for safe client-side postMessage DOM XSS validation in bug bounty programs.

## 相关案例链接
PortSwigger lab and GitHub repo linked in source.

## Evidence / 核查元数据
- verification_status: `verified_full_update`
- verification_summary: Snippet extracted and verified against source URL on 2026-05-09. Matches supplied metadata exactly; no conflicts.
- source_urls:
  - https://infosecwriteups.com/dom-xss-using-web-messages-and-javascript-url-window-postmessage-innerhtml-sink-e5db2a0f1bfe
- evidence:
  - claim: PortSwigger lab demo of postMessage to innerHTML without origin check
    source: https://infosecwriteups.com/dom-xss-using-web-messages-and-javascript-url-window-postmessage-innerhtml-sink-e5db2a0f1bfe
    verification: Direct snippet: 'The webpage listens for `postMessage` events and directly injects received data into `innerHTML` without validating origin...'

<!-- GROK_API_EXPANSION_END -->
