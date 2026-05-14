# X / Grok 情报工作流

> 目标：把 X 上碎片化技巧变成可复现、可迁移、可验证的 bug bounty 知识库。

## X Pro 建列

建议建立 6 个 Deck / Lists：

1. Top hunters
2. Platform updates
3. Tool authors
4. Client-side research
5. API / OAuth / GraphQL
6. Cloud / AI security

## 高信号搜索查询

直接复制到 X 搜索或 X Pro 搜索列：

```text
("bug bounty" OR bugbounty) (writeup OR "case study" OR "root cause") -is:retweet lang:en
(IDOR OR BOLA OR "access control") ("bug bounty" OR h1 OR hackerone OR bugcrowd) -is:retweet lang:en
(OAuth OR SAML OR SSO OR JWT OR "magic link") (bypass OR misconfig OR "bug bounty") -is:retweet lang:en
(GraphQL OR introspection OR batching) (IDOR OR auth OR authorization) -is:retweet lang:en
("business logic" OR coupon OR refund OR invoice OR subscription OR billing) (bug OR bounty OR vulnerability) -is:retweet lang:en
("web cache" OR cache poisoning OR "cache deception") (PortSwigger OR bug bounty) -is:retweet lang:en
("client-side" OR CSPT OR postMessage OR DOMPurify OR prototype) (bug bounty OR research) -is:retweet lang:en
("AI security" OR LLM OR prompt injection OR "tool calling") (bug bounty OR vulnerability OR SaaS) -is:retweet lang:en
(nuclei OR httpx OR katana OR subfinder OR caido OR burp) (template OR workflow OR trick) -is:retweet lang:en
("disclosed report" OR hacktivity OR "HackerOne report") (critical OR high) -is:retweet lang:en
```

日期窗口查询：

```text
("bug bounty" "OAuth") since:2026-01-01 until:2026-06-01 -is:retweet lang:en
("GraphQL" "IDOR") since:2026-01-01 -is:retweet lang:en
```

## Grok 分析 Prompt

把 X 搜索结果或帖子链接喂给 Grok，用这些 prompt：

```text
You are my bug bounty intelligence analyst. Extract only actionable techniques from these X posts. For each item return: title, vulnerability class, prerequisite, exact trick, why it works, authorized-only validation steps, automation potential, false-positive risk, and which target types it maps to. Ignore motivational content.
```

```text
Cluster these bug bounty tips into: API/BOLA, OAuth/SSO, GraphQL, business logic/payment, client-side, cache, cloud, AI security. Rank by novelty and transferability. Remove duplicates and low-signal posts.
```

```text
For the following trick, generate a safe lab-first validation plan and a bug bounty reporting angle. Do not include destructive payloads, brute force, DoS, or out-of-scope testing.
```

```text
Turn this thread into a trick card using exactly this schema: 标题, 来源, 作者, 漏洞类型, 适用场景, 前置条件, 核心 trick, 可迁移目标, 可自动化部分, 手工验证步骤, 可能越界点, 优先级.
```

## 情报处理规则

- 只保存能回答“在哪种目标上可迁移”的技巧。
- 所有技巧先找 lab 或本地靶场复现，再用于真实项目。
- 对涉及支付、账号、隐私、越权的技巧，必须先确认项目规则允许。
- 不保存纯 payload；保存“前置条件 + 业务路径 + 影响证明”。

## 每周情报例会

- 周一：清空上周 X 收藏，转成 trick cards。
- 周三：挑 2 条技巧做 lab 复现。
- 周五：挑 1 条技巧映射到授权目标。
- 周日：保留 Top 10，删除噪声。

## 隐私提醒

X/Grok 官方帮助页说明 Grok 可使用公开 X 帖子和实时 web 搜索；不要把未公开报告、目标敏感资产、API key、客户数据、个人隐私输入 Grok。
