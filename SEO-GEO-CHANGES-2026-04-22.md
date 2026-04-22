# SEO + GEO Foundation — Changes Shipped 2026-04-22

Landing-page commit covering the first end-to-end SEO/GEO setup per `/Users/fredericlumiere/Desktop/SEO-SETUP-PLAYBOOK.md`. See `Desktop/APIANT-SEO-Stakeholder-Summary.md` for the non-code overview.

## Bugs fixed

| Area | Bug | Fix |
|---|---|---|
| Sitemap | `robots.txt` pointed at `/sitemap.xml` returning 404 | Generated real sitemap with 37 URLs + 20-locale hreflang alternates |
| Canonical | 20 of 37 English pages had canonicals pointing at non-existent URLs (missing `-and-`, missing `.html`, mixed case) | Replaced with self-referential canonicals matching the actual file path |
| Hreflang | 37 English pages had `x-default` and `en` hreflang tags duplicated 45× each | Removed duplicates, made `localize.py` idempotent |
| Analytics | GA4 only loaded after banner accept — rejectors invisible | Consent Mode v2 with default-denied, `gtag.js` loads on every page |
| Structured data | None | Organization + WebSite on homepage; Product + Breadcrumb on 17 API App pages + 3 hub pages |
| GEO | No AI-engine signal | Added `/llms.txt` per llmstxt.org spec |

## New files

- `sitemap.xml` — 37 URLs, regenerates via `scripts/generate_sitemap.py`
- `llms.txt` — GEO summary for ChatGPT/Perplexity/Claude/Gemini
- `js/gtag-consent.js` — Consent Mode v2 bootstrap loaded before cookie-consent.js
- `scripts/generate_sitemap.py` — sitemap generator (excludes noindex/backup/redirects/servlet templates)
- `scripts/inject_seo.py` — idempotent head-injection pipeline (consent, canonical, schema, hreflang dedup)

## Modified

- `js/cookie-consent.js` — `loadGA()` now calls `gtag('consent','update',...)` instead of appending a new script tag; added `denyGA()` for reject path
- `scripts/localize.py` — `add_hreflang_tags` strips existing hreflang before appending
- 44 English HTML pages — injected gtag-consent script, canonical fixes, schema JSON-LD, deduped hreflang
- 684 localized pages — regenerated via `scripts/localize.py` to propagate all the above

## Pipeline

New repo for weekly audits: https://github.com/Fredlumiere/apiant-website-audit. Runs Monday 10:00 UTC, publishes to `https://apiant-website-audit-reports.pages.dev`. Requires `CLOUDFLARE_API_TOKEN` + `CLOUDFLARE_ACCOUNT_ID` secrets.

## Verification

```bash
# Canonical audit — should return "OK: 44, mismatch: 0"
python3 -c "
import re; from pathlib import Path
CR = re.compile(r'<link[^>]+rel=[\"\x27]canonical[\"\x27][^>]+/?>', re.I)
HR = re.compile(r'href=[\"\x27]([^\"\x27]+)[\"\x27]', re.I)
for p in Path('.').rglob('*.html'):
    ...
"

# Hreflang dedup — should return 0 (or 2 noindex pages)
grep -c 'hreflang="x-default"' index.html

# Regenerate sitemap after English edits
python3 scripts/generate_sitemap.py

# Regenerate localized pages after English edits
python3 scripts/localize.py  # or: bash scripts/update_translations.sh for translation + regen
```

## Still open

- No real FAQ sections on key pages — FAQPage schema blocked until content team adds them. Once present, `scripts/inject_seo.py` auto-detects.
- Lighthouse baseline pending until site deploys (live hreflang bug currently prevents crawler from finishing). Will finalize after push.
- `/pricing.html` → `/platform/` redirect: lose SEO signal on pricing queries. Either restore a dedicated pricing page or accept.
- Apache/server serves both `/foo` and `/foo.html` as 200 — duplicate content. Decide on a canonical shape and add server-level 301 to enforce it.
