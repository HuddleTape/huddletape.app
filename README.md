# huddletape.app — pre-launch site

Static site (plain HTML/CSS, no JavaScript, no build step) for GitHub Pages at **https://huddletape.app**.
Status: **not deployed.** Nothing has been pushed or published yet; the owner approves first.

## Files

| Path | What |
|---|---|
| `index.html` | Landing page: hero TV with ticker, parlay leg-rail, and Tailer TAILING tab; how it works; why it’s fun; pricing; FAQ; beta form |
| `beta.html` | Stand-alone beta signup page (shareable link, e.g. for the X bio) |
| `thanks.html` | Where the form sends people after they submit |
| `privacy.html`, `terms.html` | **DRAFT — pending attorney review** (`noindex`) |
| `404.html` | GitHub Pages not-found page |
| `CNAME` | `huddletape.app` (custom domain for Pages) |
| `_config.yml` | Tells Pages' Jekyll to skip `README.md`, `_tools/`, `_previews/` |
| `favicon.ico`, `favicon.svg`, `apple-touch-icon.png` | From the neon "#" mark |
| `assets/site.css` | All styles |
| `assets/img/og-card.png` | 1200×630 share card (Open Graph / X) |
| `assets/img/` | Wordmark + mark SVGs, Tailer sprite sheets |
| `assets/fonts/` | Self-hosted Anton, Barlow Semi Condensed, Chakra Petch (SIL OFL, licenses included) |
| `_tools/` | Generators (not published): `build_assets.py` (fonts/logos/icons from `/workspace/huddletape-brand`), `build_pages.py` (all HTML; edit copy here, then re-run), `og.html` (share-card source) |
| `_previews/` | Screenshots for review; git-ignored, never deployed |

Edit copy in `_tools/build_pages.py`, then run `python3 _tools/build_pages.py` (needs `pip install segno` for the TV QR code).

## Beta signup form (FormSubmit)

The form posts to `https://formsubmit.co/huddletape.app@gmail.com`. No account or server needed; submissions arrive as emails in huddletape.app@gmail.com.

**One-time setup (owner):**
1. After the site is live, submit the form once yourself.
2. FormSubmit emails huddletape.app@gmail.com an **activation link**. Click it. Until then, no signups are delivered.
3. Optional, recommended: the activation email also gives a random alias (like `formsubmit.co/abc123...`). Swap it into `action=` in `_tools/build_pages.py` and rebuild, so the Gmail address isn't in the page source for spam bots.

Built in:
- `_honey` honeypot field (hidden; bots that fill it are dropped by FormSubmit).
- `_captcha=false` (no FormSubmit captcha page; set to `true` if spam shows up).
- `_next=https://huddletape.app/thanks.html` (redirect after submit; works once the domain is live).
- `_subject`, `_template=table`, and a `source` field (`home` or `beta-page`).
- Required: name, email, 21+ checkbox. Optional: TV/streamer model.

## Compliance checklist (applied)

No sportsbook, exchange, league or team names or logos; no "Super Bowl"/"March Madness"; no lock/tout/guarantee language; nothing encourages betting. All ticker visuals are made-up and labeled **Sample data**. No app-store or "Coming soon" buttons; the CTA is the beta signup. Footer on every page: 21+ · Play responsibly · 1-800-GAMBLER · privacy · terms · support · © 2026 HuddleTape LLC. Respects `prefers-reduced-motion`.

## Deploying (after approval)

1. Create a GitHub repo and push this folder's contents (the root of the repo = this folder).
   GitHub Pages on a **private** repo needs a paid plan (Pro/Team); on the free plan the repo must be public.
2. Repo **Settings → Pages**: Source = *Deploy from a branch*, `main` / `(root)`. Custom domain = `huddletape.app` (the `CNAME` file already says this).
3. Recommended: verify the domain under your GitHub account **Settings → Pages → Verified domains** (adds a TXT record) to prevent takeover.
4. Namecheap → Domain List → huddletape.app → **Advanced DNS**. Remove the default parking records (CNAME `www` → parkingpage, URL redirect `@`), then add:

| Type | Host | Value |
|---|---|---|
| A | @ | 185.199.108.153 |
| A | @ | 185.199.109.153 |
| A | @ | 185.199.110.153 |
| A | @ | 185.199.111.153 |
| AAAA (optional) | @ | 2606:50c0:8000::153, 2606:50c0:8001::153, 2606:50c0:8002::153, 2606:50c0:8003::153 |
| CNAME | www | `<github-username>.github.io.` (no repo name) |

Verified against GitHub docs (Oct 9, 2026): https://docs.github.com/en/pages/configuring-a-custom-domain-for-your-github-pages-site/managing-a-custom-domain-for-your-github-pages-site
5. Wait for DNS (up to 24 h), then tick **Enforce HTTPS** in Pages settings. `.app` domains are HTTPS-only in browsers, so the site won't load until GitHub's certificate is issued.
6. Submit the form once and click FormSubmit's activation email (above).

Note: all links are root-relative (`/assets/...`), so preview it at the custom domain (or a local server at the folder root), not at `username.github.io/repo/`.

## Local preview

```
cd huddletape-site && python3 -m http.server 8000   # open http://localhost:8000
```
