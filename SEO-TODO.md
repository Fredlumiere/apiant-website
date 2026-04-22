# APIANT SEO + GEO — Open Todos

Last updated: 2026-04-22. Ranked by impact. Tick off as they ship.

**Live audit dashboard:** https://apiant-audit.vercel.app (credentials in `~/Desktop/APIANT-Audit-Dashboard-Credentials.txt`)
**Audit repo:** https://github.com/Fredlumiere/apiant-website-audit
**Weekly cron:** Monday 10:00 UTC (needs `VERCEL_TOKEN` secret — see P0.2 below)

---

## P0 — Ship blockers

Nothing ships without these.

- [x] **P0.1 — Deploy commit `62851c49` to apiant.com production — DONE**
      apiant.com auto-deploys from GitHub main via Apache reverse proxy to Vercel (`apache-vercel-proxy.conf`). Verified live 2026-04-22:
      ```
      curl -sI https://apiant.com/llms.txt                     → 200 ✓
      curl -s https://apiant.com/robots.txt | grep Sitemap      → /sitemap/sitemap_index.xml ✓
      curl -sL https://apiant.com | grep '"@type"'              → Organization, WebSite ✓
      curl -sL https://apiant.com | grep -c 'hreflang="x-default"' → 1 (was 45) ✓
      ```

- [ ] **P0.2 — Set `VERCEL_TOKEN` on the audit repo**
      Until set, the Monday cron will run Lighthouse but fail to redeploy the dashboard.
      ```bash
      # 1. Create token: https://vercel.com/account/tokens
      # 2. Add to repo secrets:
      gh secret set VERCEL_TOKEN --repo Fredlumiere/apiant-website-audit -b "<token>"
      # 3. Test:
      gh workflow run audit.yml --repo Fredlumiere/apiant-website-audit
      ```

- [ ] **P0.3 — Add apiant.com to Google Search Console**
      https://search.google.com/search-console → Add property → URL prefix → `https://apiant.com/` → auto-verifies via GA4 → Sitemaps → submit `https://apiant.com/sitemap/sitemap_index.xml`. Link GA4 ↔ Search Console in Admin → Product Links.

---

## P1 — Structural (infra-side, not in this repo)

- [ ] **P1.1 — Fix server-side sitemap generator**
      `sitemap0.xml` currently dumps ~35 admin/test/editor/OAuth pages that shouldn't be public, is missing the 17 API App product pages + 3 hub pages under `/apipartners/`, and has no hreflang alternates for 20 locales. Interim cover via `robots.txt` Disallow is in place.
      **Needed in the sitemap servlet:**
      - Exclude: `admin*.html`, `editor*.html`, `test*.html`, `temp.html`, `architecture-illustration*.html`, `*-next-steps.html`, `next-steps-*.html`, `google*.html` (verification files), `mcp-oauth-login.html`, `orderThankYou.html`, `apps2.html`, `index2.html`, `workshop-appointment-confirmation.html`, protected-content pages
      - Include: `/apipartners/*-turnkey-integration-solutions.html` and all 17 `/apipartners/<platform>/<platform>-<integration>-integration-and-automation-apiant.html` pages
      - Emit `<xhtml:link rel="alternate" hreflang="xx"/>` for each of 20 locales per URL

- [ ] **P1.2 — Restore or formally deprecate pricing page**
      `/pricing.html` currently redirects to `/platform/index.html`. Options:
      - Restore the 4-tier pricing page from git history (`git log --diff-filter=D -- pricing.html` to find the pre-redirect version)
      - Or remove the redirect, update paid-search copy to point at `/platform/`, and be OK with the SEO loss

- [ ] **P1.3 — Add AWS server-side 301 for `.html` vs extensionless** (DevOps ticket)
      Both `https://apiant.com/for-saas` and `https://apiant.com/for-saas.html` return 200 with identical content. Pick one as canonical (current canonicals say `.html`) and 301 the other form. apiant.com is served from AWS (not Vercel), so this is a server config change, not an in-repo change.
      **Apache snippet for the AWS box:**
      ```apache
      RewriteEngine On
      # Redirect /foo to /foo.html when /foo.html exists (excluding real dirs and known prefixes)
      RewriteCond %{REQUEST_URI} !^/(css|js|images|videos|fonts|connect|connections|apipartners|sitemap|editor|admin|api|private|protected-content|oauth|es|fr|de|zh|ja|ar|he|hi|bn|pt|ru|ko|it|nl|tr|pl|vi|th|id|sv)(/|$)
      RewriteCond %{REQUEST_FILENAME} !-d
      RewriteCond %{REQUEST_FILENAME} !-f
      RewriteCond %{DOCUMENT_ROOT}%{REQUEST_URI}.html -f
      RewriteRule ^(.+?)/?$ /$1.html [R=301,L]
      ```
      Test against /for-saas (should 301 to /for-saas.html), /css/normalize.css (should pass through), /apipartners/mindbody/... (should pass through as the .html already exists), /es/for-saas.html (should pass through).

---

## P2 — Content (needs copywriting, not code)

- [ ] **P2.1 — Add real FAQ sections to key pages**
      4–6 real Q&As each on: pricing (once restored), `/platform/`, `/for-saas.html`, `/for-si.html`, `/for-enterprises.html`, and the 3 API App hub pages.
      Use `<section class="faq">` with `<h3>` questions and `<p>` answers. Once live, re-run `python3 scripts/inject_seo.py` — it auto-wraps visible FAQs in FAQPage JSON-LD. Do NOT ship schema without real, visible FAQ content (Google penalizes fake markup).

- [ ] **P2.2 — Replace placeholder social URLs in Organization schema**
      `scripts/inject_seo.py` currently emits placeholder `sameAs` links:
      ```
      https://www.linkedin.com/company/apiant
      https://twitter.com/apiant
      https://www.youtube.com/@apiant
      https://github.com/apiant
      ```
      Verify each resolves; replace broken ones. Bad `sameAs` links signal Google that the Organization identity is uncertain.
      After update, re-run `python3 scripts/inject_seo.py` then `python3 scripts/localize.py`.

- [ ] **P2.3 — Meta descriptions audit + alt text audit**
      After P0.1 deploy, re-run the Lighthouse audit (`gh workflow run audit.yml --repo Fredlumiere/apiant-website-audit`) and open https://apiant-audit.vercel.app. Per-page reports enumerate which pages lack meta descriptions or alt text. Fill the gaps.

---

## P3 — Performance (from live Lighthouse baseline, 20 pages)

Every single audited page fails Core Web Vitals. Same root causes run across the whole site — fixing them once fixes all 20 pages.

- [ ] **P3.1 — LCP averaging 0.09 (critical)**
      Root causes likely:
      - Hero image not preloaded
      - WebFont.load script blocks paint before fonts swap in
      - jQuery from CDN on every page (used by Webflow widgets)
      - Large inline `<style>` blocks per page
      **Fix:**
      ```html
      <!-- Replace WebFont.load script block with: -->
      <link rel="preconnect" href="https://fonts.googleapis.com">
      <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
      <link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Lato:wght@300;400;700&display=swap">
      <link rel="stylesheet" href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Lato:wght@300;400;700&display=swap">
      <!-- Also preload LCP image: -->
      <link rel="preload" as="image" href="/images/hero-homepage.avif" fetchpriority="high">
      ```

- [ ] **P3.2 — 15/20 pages log console errors on load**
      Open DevTools console on the five worst performers (see P3 section table below). Triage: missing DOM nodes referenced by inline scripts, HubSpot/Smartlook race conditions, reCAPTCHA init, Turnstile widget init. Fix or suppress.

- [ ] **P3.3 — Speed Index (0.23), TTI (0.29), FCP (0.32) averages**
      Follow-on from P3.1 — fixing the font/preload issue moves all three metrics.

### Lighthouse worst-5 table (from 2026-04-22 baseline)

| Metric | Threshold | Worst pages |
|---|---|---|
| Performance | < 0.6 | `/mcp-servers.html` (0.55), `/for-enterprises.html` (0.58), `/apipartners/mindbody-turnkey-…` (0.59), `/for-si.html` (0.59), `/` (0.59) |
| Accessibility | < 0.9 | `/apipartners/mindbody/…hubspot…` (0.82), `/apipartners/cliniko/…hubspot…` (0.87), `/apipartners/donorperfect/…hubspot…` (0.87) |
| Best Practices | < 0.8 | All three hub pages + 3 product pages at 0.73 |
| SEO | < 0.9 | `/` (0.77), `/apipartners/cliniko/…hubspot…` (0.85), `/apipartners/donorperfect/…hubspot…` (0.85), `/apipartners/mindbody/…hubspot…` (0.85), `/ai.html` (0.92) |

---

## P4 — Accessibility (real violations, from baseline)

- [ ] **P4.1 — Color contrast on 11/20 pages**
      WCAG AA violation. Likely low-opacity muted text (`rgba(247, 248, 248, 0.6)` on `#0c0c0c`) failing the 4.5:1 ratio. Per-page Lighthouse reports enumerate the exact elements. Tighten opacity or pick a brighter mid-tone.

- [ ] **P4.2 — Heading order on 10/20 pages**
      Pages jump from `h2` to `h4` or skip levels. Screen readers rely on sequential hierarchy. Fix each flagged page in its per-page report.

- [ ] **P4.3 — 7 pages with links missing discernible names**
      Icon-only links or image links with empty alt. Add `aria-label` or visible text. Common pattern: social icons in footer, nav logos.

- [ ] **P4.4 — 2 pages with unlabeled form inputs**
      Inputs without `<label for="…">` or `aria-label`. Likely the contact popup or forum form.

---

## P5 — GEO (generative engine optimization, after content is in place)

- [ ] **P5.1 — Author/E-E-A-T signals on AI/technical pages**
      Pages: `/ai.html`, `/chatbot.html`, `/mcp-servers.html`, `/platform/automation-editor.html`, `/platform/assembly-editor.html`.
      Add: `<meta name="author">`, visible byline + role, publication date + last-updated, JSON-LD `Article` schema with `author`, `datePublished`, `dateModified`.

- [ ] **P5.2 — Visible citable-fact blocks**
      AI engines prefer short, factual, named statements. Promote the "Key Facts for Citation" pattern from `llms.txt` into visible page content on homepage, `/platform/`, `/for-enterprises.html`.

---

## Operational notes

- Before pushing any English HTML change, run:
  ```bash
  python3 scripts/inject_seo.py       # idempotent: consent, canonical, schema, hreflang dedup
  python3 scripts/localize.py         # regenerate locales (or: bash scripts/update_translations.sh)
  ```
- The weekly audit re-runs Monday 10:00 UTC once `VERCEL_TOKEN` is set. To trigger a fresh audit manually:
  ```bash
  gh workflow run audit.yml --repo Fredlumiere/apiant-website-audit
  ```
- Do not create a static `sitemap.xml` at the root — the real sitemap is server-generated at `/sitemap/sitemap_index.xml`. `robots.txt` now points there.
