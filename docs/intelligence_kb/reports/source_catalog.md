# Report Intelligence Source Catalog

> 渠道目录用于公开报告发现、付费/私域授权导入管理，以及灰色报告交易线索的元数据观察。默认不保存完整正文。

## Policy

- 自动采集仅面向公开网页、公开 API、公开 GitHub repo、公开 newsletter archive 和公开报告目录。

- 付费/私域内容只允许用户提供合法授权导出后导入；KB 默认仍只保存摘要、链接、短证据片段与 hash。

- 灰色 report trade 线索只进入 watchlist：不购买、不索要、不下载、不解析附件、不保存报告内容。


## platform_public

| source_id | name | reliability | legal_risk | collection_policy | entry / URL | research context | notes |
|---|---|---|---|---|---|---|---|
| `hackerone_hacktivity_api` | HackerOne Hacktivity / Hacker API | official | low | summary_links_evidence_only | [link](https://api.hackerone.com/hacker-resources/) |  | Prefer API when HACKERONE_API_USERNAME/HACKERONE_API_TOKEN are available; otherwise Tavily search only returns public links. |
| `bugcrowd_crowdstream_search` | Bugcrowd CrowdStream public disclosures | official | low | summary_links_evidence_only | [link](https://docs.bugcrowd.com/researchers/disclosure/disclosing-submissions/) |  | Use web search/extract; do not bypass login or private program gates. |
| `github_advisories_api` | GitHub Global Security Advisories API | official | low | summary_links_evidence_only | [link](https://docs.github.com/en/rest/security-advisories/global-advisories) |  | Not every GHSA is a bounty report, but advisories help correlate report/blog clusters. |
| `github_security_lab` | GitHub Security Lab Advisories | official | low | summary_links_evidence_only | [link](https://securitylab.github.com/advisories/) |  | Good source for root-cause analysis and advisory-writing patterns. |
| `yeswehack_blog_search` | YesWeHack public blog writeups | official | low | summary_links_evidence_only | [link](https://www.yeswehack.com/blog) |  | Public blog only; cluster with original researcher/platform links when available. |
| `disclose_io_directory` | disclose.io disclosure program directory | curated | low | summary_links_evidence_only | [link](https://directory.disclose.io/) |  | Mainly program/policy context; not treated as report proof unless linked report material exists. |
| `hacker101_community` | Hacker101 Community | curated | low | public_summary_links_only | [link](https://www.hackerone.com/hackers/hacker101) |  | Official beginner-to-intermediate training and community path. |
| `hacker101_ctf_private_invites` | Hacker101 CTF Invite Path | curated | medium | metadata_until_authorized_export | [link](https://ctf.hacker101.com/about) |  | Legitimate route toward private opportunities without storing private invite links. |
| `bugcrowd_community_discord` | Bugcrowd Community Discord | curated | low | metadata_until_authorized_export | [link](https://discord.com/servers/bugcrowd-community-319555028341882885) |  | Official platform-adjacent researcher community. |
| `intigriti_researchers` | Intigriti Researchers Portal | curated | low | public_summary_links_only | [link](https://www.intigriti.com/researchers) |  | European platform community and report-learning surface. |
| `yeswehack_researcher_portal` | YesWeHack Start Hunting | curated | low | public_summary_links_only | [link](https://www.yeswehack.com/researchers/start-hunting) |  | Official platform onboarding and researcher guidance. |
| `synack_red_team_apply` | Synack Red Team Application | curated | medium | metadata_until_authorized_export | [link](https://www.synack.com/red-team) |  | Legitimate private/vetted hunting ecosystem. |
| `secuna_hunt` | Secuna Hunt | curated | medium | metadata_until_authorized_export | [link](https://secuna.io/products/hunt) |  | Regional vetted bug bounty and VDP ecosystem. |
| `hackerone_community` | HackerOne Community | curated | low | public_summary_links_only | [link](https://www.hackerone.com/community) |  | Official community and education surface. |
| `bugcrowd_program_list` | Bugcrowd Program List | curated | low | public_summary_links_only | [link](https://www.bugcrowd.com/bug-bounty-list) |  | Helps identify active programs and public disclosures. |
| `google_vrp_blog_search` | Google Security Blog VRP | curated | low | public_summary_links_only | [link](https://security.googleblog.com) |  | High-quality vendor VRP report and research summaries. |
| `google_vrp_rules` | Google Bug Hunters Rules | curated | low | public_summary_links_only | [link](https://bughunters.google.com/about/rules/google-friends/6625378258649088) |  | Useful for legal scope, impact framing, and program policy learning. |
| `msrc_bounty_blog_recognition` | MSRC Blog | curated | low | public_summary_links_only | [link](https://msrc.microsoft.com/blog) |  | Vendor-grade disclosure and bounty communication examples. |
| `microsoft_researcher_recognition` | Microsoft Researcher Recognition | curated | low | public_summary_links_only | [link](https://www.microsoft.com/msrc/researcher-recognition-program) |  | Finds credible researchers and public writeups. |
| `meta_security_engineering` | Meta Security Engineering Blog | curated | low | public_summary_links_only | [link](https://engineering.fb.com/category/security) |  | Vendor-scale bug bounty and security engineering lessons. |
| `github_bounty_researchers` | GitHub Bug Bounty Researchers | curated | low | public_summary_links_only | [link](https://bounty.github.com/researchers) |  | High-signal researcher discovery and impact examples. |
| `atlassian_security_testing` | Atlassian Security Testing | curated | low | public_summary_links_only | [link](https://www.atlassian.com/trust/security/security-testing) |  | Public summary reports and platform policy examples. |
| `apple_security_bounty` | Apple Security Bounty | curated | low | public_summary_links_only | [link](https://security.apple.com/bounty) |  | Vendor program rules and impact classification reference. |
| `shopify_bug_bounty` | Shopify Bug Bounty Program | curated | low | public_summary_links_only | [link](https://hackerone.com/shopify) |  | E-commerce and business-logic report-learning target. |
| `wordfence_bounty_monthly_reports` | Wordfence Bounty Monthly Reports | curated | low | public_summary_links_only | [link](https://www.wordfence.com/blog) |  | CMS plugin bounty examples, CVSS/CWE and researcher credit. |
| `wordfence_intelligence_api` | Wordfence Intelligence API | curated | medium | metadata_until_authorized_export | [link](https://www.wordfence.com/help/wordfence-intelligence/v3-accessing-and-consuming-the-vulnerability-data-feed) |  | Structured vulnerability records with references and credits. |
| `patchstack_database` | Patchstack Database | curated | low | public_summary_links_only | [link](https://patchstack.com/database) |  | WordPress/plugin vulnerability learning and researcher credit source. |
| `patchstack_ti_api` | Patchstack Threat Intelligence API | curated | medium | metadata_until_authorized_export | [link](https://docs.patchstack.com/api-solutions/threat-intelligence-api/extended) |  | Structured CMS vulnerability intelligence with report-adjacent metadata. |
| `wpscan_vulnerability_database` | WPScan Vulnerability Database | curated | low | public_summary_links_only | [link](https://wpscan.com/vulnerability-database) |  | CMS vulnerability taxonomy, references, and plugin/theme exposure trends. |
| `plugin_vulnerabilities` | Plugin Vulnerabilities | curated | low | public_summary_links_only | [link](https://www.pluginvulnerabilities.com) |  | WordPress plugin vulnerability research and disclosure context. |

## curated_aggregators

| source_id | name | reliability | legal_risk | collection_policy | entry / URL | research context | notes |
|---|---|---|---|---|---|---|---|
| `pentesterland_writeups` | PentesterLand Writeups | curated | low | summary_links_evidence_only | [link](https://pentester.land/writeups/) |  | Aggregator; cluster with original reports/blogs when possible. |
| `hackdex` | HackDex | curated | low | summary_links_evidence_only | [link](https://hack-dex.com/) |  | Use as discovery source, not sole evidence for high confidence. |
| `bugboard` | BugBoard | curated | low | summary_links_evidence_only | [link](https://bugboard.rsecloud.com/) |  | Aggregator; prefer original link in evidence. |
| `google_vrp_writeups_repo` | Awesome Google VRP Writeups | curated | low | summary_links_evidence_only | [link](https://github.com/xdavidhu/awesome-google-vrp-writeups) |  | Excellent report-writing and impact examples; some older items are evergreen. |
| `portswigger_daily_swig_bug_bounty` | PortSwigger Daily Swig Hacking Techniques | curated | low | public_summary_links_only | [link](https://portswigger.net/daily-swig/hacking-techniques) |  | Curated reports, researcher stories, and technique context. |
| `assetnote_research` | Assetnote Research | curated | low | public_summary_links_only | [link](https://www.assetnote.io/platform/expert-security-research) |  | High-signal recon and vulnerability research. |
| `projectdiscovery_blog` | ProjectDiscovery Blog | curated | low | public_summary_links_only | [link](https://projectdiscovery.io/blog) |  | Recon automation and template-driven learning. |

## newsletter_podcast

| source_id | name | reliability | legal_risk | collection_policy | entry / URL | research context | notes |
|---|---|---|---|---|---|---|---|
| `disclosed_newsletter` | Disclosed | curated | low | summary_links_evidence_only | [link](https://getdisclosed.com/) |  | If paid/private export is imported later, require user authorization confirmation. |
| `bbre_premium_metadata` | Bug Bounty Reports Explained / BBRE | curated | medium | metadata_only | [link](https://premium.bugbountyexplained.com/) |  | No automated paid-content collection. Manual import requires authorization checkbox/export. |
| `critical_thinking_public` | Critical Thinking / Critical Research Lab public materials | curated | low | summary_links_evidence_only | [link](https://www.criticalthinkingpodcast.io/about/) |  | Public pages/podcast/newsletter only; Discord/private content must be user-authorized export. |
| `intigriti_bug_bytes` | Intigriti Bug Bytes / Blog | curated | low | summary_links_evidence_only | [link](https://newsletter.intigriti.com/) |  | Useful for report mentions and technique cross-links. |
| `ctbb_discord_premium_manual` | Critical Thinking Bug Bounty Discord | curated | medium | metadata_until_authorized_export | [link](https://discord.com/servers/1110206757227216916) |  | Current hunters share report-learning workflow, research links, and high-signal discussions. |
| `critical_research_lab_manual` | Critical Research Lab | curated | medium | metadata_until_authorized_export | [link](https://lab.ctbb.show) |  | High-signal bug bounty research lab connected to Critical Thinking. |
| `bbre_premium_manual` | Bug Bounty Reports Explained Premium | curated | medium | metadata_until_authorized_export | [link](https://premium.bugbountyexplained.com) |  | Focused report analysis and impact framing. |
| `nahamsec_discord_public` | NahamSec Discord Discovery | curated | low | metadata_until_authorized_export | [link](https://discord.com/servers/nahamsec-598608711186907146) |  | Large bug bounty learning community and event surface. |
| `nahamsec_udemy_course` | NahamSec Intro to Bug Bounty | curated | medium | metadata_until_authorized_export | [link](https://www.udemy.com/course/intro-to-bug-bounty-by-nahamsec) |  | Legitimate paid course for structured bug bounty basics and workflow. |
| `bugbountyhunter_zseano` | BugBountyHunter / Zseano Methodology | curated | low | public_summary_links_only | [link](https://www.bugbountyhunter.com/zseano) |  | Well-known methodology and hunting workflow reference. |
| `bounty_hunters_discord` | Bounty Hunters Discord Discovery | curated | low | metadata_until_authorized_export | [link](https://discord.com/servers/559875483295154188) |  | Large public bug bounty discussion community to discover legal learning leads. |

## web3_audit_bounty

| source_id | name | reliability | legal_risk | collection_policy | entry / URL | research context | notes |
|---|---|---|---|---|---|---|---|
| `code4rena_reports` | Code4rena public reports | official | low | summary_links_evidence_only | [link](https://code4rena.com/reports) |  | Web3 audit findings are treated as report-intelligence; no live target reproduction. |
| `solodit_reports` | Solodit public findings | curated | low | summary_links_evidence_only | [link](https://solodit.xyz/) |  | Use as indexed finding source; prefer original audit report as evidence. |
| `immunefi_public_reports` | Immunefi public reports and postmortems | official | low | summary_links_evidence_only | [link](https://immunefi.com/blog/) |  | Focus on impact framing and root cause; no operational replay on live protocols. |
| `sherlock_public_reports` | Sherlock public audit reports | official | low | summary_links_evidence_only | [link](https://audits.sherlock.xyz/) |  | Public Web3 audit findings; summarize root cause and impact only. |
| `cantina_public_reports` | Cantina public audit reports | official | low | summary_links_evidence_only | [link](https://cantina.xyz/portfolio) |  | Public portfolio/report discovery; keep KB cards link+summary based. |
| `codehawks_cyfrin_competitions` | Cyfrin CodeHawks Competitions | curated | low | metadata_until_authorized_export | [link](https://codehawks.cyfrin.io) |  | Web3 audit contest findings and legitimate participation path. |
| `codehawks_first_flights` | CodeHawks First Flights | curated | low | public_summary_links_only | [link](https://docs.codehawks.com/first-flights) |  | Legitimate Web3 audit learning path and practice context. |
| `hackenproof_programs_public` | HackenProof Programs | curated | low | metadata_until_authorized_export | [link](https://hackenproof.com/programs) |  | Web3 bounty scope discovery and report metadata context. |
| `hats_finance_bounties_metadata` | Hats Finance Bug Bounties | curated | low | metadata_until_authorized_export | [link](https://docs.hats.finance/welcome-to-hats-finance/bug-bounties) |  | Web3 bounty rules, vault model, and public program discovery. |
| `trail_of_bits_public_reports` | Trail of Bits Reports | curated | low | public_summary_links_only | [link](https://trailofbits.com/reports) |  | High-quality audit reports for root-cause and impact learning. |
| `openzeppelin_security_audits` | OpenZeppelin Security Audits | curated | low | public_summary_links_only | [link](https://www.openzeppelin.com/security-audits) |  | Smart contract audit report learning and methodology. |
| `spearbit_github_audits` | Spearbit Public Audit Repos | curated | low | public_summary_links_only | [link](https://github.com/spearbit-audits) |  | Web3 audit findings and report formats. |
| `zellic_reports` | Zellic Reports | curated | low | public_summary_links_only | [link](https://www.zellic.io/reports) |  | High-quality Web3/security audit reports. |

## community_social

| source_id | name | reliability | legal_risk | collection_policy | entry / URL | research context | notes |
|---|---|---|---|---|---|---|---|
| `x_report_threads` | X report threads and hunter discussions | social | low | summary_links_evidence_only | [link](https://x.com/) |  | Prefer Grok x_search for X; Tavily is for linked web verification only. |
| `reddit_bugbounty_writeups` | Reddit public bug bounty discussions | social | low | summary_links_evidence_only | [link](https://www.reddit.com/r/bugbounty/) |  | Use only as discussion/context unless primary links are present. |
| `medium_infosec_writeups` | Medium / InfoSec Writeups | researcher | low | summary_links_evidence_only | [link](https://infosecwriteups.com/) |  | Good for researcher narratives; verify claims with original report when possible. |
| `researcher_blogs_search` | Independent researcher blogs search | researcher | low | summary_links_evidence_only | [link](https://www.google.com/search?q=bug+bounty+writeup+disclosed+report+researcher+blog) |  | Catch-all public web query; treat each result as medium confidence until verified. |

## gray_trade_watchlist

| source_id | name | reliability | legal_risk | collection_policy | entry / URL | research context | notes |
|---|---|---|---|---|---|---|---|
| `manual_gray_telegram` | Manual gray-channel Telegram metadata slot | gray | high | metadata_only | `用户人工记录的公开可见 Telegram 群组、频道、帖子或目录页入口描述；不保存邀请链接、附件或报告内容。` | [ctx1](https://telegram.org/faq)<br>[ctx2](https://telegram.org/faq_channels)<br>[ctx3](https://core.telegram.org/api/channel)<br>[ctx4](https://tgstat.com/search) | Do not buy, request, download, parse, or save report contents. Only user-provided public metadata may enter channel_watchlist. |
| `manual_gray_discord` | Manual gray-channel Discord metadata slot | gray | high | metadata_only | `用户人工记录的公开可见 Discord 服务器介绍页、社区目录页或频道主题描述；不保存邀请链接、私聊内容、附件或报告内容。` | [ctx1](https://support.discord.com/hc/en-us/articles/4409308485271-Discovery-Guidelines)<br>[ctx2](https://discord.com/guidelines)<br>[ctx3](https://docs.discord.com/developers/discovery/best-practices) | No content collection. Manual review required before any legal/authorized export is imported separately. |
| `manual_gray_forum` | Manual gray-channel forum metadata slot | gray | high | metadata_only | `用户人工记录的公开论坛、市场帖、索引页或讨论串的自然语言入口描述；不保存需要登录/购买/下载后才能看到的内容。` | [ctx1](https://support.reddithelp.com/hc/en-us/articles/19695647891988-How-does-Reddit-search-work)<br>[ctx2](https://www.redditinc.com/policies/content-policy) | Only channel name/public entrance/topic tags/risk/manual notes; no attachments or private texts. |
| `manual_gray_marketplace` | Manual gray-channel marketplace metadata slot | gray | high | metadata_only | `用户人工记录的公开市场、资源目录、课程/报告交易广告的自然语言入口描述；不保存购买链接、交易方式、附件或报告内容。` | [ctx1](https://www.google.com/search/howsearchworks/) | Only public-facing metadata and risk notes. Do not buy, request, download, parse, or preserve content. |

### Gray metadata field policy

### `manual_gray_telegram`

- 可保留：公开目录/搜索面名称, 自然语言入口描述, 公开频道/群组描述摘要, 主题标签, 风险标记, 发现日期, 人工复核状态
- 禁止保留：邀请链接, 购买链接, 交易联系方式, 附件, 报告内容, 私聊内容

### `manual_gray_discord`

- 可保留：公开服务器/目录描述, 公开标签/分类, 社区规则提示, 风险标记, 发现日期, 人工复核状态
- 禁止保留：邀请链接, 购买链接, 频道消息, 成员列表, 附件, 报告内容, 私聊内容

### `manual_gray_forum`

- 可保留：公开论坛/讨论串类型, 自然语言入口描述, 主题类别, 公开规则/版规提示, 风险标记, 发现日期, 人工复核状态
- 禁止保留：交易帖直链, 联系方式, 价格, 付款方式, 附件, 报告内容, 精确可复现搜索词组合

### `manual_gray_marketplace`

- 可保留：公开市场/广告类型, 自然语言入口描述, 内容类别, 风险等级, 是否声称包含私有/NDA/付费报告, 发现日期, 人工复核状态
- 禁止保留：购买链接, 卖家账号, 付款方式, 下载链接, 附件, 报告内容, 未授权样本

