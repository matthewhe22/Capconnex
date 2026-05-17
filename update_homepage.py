"""
update_homepage.py — Inject the Capconnex Option A homepage
into Ghost CMS, mirroring the structure of update_tesla_page.py.

Usage:
    # 1. Drop `capconnex-homepage.html` (the bundled standalone file)
    #    next to this script, in /root/capconnex/ on the Oracle box.
    # 2. SSH in and run:
    cd /root/capconnex && python3 update_homepage.py

The script reads the bundled HTML, extracts <head> + <body> content,
wraps them in a namespaced <div> so the styles do not leak into the
rest of Ghost, and writes the result into the page identified by
HOMEPAGE_SLUG. Change that constant if your home page uses a
different slug.
"""

import sqlite3
import json
import os
import re
import html as html_lib

# ────────────────────────────────────────────────────────────────
# Configuration — adjust if your Ghost setup differs.
# ────────────────────────────────────────────────────────────────
DB = "/opt/ghost/content/data/ghost.db"
BUNDLE_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "capconnex-homepage.html")
HOMEPAGE_SLUG = "home"                  # change to the slug of your homepage post / page
PAGE_TITLE   = "Capconnex — Investment & applied AI"
META_TITLE   = "Capconnex — Capital that operates its own software"
META_DESC    = ("Capconnex is an Australian investment firm operating two applied‑AI "
                "products of its own: Pencil PM Feasibility for real‑estate development, "
                "and Smart EV Charging Manager for solar + battery EV orchestration.")

NAMESPACE_CLASS = "capconnex-homepage"  # wrapper class — keeps styles scoped


# ────────────────────────────────────────────────────────────────
# Read the bundled HTML and split it into head + body content.
# ────────────────────────────────────────────────────────────────
def load_bundle(path):
    with open(path, "r", encoding="utf-8") as f:
        raw = f.read()

    head_match = re.search(r"<head[^>]*>(.*?)</head>", raw, re.DOTALL | re.IGNORECASE)
    body_match = re.search(r"<body[^>]*>(.*?)</body>", raw, re.DOTALL | re.IGNORECASE)
    if not head_match or not body_match:
        raise RuntimeError(f"Could not parse <head>/<body> from {path}")

    head_inner = head_match.group(1).strip()
    body_inner = body_match.group(1).strip()

    # Strip the bundler's no‑JS / thumbnail <template> — it's an artefact
    # of the build pipeline, not something we want injected into Ghost.
    head_inner = re.sub(
        r'<template id="__bundler_thumbnail">.*?</template>',
        "", head_inner, flags=re.DOTALL)

    # Drop the page <title> (Ghost already manages the document title).
    head_inner = re.sub(r"<title>.*?</title>", "", head_inner, flags=re.DOTALL)

    # Drop <meta charset> and <meta viewport> (already set by Ghost).
    head_inner = re.sub(
        r'<meta[^>]+(charset|viewport)[^>]*>', "",
        head_inner, flags=re.IGNORECASE)

    return head_inner, body_inner


head_inner, body_inner = load_bundle(BUNDLE_PATH)

# Compose the final injected block. Order matters: fonts + CSS first,
# then the React/Babel runtime + JSX scripts, then the body markup that
# they render into. Everything is inside one namespaced <div>.
html = (
    f'<div class="{NAMESPACE_CLASS}">\n'
    f"<!-- ===== injected from capconnex-homepage.html ===== -->\n"
    f"{head_inner}\n"
    f"{body_inner}\n"
    f"</div>\n"
)

# ────────────────────────────────────────────────────────────────
# Ghost mobiledoc + plaintext + SEO meta.
# ────────────────────────────────────────────────────────────────
mobiledoc = json.dumps({
    "version": "0.3.1",
    "atoms": [],
    "markups": [],
    "sections": [[10, 0]],
    "cards": [["html", {"html": html}]],
})

plaintext = (
    "Capconnex — an Australian investment firm operating two applied-AI "
    "products of its own. Pencil PM Feasibility: real-estate development "
    "underwriting in eight seconds. Smart EV Charging Manager: dynamic Tesla "
    "current adjustment for zero-grid solar + battery charging. "
    "Investing & operating since 2019. capconnex.com.au"
)

code_head = (
    '<script type="application/ld+json">\n'
    '{\n'
    '  "@context": "https://schema.org",\n'
    '  "@type": "Organization",\n'
    '  "name": "Capconnex",\n'
    '  "url": "https://capconnex.com.au",\n'
    '  "description": "Australian investment firm operating applied-AI products in real-estate and energy.",\n'
    '  "address": {"@type": "PostalAddress", "addressCountry": "AU"},\n'
    '  "sameAs": ["https://github.com/matthewhe22/Capconnex"]\n'
    '}\n'
    '</script>\n'
    '<meta name="keywords" content="Capconnex, applied AI, investment firm, Pencil PM Feasibility, '
        'Smart EV Charging Manager, real estate development AI, Tesla solar charging, '
        'Alpha ESS, Melbourne, Australia">\n'
    '<meta name="robots" content="index, follow">\n'
)


# ────────────────────────────────────────────────────────────────
# Write to Ghost SQLite. Tries `posts` first (typical for pages too),
# matching the pattern used by update_tesla_page.py.
# ────────────────────────────────────────────────────────────────
if not os.path.exists(DB):
    raise SystemExit(
        f"Ghost database not found at {DB}.\n"
        f"Update the DB constant at the top of {os.path.basename(__file__)} "
        "or run this on the host where Ghost is installed."
    )

conn = sqlite3.connect(DB)
cur  = conn.cursor()

# Make sure a row with this slug exists; if not, surface a helpful error.
cur.execute("SELECT id, title FROM posts WHERE slug = ?", (HOMEPAGE_SLUG,))
row = cur.fetchone()
if not row:
    conn.close()
    raise SystemExit(
        f"No post/page found in Ghost with slug='{HOMEPAGE_SLUG}'.\n"
        "Create the page in Ghost Admin first (Pages → New → set the slug), "
        f"or change HOMEPAGE_SLUG at the top of {os.path.basename(__file__)}."
    )

post_id, current_title = row
print(f"Updating post id={post_id}  slug={HOMEPAGE_SLUG}  title='{current_title}' …")

cur.execute("""
    UPDATE posts SET
        title              = ?,
        html               = ?,
        mobiledoc          = ?,
        plaintext          = ?,
        codeinjection_head = ?,
        updated_at         = datetime('now')
    WHERE slug = ?
""", (
    PAGE_TITLE, html, mobiledoc, plaintext, code_head, HOMEPAGE_SLUG,
))

cur.execute("""
    UPDATE posts_meta SET
        meta_title       = ?,
        meta_description = ?,
        og_title         = ?,
        og_description   = ?
    WHERE post_id = ?
""", (
    META_TITLE, META_DESC, META_TITLE, META_DESC, post_id,
))

conn.commit()
conn.close()

print(f"✓ Homepage updated.")
print(f"  bundle size : {len(html):,} chars")
print(f"  namespace   : .{NAMESPACE_CLASS}")
print(f"  slug        : {HOMEPAGE_SLUG}")
print(f"  next step   : restart Ghost  →  systemctl restart ghost  (or `ghost restart`)")
