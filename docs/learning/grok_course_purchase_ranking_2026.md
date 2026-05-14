# Grok Expert 搜索后的课程购买排序（2026-05-04）

> 生成方式：已登录 grok.com，选择 Expert，使用 live web + X/Twitter 搜索 prompt。原始 Grok DOM 快照保存在 `data/grok_course_search_snapshot.md`。下面是结合 Grok 结果与官方页面校验后的购买决策版。

## 结论：最值得买的 10 个资源

| Rank | 资源 | 购买优先级 | 官方入口 | 价格信号 | 你的学习入口 |
|---:|---|---|---|---|---|
| 1 | Burp Suite Professional + BSCP | 立即 | https://portswigger.net/web-security/certification | BSCP 需要有效 Burp Pro；考试 4 小时，证书 5 年 | Practitioner 以下 lab 全清；OAuth/GraphQL/Business Logic/Request Smuggling/Web Cache |
| 2 | PentesterLab Pro | 立即 | https://pentesterlab.com/pro | 官方显示 Pro $19.99/mo 或 $199.99/yr | JWT、SSRF、SSTI、GraphQL、Recon、code review badges |
| 3 | APIsec University API Penetration Testing + ASCP | 立即 | https://www.apisecuniversity.com/courses/api-penetration-testing | 课程页显示 self-paced / hands-on；ASCP 是 12 小时 API 实战考试 | API Recon、BOLA、Auth、GraphQL、business logic |
| 4 | Hacking APIs, Corey Ball | 立即 | https://nostarch.com/hacking-apis | No Starch: print+ebook $59.99，ebook $47.99 | endpoint analysis、auth、BOLA、GraphQL 章节 |
| 5 | Rana Khalil Academy All-Access / OAuth 2.0 | 立即 | https://academy.ranakhalil.com/p/oauth-vulnerabilities | 官方显示 All-Access starting $29.99/mo；OAuth 课 4h+、6 labs | OAuth/OIDC、JWT、Business Logic、Access Control |
| 6 | HTB Academy Silver Annual + CWES | Month 2-3 | https://help.hackthebox.com/en/articles/13677074-academy-subscriptions-beta | Silver Annual $490/yr；CWES voucher $210；年费含部分 voucher 优惠 | Web Penetration Tester path，全程写英文报告 |
| 7 | Black Hat GraphQL | Month 2 | https://nostarch.com/black-hat-graphql | No Starch: print+ebook $59.99，ebook $47.99 | GraphQL recon、attack surface、authorization |
| 8 | TCM Security All-Access：Practical API/Web/Bug Bounty/AI | Month 2-3 | https://academy.tcm-sec.com/p/practical-bug-bounty | 官方显示 All-Access starting $29.99/mo | Practical API Hacking、Practical Web Hacking、AI Hacking 101 |
| 9 | Critical Thinking Bug Bounty / Critical Research Lab | Month 3 | https://www.criticalthinkingpodcast.io/ / https://lab.ctbb.show/ | 价格需在 Discord/站内确认；Grok 将其列为高信号社区 | 每周吸收当前 hunter 技巧、unredacted/report 思维 |
| 10 | OffSec WEB-300 / OSWE | Month 4-6，高预算 | https://portal.offsec.com/checkout/products?cid=22 | 官方 checkout：Course+Exam $1,749；Learn One $2,749/yr | source review、auth bypass、exploit chain、白盒能力 |

## Grok 搜到但我建议降级/谨慎购买

- NahamSec Intro/Udemy：社区价值高，但课程偏入门；你可把它当 methodology/社区入口，不作为主线付费课。
- Zero To Mastery Web Security/Bug Bounty：Grok 认为 2026 更新；但对你偏宽泛，只有预算富余再买。
- Pluralsight Advanced Bug Bounty Operations：如果已有公司/个人 Pluralsight 订阅可以看，不建议单独为它买订阅。
- CodeRed GraphQL course：可以作为 Black Hat GraphQL 之后的补充；注意其中 brute force/DoS 章节只在 lab 内练，不迁移到真实项目。
- BBRE Premium：Grok 提到过，但公开信息显示订阅形态可能已变化；只从官方/作者渠道确认后再考虑。

## 90 天购买顺序

### Days 1-15

1. 买 Burp Pro。
2. 买 PentesterLab Pro 年费或月费。
3. 买 Hacking APIs。
4. 买 Rana Khalil All-Access 1 个月。

目标：建立 Web/API/OAuth 主线，别再买宽泛入门课。

### Days 16-45

1. 完成 APIsec University API Penetration Testing。
2. 每天 PentesterLab 1 个 badge/lab。
3. PortSwigger：OAuth、JWT、GraphQL、Business Logic、Access Control。
4. 用 Hacking APIs 做自己的 API checklist。

目标：能在全球 API/SaaS 项目上系统测 BOLA、tenant、billing、OAuth。

### Days 46-90

1. 买 HTB Academy Silver Annual 或按模块解锁 Web Penetration Tester path。
2. 买 Black Hat GraphQL。
3. TCM All-Access 只订 1 个月，快速刷 Practical API/Web/AI。
4. 如果确认要走白盒/高级证书，再买 OSWE；否则延后。

目标：形成可提交报告能力 + 英文报告 + 项目池。

## X/Grok 继续追踪查询

```text
("bug bounty" "recommend" (course OR training OR book)) since:2025-01-01 -is:retweet lang:en
("OAuth" OR "OIDC" OR "SSO") ("bug bounty" OR writeup OR course) since:2025-01-01 -is:retweet lang:en
("GraphQL" (IDOR OR authorization OR introspection OR batching)) (bug bounty OR course OR book) since:2025-01-01 -is:retweet lang:en
("business logic" OR billing OR subscription OR invoice OR coupon OR refund) "bug bounty" since:2025-01-01 -is:retweet lang:en
("AI security" OR "LLM security" OR "prompt injection") (course OR bug bounty OR SaaS) since:2025-01-01 -is:retweet lang:en
```

## 不买原则

- 不买只在 Telegram/fcmit 镜像出现、没有官方购买页的课。
- 不买无 lab、无更新时间、无讲师公开成果的“合集课”。
- 不买 CEH 类证书作为 bug bounty ROI 主线。
- 不买承诺“快速赚大钱”的营销课。
- 不把 brute-force、DoS、intrusive 技巧迁移到真实项目。
