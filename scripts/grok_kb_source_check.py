#!/usr/bin/env python3
from __future__ import annotations
import csv, random, socket, urllib.parse, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
LEDGER=ROOT/'data/grok_research/source_ledger.tsv'
OUT=ROOT/'data/grok_research/source_check_sample.tsv'
rows=[]
with LEDGER.open() as f:
    for r in csv.DictReader(f, delimiter='\t'):
        u=r.get('source_url','')
        if u.startswith('http'):
            rows.append(r)
random.seed(20260505)
sample=random.sample(rows, min(30,len(rows)))
results=[]
for r in sample:
    u=r['source_url']
    host=urllib.parse.urlparse(u).hostname or ''
    dns='fail'; http='skip'; note=''
    try:
        socket.gethostbyname(host); dns='ok'
    except Exception as e:
        note=str(e)[:80]
    if dns=='ok':
        try:
            req=urllib.request.Request(u, method='HEAD', headers={'User-Agent':'Mozilla/5.0 bug-bounty-kb-source-check'})
            with urllib.request.urlopen(req, timeout=8) as resp:
                http=str(resp.status)
        except Exception as e:
            http='blocked_or_error'; note=str(e)[:120]
    results.append([r['id'],r['type'],r['title'],host,dns,http,u,note])
OUT.parent.mkdir(parents=True, exist_ok=True)
with OUT.open('w', newline='') as f:
    w=csv.writer(f, delimiter='\t')
    w.writerow(['id','type','title','host','dns','http','url','note'])
    w.writerows(results)
print('sample',len(results),'dns_ok',sum(1 for x in results if x[4]=='ok'),'http_2xx_3xx',sum(1 for x in results if x[5].isdigit() and int(x[5])<400),'out',OUT)
