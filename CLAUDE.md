# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **APIANT marketing website**, a static HTML site originally built with Webflow, now maintained by hand. APIANT is a white-label integration platform (iPaaS) serving SaaS companies, System Integrators, and enterprises. The site markets both the platform itself and 17 turnkey "API App" integration products across three verticals: Mindbody (10 products), Cliniko (3), and DonorPerfect (4).

**Domain:** apiant.com
**Theme:** Dark mode (most pages)

## Tech Stack

- **Static HTML.** No build system, no bundler, no package.json. Pages are standalone `.html` files.
- **CSS:** `css/normalize.css`, `css/components.css`, `css/apiant.css` (global). Pages also contain extensive `<style>` blocks for page-specific styles.
- **JS:** `js/apiant.js` (manages sign-in/dashboard button state). jQuery 3.5.1 loaded from CDN. Heavy use of inline `<script>` blocks per page.
- **Fonts:** Lato, Open Sans, DM Sans, Inter via Google Fonts WebFont loader.
- **Analytics:** Google Analytics (G-G902ZQ3PZZ), Smartlook session recording, HubSpot (5004658).
- **Forms:** Google reCAPTCHA v2, submissions go to APIANT webhooks.
- **Legal content:** Privacy and Cookie pages use Termly embeds (not static HTML).

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
formapps.html                         FormApps (embeddable UIs)
mcp-servers.html                      MCP Servers

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
  servlettemplateconnect.html         Server-side template with {TEMPLATE_*} placeholders

connections/
  connections.html                    Static single-app page (Cliniko example)
  servlettemplateconnections.html     Server-side template with {TEMPLATE_*} placeholders

appconnect-next-steps.html            Post-signup (Zapier), noindex
shopconnect-next-steps.html           Post-signup (Shopify), noindex
mailconnect-next-steps.html           Post-signup (Mailchimp), noindex
zoomconnect-nextsteps.html            Post-signup (Zoom), noindex

privacy.html / cookie-policy.html / tos.html    Legal pages
401.html / 404.html                             Error pages
```

## Servlet Template Pages

`connect/servlettemplateconnect.html` and `connections/servlettemplateconnections.html` are server-side templates. The APIANT backend replaces placeholders like `{TEMPLATE_FROM_APP}`, `{TEMPLATE_TO_APP}`, `{TEMPLATE_FROM_ICON}`, etc. to generate unique SEO pages for every app combination. Do not change the `{TEMPLATE_*}` placeholder syntax.

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

- `SITE-DOCUMENTATION.md`: Complete page-by-page content documentation
- `APIANT-Website-Revision-Plan-v2-FINAL.md`: Strategic plan for site restructure, messaging guidelines, voice principles, competitive positioning
- `API-APP-PAGE-PLAYBOOK.md`: Template/playbook for redesigning API App product pages (proven on Mindbody+HubSpot)
- `API_APPS_FEATURES.md`: Complete feature reference for all 17 products
- `HOMEPAGE-COPY-WEBFLOW-READY.md`: Approved homepage copy

## Voice and Messaging Rules

From the revision plan (these apply to all page copy):
- **Direct.** No corporate fluff. "The AI reads API docs and builds connectors", not "Leverage AI-powered capabilities."
- **Technical, but not jargon-dense.** "Bi-directional sync with custom objects and rate-limited multi-location support."
- **Confident without arrogance.** "We believe we're the first integration platform to do this."
- **Builder-to-builder tone.** Write like explaining the platform over a Zoom call, not like a press release.

**Data Engine messaging:** Always say "unified data processing engine," "format-agnostic," "XPath (an open W3C standard)." Never expose internals like "VTD-XML," "non-extractive parser," "converts JSON to XML internally," or specific memory model details.

## Important Conventions

- **Never use em dashes** (the `—` character) anywhere: not in code, copy, comments, or commit messages. Use commas, periods, colons, or parentheses instead.
- Pages use Webflow's class naming (`w-*` classes). Preserve these; they tie to the base CSS.
- Inline styles and `<style>` blocks are the norm. Page-specific CSS lives in the page's `<head>`.
- Images are in `/images/` (900+ files). Product screenshots, logos, partner badges.
- Videos are in `/videos/`. Some pages also embed YouTube/Wistia/Calendly.
- The `backup/` directory contains staging/backup versions of pages, not live content.
- Hidden placeholder testimonials ("Emily Chen / DevOps Specialist") exist in product page code with `class="hide"`. These are template filler, not real content.
