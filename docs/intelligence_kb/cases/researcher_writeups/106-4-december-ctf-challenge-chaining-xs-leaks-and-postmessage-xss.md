<!-- GROK_API_SCAFFOLD_START -->
---
type: case
title: "December CTF Challenge: Chaining XS leaks and postMessage XSS"
vuln_class: "postMessage DOM XSS"
source_url: "https://www.intigriti.com/researchers/blog/hacking-tools/december-ctf-challenge-xs-leaks-postmessage-xss"
source_author: "Renwa"
source_date: "2025-12-24"
confidence: "high"
risk_level: "low"
freshness: "2026-05"
target_types:
  - "Web apps using postMessage"
---

# December CTF Challenge: Chaining XS leaks and postMessage XSS

## 链接
- https://www.intigriti.com/researchers/blog/hacking-tools/december-ctf-challenge-xs-leaks-postmessage-xss

## 漏洞类型
postMessage DOM XSS

## 目标业务场景
Web apps using postMessage

## 关键利用链摘要
Chain XS-Leak + CSP bypass + DOM clobbering + unsafe postMessage handler to achieve 1-click XSS.

## 可迁移技法
仅迁移到授权项目、靶场或自有环境；优先提炼前置条件、权限边界、状态机或集成点，不复现真实第三方目标。

## 为什么值得收藏
用于学习公开案例的根因、impact 表达、报告结构与授权范围内的验证思路。
<!-- GROK_API_SCAFFOLD_END -->

<!-- GROK_API_EXPANSION_START -->

## Grok API 扩展补充

## December CTF Challenge: Chaining XS leaks and postMessage XSS

2025 Intigriti CTF writeup (Thanos-themed) demonstrating client-side postMessage exploitation.

Challenge rules: XSS on main page only, latest Chrome, ≤1 click, no self-XSS/MiTM.

Stones collected: navigation timing leak, CSP bypass + HTML injection, JSONP + DOM Clobbering, Shadow DOM extraction, Sandbox escape, Fragment length timing attack.

Link: https://www.intigriti.com/researchers/blog/hacking-tools/december-ctf-challenge-xs-leaks-postmessage-xss

High-level reproduction and full chain in source for authorized bug bounty practice.

> 安全边界：本卡仅用于授权项目、靶场或自有环境；所有验证默认使用合成数据、测试账号、沙箱/测试卡和最小影响证明。

## Evidence / 核查元数据
- verification_status: `verified_full_update`
- verification_summary: Snippet extracted and verified against source URL on 2026-05-09. Matches supplied metadata exactly; no conflicts.
- source_urls:
  - https://www.intigriti.com/researchers/blog/hacking-tools/december-ctf-challenge-xs-leaks-postmessage-xss
- evidence:
  - claim: Challenge overview, stones, and rules from 2025-12-24 Intigriti CTF
    source: https://www.intigriti.com/researchers/blog/hacking-tools/december-ctf-challenge-xs-leaks-postmessage-xss
    verification: Direct snippet match including 'Should leverage a XSS vulnerability...' and stone list.

<!-- GROK_API_EXPANSION_END -->

<!-- backlink: docs/checklists/cors_postmessage_websocket.md -->

<!-- backlink: docs/checklists/cspt_client_path_traversal.md -->

<!-- backlink: docs/checklists/prototype_pollution_xss_chain.md -->
