# 情报源地图 / Intelligence Source Map

> 机读版：`sources.yaml`（被 `apps/grok-kb-agent-suite/backend/connectors/` 加载）。
> 本文件是**人读版**，按区域和优先级整理；每个源对应 sources.yaml 中的 id。
>
> 信号密度：H = 高（每周多条可行动） / M = 中（双周一条） / L = 低（偶发）。
> Region：en (英文) / cn (中文) / jp (日本) / kr (韩国) / sea (东南亚) / web3 / ai / global。
> 自动化：connector 字段决定。
>
> 添加新源：
>   1. 在 `sources.yaml` 末尾追加一项；id 必须唯一。
>   2. 在本文件相应区段加一行人读说明。
>   3. 跑 `make sources-pull SOURCE=<id>` 验证连通。

---

## 1. 英文 — 研究博客（rss_generic）

| id | 描述 | 信号 |
|---|---|---|
| portswigger-research | PortSwigger 官方研究（James Kettle 等） | H |
| assetnote | Assetnote SaaS / edge / recon 研究 | H |
| watchtowr-labs | watchtowr Edge appliance 0day | H |
| project-zero | Google Project Zero | H |
| synacktiv | Synacktiv publications | H |
| ncc-group | NCC Group Research | H |
| trail-of-bits | Trail of Bits | H |
| doyensec | Doyensec | M |
| include-security | Include Security | M |
| praetorian | Praetorian | M |
| pd-blog | ProjectDiscovery 工具与新模板 | M |
| detectify-labs | Detectify Labs | M |
| securitum | Securitum Research | M |
| github-sec-lab | GitHub Security Lab | M |
| orange-tsai | Orange Tsai | M |
| sam-curry | Sam Curry | M |
| embrace-the-red | Embrace The Red — LLM/Prompt Injection | H |
| simon-willison | Simon Willison（LLM tooling） | H |

## 2. 英文 — Newsletter / 周刊 / Podcast（rss_generic）

| id | 描述 | 信号 |
|---|---|---|
| tldr-sec | Clint Gibler 的 tl;dr sec | H |
| ct-newsletter | Critical Thinking 邮件版 | H |
| bbre-substack | Bug Bounty Reports Explained Substack | H |
| intigriti-bug-bytes | Intigriti Bug Bytes | H |
| hackerone-blog | HackerOne 博客 | M |
| bugcrowd-blog | Bugcrowd 博客 | M |
| risky-biz | Risky Business 周播 | M |

## 3. Web3（rss_generic）

| id | 描述 | 信号 |
|---|---|---|
| immunefi-blog | Immunefi 官方 | H |
| rekt-news | Rekt News | H |
| samczsun | samczsun 个人博客 | M |

## 4. 亚洲（rss_generic）

| id | 区域 | 描述 |
|---|---|---|
| jpcert | jp | JPCERT/CC 通报 |
| ipa-jp | jp | IPA JVN advisory |
| flatt-security | jp | Flatt Security 博客 |
| ahnlab-asec | kr | AhnLab ASEC |
| vincss | sea | VinCSS（越南） |
| viettel-cs | sea | Viettel Cyber Security |

## 5. 中文 — 老牌站点（rss_generic）

| id | 描述 | 信号 |
|---|---|---|
| anquanke | 安全客 | H |
| freebuf | FreeBuf | M |
| seebug-paper | Seebug Paper（创宇 404） | H |

## 6. 中文 — 论坛 / Discourse / Discuz（cn_forum）

| id | 平台 | 描述 |
|---|---|---|
| linuxdo-security-tag | linux.do | #security 标签 |
| linuxdo-vuln-tag | linux.do | #漏洞 标签 |
| 90sec-latest | 90sec | Discourse 最新 |
| 52pojie-android-pentest | 52pojie | 移动安全板块 |

## 7. 微信公众号（wechat_rss via 本地 wechat2rss bridge）

> 部署：`make wechat-rss-up`（启动 docker-compose 在 127.0.0.1:8080）。
> 每条 url 都指向本地 bridge；biz 字段先占位（接入 bridge 时填真实值）。

| id | 公众号 |
|---|---|
| wechat-ctsrc | 携程安全应急响应中心 |
| wechat-tsrc | 腾讯安全应急响应中心 |
| wechat-asrc | 阿里安全响应中心 |
| wechat-bsrc | 百度安全应急响应中心 |
| wechat-mtsrc | 美团安全应急响应中心 |
| wechat-bytesrc | 字节跳动安全中心 |
| wechat-jsrc | 京东安全应急响应中心 |
| wechat-dsrc | 滴滴安全应急响应中心 |
| wechat-misrc | 小米安全中心 |
| wechat-bilibili | 哔哩哔哩安全应急响应中心 |
| wechat-nsrc | 网易安全中心 |
| wechat-xinanzhilu | 信安之路 |
| wechat-leishen | 雷神众测 |
| wechat-changting | 长亭安全 |
| wechat-knownsec-404 | 知道创宇 404 实验室 |
| wechat-anheng | 安恒安全研究院 |
| wechat-sangfor | 深信服千里目实验室 |
| wechat-anying | 暗影安全 |
| wechat-teamt5 | TeamT5（台湾） |
| wechat-vulpecker | 360 漏洞研究院 / Vulpecker Team |
| wechat-moan | 默安玄甲实验室 |

## 8. YouTube 频道（youtube_channel）

> 直接走 YT 公开 RSS（无需 API key）。channel_id 已填，缺失则需人工补全。

| id | 频道 |
|---|---|
| yt-ctbb | Critical Thinking BB Podcast |
| yt-nahamsec | NahamSec |
| yt-bbre | Bug Bounty Reports Explained |
| yt-stok | STÖK |
| yt-insiderphd | InsiderPhD |
| yt-ippsec | IppSec |
| yt-defcon | DEF CON |
| yt-blackhat | Black Hat |
| yt-offensivecon | OffensiveCon |

## 9. GitHub 仓库（github_repo — commits/releases/tags）

| id | 仓 | feed |
|---|---|---|
| gh-nuclei-templates | projectdiscovery/nuclei-templates | commits |
| gh-trickest-cve | trickest/cve | commits |
| gh-poc-in-github | nomi-sec/PoC-in-GitHub | commits |
| gh-h1-reports | reddelexc/hackerone-reports | commits |
| gh-defihacklabs | SunWeb3Sec/DeFiHackLabs | commits |
| gh-c4-reports | code-423n4/reports | commits |
| gh-tob-publications | trailofbits/publications | commits |
| gh-spearbit-portfolio | spearbit/portfolio | commits |
| gh-bambdas | PortSwigger/bambdas | releases |
| gh-bchecks | PortSwigger/BChecks | releases |
| gh-vrt | bugcrowd/vulnerability-rating-taxonomy | releases |
| gh-payloads | swisskyrepo/PayloadsAllTheThings | releases |
| gh-hacktricks | HackTricks-wiki/hacktricks | commits |
| gh-threekiii-poc | Threekiii/Awesome-POC | commits |

## 10. CVE / KEV / OSV / ZDI（cve_kev）

| id | feed | 用途 |
|---|---|---|
| cve-nvd-recent | nvd_recent | NVD 14 天滚动窗口 |
| cve-cisa-kev | cisa_kev | CISA 已被利用列表 |
| cve-osv-pypi | osv | PyPI 漏洞 |
| cve-osv-npm | osv | npm 漏洞 |
| cve-zdi | zdi | ZDI advisories |

---

## 已知未自动化的源（人工 / Phase 4 待启用）

下列源已在调研产物中盘点，**未** 进入 sources.yaml，因为它们需要：
- X / Twitter handle（需 nitter_x.py，Phase 4 实装；当前可用 X Pro 列表手工跟）
- HackerOne hacktivity / Bugcrowd Crowdstream / Pentester Land writeups.json（需 hacktivity_h1.py，Phase 4）
- Discord 频道（需 discord_bot.py，受 ToS 与邀请码限制，Phase 4 单独立项）
- 邀请制论坛（T00ls / 先知社区登录态、内部 TG 群）

完整候选源清单见：
- `~/.claude/plans/bugbountyplantform-velvety-volcano-agent-aed2a3b728cdd6e39.md`（英文圈 11 类）
- `~/.claude/plans/bugbountyplantform-velvety-volcano-agent-a2f2215f25adc0312.md`（中文+亚洲圈 8 类）

---

## 个人跟踪分组建议（保留自旧版本）

不要盲目复制 "top hacker list"。按输出类型分组，每月淘汰低信号账号：

- 写 disclosed report 的 hunter
- 做 client-side / XSS 的 researcher
- 做 API / OAuth / GraphQL 的 hunter
- 做 tooling 的作者
- 做 cloud / SaaS / AI security 的研究员
- 平台官方、triager、program manager
