#!/bin/bash
set -e

REPO_DIR="$HOME/capconnex"
TIMESTAMP="${1:-latest}"

if [ "$TIMESTAMP" = "latest" ]; then
    BACKUP_DIR="$REPO_DIR/content"
else
    BACKUP_DIR="$REPO_DIR/backups/$TIMESTAMP"
fi

echo "🔄 部署 Ghost 内容... 来源: $BACKUP_DIR"
cd "$REPO_DIR" && git pull origin main 2>&1 || true

docker cp "$BACKUP_DIR/ghost-db.bin" ghost-capconnex:/var/lib/ghost/content/data/ghost.db
docker cp "$BACKUP_DIR/config.json" ghost-capconnex:/var/lib/ghost/config.production.json
docker exec ghost-capconnex sh -c "rm -rf /var/lib/ghost/content/images/*"
docker cp "$BACKUP_DIR/images/." ghost-capconnex:/var/lib/ghost/content/images/
docker exec ghost-capconnex sh -c "rm -rf /var/lib/ghost/content/themes/*"
docker cp "$BACKUP_DIR/themes/." ghost-capconnex:/var/lib/ghost/content/themes/
docker exec ghost-capconnex sh -c "chown -R node:node /var/lib/ghost/content"

docker restart ghost-capconnex
sleep 15
echo "部署完成! $(curl -sL -o /dev/null -w '%{http_code}' https://capconnex.com.au/)"
