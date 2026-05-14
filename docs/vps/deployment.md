# VPS 部署说明

## 推荐目录

```bash
mkdir -p ~/bbos/{configs,data,logs,tools}
```

## 安装工具

先阅读 `scripts/install_vps_tools.sh`，确认来源后再执行。该脚本不会自动运行 recon。

## 运行

```bash
python3 scripts/recon_pipeline.py --config config/scope.example.json --dry-run
python3 scripts/recon_pipeline.py --config config/scope.myprogram.json
```

## Cron 示例

```cron
# 每天凌晨 03:20 跑一次某授权项目
20 3 * * * cd /path/to/Bug\ Bounty\ Hunting && python3 scripts/recon_pipeline.py --config config/scope.myprogram.json >> logs/cron.myprogram.log 2>&1
```

## 通知环境变量

```bash
export DISCORD_WEBHOOK_URL='https://discord.com/api/webhooks/...'
# 或
export TELEGRAM_BOT_TOKEN='123:abc'
export TELEGRAM_CHAT_ID='123456789'
```

通知只发送 diff 摘要，不发送敏感响应体。
