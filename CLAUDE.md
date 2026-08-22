# CLAUDE.md

<!-- qa-board:pointer -->
> **QA for this product:** https://claude.ai/code/artifact/ec361dc1-2cff-44dd-a06c-dac05a0b1f60
> Data lives in `.claude/qa/board.json`. Claude Code: use `/qa-board`, and
> see the QA section at the bottom of this file before testing anything.

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **APIANT marketing website**, a static HTML site originally built with Webflow, now maintained by hand. APIANT is a white-label integration platform (iPaaS) serving SaaS companies, System Integrators, and enterprises. The site markets both the platform itself and 17 turnkey "API App" integration products across three verticals: Mindbody (10 products), Cliniko (3), and DonorPerfect (4).

**Domain:** apiant.com
**Theme:** Dark mode (most pages)

## Tech Stack

- **Static HTML.** No build system, no bundler, no package.json. Pages are standalone `.html` files.
- **CSS:** `css/normalize.css`, `css/components.css`, `css/apiant.css` (global). Pages also contain extensive `<style>` blocks for page-specific styles.
- **JS:** `js/apiant.js` (manages sign-in/dashboard button state). jQuery 3.5.1 loaded from CDN. Heavy use of inline `<script>` blocks per page.
- **Hosted product widgets (`js/calendarconnect-widget-*.js`):** not part of this site. These are served from `apiant.com/js/` for embedding on *customer* websites. Source of truth is the `calendarconnect-mindbody-calendly` repo, `test/optiforme-demo/calendarconnect-widget.js` (the localisable v4.0 build, the one with `data-label-*` support; the `test/apiant-gym-demo/` build is the same widget without it, so it is a subset). The copies here are published artifacts and must match the source byte for byte. Do not edit them here, do not minify, transpile, reformat or lint-fix them, and exclude them from any pipeline that touches `js/`. The header comment is customer-facing documentation and must survive. `-4.0.js` is the immutable pinned build, `-4.js` is the floating 4.x alias customers embed. To ship a change, edit the source repo and re-copy both files.
- **Fonts:** Lato, Open Sans, DM Sans, Inter via Google Fonts WebFont loader.
- **Analytics:** Google Analytics (G-G902ZQ3PZZ), Smartlook session recording, HubSpot (5004658). All loaded conditionally via `js/cookie-consent.js` based on user consent.
- **Cookie Consent:** Self-hosted banner (`js/cookie-consent.js`, `css/cookie-consent.css`). Controls loading of GA, Smartlook, HubSpot, and Facebook Pixel. Consent stored in `apiant_cc` cookie.
- **Forms:** Google reCAPTCHA v2, submissions go to APIANT webhooks.
- **Legal content:** Privacy, Cookie Policy, Terms of Service, and DPA pages are native HTML (no third-party embeds).

## Development

There is no build step, test suite, or linter. To develop:
- Edit HTML/CSS/JS files directly
- Open `.html` files in a browser to preview (or use a local server like `python3 -m http.server`)
- Changes are deployed by pushing to the server that hosts apiant.com

## Workflow Conventions

**GitHub repo**: `Fredlumiere/apiant-website`

When a user prompt starts with `b:`, treat it as a bug report:
1. Create a GitHub issue using `gh issue create --repo Fredlumiere/apiant-website --title "..." --body "..." --label bug` before starting work.
2. Work on the fix.
3. Ask the user to verify the fix before committing.
4. Once confirmed, commit with `Fixes #<number>` in the commit message so the issue closes automatically on push.
5. After the fix is pushed, add a troubleshooting log to the issue using `gh issue comment <number> --repo Fredlumiere/apiant-website --body "..."`. The comment must include:
   - **Root cause**: What was actually causing the bug.
   - **What was tried**: Each approach attempted, in order, and why it did or didn't work.
   - **Resolution**: The final fix and why it works.
   This creates a knowledge base of past issues and solutions for future debugging.

## Site Architecture

```
index.html                            Homepage (builder-first gateway)
apps.html                             Prebuilt Connectors catalog (AJAX from apiant.com/jspAppCatalog.jsp)
for-saas.html                         For SaaS Companies
for-si.html                           For System Integrators
for-enterprises.html                  For Enterprises
ai.html                               AI Capabilities
chatbot.html                          AI Chatbot (GDPR compliance example)
formapps.html                         FormApps (embeddable UIs)
mcp-servers.html                      MCP Servers

compare/
  prismatic.html                      APIANT vs Prismatic executive comparison (noindex; framework page, one file per competitor)
  competitors.json                    Manifest the competitor selector reads; add an entry per new comparison page

platform/
  index.html                          Platform overview
  automation-editor.html              Automation Editor
  assembly-editor.html                Assembly Editor + AI Co-Pilot
  admin-console.html                  Admin Console

apipartners/
  mindbody-turnkey-integration-solutions.html     Mindbody hub
  cliniko-turnkey-integration-solutions.html      Cliniko hub
  donorperfect-turnkey-integration-solutions.html DonorPerfect hub
  mindbody/   (10 product pages)
  cliniko/    (3 product pages)
  donorperfect/ (4 product pages)

connect/
  connect.html                        Static two-app connect page (Cliniko+Stripe example)
  servletTemplateConnect.html         Server-side template with {TEMPLATE_*} placeholders

connections/
  connections.html                    Static single-app page (Cliniko example)
  servletTemplateConnections.html     Server-side template with {TEMPLATE_*} placeholders

appconnect-next-steps.html            Post-signup (Zapier), noindex
shopconnect-next-steps.html           Post-signup (Shopify), noindex
mailconnect-next-steps.html           Post-signup (Mailchimp), noindex
zoomconnect-nextsteps.html            Post-signup (Zoom), noindex

privacy.html / cookie-policy.html / tos.html    Legal pages
401.html / 404.html                             Error pages
```

## Servlet Template Pages

`connect/servletTemplateConnect.html` and `connections/servletTemplateConnections.html` are server-side templates. The APIANT backend replaces placeholders like `{TEMPLATE_FROM_APP}`, `{TEMPLATE_TO_APP}`, `{TEMPLATE_FROM_ICON}`, etc. to generate unique SEO pages for every app combination. Do not change the `{TEMPLATE_*}` placeholder syntax.

## Blog System (generated from Supabase, do NOT hand-edit)

Everything under `blog/` is a build artifact: `blog/index.html`, `blog/posts/<slug>/index.html`, `blog/category/<slug>/index.html`, `blog/feed.xml`, `blog/search-index.json`, and all `<lang>/blog/...` copies. `scripts/build_blog.py` regenerates them from the Supabase `blog_posts` table (the post body is the `body_md` Markdown column). The deploy workflow runs `build_blog.py --all` on every push to `main`, so any manual edit to a generated blog file is overwritten on the next deploy.

To change a post, edit `body_md` (or other `blog_posts` fields) in Supabase, then regenerate via `gh workflow run build-blog.yml -f post_id=<uuid>` (or flip the post `status` to `publishing`). The in-article TOC and heading anchors are auto-generated from `##`/`###` headings; pipe tables are supported. Full details: `docs/blog-content-editing.md`.

**Blog images ("nanobanana"):** hero and inline illustrations are generated with **Nano Banana** = Google's `gemini-2.5-flash-image` model via the `@google/genai` SDK (run with `bun`). The key is `GEMINI_API_KEY` (exported in `~/.zshrc`, so it's in the shell env). Images are hosted in the Supabase Storage `blog-media` bucket and referenced from `hero_image_url` / inline `![](url)`. Full recipe (prompt art direction, convert, upload): `docs/blog-image-generation.md`.

## Common Page Patterns

All main pages share:
- **Navigation bar** with logo, Platform/Solutions/Connectors/Resources dropdowns, and Sign In/Dashboard + "Start Building" CTA
- **Footer** with Privacy Policy, Cookie Policy, Terms of Service, Community, Documentation, Blog links
- **White Paper CTA** section ("The Deep Integration Gap") with download form
- **Contact/Demo popup form** with fields: First Name, Last Name, Work Email, Mobile, Company, Country, Company Type (SaaS/SI/Enterprise), integration needs textarea, reCAPTCHA

The nav and footer are duplicated in each HTML file (no includes/partials system). When updating nav or footer, changes must be applied to every page.

## Product Naming

| Product Name    | Integration Type |
|----------------|-----------------|
| CRMConnect     | CRM integrations (HubSpot, ActiveCampaign, Keap, Klaviyo, HighLevel, Zoho CRM, Salesforce) |
| ShopConnect    | Shopify |
| ZoomConnect    | Zoom |
| CalendarConnect| Calendly |
| AppConnect     | Zapier |
| MailConnect    | Mailchimp |

## Key Reference Documents

- `docs/README.md`: Index of technical documentation
- `docs/site-maintenance-guide.md`: Shared elements, CSS architecture, cross-page updates
- `docs/forms-and-integrations.md`: Form flows, webhooks, analytics, third-party scripts
- `docs/servlet-templates.md`: `{TEMPLATE_*}` placeholder system for dynamic SEO pages
- `SITE-DOCUMENTATION.md`: Complete page-by-page content documentation
- `APIANT-Website-Revision-Plan-v2-FINAL.md`: Strategic plan for site restructure, messaging guidelines, voice principles, competitive positioning
- `API-APP-PAGE-PLAYBOOK.md`: Template/playbook for redesigning API App product pages (proven on Mindbody+HubSpot)
- `API_APPS_FEATURES.md`: Complete feature reference for all 17 products
- `HOMEPAGE-COPY-WEBFLOW-READY.md`: Approved homepage copy

**Keeping docs current**: When a code change affects behavior documented in `docs/`, update the relevant doc in the same commit. This includes changes to: shared page elements (nav, footer, head boilerplate), forms, webhook URLs, analytics setup, CSS architecture, or servlet templates.

## Voice and Messaging Rules

From the revision plan (these apply to all page copy):
- **Direct.** No corporate fluff. "The AI reads API docs and builds connectors", not "Leverage AI-powered capabilities."
- **Technical, but not jargon-dense.** "Bi-directional sync with custom objects and rate-limited multi-location support."
- **Confident without arrogance.** "We believe we're the first integration platform to do this."
- **Builder-to-builder tone.** Write like explaining the platform over a Zoom call, not like a press release.

**Data Engine messaging:** Always say "unified data processing engine," "format-agnostic," "XPath (an open W3C standard)." Never expose internals like "VTD-XML," "non-extractive parser," "converts JSON to XML internally," or specific memory model details.

## Localization (i18n)

The site is localized into 20 languages (English + 19). Localized pages live in subdirectories (`/es/`, `/fr/`, `/de/`, etc.).

**Translations run in CI on every push to `main`.** `.github/workflows/deploy.yml` runs `scripts/update_translations.sh` against the new English source, auto-commits the regenerated locale files with `[skip ci]` to avoid recursion, then rsyncs to apiant.com. `GOOGLE_TRANSLATE_API_KEY` lives in GitHub Actions secrets; collaborators do not need a local key.

**Default workflow:** edit English HTML, commit, push. CI handles translation regen + deploy.

**Local manual run** (only needed when iterating on translation logic itself, or testing a translation change before pushing):

```bash
bash scripts/update_translations.sh
```

The script prefers an existing `GOOGLE_TRANSLATE_API_KEY` env var and falls back to sourcing `~/.apiant_keys`:

```bash
# ~/.apiant_keys
export GOOGLE_TRANSLATE_API_KEY="your-key"
```

`scripts/translate_api.py` also supports DeepL (`DEEPL_API_KEY`, better quality for European languages) when invoked directly, but the `update_translations.sh` wrapper calls it with `--provider google`.

Key files:
- `scripts/update_translations.sh` - one-command update (extract + translate + regenerate)
- `scripts/localize.py` - page generation engine
- `scripts/translate_api.py` - Google Translate (default) / DeepL API pipeline
- `scripts/extract_strings.py` - string extraction from HTML
- `i18n/shared_ui.json` - hand-curated nav/footer/form translations
- `i18n/{lang}.json` - per-language translation dictionaries
- `js/i18n.js` - browser language detection, auto-redirect, language switcher
- `css/rtl.css` - RTL support for Arabic

Languages: es, fr, zh, hi, ar, bn, pt, ru, ja, de, ko, it, nl, tr, pl, vi, th, id, sv

## Important Conventions

- **Never use em dashes** (the `—` character) anywhere: not in code, copy, comments, or commit messages. Use commas, periods, colons, or parentheses instead.
- Pages use Webflow's class naming (`w-*` classes). Preserve these; they tie to the base CSS.
- Inline styles and `<style>` blocks are the norm. Page-specific CSS lives in the page's `<head>`.
- Images are in `/images/` (900+ files). Product screenshots, logos, partner badges.
- Videos are in `/videos/`. Some pages also embed YouTube/Wistia/Calendly.
- The `backup/` directory contains staging/backup versions of pages, not live content.
- Hidden placeholder testimonials ("Emily Chen / DevOps Specialist") exist in product page code with `class="hide"`. These are template filler, not real content.

## UI Reference Assets (uisnap)

When asked to generate SVG illustrations, Lottie animations, or animated SVGs from screenshots or recordings, look in `.uisnap/` for processed reference materials. Each subdirectory contains a `manifest.json` describing the source material, extracted frames (if video/GIF), and any style or format hints provided by the user. Read the manifest first, then read the image files to understand the visual content before generating assets.

<!-- qa-board:start -->
## QA: where it happens

QA for apiant-website lives on a published board, not in this file and not in a
test runner. One page, one URL, updated from inside this repo.

- **Board:** https://claude.ai/code/artifact/ec361dc1-2cff-44dd-a06c-dac05a0b1f60
- **Portfolio:** https://claude.ai/code/artifact/55be025c-e2fb-490c-93a2-dc7d2e3ea009 places this product next to the other APIANT
  ones. Internal only: to show a single product to someone outside the team,
  send that product's own board above, never the portfolio.

The page is a render. `.claude/qa/board.json`, committed here, **is** the
board: areas, test rows, coverage decisions, issues and the run log. Read the
JSON to know the truth; open the URL to show someone.

### Instructions for Claude Code

Read `.claude/qa/board.json` before doing any QA work in this repo and treat
it as the record of what is tested. Do not build a parallel checklist in chat:
work that is not on the board is work nobody else can see.

Use the `/qa-board` skill for every QA action.

| You want to | Run |
|---|---|
| see what needs testing | `/qa-board` |
| find surfaces with no row | `/qa-board scan` |
| find passes whose code has since changed | `/qa-board drift` |
| reconcile the board against the tracker | `/qa-board issues` |
| all three, then publish | `/qa-board refresh` |
| run tests and record verdicts | `/qa-board start` |
| fix a failing row and re-verify it | `/qa-board fix` |
| push the page live again | `/qa-board publish` |

**Always publish to the URL in `.claude/qa/artifact-url`.** Publishing
without it creates a second artifact, and everyone holding the old link keeps
reading a page that will never update again.

**Only mark a row `pass` from something you observed in that session.** A
merged fix is not a pass. A green CI run is not a pass for a product
behaviour. If the code shipped but nobody exercised it, the row stays
`pending` and the note says exactly that. This rule is the only reason the
board is worth reading.

**For anything with an allow path and a deny path, test both.** An endpoint
that serves the right caller and an endpoint that refuses the wrong one are
two different tests, and passing only the first is how an auth hole ships
green.

Never hand-edit `.claude/qa/board.html`. It is generated, it is gitignored,
and `render.mjs` validates the data before it writes.

### GitHub issues

The board and the tracker have to agree, and `/qa-board issues` is the pass
that checks both directions: rows whose status drifted from the tracker, and
open issues the board never mentions. Run it before you publish.

- When a test fails and it is a real bug, file the issue **first**, then fix,
  then re-run the test that caught it. Link the issue from the row's note:
  notes accept inline HTML, so `<a href='...'>#12</a>` works.
  Use `gh issue create --label bug`.
- Reference the issue in the commit (`Fixes #12`) so it closes on push.
- When an issue closes, reconcile the row that referenced it. A row still
  reading `fail` against a closed issue is the most common way this board
  goes stale, and it is read as a live problem by everyone holding the link.
- **Do not open issues automatically during a QA run.** Report what you found
  and recommend what deserves a ticket, then wait. A tracker filling itself
  with plausible-looking findings nobody triaged is worse than an empty one.

Tracker: https://github.com/Fredlumiere/apiant-website/issues
<!-- qa-board:end -->
