#!/usr/bin/env bash
# ============================================================
# Capconnex static site deployer
# Run on your Mac. Pushes ./site/ to Oracle /opt/capconnex-static/
# ============================================================
set -euo pipefail

SITE_DIR="${1:-./site}"
SSH_KEY="$HOME/.ssh/oracle_ghost"
HOST="ubuntu@207.211.143.253"
REMOTE_DIR="/opt/capconnex-static"

# ----- sanity -----
if [ ! -f "$SITE_DIR/index.html" ]; then
  echo "[!] Couldn't find $SITE_DIR/index.html"
  echo "    Usage: $0 [path/to/site]"
  echo "    Defaults to ./site"
  exit 1
fi
if [ ! -f "$SSH_KEY" ]; then
  echo "[!] SSH key not found at $SSH_KEY"
  exit 1
fi
if ! command -v rsync >/dev/null 2>&1; then
  echo "[!] rsync not installed. brew install rsync"
  exit 1
fi

echo "→ Verifying SSH access to $HOST"
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no -o ConnectTimeout=10 "$HOST" 'echo OK'

echo "→ Ensuring $REMOTE_DIR exists"
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$HOST" \
  "sudo mkdir -p $REMOTE_DIR && sudo chown ubuntu:ubuntu $REMOTE_DIR"

echo "→ Syncing $SITE_DIR  →  $HOST:$REMOTE_DIR"
rsync -av --delete \
  --exclude='.git' \
  --exclude='*.md' \
  --exclude='partials/' \
  --exclude='deploy-capconnex.sh' \
  -e "ssh -i $SSH_KEY -o StrictHostKeyChecking=no" \
  "$SITE_DIR/" "$HOST:$REMOTE_DIR/"

echo "→ Quick smoke test"
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$HOST" "ls -la $REMOTE_DIR/ | head -20"

echo
echo "✓ Files synced to Oracle."
echo
echo "Next: if nginx isn't pointed at $REMOTE_DIR yet, follow DEPLOY.md step 2."
echo "Then:  curl -I http://capconnex.com.au/"
