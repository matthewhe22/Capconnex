#!/bin/bash
set -e

REPO_DIR="/root/capconnex"
TIMESTAMP="${1:-latest}"

if [ "$TIMESTAMP" = "latest" ]; then
    BACKUP_DIR="$REPO_DIR/content"
else
    BACKUP_DIR="$REPO_DIR/backups/$TIMESTAMP"
fi

echo "🔄 部署 Ghost 内容..."
echo "   来源: $BACKUP_DIR"

cd "$REPO_DIR"
git pull origin main 2>&1 || true

echo "📦 恢复数据库..."
docker cp "$BACKUP_DIR/ghost-db.bin" ghost-capconnex:/var/lib/ghost/content/data/ghost.db

echo "📦 恢复配置..."
docker cp "$BACKUP_DIR/config.json" ghost-capconnex:/var/lib/ghost/config.production.json

echo "📦 恢复图片..."
docker exec ghost-capconnex sh -c "rm -rf /var/lib/ghost/content/images/*"
docker cp "$BACKUP_DIR/images/." ghost-capconnex:/var/lib/ghost/content/images/

echo "📦 恢复主题..."
docker exec ghost-capconnex sh -c "rm -rf /var/lib/ghost/content/themes/*"
docker cp "$BACKUP_DIR/themes/." ghost-capconnex:/var/lib/ghost/content/themes/

docker exec ghost-capconnex sh -c "chown -R node:node /var/lib/ghost/content"

echo "🔄 重启 Ghost..."
docker restart ghost-capconnex

sleep 15
curl -sL -o /dev/null -w "状态: %{http_code}\n" https://capconnex.com.au/
echo "✅ 部署完成!"
