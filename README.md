# Capconnex Ghost 备份与部署

## 目录

- `backups/<timestamp>/` — 每次备份
- `content/` — 最新备份快捷方式
- `backup.sh` — 备份脚本 (Oracle → GitHub)
- `deploy.sh` — 部署脚本 (GitHub → Oracle)

## 使用

```bash
# 备份
cd /root/capconnex && bash backup.sh

# 部署最新
cd /root/capconnex && bash deploy.sh

# 部署指定版本
cd /root/capconnex && bash deploy.sh 2026-05-17_14-30-00
```
