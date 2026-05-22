# Deploying to Oracle (`ubuntu@207.211.143.253`)

> **Why a script instead of `git push` to the Oracle host:** the sandbox doesn't have your SSH key (`~/.ssh/oracle_ghost`) and can't reach the Oracle public IP from here anyway. So all the SSH/rsync runs from **your Mac**.

The site lives on Oracle at `/opt/capconnex-static/`. nginx serves that folder at the root of `capconnex.com.au`. Ghost stays in its Docker container, untouched, ready to be reattached at `/cms/` later if you want a blog back.

---

## Step 0 — Check what's fronting Ghost right now (≈ 30 sec)

You need this to know **where to put the new nginx site config**. From your Mac:

```bash
ssh -i ~/.ssh/oracle_ghost ubuntu@207.211.143.253 '
  echo "=== docker ps ===";
  docker ps --format "table {{.Names}}\t{{.Ports}}\t{{.Image}}";
  echo;
  echo "=== /etc/nginx/sites-enabled ===";
  ls /etc/nginx/sites-enabled/ 2>/dev/null || echo "no host nginx";
  echo;
  echo "=== ports listening on host ===";
  sudo ss -tlnp | grep -E ":80 |:443 " 2>/dev/null || true
'
```

Three likely cases:

| Case | What you'll see | Path forward |
|---|---|---|
| **A.** Host nginx | `/etc/nginx/sites-enabled/...` exists, port 80/443 on host | Use `nginx-host.conf` below, drop into `/etc/nginx/sites-available/` |
| **B.** Docker nginx | A container named `nginx`/`caddy`/`npm` with `0.0.0.0:80->80` | Mount `/opt/capconnex-static` into it, use config below |
| **C.** Ghost direct on 80/443 | Only `ghost-capconnex` listening on host ports | Need to insert a reverse proxy. See "Case C" below. |

Tell me which case you have if it's not obvious — I'll tailor the next step.

---

## Step 1 — From your Mac: push the site to Oracle

Save this snippet on your Mac as `deploy-capconnex.sh`:

```bash
#!/usr/bin/env bash
set -euo pipefail

# CONFIGURE: where you have the site/ folder locally
SITE_DIR="${1:-./site}"
SSH_KEY="$HOME/.ssh/oracle_ghost"
HOST="ubuntu@207.211.143.253"
REMOTE_DIR="/opt/capconnex-static"

if [ ! -f "$SITE_DIR/index.html" ]; then
  echo "Couldn't find $SITE_DIR/index.html. Pass the path to site/ as first arg." >&2
  exit 1
fi

echo "→ Ensuring $REMOTE_DIR exists on Oracle"
ssh -i "$SSH_KEY" -o StrictHostKeyChecking=no "$HOST" "sudo mkdir -p $REMOTE_DIR && sudo chown ubuntu:ubuntu $REMOTE_DIR"

echo "→ Rsyncing site files"
rsync -av --delete \
  --exclude='.git' --exclude='*.md' --exclude='partials' --exclude='DEPLOY.md' \
  -e "ssh -i $SSH_KEY -o StrictHostKeyChecking=no" \
  "$SITE_DIR/" "$HOST:$REMOTE_DIR/"

echo "→ Done. Files live at $REMOTE_DIR on Oracle."
```

Then run:

```bash
chmod +x deploy-capconnex.sh
./deploy-capconnex.sh /path/to/Capconnex-redesign/site
```

That's the **push**. The site is now on Oracle but not served yet. Step 2 wires nginx.

---

## Step 2 — Wire nginx (one-time)

### Case A — Host nginx already running

Save this on Oracle at `/etc/nginx/sites-available/capconnex`:

```nginx
# /etc/nginx/sites-available/capconnex
server {
    listen 80;
    listen [::]:80;
    server_name capconnex.com.au www.capconnex.com.au;

    root /opt/capconnex-static;
    index index.html;

    # Pretty URLs: /about → /about.html
    location / {
        try_files $uri $uri.html $uri/ =404;
    }

    error_page 404 /404.html;

    # Cache static assets
    location ~* \.(css|js|svg|woff2?|png|jpg|jpeg|gif|ico)$ {
        expires 7d;
        add_header Cache-Control "public, immutable";
    }

    # OPTIONAL: re-attach Ghost as a blog at /cms/ later
    # location /cms/ {
    #     proxy_pass http://127.0.0.1:2368/;
    #     proxy_set_header Host $host;
    #     proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    #     proxy_set_header X-Forwarded-Proto $scheme;
    # }
}
```

Enable + reload:

```bash
ssh -i ~/.ssh/oracle_ghost ubuntu@207.211.143.253 '
  sudo ln -sf /etc/nginx/sites-available/capconnex /etc/nginx/sites-enabled/capconnex
  # If an old "default" or Ghost site is there, remove it:
  # sudo rm /etc/nginx/sites-enabled/default
  sudo nginx -t && sudo systemctl reload nginx
'
```

HTTPS — if you don't have a cert yet, after the HTTP site is responding correctly:

```bash
ssh -i ~/.ssh/oracle_ghost ubuntu@207.211.143.253 '
  sudo certbot --nginx -d capconnex.com.au -d www.capconnex.com.au --redirect
'
```

### Case B — Docker nginx

If nginx is in a container, mount `/opt/capconnex-static` into it and add the conf to the container's `conf.d`. The exact docker-compose change depends on your setup — share the relevant compose file or `docker inspect` output and I'll tailor it.

### Case C — Ghost is on 80/443 directly

Easiest: install host nginx in front of Ghost.

```bash
ssh -i ~/.ssh/oracle_ghost ubuntu@207.211.143.253 '
  sudo apt update && sudo apt install -y nginx certbot python3-certbot-nginx
  # Move Ghost off port 80 — change docker compose to bind to 127.0.0.1:2368
  # (do that manually, then docker restart ghost-capconnex)
'
```

Then proceed with **Case A** above.

---

## Step 3 — Verify

```bash
# From your Mac (or any client):
curl -I https://capconnex.com.au/
curl -I https://capconnex.com.au/pencil.html
curl -I https://capconnex.com.au/about.html
```

You should see `200 OK` and `content-type: text/html`. Visit in a browser and check the contact form works (after you've pasted in the Web3Forms access key).

---

## Rollback

The previous Ghost site is **untouched** — it's still running in Docker. If you need to roll back:

```bash
ssh -i ~/.ssh/oracle_ghost ubuntu@207.211.143.253 '
  sudo rm /etc/nginx/sites-enabled/capconnex
  # Restore previous site config (whatever was there before)
  sudo nginx -t && sudo systemctl reload nginx
'
```

---

## Future: re-attach Ghost as a blog

Uncomment the `/cms/` block in the nginx config and reload. Ghost continues serving as it does today, just at `capconnex.com.au/cms/` instead of root. You'd want to set `url: https://capconnex.com.au/cms` in Ghost's `config.production.json` for links to come out right.
