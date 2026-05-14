# Gray Channel Research Protocol

> 目标：对灰色 Bug Bounty report trade 生态做完整的渠道层调研闭环，同时避免保存邀请链接、购买链接、附件、报告正文、交易联系方式或未授权内容。

## 解释

- “完整调研”在本库中定义为：覆盖预设平台/渠道类型、记录公开发现面、记录可保留字段与禁止字段、留下核查来源和人工复核状态。
- 不能承诺穷尽隐藏、私密、临时、邀请制或已删除渠道；这些只能标记为 `coverage_gap`，不能通过购买/加入/下载来补齐。
- 任何疑似泄露、NDA、私有报告内容只允许进入 `channel_watchlist` 的风险元数据，不进入 report card。

## 允许保留的信息

- 平台/渠道类型、自然语言入口描述、公开目录/搜索面名称、公开主题标签、公开描述摘要、风险等级、发现日期、人工复核状态。
- 平台级公开文档、公开搜索/发现面的首页或说明页、合规政策链接。

## 禁止保留的信息

- 具体邀请链接、购买链接、交易联系方式、价格/付款方式、附件、报告正文、未授权样本、私聊内容、绕过访问限制方法。

## telegram_public_discovery_surface

- Platform: `telegram`
- Purpose: 识别公开可见的频道/群组/帖子目录与描述性元数据，不进入频道、不保存邀请链接、不下载附件。
- Public context URLs:
  - [https://telegram.org/faq](https://telegram.org/faq)
  - [https://telegram.org/faq_channels](https://telegram.org/faq_channels)
  - [https://core.telegram.org/api/channel](https://core.telegram.org/api/channel)
  - [https://tgstat.com/search](https://tgstat.com/search)
- Retainable info:
  - 平台类型
  - 公开目录/搜索面的名称
  - 自然语言入口描述
  - 主题标签
  - 公开描述摘要
  - 可见成员/订阅量范围（如公开显示）
  - 最近可见活跃时间范围
  - 疑似售卖/泄露/NDA 风险标记
  - 发现日期
  - 人工复核结论
  - 是否需要举报/忽略
- Prohibited info:
  - 具体邀请链接
  - 购买链接
  - 交易联系方式
  - 附件
  - 报告正文
  - 泄露报告标题清单
  - 私聊内容
  - 绕过访问限制的方法
- Coverage notes: 覆盖 Telegram 官方公开用户名/频道说明、频道 FAQ、API 中 public username/private invite link 区分，以及一个公开频道搜索面样例；不进行具体关键词拉取。

## discord_public_discovery_surface

- Platform: `discord`
- Purpose: 识别公开 Discord Discovery/App Directory/社区目录层面的元数据，不保存服务器邀请、频道内容或私域材料。
- Public context URLs:
  - [https://support.discord.com/hc/en-us/articles/4409308485271-Discovery-Guidelines](https://support.discord.com/hc/en-us/articles/4409308485271-Discovery-Guidelines)
  - [https://discord.com/guidelines](https://discord.com/guidelines)
  - [https://docs.discord.com/developers/discovery/best-practices](https://docs.discord.com/developers/discovery/best-practices)
- Retainable info:
  - 公开目录类型
  - 服务器/社区的自然语言入口描述
  - 公开标签/分类
  - 规则/风险提示
  - 是否涉及售卖或疑似未授权材料
  - 人工复核状态
  - 发现日期
- Prohibited info:
  - 服务器邀请链接
  - 购买/付款链接
  - 频道消息
  - 成员列表
  - 附件
  - 报告正文
  - 私聊记录
  - 规避平台审核或发现限制的方法
- Coverage notes: 覆盖 Discord Discovery 指南、Community Guidelines 与 App Directory discovery 文档；只记录公开目录层元数据。

## reddit_forum_public_discussion_surface

- Platform: `reddit/forum`
- Purpose: 识别公开社区/论坛讨论中关于 report trade 的存在性、风险和指向性元数据，不保存交易入口或具体报告。
- Public context URLs:
  - [https://support.reddithelp.com/hc/en-us/articles/19695647891988-How-does-Reddit-search-work](https://support.reddithelp.com/hc/en-us/articles/19695647891988-How-does-Reddit-search-work)
  - [https://www.redditinc.com/policies/content-policy](https://www.redditinc.com/policies/content-policy)
- Retainable info:
  - 公开社区/论坛类型
  - 讨论主题类别
  - 自然语言入口描述
  - 风险关键词类别（不保存精确交易词组合）
  - 公开规则/版规提示
  - 是否疑似售卖泄露/NDA 内容
  - 人工复核状态
  - 发现日期
- Prohibited info:
  - 具体交易帖 URL
  - 卖家/买家联系方式
  - 价格
  - 付款方式
  - 附件
  - 报告正文
  - 精确可复现搜索词组合
- Coverage notes: 覆盖 Reddit 官方搜索能力说明和内容政策入口；论坛类以人工元数据记录为主。

## marketplace_public_ad_surface

- Platform: `marketplace`
- Purpose: 记录公开市场/资源目录/广告层面的存在性与风险，不保存购买路径、卖家联系或商品内容。
- Public context URLs:
  - [https://www.google.com/search/howsearchworks/](https://www.google.com/search/howsearchworks/)
- Retainable info:
  - 市场类型
  - 公开广告/目录的自然语言入口描述
  - 内容类别
  - 是否声称包含私有/NDA/付费报告
  - 风险等级
  - 人工复核状态
  - 发现日期
- Prohibited info:
  - 购买链接
  - 卖家账号
  - 付款方式
  - 下载链接
  - 附件
  - 报告正文
  - 未授权数据样本
- Coverage notes: 只保留市场/广告层风险画像；不构造或保存可直接定位交易的搜索词与链接。
