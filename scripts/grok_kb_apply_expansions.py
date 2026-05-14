#!/usr/bin/env python3
"""Apply manually saved Grok expansion outputs to Obsidian KB cards.

Expected expanded output format:
<!--CARD: docs/intelligence_kb/.../file.md -->
---
frontmatter...
---
# Title
...
<!--ENDCARD-->
"""
from __future__ import annotations
import argparse, re
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

def reconstruct_generic_code(text: str) -> str:
    """Reconstruct markdown code blocks from browser DOM snapshot generic lines."""
    lines=[]
    for raw in text.splitlines():
        line=raw.strip()
        m=re.match(r'- generic: (.*)$', line)
        if not m:
            continue
        val=m.group(1).strip()
        if val.startswith('"') and val.endswith('"'):
            val=val[1:-1].replace('\\"','"')
        lines.append(val)
    return '\n'.join(lines)

def sanitize_markdown(text: str) -> str:
    """Keep cards useful for authorized/lab work while removing unsafe operational abuse details."""
    replacements = [
        (r'cat `?\.git/config`?', '读取自有 lab 中的合成标记文件'),
        (r'curl 到 attacker 服务器', '记录到自有 lab 日志端点'),
        (r'curl to attacker server', 'record to an owned lab logging endpoint'),
        (r'exfil(?:trate|tration)?', '验证暴露风险（不导出真实敏感数据）'),
        (r'secret exfil', 'secret 暴露风险验证（仅合成 secret）'),
        (r'恶意 payload', '无害测试 payload'),
        (r'malicious payload', 'benign lab payload'),
        (r'恶意 artifact', '无害测试 artifact'),
        (r'malicious artifact', 'benign lab artifact'),
        (r'后门', '持久化风险标记'),
        (r'brute passwords', '在 lab 中验证速率限制缺陷'),
        (r'brute force login/OTP', '授权 lab 中的认证速率限制验证'),
        (r'大规模 fuzz', '低速率、授权范围内的组合测试'),
    ]
    for pat, repl in replacements:
        text=re.sub(pat, repl, text, flags=re.I)
    # Normalize Grok frontmatter to KB schema.
    if text.lstrip().startswith('---'):
        if 'source_author:' not in text or 'source_date:' not in text:
            m = re.search(r'^author_date:\s*(.*?)\s*/\s*(.*?)$', text, flags=re.M)
            if m:
                if 'source_author:' not in text:
                    text = text.replace(m.group(0), f"source_author: {m.group(1).strip()}\nsource_date: {m.group(2).strip()}", 1)
                else:
                    text = text.replace(m.group(0), f"source_date: {m.group(2).strip()}", 1)
        if 'collected_at:' not in text:
            text = text.replace('---\n', '---\ncollected_at: 2026-05-05\n', 1)
        if 'risk_level:' not in text:
            risk = 'high' if re.search(r'credential|token|secret|payment|billing|rce|ci/cd|github actions|oauth|sso|jwt|idor|bola|access control', text, flags=re.I) else 'medium'
            text = text.replace('---\n', f'---\nrisk_level: {risk}\n', 1)
        if 'target_types:' not in text:
            mt = re.search(r'^target_type:\s*(.*?)$', text, flags=re.M)
            if mt:
                text = text.replace(mt.group(0), f"target_types:\n  - {mt.group(1).strip()}", 1)
    guard='\n\n> 安全边界：本卡仅用于授权项目、靶场或自有环境；任何涉及凭证、CI/CD、支付、账号状态或真实用户数据的验证都必须使用合成数据和最小影响证明。\n'
    if '安全边界' not in text:
        text += guard
    return text

CARD_RE = re.compile(r'<!--CARD:\s*(.*?)\s*-->(.*?)(?=<!--CARD:|\Z)', re.S)

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--expanded-dir', required=True)
    ap.add_argument('--dry-run', action='store_true')
    args=ap.parse_args()
    exp=Path(args.expanded_dir)
    count=0
    for f in sorted(exp.glob('*.md')):
        text=f.read_text(errors='ignore')
        if '- generic:' in text:
            text = reconstruct_generic_code(text)
        elif '<!--CARD:' not in text:
            text = reconstruct_generic_code(text)
        for rel, body in CARD_RE.findall(text):
            body=body.replace('<!--ENDCARD-->','').strip()+"\n"
            body=sanitize_markdown(body)
            # tolerate accidental code fences around output
            body=re.sub(r'^```(?:markdown|md)?\s*\n','',body)
            body=re.sub(r'\n```\s*$','\n',body)
            path=(ROOT/rel.strip()).resolve()
            if not str(path).startswith(str(ROOT.resolve())):
                print(f'skip outside root: {rel}')
                continue
            if args.dry_run:
                print(f'would write {path} ({len(body)} bytes)')
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(body, encoding='utf-8')
                print(f'wrote {path}')
            count+=1
    print(f'applied {count} cards')
if __name__ == '__main__':
    main()
