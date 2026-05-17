#!/bin/bash
set -e

REPO_DIR="$HOME/capconnex"
TIMESTAMP=$(date +%Y-%m-%d_%H-%M-%S)

echo "🔄 开始备份 Ghost 内容..."
mkdir -p /tmp/ghost-export

echo "📦 导出数据库..."
docker cp ghost-capconnex:/var/lib/ghost/content/data/ghost.db /tmp/ghost-export/ghost-db.bin

echo "📦 导出配置..."
docker cp ghost-capconnex:/var/lib/ghost/config.production.json /tmp/ghost-export/config.json

echo "📦 导出图片..."
docker cp ghost-capconnex:/var/lib/ghost/content/images /tmp/ghost-export/images

echo "📦 导出主题..."
docker cp ghost-capconnex:/var/lib/ghost/content/themes /tmp/ghost-export/themes

cd "$REPO_DIR"
git pull origin main 2>&1 || true

mkdir -p "backups/$TIMESTAMP"
cp -r /tmp/ghost-export/* "backups/$TIMESTAMP/"
echo "✅ 备份保存到 backups/$TIMESTAMP/"

rm -rf content
cp -r "backups/$TIMESTAMP" content

git add -A
git commit -m "🔄 Ghost backup $TIMESTAMP" --allow-empty
git push origin main 2>&1

rm -rf /tmp/ghost-export
echo "✅ 备份完成! https://github.com/matthewhe22/Capconnex"
