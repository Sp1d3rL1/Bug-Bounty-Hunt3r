#!/usr/bin/env python3
"""Apply Grok DOM-snapshot expansions by mapping answer blocks to batch prompt CARD_DEST order.

Use when Grok strips HTML comments from markdown output in the browser DOM snapshot.
This appends/replaces a 'Grok Expert 扩展补充' section in each target card.
"""
from __future__ import annotations
import argparse, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]
START='<!-- GROK_EXPANSION_START -->'
END='<!-- GROK_EXPANSION_END -->'

def read_prompt_dests(prompt_path: Path):
    text=prompt_path.read_text(errors='ignore')
    return re.findall(r'^CARD_DEST:\s*(.+)$', text, flags=re.M)

def clean_quoted(s: str) -> str:
    s=s.strip()
    if s.startswith('"') and s.endswith('"'):
        s=s[1:-1]
    s=s.replace('\\"','"')
    return s.strip()

def sanitize_text(text: str) -> str:
    """Keep authorized/lab context explicit and avoid turning cards into abuse playbooks."""
    replacements = [
        (r'Direct data exfil/overwrite', '授权范围内的数据暴露/覆盖风险验证'),
        (r'data exfiltration', '数据暴露风险验证（不导出真实敏感数据）'),
        (r'exfil(?:trate|tration)?', '验证暴露风险（不导出真实敏感数据）'),
        (r'真实数据下载', '真实敏感数据下载'),
        (r'attacker-controlled', 'tester-controlled'),
        (r'attacker GH repo', 'tester-controlled GitHub repository in Lab/authorized scope'),
        (r'攻击者控制', '测试者控制'),
        (r'Full AWS account control', '云权限边界影响验证'),
        (r'full account control', '权限边界影响验证'),
        (r'账户接管（ATO）', '账号状态影响验证（ATO 风险）'),
        (r'实现数据“外传”演示', '实现出站复制风险演示'),
        (r'payload', '测试载荷'),
        (r'枚举支付网关测试卡凭证', '使用项目允许的测试卡/沙箱凭证组合'),
        (r'并发申请同一优惠码（使用Turbo Intruder）', '在 Lab 中低并发验证同一优惠码的状态竞争风险'),
        (r'Turbo Intruder', '低速率授权并发验证工具'),
        (r'token leak', 'token exposure risk'),
        (r'WAF 绕过能力', 'WAF 规则差异与暴露识别能力'),
        (r'WAF bypass', 'WAF rule-difference validation'),
        (r'bulk data theft', 'bulk data exposure risk'),
        (r'production DoS', 'production-impact recursion test'),
        (r'victim tenant ID', '另一测试租户ID'),
        (r'受害者tenant ID', '另一测试租户ID'),
        (r'受害者组织数据', '另一测试租户的合成数据'),
        (r'攻击者可', '未授权第三方可能'),
    ]
    for pat, repl in replacements:
        text=re.sub(pat, repl, text, flags=re.I)
    return text

def dom_to_markdown(block: str) -> str:
    out=[]
    pending_link_text=None
    in_code=False
    # Some Grok DOM snapshots render the answer as a Markdown code block:
    # every actual Markdown line appears as "- generic: ...". In that shape,
    # preserve semantic Markdown lines but skip card markers/frontmatter.
    generic_markdown = '<!--CARD:' in block or re.search(r'- generic:\s*"?#\s*核心思路', block)
    generic_content_started = not generic_markdown

    def close_code():
        nonlocal in_code
        if in_code:
            out.append('```')
            in_code=False

    for raw in block.splitlines():
        line=raw.strip()
        if not line or 'region ' in line or 'alert' in line:
            continue
        if re.search(r'- button "(?:复制|创建共享链接|赞|踩|Regenerate|朗读|编辑|自动换行)"', line):
            continue

        if re.match(r'- code:', line):
            if not in_code:
                out.append('```text')
                in_code=True
            continue

        mg=re.search(r'- generic: (.*)$', line)
        if mg:
            val=clean_quoted(mg.group(1))
            if generic_markdown:
                if val.startswith('<!--CARD:') or val.startswith('<!--ENDCARD'):
                    continue
                if val == '---' and not generic_content_started:
                    continue
                if not generic_content_started:
                    if re.match(r'^(?:#\s+)?核心思路$', val):
                        generic_content_started = True
                    elif val.startswith('# '):
                        generic_content_started = True
                    else:
                        # YAML/frontmatter metadata already exists in the destination card.
                        continue
                if val and val not in {'text', 'Markdown'}:
                    out.append(val)
                continue
            if in_code and val and val not in {'text'}:
                out.append(val)
            # Other generic nodes are usually UI/sidebar noise in DOM snapshots.
            continue

        # Leaving a code block when the next semantic node starts.
        close_code()

        mh=re.search(r'- heading "(.*?)" \[level=(\d+)\]', line)
        if mh:
            title=mh.group(1).replace('\\"', '"')
            # The level-2 heading often contains Grok's whole metadata blob; existing card already has it.
            if re.match(r'id:\s*"?\d+"?\s+title:', title) or (
                title.startswith('title: ') and ('vuln_class:' in title or 'source_url:' in title)
            ):
                continue
            out.append('\n' + '#' * int(mh.group(2)) + ' ' + title)
            continue

        mt=re.search(r'- text: (.*)$', line)
        if mt:
            txt=clean_quoted(mt.group(1)).replace('\\"', '"')
            if txt and not re.match(r'id:\s*"?\d+"?\s+title:', txt) and not (
                txt.startswith('title: ') and ('vuln_class:' in txt or 'source_url:' in txt)
            ):
                out.append(txt)
            continue

        ms=re.search(r'- strong: (.*)$', line)
        if ms:
            txt=clean_quoted(ms.group(1))
            if txt:
                out.append(f'- **{txt}**')
            continue

        mp=re.search(r'- paragraph: (.*)$', line)
        if mp:
            txt=clean_quoted(mp.group(1))
            if txt: out.append(txt)
            continue

        ml=re.search(r'- listitem: (.*)$', line)
        if ml:
            txt=clean_quoted(ml.group(1))
            out.append(f'- {txt}')
            continue

        mlink=re.search(r'- link "(.*?)":', line)
        if mlink:
            pending_link_text=mlink.group(1)
            continue
        murl=re.search(r'- /url: (.*)$', line)
        if murl and pending_link_text:
            url=murl.group(1).strip()
            out.append(f'- [{pending_link_text}]({url})')
            pending_link_text=None
            continue
    close_code()
    # normalize blank lines and remove empty code fences
    text='\n'.join(out)
    text=re.sub(r'```text\n```', '', text)
    text=re.sub(r'\n{3,}', '\n\n', text)
    return sanitize_text(text.strip())

def extract_blocks(dom_text: str):
    # Only answer blocks: Grok output usually starts cards with a heading/text node containing id/title metadata.
    start_re=re.compile(
        r"- generic:\s*\"?<!--CARD:\s*|"
        r"(?:- ')?heading \"id:\s*(?:\\\")?\d+(?:\\\")?\s+title:|"
        r"(?:- ')?heading \"title:\s+.*?(?:vuln_class:|source_url:)|"
        r"- text: \"id:\s*(?:\\\")?\d+(?:\\\")?\s+title:|"
        r"- text: \"title:\s+.*?(?:vuln_class:|source_url:)|"
        r"^id:\s*\d+\s+title:",
        re.M,
    )
    starts=[m.start() for m in start_re.finditer(dom_text)]
    blocks=[]
    for i,st in enumerate(starts):
        en=starts[i+1] if i+1 < len(starts) else len(dom_text)
        block=dom_text[st:en]
        # stop after the answer card when Grok UI action buttons begin
        cut=re.search(r'\n\s*- button "复制"|\n\s*- button "创建共享链接"', block)
        if cut:
            block=block[:cut.start()]
        md=dom_to_markdown(block)
        if len(md) > 200 and '核心思路' in md:
            blocks.append(md)
    return blocks

def apply_one(prompt_path: Path, output_path: Path, dry_run=False):
    dests=read_prompt_dests(prompt_path)
    dom=output_path.read_text(errors='ignore')
    blocks=extract_blocks(dom)
    n=min(len(dests), len(blocks))
    print(f'{output_path.name}: dests={len(dests)} blocks={len(blocks)} apply={n}')
    for dest,block in zip(dests[:n], blocks[:n]):
        # prompt uses absolute paths; support both abs and repo-relative
        p=Path(dest)
        if not p.is_absolute(): p=ROOT/dest
        if not str(p.resolve()).startswith(str(ROOT.resolve())):
            print(f' skip outside root: {p}')
            continue
        old=p.read_text(errors='ignore') if p.exists() else ''
        section=f"\n\n{START}\n\n## Grok Expert 扩展补充\n\n{block}\n\n{END}\n"
        if START in old and END in old:
            new=re.sub(re.escape(START)+r'[\s\S]*?'+re.escape(END), section.strip(), old)
        else:
            new=old.rstrip()+section
        if dry_run:
            print(f' would update {p}')
        else:
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_text(new, encoding='utf-8')
    return n

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--prompt-dir', default='data/grok_research/prompts/2026-05-05/expansion_batches')
    ap.add_argument('--expanded-dir', default='data/grok_research/expanded/2026-05-05')
    ap.add_argument('--batch', help='e.g. 001')
    ap.add_argument('--dry-run', action='store_true')
    args=ap.parse_args()
    prompt_dir=ROOT/args.prompt_dir
    expanded_dir=ROOT/args.expanded_dir
    total=0
    outs=sorted(expanded_dir.glob('batch_*.md'))
    if args.batch:
        outs=[expanded_dir/f'batch_{args.batch}.md']
    for out in outs:
        m=re.search(r'batch_(\d+)\.md$', out.name)
        if not m or not out.exists(): continue
        prompt=prompt_dir/f'batch_{m.group(1)}.prompt.md'
        if prompt.exists():
            total += apply_one(prompt,out,args.dry_run)
    print(f'total applied {total}')
if __name__=='__main__':
    main()
