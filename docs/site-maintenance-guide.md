# Site Maintenance Guide

> How to update shared elements, add new pages, and work with the CSS system.

## Table of Contents

1. [No Templating System](#no-templating-system)
2. [Head Boilerplate](#head-boilerplate)
3. [Structured Data and Open Graph (enforced by the build)](#structured-data-and-open-graph-enforced-by-the-build)
4. [The language-switcher `<style>` block](#the-language-switcher-style-block)
5. [Navigation Bar](#navigation-bar)
6. [Footer](#footer)
7. [Adding a New Page](#adding-a-new-page)
8. [CSS Architecture](#css-architecture)
9. [Page-Specific Styles](#page-specific-styles)
10. [Webflow Class Conventions](#webflow-class-conventions)
11. [Images and Assets](#images-and-assets)
12. [Cross-Page Update Checklist](#cross-page-update-checklist)

---

## No Templating System

This site has **no includes, partials, or build system for page content**. Every HTML file is standalone. The navigation bar, footer, head boilerplate, and popup forms are duplicated across all 94 English pages. When any shared element changes, the update must be applied to every page manually.

There is one exception worth knowing, because it is the closest thing to a template the site has. `scripts/localize.py` reads each English page and writes the 20 localised copies, and while it is there it also normalises the hreflang tags, the canonical, the Open Graph tags, the language switcher and the FAQ structured data. Anything that function owns is regenerated on every push to `main`, so hand-editing it in the HTML is wasted work. See [Structured Data and Open Graph](#structured-data-and-open-graph-enforced-by-the-build) for what it owns.

**Pages that contain shared elements (43 total):**
- Root: `index.html`, `apps.html`, `ai.html`, `formapps.html`, `mcp-servers.html`, `for-saas.html`, `for-si.html`, `for-enterprises.html`
- Platform: `platform/index.html`, `platform/automation-editor.html`, `platform/assembly-editor.html`, `platform/admin-console.html`
- API Partners hub pages: `apipartners/mindbody-turnkey-integration-solutions.html`, `apipartners/cliniko-turnkey-integration-solutions.html`, `apipartners/donorperfect-turnkey-integration-solutions.html`
- API Partners product pages: 10 Mindbody, 3 Cliniko, 4 DonorPerfect (in `apipartners/{vertical}/`)
- Connect/Connections: `connect/connect.html`, `connect/servletTemplateConnect.html`, `connections/connections.html`, `connections/servletTemplateConnections.html`
- Next-steps: `appconnect-next-steps.html`, `shopconnect-next-steps.html`, `mailconnect-next-steps.html`, `zoomconnect-nextsteps.html`
- Legal: `privacy.html`, `cookie-policy.html`, `tos.html`
- Error: `401.html`, `404.html`

## Head Boilerplate

Every page includes the same `<head>` structure in this order:

```html
<head>
  <meta charset="utf-8">
  <title>Page Title | APIANT</title>
  <!-- OG and Twitter meta tags (page-specific) -->
  <meta content="width=device-width, initial-scale=1" name="viewport">

  <!-- 1. CSS (path depth varies by page location) -->
  <link href="css/normalize.css" rel="stylesheet">
  <link href="css/components.css" rel="stylesheet">
  <link href="css/apiant.css" rel="stylesheet">

  <!-- 2. Google Fonts via WebFont loader -->
  <link href="https://fonts.googleapis.com" rel="preconnect">
  <link href="https://fonts.gstatic.com" rel="preconnect" crossorigin="anonymous">
  <script src="https://ajax.googleapis.com/ajax/libs/webfont/1.6.26/webfont.js"></script>
  <script>
    WebFont.load({
      google: {
        families: ["Lato:100,...,900", "Open Sans:300,...,800", "DM Sans:300,...,700", "Inter:300,...,700"]
      }
    });
  </script>

  <!-- 3. Webflow touch detection -->
  <script>
    !function(o,c){var n=c.documentElement,t=" w-mod-";n.className+=t+"js",...}(window,document);
  </script>

  <!-- 4. Favicon -->
  <link href="images/favicon.png" rel="shortcut icon">
  <link href="images/webclip.ico" rel="apple-touch-icon">
  <link rel="icon" href="https://apiant.com/favicon.ico">

  <!-- 5. reCAPTCHA -->
  <script src="https://www.google.com/recaptcha/api.js"></script>

  <!-- 6. Google Analytics -->
  <script async src="https://www.googletagmanager.com/gtag/js?id=G-G902ZQ3PZZ"></script>
  <script>
    window.dataLayer = window.dataLayer || [];
    function gtag(){dataLayer.push(arguments);}
    gtag('js', new Date());
    gtag('config', 'G-G902ZQ3PZZ');
  </script>

  <!-- 7. Page-specific <style> block -->
  <style>/* page styles */</style>
</head>
```

**Important:** CSS paths are relative. Pages at the root use `css/apiant.css`, pages in `platform/` use `../css/apiant.css`, and pages in `apipartners/mindbody/` use `../../css/apiant.css`. Get this wrong and the page loses all styling.

## Structured Data and Open Graph (enforced by the build)

Three invariants hold on every page the localisation pipeline touches. They are
enforced in `scripts/localize.py`, which runs in CI on every push to `main`, so
you do not hand-maintain them and you should not hand-edit them:

1. **`og:url` equals the page's own canonical URL.** Absolute, and per locale:
   the Spanish page points at the Spanish URL, not the English one. Set by
   `normalize_open_graph()`. A page with no canonical is left alone; the
   function never invents one.
2. **`og:type` appears exactly once.** Webflow emitted one and a later hand-edit
   added a second on all 20 API-partner pages. `normalize_open_graph()` keeps
   the first and drops the rest.
3. **FAQPage JSON-LD is generated from the rendered FAQ, never written by
   hand.** `rebuild_faq_jsonld()` reads the question and answer text out of the
   DOM after translation and rewrites the block, so a Spanish page carries
   Spanish schema and the schema cannot drift from what a visitor reads. Google
   requires FAQ schema to match visible content; generating it is the only way
   that stays true.

Two FAQ markup shapes are recognised: the Webflow accordion on the API-App
product pages (`.question-text` followed by `.answer-text`) and the simpler
`.faq-item` block (`h3` + `p`) on the partner hub pages. A third shape would be
invisible to the generator, so reuse one of these two.

To add a FAQ to a page, write the visible accordion and add an empty FAQPage
block; the next build fills it in. To check the current state without a build:

```bash
# every FAQPage entry must be findable in the page's own rendered text
python3 - <<'EOF'
import re, json, glob, html
for p in glob.glob('apipartners/*/*.html'):
    h = open(p).read()
    vis = re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', re.sub(r'<(script|style).*?</\1>', '', h, flags=re.S)))
    for b in re.findall(r'<script type="application/ld\+json">(.*?)</script>', h, re.S):
        if '"FAQPage"' not in b: continue
        for e in json.loads(b)['mainEntity']:
            if e['name'] not in vis: print('NOT ON PAGE:', p, e['name'][:60])
EOF
```

## The language-switcher `<style>` block

`add_language_switcher()` appends one `<style data-apiant="lang-switcher-css">`
block per page. **Do not remove the `data-apiant` attribute**: it is how the
next build finds its own block to replace.

Before this marker existed the build removed the previous block by deleting the
lines that mentioned `.lang-switcher`. Everything else the block declared
survived, the leftover was kept because it was not empty, and a fresh copy went
on top. One dead 3.4 KB block accumulated per deploy: by September 2026 there
were 250 of them on some pages, 92% of the bytes of `/es/platform/admin-console`,
and 757 MB across the repo. If you ever change what that block contains, change
it in `SWITCHER_CSS` and leave the removal logic matching on the marker.

`SWITCHER_CSS` also carries `.listed-addons`, `.pricing-holder` and
`.addon-container-copy` rules that have nothing to do with the switcher; they
were folded into the constant at some point and every page now depends on being
served them. Untangle that before trusting the constant's name.

## Navigation Bar

The nav bar uses Webflow's dropdown system (`w-dropdown`, `w-dropdown-toggle`, `w-dropdown-list` classes). It contains:

- Logo linking to `index.html`
- **Platform** dropdown: Platform Overview, Automation Editor, Assembly Editor, Admin Console
- **Solutions** dropdown: For SaaS Companies, For System Integrators, For Enterprises
- **Connectors** dropdown: Apps catalog link
- **Resources** dropdown: AI, FormApps, MCP Servers, Documentation, Blog, Community
- **Products** mega-dropdown: All 17 API App product links organized by vertical (Mindbody, Cliniko, DonorPerfect)
- Auth buttons: "Sign In" / "Dashboard" (toggled by `apiant_dynamic.js` from the APIANT server)
- "Start Building" CTA button

When adding a new product page, the Products mega-dropdown must be updated on every page.

## Footer

The footer contains links to:
- Privacy Policy (`privacy.html`)
- Cookie Policy (`cookie-policy.html`)
- Terms of Service (`tos.html`)
- Community (external link)
- Documentation (external link)
- Blog (external link)

Like the nav, the footer is duplicated in every HTML file.

## Adding a New Page

1. Copy an existing page at the same directory depth (for correct relative CSS/image paths)
2. Update `<title>`, OG meta tags, and Twitter meta tags
3. Update the page-specific content
4. Ensure the nav bar matches the current version (copy from a recently updated page)
5. Ensure the footer matches the current version
6. Add the page to the nav bar on ALL other pages if it should appear in navigation
7. Update `CLAUDE.md` site architecture section

## CSS Architecture

### Files

| File | Size | Purpose |
|------|------|---------|
| `css/normalize.css` | Small | Browser reset (standard) |
| `css/components.css` | Small | Webflow component defaults |
| `css/apiant.css` | Large | All site styles, exported from Webflow |

### CSS Custom Properties (in `apiant.css`)

The site uses CSS custom properties for theming, defined in `:root`:

**Dark mode (default):**
| Property | Value | Usage |
|----------|-------|-------|
| `--bg-color` | `#0c0c0c` | Page background |
| `--heading-color` | `#f7f8f8` | Heading text |
| `--paragraph-color` | `#fffc` | Body text |
| `--paragraph-dim` | `#fff9` | Dimmed text |
| `--accent-color` | `#f36725` | Orange accent (CTAs, highlights) |
| `--accent-color-dim` | `#f367251a` | Subtle accent background |
| `--element-stroke-color` | `#4f4f4f7d` | Borders |
| `--element-color-01` | `#7d7d7d45` | Card backgrounds |
| `--element-color-02` | `#36363621` | Secondary backgrounds |
| `--border-background-glow` | `#f36725` | Glow effects |

**White mode variants (prefix `--_white-mode---`):**
| Property | Value |
|----------|-------|
| `--_white-mode---bg-color` | `#fcfdff` |
| `--_white-mode---heading-color` | `#0f131a` |
| `--_white-mode---paragraph-color` | `#000c` |
| `--_white-mode---accent-color` | `#f36725` |

White mode properties are used on specific sections that need a light background.

### Font families

| Font | CSS Variable | Usage |
|------|-------------|-------|
| DM Sans | `--_fonts-spaces---heading-font` | Headings |
| Inter | `--_fonts-spaces---paragraph-font` | Body text |
| Lato | (direct usage) | Legacy Webflow content |
| Open Sans | (direct usage) | Legacy Webflow content |

### Container width

`--_fonts-spaces---container-size: 1200px` is the max content width.

## Page-Specific Styles

Most pages have a `<style>` block in the `<head>` with page-specific CSS. Common patterns:

- **Add-on selection styles**: `.listed-addons`, `#additional_mindbody_locations.selected` (green border on selection)
- **API App logo animation**: `.apiapplogo .pill` with gold gradient animation (`@keyframes goldShine`)
- **Pricing slider styles**: Custom range slider styling for product pages
- **Section-specific overrides**: Layout tweaks, background images, responsive adjustments

## Webflow Class Conventions

The site was originally built in Webflow. All classes follow Webflow's naming:

| Pattern | Example | Purpose |
|---------|---------|---------|
| `w-*` | `w-dropdown`, `w-form`, `w-layout-grid` | Webflow system classes |
| `w--open` | Added dynamically | Webflow dropdown open state |
| `w-mod-*` | `w-mod-js`, `w-mod-touch` | Webflow feature detection |
| Semantic | `nav-bar`, `footer-section`, `hero-section` | Custom Webflow-named classes |

**Do not rename or remove `w-*` classes.** They are tied to `apiant.css` and `components.css` styling and to the Webflow JS runtime (`js/apiant.js`).

## Images and Assets

- **Directory**: `/images/` (900+ files)
- **Naming**: No strict convention; mix of descriptive names and Webflow-generated hashes
- **Formats**: PNG, SVG, AVIF, WebP, JPG
- **Videos**: `/videos/` (MP4 files, some also on YouTube/Wistia)
- **External images**: Some OG images reference `cdn.prod.website-files.com` (Webflow CDN from the original export)

## Cross-Page Update Checklist

When making changes that affect shared elements, use this checklist:

### Nav bar change
- [ ] Update all 43+ HTML files
- [ ] Verify relative link paths are correct for each directory depth (root, `platform/`, `apipartners/`, `apipartners/{vertical}/`, `connect/`, `connections/`)
- [ ] Test dropdown behavior (Webflow JS relies on specific class structure)

### Footer change
- [ ] Update all 43+ HTML files
- [ ] Verify relative link paths

### New product page
- [ ] Create the page in the correct `apipartners/{vertical}/` directory
- [ ] Add to Products mega-dropdown on ALL pages
- [ ] Add to the relevant hub page (Mindbody/Cliniko/DonorPerfect)
- [ ] Update `CLAUDE.md` site architecture
- [ ] Update `SITE-DOCUMENTATION.md`
- [ ] Update `API_APPS_FEATURES.md` if applicable

### Head boilerplate change (analytics, fonts, scripts)
- [ ] Update all 43+ HTML files
- [ ] Account for different relative paths per directory depth

### Tip: Batch updates with grep/sed

Since there's no templating system, use `grep` to find all instances and `sed` for batch replacements:
```bash
# Find all pages containing a specific nav link
grep -rl "old-link-text" --include="*.html" .

# Replace across all HTML files (test with --dry-run first)
sed -i '' 's/old-text/new-text/g' $(grep -rl "old-text" --include="*.html" .)
```
