const $ = (selector) => document.querySelector(selector);
const prefersReducedMotion = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
const LANG_STORAGE_KEY = 'grok_kb_ui_language';

let currentLang = normalizeLang(localStorage.getItem(LANG_STORAGE_KEY) || 'zh-CN');
let currentHealth = null;
let currentJobs = [];

const I18N = {
  'zh-CN': {
    'skip.workspace': '跳到工作区',
    'button.menu': '菜单',
    'button.refresh': '刷新',
    'button.runPipeline': '启动全量采集',
    'button.discoverReports': '发现报告',
    'button.clusterReports': '聚类报告',
    'button.enrichReports': '增强报告',
    'button.applyReports': '写入报告卡片',
    'button.discoverTechniques': '提交技法发现',
    'button.expand': '提交扩展',
    'button.batch': '准备 / 提交 Batch',
    'button.runQa': '运行质量门',
    'button.verifyTavily': '用 Tavily 核查来源',
    'button.buildCatalog': '构建来源目录',
    'button.discoverCatalog': '按目录发现',
    'button.discoverSource': '发现单源',
    'button.importAuthorized': '导入授权导出',
    'button.generatePrompts': '生成提示词',
    'button.importChannels': '导入渠道结果',
    'button.applyChannels': '应用到来源目录',
    'button.validateRecords': '验证手动记录',
    'button.exportIndex': '导出渠道索引',
    'button.triageSources': '排序来源',
    'nav.home': '首页',
    'nav.homeSub': '状态与下一步',
    'nav.collect': '采集',
    'nav.collectSub': '报告 / 技法 / 全量',
    'nav.review': '复核',
    'nav.reviewSub': '任务、核查与质量门',
    'nav.settings': '设置',
    'nav.settingsSub': '来源、渠道与能力',
    'home.eyebrow': '证据优先 · 分步采集 · 可复核输出',
    'home.title': '情报采集工作台',
    'home.lede': '首页只保留系统状态、推荐下一步和核心入口。复杂表单已收进采集、复核与设置，让你从“该做什么”开始，而不是从参数堆里找路。',
    'home.cta.collect': '开始采集',
    'home.cta.review': '查看任务',
    'home.cta.settings': '检查设置',
    'home.health': '服务健康',
    'home.next.eyebrow': '推荐下一步',
    'home.runway.eyebrow': '运行状态',
    'home.runway.title': '准备情况',
    'kpi.keys': 'API Key',
    'kpi.keysSub': '已配置供应商',
    'kpi.sources': '来源面',
    'kpi.sourcesSub': '目录 / Watchlist / 手动索引',
    'kpi.jobs': '任务队列',
    'kpi.jobsSub': '成功 / 运行 / 失败',
    'kpi.latest': '最近任务',
    'kpi.latestSub': '最新 action',
    'quick.pipeline.title': '全量采集',
    'quick.pipeline.body': '串联来源目录、报告、技法与质量检查。',
    'quick.reports.title': '公开报告采集',
    'quick.reports.body': '寻找真实公开报告，并转为可学习卡片。',
    'quick.techniques.title': '技法情报采集',
    'quick.techniques.body': '收集 2025–2026 技法、案例和研究线索。',
    'quick.review.title': '结果复核',
    'quick.review.body': '查看任务、失败原因、核查与 KB 质量门。',
    'collect.eyebrow': '采集工作流',
    'collect.title': '从目标任务开始',
    'collect.lede': '这里按“全量、报告、技法”组织，而不是按底层脚本名组织。常用字段直接显示，低频参数收进高级操作。',
    'collect.openReview': '打开复核',
    'pipeline.title': '全量采集',
    'pipeline.what': '一键串联目录、报告、技法、核查与质量门，适合日常稳定运行。',
    'pipeline.output': '候选、聚类、卡片、索引与验证结果。',
    'pipeline.next': '运行后到复核页查看失败项与输出目录。',
    'reports.title': '报告采集',
    'reports.what': '从公开平台、研究员博客和新闻源中寻找真实 Bug Bounty 报告。',
    'reports.output': '报告候选列表、来源链接、聚类与报告卡片。',
    'reports.next': '先 Discover，再 Cluster / Enrich / Apply。',
    'reports.cluster.title': '报告聚类',
    'reports.cluster.hint': '按 canonical URL / 平台 report id / title+program+class 去重聚类。',
    'reports.enrich.title': '报告增强',
    'reports.apply.title': '写入报告卡片',
    'reports.apply.hint': '写入 reports/*，更新 report index 与 report_ledger.tsv。',
    'techniques.title': '技法采集',
    'techniques.what': '收集 X/Web 中近两年技法、旧洞新挖与可迁移研究线索。',
    'techniques.output': '候选技法、来源 URL、扩展批次与 KB 卡片。',
    'techniques.next': '先 Discover Topic，高质量后再 Expand / Batch。',
    'techniques.expand.title': '扩展批次',
    'techniques.batch.title': 'Batch API',
    'review.eyebrow': '复核与反馈',
    'review.title': '任务、核查与质量门',
    'review.lede': '这里集中展示运行状态、失败原因、Tavily 核查和 KB 验证。采集完成后优先看这里。',
    'review.summary.eyebrow': '最近状态',
    'review.summary.title': '任务摘要',
    'qa.title': '质量门',
    'qa.what': '重建索引并运行 KB validator；Apply 后建议执行。',
    'qa.validate.body': '用于确认索引、frontmatter、ledger 和合规边界仍然有效。',
    'jobs.eyebrow': '执行日志',
    'jobs.title': '最近任务',
    'settings.eyebrow': '设置与高级能力',
    'settings.title': '来源、渠道与系统能力',
    'settings.lede': '这里保留低频但必要的配置型功能。默认折叠，避免干扰日常采集。',
    'settings.backCollect': '返回采集',
    'settings.keys.eyebrow': '凭证状态',
    'settings.keys.title': 'API Key 与来源状态',
    'settings.keys.body': '这里只显示是否生效，不展示密钥内容。若缺少关键 key，首页会优先提示修复设置。',
    'catalog.title': '来源目录',
    'catalog.what': '生成或更新公开平台、聚合器、newsletter、Web3、社区与灰色元数据 watchlist。',
    'catalog.discover.title': '按目录发现',
    'catalog.discover.hint': 'gray_metadata_only 只生成 channel metadata，不进入 enrich/apply。',
    'catalog.source.title': '单源发现',
    'catalog.manual.title': '授权导入',
    'catalog.manual.hint': '用于付费 newsletter/Discord/Telegram 私域的用户授权导出；仍只保存摘要、链接、证据短片段/hash。',
    'manual.title': '手动渠道研究',
    'manual.what': '用于记录合法入口、发现路径、trashcan 元数据和待复核线索。',
    'manual.prompts.title': '生成调研提示词',
    'manual.prompts.hint': '生成 Grok Expert 调研 prompt，用于收集合法付费/私域/小众渠道入口与完整发现记录。',
    'manual.import.title': '导入 Grok TSV',
    'manual.import.hint': '导入时自动分流：合法入口 / Trashcan / 待复核。不保存私邀、付款、附件或全文。',
    'manual.apply.title': '应用到来源目录',
    'manual.validate.title': '验证发现记录',
    'manual.validate.hint': '检查私邀、付款页、附件 URL、长正文、缺失合法获取方式等问题；硬阻断项以 warning 进入 trashcan。',
    'manual.export.title': 'Trashcan 与索引',
    'manual.export.hint': '导出 Obsidian 导航页：合法入口 / Trashcan / 待复核。',
    'manual.triage.title': '来源排序',
    'powerups.title': '系统能力',
    'powerups.what': '当前平台加载的 powerup/skill 说明。默认作为高级参考，不放在首页。',
    'advanced.pipeline': '高级参数',
    'advanced.reportSteps': '高级操作：聚类、增强、写入',
    'advanced.techniqueSteps': '高级操作：扩展批次与 Batch API',
    'advanced.tavily': '高级操作：Tavily 单独核查',
    'advanced.catalog': '高级操作：目录发现、单源发现、人工导入',
    'advanced.manual': '高级操作：提示词、导入、验证与索引',
    'advanced.powerups': '查看 Powerup Skills',
    'card.output': '产出',
    'card.next': '下一步',
    'form.mode': '模式',
    'form.fromDate': '开始日期',
    'form.toDate': '结束日期',
    'form.reportLimit': '报告限制/来源',
    'form.enrichLimit': '增强限制/轮',
    'form.techniqueLimit': '技法限制/主题',
    'form.startBatch': '起始批次',
    'form.reportsOnly': '只运行报告',
    'form.techniquesOnly': '只运行技法',
    'form.dryRun': '仅试运行',
    'form.dryRunFirst': '先试运行',
    'form.sourcePreset': '来源预设',
    'form.limit': '限制',
    'form.topic': '主题',
    'form.vulnClass': '漏洞类型',
    'form.runDir': '运行目录',
    'form.inputOverride': '输入覆盖',
    'form.skipTavily': '跳过 Tavily Extract',
    'form.attachTavily': '附加 Tavily web context',
    'form.fromBatch': '起始批次',
    'form.toBatch': '结束批次',
    'form.useSearch': '使用 X/Web Search',
    'form.tavilyPreverify': 'Tavily 预核查 web 来源',
    'form.dryRunRequest': '仅生成请求 JSON',
    'form.writeBack': '写回 cards JSON',
    'form.searchMissing': '搜索替代来源',
    'form.preset': '预设',
    'form.tier': 'Tier',
    'form.sourceId': 'Source ID',
    'form.inputJson': '输入 JSON',
    'form.authConfirmed': '我确认拥有该导出的合法使用权',
    'form.outputDir': '输出目录',
    'form.inputFile': '输入 TSV/JSONL',
    'form.researchTopic': '研究主题',
    'form.promptQuery': 'Prompt / Query',
    'form.toolUsed': '使用工具',
    'form.replaceSource': '替换已有 source_id',
    'form.tierPreset': 'Tier / Preset',
    'form.printOnly': '仅打印',
    'placeholder.vulnClass': 'IDOR / OAuth / payment / GraphQL',
    'placeholder.reportRunDir': 'apps/grok-kb-agent-suite/data/runs/report_<job>',
    'placeholder.candidates': '<run_dir>/discovery/candidates.jsonl',
    'placeholder.clusters': '<run_dir>/clusters/clusters.json',
    'placeholder.grokRunDir': 'data/grok_api/runs/<run_id>',
    'placeholder.authorizedExport': 'path/to/authorized_export.json',
    'placeholder.optionalRunDir': '可选输出运行目录',
    'placeholder.optionalPromptDir': '可选 prompt 输出目录',
    'status.ready': '已就绪',
    'status.missing': '缺失',
    'status.pending': '待检查',
    'status.ok': '全部就绪',
    'status.warning': '需要处理',
    'status.succeeded': '成功',
    'status.failed': '失败',
    'status.running': '运行中',
    'status.queued': '排队中',
    'status.none': '未运行',
    'toast.submitting': '正在提交…',
    'toast.submitted': '{action} 已提交：{id}。可在复核页查看进度。',
    'toast.failed': '{action} 失败：{error}',
    'toast.healthFailed': '健康检查失败：{error}',
    'toast.skillsFailed': '能力刷新失败：{error}',
    'jobs.empty.title': '还没有任务',
    'jobs.empty.body': '启动一次全量采集、报告发现或技法发现后，任务会显示在这里。',
    'jobs.noOutput': '暂无输出。',
    'jobs.runDir': '运行目录',
    'jobs.output': '输出',
    'skills.empty.title': '未发现 powerup',
    'skills.empty.body': '请检查 suite skills/powerups 目录。',
    'summary.total': '总任务',
    'summary.failed': '失败任务',
    'summary.running': '运行中',
    'summary.latest': '最新任务',
    'recommend.keys.title': '先修复关键 API Key',
    'recommend.keys.body': 'xAI/Grok 或 Tavily 未就绪时，采集和核查会不完整。请先到设置页确认 .env 是否生效。',
    'recommend.keys.cta': '检查设置',
    'recommend.failed.title': '先处理失败任务',
    'recommend.failed.body': '最近存在失败任务。建议进入复核页查看错误摘要，再决定是否重跑。',
    'recommend.failed.cta': '查看失败任务',
    'recommend.running.title': '任务正在运行',
    'recommend.running.body': '当前已有任务运行中。进入复核页观察输出，避免重复提交造成噪声或成本浪费。',
    'recommend.running.cta': '查看进度',
    'recommend.first.title': '从一次小规模采集开始',
    'recommend.first.body': '还没有历史任务。建议用 steady/smoke 模式跑一次全量采集，确认来源和输出目录都正常。',
    'recommend.first.cta': '开始采集',
    'recommend.next.title': '可以启动下一轮采集',
    'recommend.next.body': '关键状态正常。建议按目标选择公开报告采集或技法采集，并在复核页检查输出。',
    'recommend.next.cta': '进入采集',
  },
  en: {
    'skip.workspace': 'Skip to workspace',
    'button.menu': 'Menu',
    'button.refresh': 'Refresh',
    'button.runPipeline': 'Run full pipeline',
    'button.discoverReports': 'Discover reports',
    'button.clusterReports': 'Cluster reports',
    'button.enrichReports': 'Enrich reports',
    'button.applyReports': 'Apply report cards',
    'button.discoverTechniques': 'Submit technique discovery',
    'button.expand': 'Submit expansion',
    'button.batch': 'Prepare / submit batch',
    'button.runQa': 'Run QA gate',
    'button.verifyTavily': 'Verify sources with Tavily',
    'button.buildCatalog': 'Build source catalog',
    'button.discoverCatalog': 'Discover by catalog',
    'button.discoverSource': 'Discover source',
    'button.importAuthorized': 'Import authorized export',
    'button.generatePrompts': 'Generate prompts',
    'button.importChannels': 'Import channel results',
    'button.applyChannels': 'Apply to source catalog',
    'button.validateRecords': 'Validate manual records',
    'button.exportIndex': 'Export channel index',
    'button.triageSources': 'Triage sources',
    'nav.home': 'Home',
    'nav.homeSub': 'Status and next step',
    'nav.collect': 'Collect',
    'nav.collectSub': 'Reports / techniques / full run',
    'nav.review': 'Review',
    'nav.reviewSub': 'Jobs, checks, QA gate',
    'nav.settings': 'Settings',
    'nav.settingsSub': 'Sources, channels, skills',
    'home.eyebrow': 'Evidence-first · guided collection · reviewable output',
    'home.title': 'Bug Bounty Intelligence Workbench',
    'home.lede': 'The home page now shows only health, the recommended next step, and core entry points. Deeper forms live under Collect, Review, and Settings so you start from the job, not from a wall of parameters.',
    'home.cta.collect': 'Start collecting',
    'home.cta.review': 'View jobs',
    'home.cta.settings': 'Check settings',
    'home.health': 'Service health',
    'home.next.eyebrow': 'Recommended next step',
    'home.runway.eyebrow': 'Runway',
    'home.runway.title': 'Readiness',
    'kpi.keys': 'API keys',
    'kpi.keysSub': 'Configured providers',
    'kpi.sources': 'Source surfaces',
    'kpi.sourcesSub': 'Catalog / watchlist / manual index',
    'kpi.jobs': 'Job queue',
    'kpi.jobsSub': 'Succeeded / running / failed',
    'kpi.latest': 'Latest run',
    'kpi.latestSub': 'Most recent action',
    'quick.pipeline.title': 'Full pipeline',
    'quick.pipeline.body': 'Chain source catalog, reports, techniques, and QA.',
    'quick.reports.title': 'Public report collection',
    'quick.reports.body': 'Find real public reports and turn them into learning cards.',
    'quick.techniques.title': 'Technique collection',
    'quick.techniques.body': 'Collect 2025–2026 techniques, cases, and research leads.',
    'quick.review.title': 'Review results',
    'quick.review.body': 'Inspect jobs, failures, verification, and the KB quality gate.',
    'collect.eyebrow': 'Collection workflows',
    'collect.title': 'Start from the job',
    'collect.lede': 'This page is organized by user tasks — full run, reports, techniques — not by script names. Common fields stay visible; low-frequency controls live in advanced sections.',
    'collect.openReview': 'Open review',
    'pipeline.title': 'Full pipeline',
    'pipeline.what': 'Run catalog, reports, techniques, verification, and QA in one guided flow for steady daily operation.',
    'pipeline.output': 'Candidates, clusters, cards, indexes, and verification results.',
    'pipeline.next': 'After running, open Review to inspect failures and output directories.',
    'reports.title': 'Report collection',
    'reports.what': 'Find real Bug Bounty reports from public platforms, researcher blogs, and newsletters.',
    'reports.output': 'Report candidates, source URLs, clusters, and report cards.',
    'reports.next': 'Run Discover first, then Cluster / Enrich / Apply.',
    'reports.cluster.title': 'Report clustering',
    'reports.cluster.hint': 'Deduplicate by canonical URL, platform report id, or title+program+class.',
    'reports.enrich.title': 'Report enrichment',
    'reports.apply.title': 'Apply report cards',
    'reports.apply.hint': 'Write reports/* and update the report index plus report_ledger.tsv.',
    'techniques.title': 'Technique collection',
    'techniques.what': 'Collect recent X/Web techniques, evergreen methods in new contexts, and transferable research leads.',
    'techniques.output': 'Technique candidates, source URLs, expansion batches, and KB cards.',
    'techniques.next': 'Run Discover Topic first; expand or batch only after quality looks good.',
    'techniques.expand.title': 'Expand batches',
    'techniques.batch.title': 'Batch API',
    'review.eyebrow': 'Review and feedback',
    'review.title': 'Jobs, verification, and QA gate',
    'review.lede': 'This is where run status, failures, Tavily checks, and KB validation live. After collection, start here.',
    'review.summary.eyebrow': 'Recent state',
    'review.summary.title': 'Job summary',
    'qa.title': 'QA gate',
    'qa.what': 'Rebuild indexes and run the KB validator; recommended after apply steps.',
    'qa.validate.body': 'Use this to confirm indexes, frontmatter, ledgers, and compliance boundaries remain valid.',
    'jobs.eyebrow': 'Execution log',
    'jobs.title': 'Recent jobs',
    'settings.eyebrow': 'Settings and advanced capabilities',
    'settings.title': 'Sources, channels, and system skills',
    'settings.lede': 'Low-frequency but necessary controls live here. They are collapsed by default so daily collection stays focused.',
    'settings.backCollect': 'Back to collect',
    'settings.keys.eyebrow': 'Credential status',
    'settings.keys.title': 'API keys and source state',
    'settings.keys.body': 'Only readiness is shown here; secret values are never displayed. If a key is missing, Home will recommend fixing Settings first.',
    'catalog.title': 'Source catalog',
    'catalog.what': 'Build or update public platforms, aggregators, newsletters, Web3, community sources, and gray metadata watchlists.',
    'catalog.discover.title': 'Discover by catalog',
    'catalog.discover.hint': 'gray_metadata_only creates channel metadata only; it does not enter enrich/apply.',
    'catalog.source.title': 'Single-source discovery',
    'catalog.manual.title': 'Authorized import',
    'catalog.manual.hint': 'For user-authorized exports from paid newsletters or private communities; still stores summaries, links, short evidence snippets, and hashes only.',
    'manual.title': 'Manual channel research',
    'manual.what': 'Record legitimate entry points, discovery paths, trashcan metadata, and review leads.',
    'manual.prompts.title': 'Generate research prompts',
    'manual.prompts.hint': 'Generate Grok Expert prompts for legitimate gated/private/niche channels and full discovery records.',
    'manual.import.title': 'Import Grok TSV',
    'manual.import.hint': 'Imports are routed into legitimate entries, Trashcan, or review queue. Invite links, payment pages, attachments, and full text are not stored.',
    'manual.apply.title': 'Apply to source catalog',
    'manual.validate.title': 'Validate discovery records',
    'manual.validate.hint': 'Checks invite links, payment pages, attachment URLs, long full text, and missing legal acquisition paths; hard-blocked items become trashcan warnings.',
    'manual.export.title': 'Trashcan and index',
    'manual.export.hint': 'Export the Obsidian navigation page: legitimate entries / Trashcan / review queue.',
    'manual.triage.title': 'Source triage',
    'powerups.title': 'System skills',
    'powerups.what': 'Loaded powerup/skill descriptions. Kept as advanced reference instead of a home-page module.',
    'advanced.pipeline': 'Advanced parameters',
    'advanced.reportSteps': 'Advanced actions: cluster, enrich, apply',
    'advanced.techniqueSteps': 'Advanced actions: batch expansion and Batch API',
    'advanced.tavily': 'Advanced action: standalone Tavily verification',
    'advanced.catalog': 'Advanced actions: catalog discovery, single source, manual import',
    'advanced.manual': 'Advanced actions: prompts, import, validation, index',
    'advanced.powerups': 'View Powerup Skills',
    'card.output': 'Output',
    'card.next': 'Next step',
    'form.mode': 'Mode',
    'form.fromDate': 'From date',
    'form.toDate': 'To date',
    'form.reportLimit': 'Report limit/source',
    'form.enrichLimit': 'Enrich limit/run',
    'form.techniqueLimit': 'Technique limit/topic',
    'form.startBatch': 'Start batch',
    'form.reportsOnly': 'Reports only',
    'form.techniquesOnly': 'Techniques only',
    'form.dryRun': 'Dry run only',
    'form.dryRunFirst': 'Dry run first',
    'form.sourcePreset': 'Source preset',
    'form.limit': 'Limit',
    'form.topic': 'Topic',
    'form.vulnClass': 'Vulnerability class',
    'form.runDir': 'Run directory',
    'form.inputOverride': 'Input override',
    'form.skipTavily': 'Skip Tavily Extract',
    'form.attachTavily': 'Attach Tavily web context',
    'form.fromBatch': 'From batch',
    'form.toBatch': 'To batch',
    'form.useSearch': 'Use X/Web Search',
    'form.tavilyPreverify': 'Tavily pre-verify web sources',
    'form.dryRunRequest': 'Dry run request JSON',
    'form.writeBack': 'Write back to cards JSON',
    'form.searchMissing': 'Search alternate sources',
    'form.preset': 'Preset',
    'form.tier': 'Tier',
    'form.sourceId': 'Source ID',
    'form.inputJson': 'Input JSON',
    'form.authConfirmed': 'I confirm I am authorized to use this export',
    'form.outputDir': 'Output directory',
    'form.inputFile': 'Input TSV/JSONL',
    'form.researchTopic': 'Research topic',
    'form.promptQuery': 'Prompt / query',
    'form.toolUsed': 'Tool used',
    'form.replaceSource': 'Replace existing source_id',
    'form.tierPreset': 'Tier / preset',
    'form.printOnly': 'Print only',
    'placeholder.vulnClass': 'IDOR / OAuth / payment / GraphQL',
    'placeholder.reportRunDir': 'apps/grok-kb-agent-suite/data/runs/report_<job>',
    'placeholder.candidates': '<run_dir>/discovery/candidates.jsonl',
    'placeholder.clusters': '<run_dir>/clusters/clusters.json',
    'placeholder.grokRunDir': 'data/grok_api/runs/<run_id>',
    'placeholder.authorizedExport': 'path/to/authorized_export.json',
    'placeholder.optionalRunDir': 'optional output run dir',
    'placeholder.optionalPromptDir': 'optional prompt output dir',
    'status.ready': '已就绪',
    'status.missing': '缺失',
    'status.pending': 'pending',
    'status.ok': 'all systems ready',
    'status.warning': 'needs attention',
    'status.succeeded': 'succeeded',
    'status.failed': 'failed',
    'status.running': 'running',
    'status.queued': 'queued',
    'status.none': 'not run',
    'toast.submitting': 'Submitting…',
    'toast.submitted': '{action} submitted: {id}. Open Review to monitor progress.',
    'toast.failed': '{action} failed: {error}',
    'toast.healthFailed': 'Health check failed: {error}',
    'toast.skillsFailed': 'Skills refresh failed: {error}',
    'jobs.empty.title': 'No jobs yet',
    'jobs.empty.body': 'Start a pipeline, report discovery, or technique discovery job and it will appear here.',
    'jobs.noOutput': 'No output yet.',
    'jobs.runDir': 'Run dir',
    'jobs.output': 'Output',
    'skills.empty.title': 'No powerups found',
    'skills.empty.body': 'Check the suite skills/powerups directory.',
    'summary.total': 'Total jobs',
    'summary.failed': 'Failed jobs',
    'summary.running': 'Running',
    'summary.latest': 'Latest job',
    'recommend.keys.title': 'Fix critical API keys first',
    'recommend.keys.body': 'Collection and verification are incomplete while xAI/Grok or Tavily is missing. Open Settings and confirm that .env is loaded.',
    'recommend.keys.cta': 'Check settings',
    'recommend.failed.title': 'Review failed jobs first',
    'recommend.failed.body': 'Some recent jobs failed. Open Review, inspect the error summary, then decide whether to rerun.',
    'recommend.failed.cta': 'View failed jobs',
    'recommend.running.title': 'A job is already running',
    'recommend.running.body': 'Monitor the current run in Review to avoid duplicate submissions, extra noise, or unnecessary cost.',
    'recommend.running.cta': 'View progress',
    'recommend.first.title': 'Start with a small run',
    'recommend.first.body': 'No job history yet. Run smoke or steady mode once to confirm sources and output paths are healthy.',
    'recommend.first.cta': 'Start collecting',
    'recommend.next.title': 'Ready for the next collection run',
    'recommend.next.body': 'Core status looks good. Pick report collection or technique collection, then review the output.',
    'recommend.next.cta': 'Go to Collect',
  }
};

const ACTION_LABELS = {
  intel_pipeline: { 'zh-CN': '全量采集', en: 'Full pipeline' },
  report_discover: { 'zh-CN': '报告发现', en: 'Report discovery' },
  report_cluster: { 'zh-CN': '报告聚类', en: 'Report clustering' },
  report_enrich: { 'zh-CN': '报告增强', en: 'Report enrichment' },
  report_apply: { 'zh-CN': '写入报告卡片', en: 'Apply report cards' },
  discover: { 'zh-CN': '技法发现', en: 'Technique discovery' },
  expand: { 'zh-CN': '扩展批次', en: 'Expand batches' },
  batch_submit: { 'zh-CN': 'Batch API', en: 'Batch API' },
  tavily_verify: { 'zh-CN': 'Tavily 核查', en: 'Tavily verify' },
  validate: { 'zh-CN': '质量门', en: 'QA gate' },
  report_catalog_build: { 'zh-CN': '构建来源目录', en: 'Build source catalog' },
  report_discover_catalog: { 'zh-CN': '目录发现', en: 'Catalog discovery' },
  report_discover_source: { 'zh-CN': '单源发现', en: 'Source discovery' },
  report_import_manual: { 'zh-CN': '授权导入', en: 'Authorized import' },
  manual_channel_prompts: { 'zh-CN': '生成渠道提示词', en: 'Manual channel prompts' },
  import_manual_channel_results: { 'zh-CN': '导入渠道结果', en: 'Import channel results' },
  apply_manual_channel_catalog: { 'zh-CN': '应用渠道目录', en: 'Apply channel catalog' },
  validate_discovery_records: { 'zh-CN': '验证发现记录', en: 'Validate records' },
  export_manual_channel_index: { 'zh-CN': '导出渠道索引', en: 'Export channel index' },
  report_triage_sources: { 'zh-CN': '来源排序', en: 'Source triage' },
};

function normalizeLang(lang) {
  return lang === 'en' ? 'en' : 'zh-CN';
}

function t(key, params = {}) {
  const dict = I18N[currentLang] || I18N['zh-CN'];
  let value = dict[key] ?? I18N['zh-CN'][key] ?? key;
  for (const [name, replacement] of Object.entries(params)) {
    value = value.replaceAll(`{${name}}`, String(replacement));
  }
  return value;
}

function friendlyAction(action) {
  return ACTION_LABELS[action]?.[currentLang] || action || '—';
}

function statusLabel(status) {
  if (!status) return t('status.none');
  return t(`status.${status}`) || status;
}

function applyI18n() {
  document.documentElement.lang = currentLang;
  document.querySelectorAll('[data-i18n]').forEach((el) => { el.textContent = t(el.dataset.i18n); });
  document.querySelectorAll('[data-i18n-placeholder]').forEach((el) => { el.placeholder = t(el.dataset.i18nPlaceholder); });
  document.querySelectorAll('[data-lang-choice]').forEach((button) => {
    const active = normalizeLang(button.dataset.langChoice) === currentLang;
    button.classList.toggle('active', active);
    button.setAttribute('aria-pressed', String(active));
  });
  updateRefreshStamp();
  renderRecommendation();
  refreshWorkflowStates(currentJobs);
  renderReviewSummary(currentJobs);
}

function bindLanguageSwitches() {
  document.querySelectorAll('[data-lang-choice]').forEach((button) => {
    button.addEventListener('click', () => {
      currentLang = normalizeLang(button.dataset.langChoice);
      localStorage.setItem(LANG_STORAGE_KEY, currentLang);
      applyI18n();
    });
  });
}

async function api(path, opts = {}) {
  const res = await fetch(path, { headers: { 'content-type': 'application/json' }, ...opts });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error || res.statusText);
  return data;
}

function formData(form) {
  const fd = new FormData(form);
  const obj = {};
  for (const [k, v] of fd.entries()) obj[k] = v;
  for (const el of form.querySelectorAll('input[type="checkbox"]')) obj[el.name] = el.checked;
  for (const el of form.querySelectorAll('input[type="number"]')) obj[el.name] = Number(el.value);
  return obj;
}

function escapeHtml(s) {
  return String(s ?? '').replace(/[&<>"']/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
}

function chip(label, ok, index = 0) {
  const state = ok ? 'ok' : 'warn';
  return `<div class="health-row ${state}" style="--stagger: ${Math.min(index * 36, 240)}ms"><span>${escapeHtml(label)}</span><strong>${ok ? t('status.ready') : t('status.missing')}</strong></div>`;
}

function showToast(message) {
  const toast = $('#toast');
  if (!toast) return;
  toast.textContent = message;
  toast.classList.add('show');
  clearTimeout(showToast._timer);
  showToast._timer = setTimeout(() => toast.classList.remove('show'), 4200);
}

function flashTarget(el) {
  if (!el || prefersReducedMotion) return;
  el.classList.remove('target-flash');
  void el.offsetWidth;
  el.classList.add('target-flash');
}

function pulseIfChanged(selector, nextText) {
  const el = $(selector);
  if (!el) return;
  const changed = el.textContent !== String(nextText);
  el.textContent = nextText;
  if (changed && !prefersReducedMotion) {
    el.classList.remove('pulse-once');
    void el.offsetWidth;
    el.classList.add('pulse-once');
  }
}

function updateScrollProgress() {
  const progress = $('#scrollProgress');
  if (!progress) return;
  const max = document.documentElement.scrollHeight - window.innerHeight;
  const ratio = max > 0 ? Math.min(1, Math.max(0, window.scrollY / max)) : 0;
  progress.style.transform = `scaleX(${ratio})`;
}

function updateRefreshStamp() {
  const el = $('#lastRefresh');
  if (el) el.textContent = `${currentLang === 'zh-CN' ? '刷新于' : 'refreshed'} ${new Date().toLocaleTimeString()}`;
}

function providerRows(h) {
  return [
    ['xAI / Grok', h?.has_xai_key],
    ['Tavily verifier', h?.has_tavily_key],
    ['HackerOne', h?.has_hackerone_key],
    ['GitHub', h?.has_github_token],
    ['Bugcrowd', h?.has_bugcrowd_token],
    ['Source catalog', h?.has_report_source_catalog],
    ['Manual channel index', h?.has_manual_channel_index],
  ];
}

async function refreshHealth() {
  try {
    const h = await api('/api/health');
    currentHealth = h;
    const providers = [h.has_xai_key, h.has_tavily_key, h.has_hackerone_key, h.has_github_token, h.has_bugcrowd_token];
    const sources = [h.has_report_source_catalog, h.has_report_watchlist, h.has_manual_channel_index];
    document.querySelectorAll('.status-dot').forEach(dot => dot.classList.toggle('ok', Boolean(h.ok)));
    const sidebarStatus = $('#sidebarStatus');
    if (sidebarStatus) sidebarStatus.textContent = h.ok ? t('status.ok') : t('status.warning');
    const rows = providerRows(h);
    const health = $('#health');
    if (health) {
      health.innerHTML = [
        ...rows.slice(0, 6).map(([label, ok], index) => chip(label, ok, index)),
        `<span class="health-path">${escapeHtml(h.project_root)}</span>`
      ].join('');
    }
    const settingsSummary = $('#settingsProviderSummary');
    if (settingsSummary) {
      settingsSummary.innerHTML = rows.map(([label, ok], index) => chip(label, ok, index)).join('');
    }
    pulseIfChanged('#kpiKeys', `${providers.filter(Boolean).length}/${providers.length}`);
    pulseIfChanged('#kpiSources', `${sources.filter(Boolean).length}/${sources.length}`);
    updateRefreshStamp();
    renderRecommendation();
  } catch (err) {
    const health = $('#health');
    if (health) health.innerHTML = `<div class="health-row warn"><span>health</span><strong>${escapeHtml(err.message)}</strong></div>`;
    showToast(t('toast.healthFailed', { error: err.message }));
  }
}

async function refreshSkills() {
  const skills = $('#skills');
  if (!skills) return;
  const data = await api('/api/skills');
  const manifestName = data.manifest?.name ? `<p>${escapeHtml(data.manifest.name)}</p>` : '';
  skills.innerHTML = data.skills.map((s, index) => `
    <article class="card" style="--stagger: ${Math.min(index * 35, 280)}ms">
      <h3>${escapeHtml(s.name)} <span class="badge info">powerup</span></h3>
      ${manifestName}
      <pre>${escapeHtml(s.preview)}</pre>
    </article>`).join('') || `<article class="card"><h3>${t('skills.empty.title')}</h3><p>${t('skills.empty.body')}</p></article>`;
}

function jobRunDir(job) {
  const cmd = Array.isArray(job.command) ? job.command : [];
  const idx = cmd.indexOf('--run-dir');
  if (idx >= 0 && cmd[idx + 1]) return cmd[idx + 1];
  const tail = `${job.stdout_tail || ''}\n${job.stderr_tail || ''}`;
  const m = tail.match(/run_dir=([^\s]+)/);
  return m ? m[1] : '';
}

function statusBadge(status) {
  const tone = status === 'succeeded' ? 'success' : status === 'failed' ? 'failed' : status === 'running' ? 'info' : status ? 'warning' : '';
  return `<span class="badge ${tone}">${escapeHtml(statusLabel(status))}</span>`;
}

function latestByAction(jobs) {
  return jobs.reduce((acc, job) => {
    if (job?.action && !acc[job.action]) acc[job.action] = job;
    return acc;
  }, {});
}

function refreshWorkflowStates(jobs = []) {
  const latest = latestByAction(jobs);
  document.querySelectorAll('[data-action-status]').forEach((el) => {
    const actions = (el.dataset.actionStatus || '').split(',').map(s => s.trim()).filter(Boolean);
    const job = actions.map(action => latest[action]).find(Boolean);
    const status = job?.status || '';
    el.textContent = statusLabel(status);
    el.className = `badge ${status === 'succeeded' ? 'success' : status === 'failed' ? 'failed' : status === 'running' ? 'info' : 'warning'}`;
  });
}

function renderReviewSummary(jobs = []) {
  const summary = $('#reviewSummary');
  if (!summary) return;
  const counts = jobs.reduce((acc, j) => { acc[j.status] = (acc[j.status] || 0) + 1; return acc; }, {});
  const latest = jobs[0];
  summary.innerHTML = `
    <div class="summary-row"><span>${t('summary.total')}</span><strong>${jobs.length}</strong></div>
    <div class="summary-row"><span>${t('summary.running')}</span><strong>${counts.running || 0}</strong></div>
    <div class="summary-row"><span>${t('summary.failed')}</span><strong>${counts.failed || 0}</strong></div>
    <div class="summary-row"><span>${t('summary.latest')}</span><strong>${escapeHtml(latest ? friendlyAction(latest.action) : '—')}</strong></div>`;
}

function renderRecommendation() {
  const title = $('#nextActionTitle');
  const body = $('#nextActionBody');
  const button = $('#nextActionButton');
  if (!title || !body || !button) return;

  let key = 'recommend.next';
  let route = 'collect';
  const missingCriticalKey = currentHealth && (!currentHealth.has_xai_key || !currentHealth.has_tavily_key);
  const hasFailed = currentJobs.some(job => job.status === 'failed');
  const hasRunning = currentJobs.some(job => job.status === 'running');

  if (missingCriticalKey) { key = 'recommend.keys'; route = 'settings'; }
  else if (hasFailed) { key = 'recommend.failed'; route = 'review'; }
  else if (hasRunning) { key = 'recommend.running'; route = 'review'; }
  else if (!currentJobs.length) { key = 'recommend.first'; route = 'collect'; }

  title.textContent = t(`${key}.title`);
  body.textContent = t(`${key}.body`);
  button.textContent = t(`${key}.cta`);
  button.href = `#${route}`;
  button.dataset.routeLink = route;
}

async function refreshJobs() {
  const data = await api('/api/jobs');
  const jobs = data.jobs || [];
  currentJobs = jobs;
  const counts = jobs.reduce((acc, j) => { acc[j.status] = (acc[j.status] || 0) + 1; return acc; }, {});
  const latest = jobs[0];
  pulseIfChanged('#kpiJobs', `${counts.succeeded || 0}/${counts.running || 0}/${counts.failed || 0}`);
  pulseIfChanged('#kpiLatest', latest ? friendlyAction(latest.action) : 'none');
  pulseIfChanged('#jobsCount', `${jobs.length}`);
  refreshWorkflowStates(jobs);
  renderReviewSummary(jobs);
  renderRecommendation();

  const jobsEl = $('#jobs');
  if (!jobsEl) return;
  jobsEl.innerHTML = jobs.slice(0, 40).map((j, index) => {
    const runDir = jobRunDir(j);
    const output = [j.stdout_tail || '', j.stderr_tail || ''].filter(Boolean).join('\n\n');
    return `<article class="card job-card ${escapeHtml(j.status)}" style="--stagger: ${Math.min(index * 35, 280)}ms">
      <h3>${escapeHtml(friendlyAction(j.action))} ${statusBadge(j.status)}</h3>
      <p>${escapeHtml(j.id)}</p>
      <div class="job-meta">
        <span class="badge">${escapeHtml(j.created_at || '')}</span>
        ${j.returncode !== undefined && j.returncode !== null ? `<span class="badge">rc=${escapeHtml(j.returncode)}</span>` : ''}
        <span class="badge info">${escapeHtml(j.action || '')}</span>
      </div>
      ${runDir ? `<p><strong>${t('jobs.runDir')}:</strong> ${escapeHtml(runDir)}</p>` : ''}
      <details class="output-details"><summary>${t('jobs.output')}</summary><pre>${escapeHtml(output || t('jobs.noOutput'))}</pre></details>
    </article>`;
  }).join('') || `<article class="card"><h3>${t('jobs.empty.title')}</h3><p>${t('jobs.empty.body')}</p></article>`;
}

async function submitJob(action, payload, button) {
  const label = button?.textContent;
  if (button) {
    button.disabled = true;
    button.classList.add('is-loading');
    button.textContent = t('toast.submitting');
  }
  try {
    const data = await api('/api/jobs', { method: 'POST', body: JSON.stringify({ action, ...payload }) });
    showToast(t('toast.submitted', { action: friendlyAction(action), id: data.job?.id || 'queued' }));
    await refreshJobs();
    return data;
  } catch (err) {
    showToast(t('toast.failed', { action: friendlyAction(action), error: err.message }));
    throw err;
  } finally {
    if (button) {
      button.disabled = false;
      button.classList.remove('is-loading');
      button.textContent = label;
    }
  }
}

function bindJob(formId, action, payloadFactory = formData) {
  const form = $(formId);
  if (!form) return;
  form.addEventListener('submit', async (event) => {
    event.preventDefault();
    const button = form.querySelector('button');
    await submitJob(action, payloadFactory(form), button);
  });
}

bindJob('#expandForm', 'expand');
bindJob('#pipelineForm', 'intel_pipeline');
bindJob('#reportCatalogForm', 'report_catalog_build');
bindJob('#reportCatalogDiscoverForm', 'report_discover_catalog');
bindJob('#reportSourceDiscoverForm', 'report_discover_source');
bindJob('#reportManualImportForm', 'report_import_manual');
bindJob('#manualChannelPromptsForm', 'manual_channel_prompts');
bindJob('#manualChannelImportForm', 'import_manual_channel_results');
bindJob('#manualChannelApplyForm', 'apply_manual_channel_catalog');
bindJob('#manualChannelValidateForm', 'validate_discovery_records');
bindJob('#manualChannelExportForm', 'export_manual_channel_index');
bindJob('#reportTriageSourcesForm', 'report_triage_sources');
bindJob('#reportDiscoverForm', 'report_discover');
bindJob('#reportClusterForm', 'report_cluster');
bindJob('#reportEnrichForm', 'report_enrich');
bindJob('#reportApplyForm', 'report_apply');
bindJob('#discoverForm', 'discover');
bindJob('#batchForm', 'batch_submit');
bindJob('#tavilyVerifyForm', 'tavily_verify');
bindJob('#validateForm', 'validate', () => ({}));

$('#refreshJobs')?.addEventListener('click', refreshJobs);
$('#refreshSkills')?.addEventListener('click', refreshSkills);

const routeAliases = {
  pipeline: 'collect',
  reports: 'collect',
  techniques: 'collect',
  qa: 'review',
  jobs: 'review',
  channels: 'settings',
  powerups: 'settings',
};
const validRoutes = new Set([...document.querySelectorAll('[data-route]')].map(view => view.dataset.route));

function getRouteFromHash() {
  const raw = (location.hash || '#home').slice(1);
  if (validRoutes.has(raw)) return raw;
  return routeAliases[raw] || 'home';
}

function routeTo(route, options = {}) {
  route = routeAliases[route] || route;
  if (!validRoutes.has(route)) route = 'home';
  document.querySelectorAll('[data-route]').forEach(view => {
    view.classList.toggle('active', view.dataset.route === route);
  });
  document.querySelectorAll('[data-route-link]').forEach(link => {
    const active = link.dataset.routeLink === route;
    link.classList.toggle('active', active);
    if (active) link.setAttribute('aria-current', 'page');
    else link.removeAttribute('aria-current');
  });
  if (!options.replace && location.hash !== `#${route}`) history.pushState(null, '', `#${route}`);
  if (options.replace && location.hash !== `#${route}`) history.replaceState(null, '', `#${route}`);
  document.body.classList.remove('nav-open');
  $('#openNav')?.setAttribute('aria-expanded', 'false');
  const activeView = document.querySelector(`[data-route="${route}"]`);
  if (activeView && !options.silent) {
    window.scrollTo({ top: 0, behavior: prefersReducedMotion ? 'auto' : 'smooth' });
    revealActiveRoute(activeView);
    flashTarget(activeView.querySelector('.panel') || activeView);
  } else if (activeView) {
    revealActiveRoute(activeView);
  }
  updateScrollProgress();
}

function revealActiveRoute(activeView) {
  if (!activeView) return;
  activeView.querySelectorAll('.reveal-ready').forEach((el) => el.classList.add('is-visible'));
}

function bindRouteLinks() {
  document.addEventListener('click', (event) => {
    const link = event.target.closest('[data-route-link]');
    if (!link) return;
    const route = link.dataset.routeLink;
    if (!route || !validRoutes.has(route)) return;
    event.preventDefault();
    routeTo(route);
  });
  window.addEventListener('hashchange', () => routeTo(getRouteFromHash(), { replace: true, silent: true }));
  $('#openNav')?.addEventListener('click', () => {
    const next = !document.body.classList.contains('nav-open');
    document.body.classList.toggle('nav-open', next);
    $('#openNav')?.setAttribute('aria-expanded', String(next));
  });
}

function bindRevealObserver() {
  const cards = [...document.querySelectorAll('.workflow-card, .workflow-panel, .settings-card, .review-summary, .jobs-panel, .job-card, .skills .card')];
  if (prefersReducedMotion || !('IntersectionObserver' in window)) {
    cards.forEach(card => card.classList.add('is-visible'));
    return;
  }
  cards.forEach(card => card.classList.add('reveal-ready'));
  const observer = new IntersectionObserver((entries) => {
    for (const entry of entries) {
      if (entry.isIntersecting) {
        entry.target.classList.add('is-visible');
        observer.unobserve(entry.target);
      }
    }
  }, { threshold: 0.08, rootMargin: '0px 0px -40px 0px' });
  cards.forEach(card => observer.observe(card));
}

function initializeChrome() {
  document.body.classList.add('is-ready');
  applyI18n();
  routeTo(getRouteFromHash(), { replace: true });
  updateScrollProgress();
}

window.addEventListener('scroll', updateScrollProgress, { passive: true });
window.addEventListener('resize', updateScrollProgress);
bindLanguageSwitches();
bindRouteLinks();
bindRevealObserver();
if (document.readyState === 'loading') document.addEventListener('DOMContentLoaded', initializeChrome, { once: true });
else requestAnimationFrame(initializeChrome);

refreshHealth();
refreshSkills().catch(err => showToast(t('toast.skillsFailed', { error: err.message })));
refreshJobs().catch(err => showToast(t('toast.failed', { action: 'jobs', error: err.message })));
setInterval(refreshJobs, 5000);
setInterval(refreshHealth, 30000);

// ---------------------------------------------------------------------------
// #sources route — connector health table
// ---------------------------------------------------------------------------

async function refreshSources() {
  const tbody = document.querySelector('#sourcesTable tbody');
  const summary = document.getElementById('sourcesSummary');
  if (!tbody) return;
  summary.textContent = 'loading…';
  tbody.innerHTML = '';
  try {
    const r = await fetch('/api/sources');
    const data = await r.json();
    if (data.error) throw new Error(data.error);
    const rows = data.sources || [];
    summary.textContent = `${rows.length} sources · connectors registered: ${(data.connectors || []).join(', ')}`;
    rows.forEach(src => {
      const tr = document.createElement('tr');
      const m = src.last_metric || {};
      const counts = m.fetched ? `${m.fetched}/${m.persisted}/${m.deduped}` : '—';
      tr.innerHTML = `
        <td><code>${src.id}</code></td>
        <td>${src.name || ''}</td>
        <td>${src.connector || ''}</td>
        <td><code>${src.cadence || ''}</code></td>
        <td>${src.density || ''}</td>
        <td>${src.region || ''}</td>
        <td>${m.ts || '—'}</td>
        <td>${counts}</td>
        <td><button type="button" data-trigger="${src.id}" class="button-link compact">trigger</button></td>
      `;
      tbody.appendChild(tr);
    });
  } catch (e) {
    summary.textContent = `error: ${e.message}`;
  }
}

document.addEventListener('click', async (ev) => {
  const btn = ev.target.closest('[data-trigger]');
  if (!btn) return;
  ev.preventDefault();
  const sid = btn.dataset.trigger;
  btn.disabled = true;
  btn.textContent = '…';
  try {
    const r = await fetch(`/api/sources/${encodeURIComponent(sid)}/trigger`, { method: 'POST' });
    const data = await r.json();
    showToast(`queued ${sid}: job ${data.job?.id || '?'}`);
  } catch (e) {
    showToast(`trigger failed: ${e.message}`);
  } finally {
    btn.disabled = false;
    btn.textContent = 'trigger';
    setTimeout(refreshSources, 1500);
  }
});

document.getElementById('sourcesRefreshBtn')?.addEventListener('click', refreshSources);
document.getElementById('sourcesPullAllBtn')?.addEventListener('click', async () => {
  try {
    const r = await fetch('/api/jobs', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ action: 'connector_trigger', source_id: '__all__' })
    });
    const data = await r.json();
    showToast(`queued bulk pull: job ${data.job?.id || '?'}`);
  } catch (e) {
    showToast(`bulk pull failed: ${e.message}`);
  }
});

window.addEventListener('hashchange', () => {
  if (location.hash === '#sources') refreshSources();
});
if (location.hash === '#sources') refreshSources();
