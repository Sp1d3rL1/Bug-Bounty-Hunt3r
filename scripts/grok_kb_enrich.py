#!/usr/bin/env python3
"""Enrich first-pass Grok cards into more useful Obsidian knowledge notes.

This does not invent exploit payloads. It expands Grok-collected one-line tricks into
structured, authorized/lab-only research checklists and adds derived technique cards
for case records so cases remain link-only while techniques become searchable.
"""
from __future__ import annotations
import csv, re, unicodedata
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
KB = ROOT / 'docs' / 'intelligence_kb'
LEDGER = ROOT / 'data' / 'grok_research' / 'source_ledger.tsv'

TECH_BASES = {
    'new_method': KB/'techniques/new_2024_2026',
    'evergreen': KB/'techniques/evergreen_new_context',
    'trick': KB/'techniques/niche_tricks',
}

CASE_BASES = [KB/'cases/public_reports', KB/'cases/x_threads', KB/'cases/researcher_writeups']

def slugify(s: str, maxlen=88):
    s = unicodedata.normalize('NFKD', s).encode('ascii','ignore').decode('ascii')
    s = re.sub(r'[^a-zA-Z0-9]+','-',s.lower()).strip('-')
    return (s[:maxlen].strip('-') or 'untitled')

def classify_category(row):
    blob = ' '.join([row.get('vuln_class',''), row.get('title',''), row.get('one_line_trick',''), row.get('raw_file','')]).lower()
    if 'topic_11' in blob or 'classic' in blob or 'evergreen' in blob or 'old bug' in blob:
        return 'evergreen'
    if 'topic_12' in blob or 'trick' in blob or 'bypass' in blob or 'til' in blob or 'weird' in blob:
        return 'trick'
    return 'new_method'

def risk(row):
    blob=' '.join([row.get('vuln_class',''),row.get('title',''),row.get('one_line_trick','')]).lower()
    if any(x in blob for x in ['payment','billing','refund','coupon','subscription','race','webhook','token','jwt','oauth','sso','saml','tenant','idor','bola','prompt injection','tool calling','request smuggling']):
        return 'high'
    if any(x in blob for x in ['xss','cache','cloud','secret','ssrf','graphql','postmessage','dom']):
        return 'medium'
    return 'low'

def targets(row):
    raw=row.get('target_type','') or 'Web/API'
    parts=[p.strip() for p in re.split(r'[,/;]+', raw) if p.strip()]
    return parts or ['Web','API']

def yaml_list(vals):
    return '\n'.join(f'  - {v}' for v in vals)

def archetype_sections(row):
    vc = row.get('vuln_class','').lower()
    trick = row.get('one_line_trick','')
    useful = row.get('why_useful','')
    title = row.get('title','')
    target = row.get('target_type','')

    common = {
        'why': [
            '现代 Web/API 产品通常由多个前端、移动端、后台任务和第三方集成共同访问同一资源，容易出现某一路径缺少服务端校验。',
            'Bug Bounty 中高价值点通常不是单一 payload，而是“业务前提 + 可控对象 + 服务端信任边界 + 可证明影响”的组合。',
        ],
        'manual': [
            '确认 scope、禁止项、速率限制与是否允许该功能测试。',
            '准备至少两个自有测试账号；多租户场景准备两个 organization/workspace。',
            '先完整走通正常业务流，记录对象 ID、角色、状态、token、请求路径。',
            '只替换一个变量或一步状态，观察服务端响应和后续副作用。',
            '用最小必要数据证明影响；不读取、不导出第三方真实数据。',
        ],
        'automation': [
            '可自动化收集 endpoint、参数、对象 ID 形态、历史 URL、JS 中的隐藏 API。',
            '可自动化做“候选点标记”和“差异对比”，但越权、支付、账号状态影响必须手工确认。',
        ],
    }
    extra = []
    if any(x in vc for x in ['idor','bola','access']):
        extra = [
            '建立 A/B 双账号或双租户矩阵，分别收集 list/detail/export/update/delete 请求。',
            '测试 path、query、JSON body、header、GraphQL variables、批处理任务中的对象引用。',
            '重点看“读接口已修，写接口/导出接口/异步任务/移动端接口未修”的差异。',
        ]
    elif any(x in vc for x in ['oauth','sso','saml','jwt','magic']):
        extra = [
            '绘制登录、注册、账号绑定、邀请、SSO 回调、magic link 的完整状态机。',
            '重点确认 redirect/state/nonce/audience/issuer/email claim/account linking 的服务端校验。',
            '使用自有账号验证跨账号绑定或会话混淆，避免触达第三方账户。',
        ]
    elif 'graphql' in vc:
        extra = [
            '收集 schema、operation name、variables、node/id 解析路径和批量查询能力。',
            '对同一对象分别测试 query、mutation、nested resolver、batching、alias 场景。',
            '关注“列表受限但 node 直取未校验”“mutation 校验弱于 query”的差异。',
        ]
    elif any(x in vc for x in ['payment','billing','coupon','refund','subscription','webhook']):
        extra = [
            '只在明确允许支付测试的项目中使用 sandbox/test card/0 元或小额测试。',
            '绘制订单、折扣、发票、订阅、退款、webhook、权益发放的状态流转。',
            '关注客户端价格、重复 webhook、并发取消/退款、跨租户 invoice/receipt 访问。',
        ]
    elif any(x in vc for x in ['postmessage','dom','cspt','xss','prototype','dompurify']):
        extra = [
            '枚举 message listeners、URL fragment/query sink、client-side routing、sanitizer 配置和 trusted origins。',
            '优先在本地或授权测试页面复现，真实项目只证明可控 sink 与安全影响。',
            '关注 OAuth callback、embed/widget、support chat、docs preview 等富客户端功能。',
        ]
    elif any(x in vc for x in ['cache','smuggling','http2','http3']):
        extra = [
            '先识别 CDN、反向代理、cache key、vary header、normalization 和前后端协议差异。',
            '只做低频、无破坏的 cache key/响应差异验证；避免影响真实用户缓存。',
            '优先使用 PortSwigger lab 复现具体变体，再迁移为授权环境的最小化检测。',
        ]
    elif any(x in vc for x in ['cloud','github','ci','artifact','secret','bucket']):
        extra = [
            '使用授权域名、组织名、公开仓库、证书、ASN、存储命名规律建立资产图。',
            '对公开暴露只证明可访问性和最小元数据；不要下载大批量文件或读取敏感内容。',
            '把 findings 关联回业务资产、权限边界或可利用路径，避免只报低价值暴露。',
        ]
    elif any(x in vc for x in ['ai','llm','prompt','tool']):
        extra = [
            '识别模型可访问的数据源、工具、插件、检索索引、用户/租户边界和输出通道。',
            '在自有数据/测试空间中验证 prompt injection、tool-call 越权、跨租户检索泄露。',
            '报告时强调信任边界、数据隔离和工具权限，而非“越狱”本身。',
        ]
    else:
        extra = [
            '把该技巧拆成：入口发现、可控输入、信任边界、影响证明四段。',
            '先找 lab/本地靶场复现，再映射到授权目标。',
        ]
    return common, extra

def detailed_tech_markdown(row, category, derived=False):
    common, extra = archetype_sections(row)
    title = row['title'] if not derived else f"Derived technique from case: {row['title']}"
    vc=row.get('vuln_class','')
    source=row.get('source_url','')
    body=f"""---
type: technique
category: {category}
derived_from_case: {str(derived).lower()}
vuln_class: {vc}
source_url: {source}
source_author: {row.get('author','')}
source_date: {row.get('date','')}
collected_at: {date.today().isoformat()}
freshness: {('2026' if '2026' in row.get('date','') else '2025' if '2025' in row.get('date','') else '2024' if '2024' in row.get('date','') else 'evergreen')}
confidence: {row.get('confidence','medium') or 'medium'}
risk_level: {risk(row)}
target_types:
{yaml_list(targets(row))}
---

# {title}

## 核心思路

{row.get('one_line_trick','')}

## 前置条件

- 目标明确在授权 Bug Bounty scope 内，且 rules 未禁止该测试类别。
- 存在与 `{vc}` 相关的业务对象、接口、前端入口或集成链路。
- 使用自有测试账号、测试租户、sandbox 或平台允许的测试数据。
- 如果涉及支付/账号/隐私/生产状态变化，必须先确认项目允许并采用最小影响验证。

## 完整技法细节

- 来源要点：{row.get('why_useful','')}
- 适用场景：{row.get('target_type','')}
- 技法拆解：先找到可控入口，再确认服务端信任边界，最后用最小化证据证明影响。
"""
    for x in extra:
        body += f"- {x}\n"
    body += "\n## 适用目标画像\n\n"
    for t in targets(row): body += f"- {t}\n"
    body += "\n## 为什么有效\n\n"
    for x in common['why']: body += f"- {x}\n"
    body += f"- 本条技巧的价值点：{row.get('why_useful','')}\n"
    body += "\n## 手工验证流程（授权 / Lab only）\n\n"
    for i,x in enumerate(common['manual']+extra,1): body += f"{i}. {x}\n"
    body += "\n## 可自动化部分\n\n"
    for x in common['automation']: body += f"- {x}\n"
    body += "\n## 误报/失败条件\n\n- 只有客户端表现异常，没有服务端影响。\n- 只能影响当前自有账号，无法证明跨权限、跨租户、财务、数据或流程影响。\n- 目标业务前提不存在，或服务端已做完整对象归属/状态校验。\n- 来源帖子/案例缺少可验证链接时，需降级为 review_queue 并二次确认。\n\n## 授权边界\n\n仅用于授权项目、靶场或自有环境。禁止无授权扫描、凭证滥用、爆破、DoS、真实支付损害、读取第三方真实隐私数据或绕过平台规则。\n\n## 报告 impact 角度\n\n- 说明攻击者前提、受影响对象、服务端缺失的校验，以及可造成的数据访问、权限提升、财务损失、业务流程绕过或租户隔离破坏。\n- 证据只保留最小必要截图/请求响应，并打码 token、cookie、PII、支付信息。\n\n## 相关案例链接\n\n"
    if source: body += f"- {source}\n"
    else: body += "- TODO: 二次确认来源链接。\n"
    return body

def detailed_case_markdown(row):
    return f"""---
type: case
vuln_class: {row.get('vuln_class','')}
source_url: {row.get('source_url','')}
source_author: {row.get('author','')}
source_date: {row.get('date','')}
collected_at: {date.today().isoformat()}
freshness: {('2026' if '2026' in row.get('date','') else '2025' if '2025' in row.get('date','') else '2024' if '2024' in row.get('date','') else 'evergreen')}
confidence: {row.get('confidence','medium') or 'medium'}
target_types:
{yaml_list(targets(row))}
---

# {row.get('title','Untitled')}

## 链接

{row.get('source_url','')}

## 漏洞类型

{row.get('vuln_class','')}

## 目标业务场景

{row.get('target_type','')}

## 关键利用链摘要

{row.get('one_line_trick','')}

## 可迁移技法

{row.get('why_useful','')}

## 为什么值得收藏

- 该案例可作为 `{row.get('vuln_class','')}` 的业务前提、影响证明和报告写法参考。
- 只在本地保存链接和摘要；完整复现以原文、靶场或明确授权环境为准。
- 迁移时优先提取“对象/状态/权限边界”而不是照搬请求。

## 安全边界

案例中涉及的目标、账号、数据均不可在未授权环境复现；真实项目中只使用自有测试账号和最小必要证据。
"""

def load_rows():
    with LEDGER.open() as f:
        return list(csv.DictReader(f, delimiter='\t'))

def case_path_for(row):
    blob=(row.get('source_url','')+' '+row.get('title','')).lower()
    if any(x in blob for x in ['hackerone','bugcrowd','intigriti','yeswehack']): base=KB/'cases/public_reports'
    elif any(x in blob for x in ['x.com','twitter.com']): base=KB/'cases/x_threads'
    else: base=KB/'cases/researcher_writeups'
    return base/(slugify(f"{row.get('id','')}-{row.get('title','')}")+'.md')

rows=load_rows()
# Re-enrich existing technique and case cards, then derive searchable technique cards from cases.
for row in rows:
    typ=row.get('type','').lower()
    if typ=='technique':
        cat=classify_category(row)
        p=TECH_BASES[cat]/(slugify(f"{row.get('id','')}-{row.get('title','')}")+'.md')
        p.write_text(detailed_tech_markdown(row, cat, False), encoding='utf-8')
    elif typ=='case':
        p=case_path_for(row)
        p.write_text(detailed_case_markdown(row), encoding='utf-8')
        # Derived technique card keeps cases link-only while making technique knowledge searchable.
        cat=classify_category(row)
        dp=TECH_BASES[cat]/(slugify(f"case-derived-{row.get('id','')}-{row.get('title','')}")+'.md')
        dp.write_text(detailed_tech_markdown(row, cat, True), encoding='utf-8')
    elif typ=='resource':
        rp=KB/'review_queue'/(slugify(f"resource-{row.get('id','')}-{row.get('title','')}")+'.md')
        rp.write_text(f"# {row.get('title','')}\n\n- Type: resource\n- Author: {row.get('author','')}\n- Date: {row.get('date','')}\n- Source: {row.get('source_url','')}\n- Class: {row.get('vuln_class','')}\n- Why useful: {row.get('why_useful','')}\n- Confidence: {row.get('confidence','')}\n\n## Next action\n\n二次确认是否应加入 `resources/` 或转换为技法卡。\n", encoding='utf-8')
print('enriched rows', len(rows))
