#!/usr/bin/env python3
"""Send non-sensitive recon diff summaries to Discord or Telegram.

Only send files you have reviewed. Do not send tokens, cookies, raw responses,
private reports, or personal data.
"""
from __future__ import annotations
import argparse, json, os, urllib.request
from pathlib import Path

MAX_CHARS = 3500

def post_json(url: str, payload: dict):
    data = json.dumps(payload).encode()
    req = urllib.request.Request(url, data=data, headers={'Content-Type': 'application/json'})
    with urllib.request.urlopen(req, timeout=20) as r:
        return r.status

def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--title', required=True)
    ap.add_argument('--file', required=True)
    args = ap.parse_args()
    text = Path(args.file).read_text(errors='ignore')[:MAX_CHARS]
    discord = os.getenv('DISCORD_WEBHOOK_URL')
    tg_token = os.getenv('TELEGRAM_BOT_TOKEN')
    tg_chat = os.getenv('TELEGRAM_CHAT_ID')
    message = f"**{args.title}**\n```text\n{text}\n```"
    if discord:
        post_json(discord, {'content': message})
        print('sent discord')
    elif tg_token and tg_chat:
        url = f'https://api.telegram.org/bot{tg_token}/sendMessage'
        post_json(url, {'chat_id': tg_chat, 'text': f'{args.title}\n\n{text}', 'disable_web_page_preview': True})
        print('sent telegram')
    else:
        print('no webhook env configured')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
