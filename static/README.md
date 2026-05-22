# Capconnex — Static Site Redesign (2026)

A vanilla-HTML + custom-CSS marketing site for [capconnex.com.au](https://capconnex.com.au), replacing the Ghost-based site. No framework, no build step — just files you can drop straight onto nginx.

## Pages

| URL | File | Purpose |
|---|---|---|
| `/` | `index.html` | Home — hero, products, how we work, why Capconnex, CTA |
| `/about.html` | `about.html` | About — story, milestones, disciplines, principles |
| `/pencil.html` | `pencil.html` | Pencil Feasibility — product page with **Open App** button to `pencil.capconnex.com.au` |
| `/ev-charging.html` | `ev-charging.html` | Smart EV Charging Manager — product page with live-dashboard mock |
| `/ocorder.html` | `ocorder.html` | OC Order — product page for strata / owners' corp tooling |
| `/contact.html` | `contact.html` | Contact — info + Web3Forms-powered form |
| `/404.html` | `404.html` | Not-found page |

## Design system

- **Font:** Mulish (Google Fonts) — 400 / 600 / 700 / 800
- **Palette:**
  - Navy `#0A1628` (primary dark)
  - Gold `#C8A951` (accent / CTA)
  - Cream `#E8E4DC` (warm background)
  - Text `#2D3748`
- **Motion:** Intersection-Observer scroll reveal, easing count-up on stats, hover lifts, dropdown nav with `backdrop-filter` glassmorphism.
- All tokens live as CSS custom properties at the top of `css/styles.css`.

Respects `prefers-reduced-motion`.

## Local preview

From this folder (`site/`):

```bash
python3 -m http.server 8080
# then open http://localhost:8080/
```

Or simply open `index.html` in a browser — everything is relative paths against `/css/` and `/js/`, so absolute paths work best from a server root.

## Before you deploy

### 1. Fill in your Web3Forms access key

`contact.html` posts to Web3Forms. Sign up at <https://web3forms.com/> with `matthew.he@capconnex.com.au`, grab the access key from the dashboard, then replace this line in `contact.html`:

```html
<input type="hidden" name="access_key" value="YOUR_WEB3FORMS_ACCESS_KEY">
```

…with your real key. That's it — no backend needed.

### 2. Confirm what's fronting Ghost on Oracle

On the server, run:

```bash
docker ps
ls /etc/nginx/sites-enabled/ 2>/dev/null
```

Whether you have a host-installed nginx, a docker nginx, or nginx-proxy-manager affects the deploy step. See `DEPLOY.md`.

## Repo layout

```
site/
├── index.html
├── about.html
├── pencil.html
├── ev-charging.html
├── ocorder.html
├── contact.html
├── 404.html
├── assets/
│   └── favicon.svg
├── css/
│   └── styles.css
├── js/
│   └── main.js
├── partials/          ← source-of-truth for nav/footer (copy-paste if editing)
│   ├── head.html
│   └── nav-footer.html
├── README.md          ← this file
└── DEPLOY.md          ← server setup + deploy commands
```

## Notes / known TODOs

- `ev-charging.html` is built from the public homepage's EV product copy + extrapolation. If the original repo has a fuller "EV concept" page, drop its copy in here when the PAT issue is resolved.
- Web3Forms access key is a placeholder — see above.
- About-page milestones (2018–2026) are my best-guess narrative based on the brief (founded 2014, Melbourne, investment + valuation + tech). Tighten with real dates if you have them.
