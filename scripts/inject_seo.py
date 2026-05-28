#!/usr/bin/env python3
"""Inject SEO + GEO foundation into every English HTML page in the repo.

Idempotent, safe to run repeatedly. For each indexable English page:
  1. Add <script src="/js/gtag-consent.js"></script> just before the
     cookie-consent.js tag (loads gtag with Consent Mode v2 default-denied
     before the banner initializes).
  2. Add <link rel="canonical" href="..."/> pointing at the page's
     apiant.com URL if one isn't present.
  3. On index.html, inject Organization + WebSite JSON-LD schema.
  4. On every API App product page, inject Product JSON-LD schema derived
     from filename (e.g. mindbody-hubspot-...) + meta description.
  5. On apipartners hub pages, inject BreadcrumbList JSON-LD.

Run AFTER editing any English page, BEFORE scripts/update_translations.sh so
localized pages pick up the changes too.
"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://apiant.com"

CONSENT_TAG = '<script src="/js/gtag-consent.js"></script>'
COOKIE_TAG_RE = re.compile(r'<script[^>]+src=["\'][/]?js/cookie-consent\.js["\'][^>]*>\s*</script>', re.I)
CANONICAL_RE = re.compile(r'<link[^>]+rel=["\']canonical["\'][^>]*/?>', re.I)
NOINDEX_META_RE = re.compile(r'<meta\b[^>]*name\s*=\s*["\']robots["\'][^>]*content\s*=\s*["\'][^"\']*noindex', re.I)
NOINDEX_META_REV_RE = re.compile(r'<meta\b[^>]*content\s*=\s*["\'][^"\']*noindex[^"\']*["\'][^>]*name\s*=\s*["\']robots["\']', re.I)
HEAD_CLOSE_RE = re.compile(r'</head>', re.I)
TITLE_RE = re.compile(r'<title>([^<]+)</title>', re.I)
META_DESC_RE = re.compile(r'<meta[^>]*name=["\']description["\'][^>]*content=["\']([^"\']+)["\']', re.I)
META_DESC_REV_RE = re.compile(r'<meta[^>]*content=["\']([^"\']+)["\'][^>]*name=["\']description["\']', re.I)


def find_meta_description(content: str) -> str | None:
    m = META_DESC_RE.search(content)
    if m:
        return m.group(1)
    m = META_DESC_REV_RE.search(content)
    if m:
        return m.group(1)
    return None
SCHEMA_MARKER = '<!-- apiant-seo:schema -->'
FAQ_SCHEMA_MARKER = '<!-- apiant-seo:faq -->'
OGURL_MARKER = '<!-- apiant-seo:ogurl -->'
SOFTWAREAPP_MARKER = '<!-- apiant-seo:softwareapplication -->'
OGURL_TAG_RE = re.compile(r'<meta[^>]+property=["\']og:url["\'][^>]*/?>', re.I)
FAQ_SECTION_RE = re.compile(r'<section\b[^>]*class\s*=\s*["\'][^"\']*\bfaq\b[^"\']*["\'][^>]*>(.*?)</section>', re.I | re.S)
FAQ_ITEM_RE = re.compile(r'<h3[^>]*>(.*?)</h3>\s*<p[^>]*>(.*?)</p>', re.I | re.S)
TAG_RE = re.compile(r'<[^>]+>')

APP_HUB_DESCRIPTIONS = {
    "mindbody": "Turnkey Mindbody integrations connecting your studio platform to CRMs, email marketing, commerce, and video conferencing.",
    "cliniko": "Turnkey Cliniko integrations connecting your clinical practice platform to CRMs and sales pipelines.",
    "donorperfect": "Turnkey DonorPerfect integrations connecting your fundraising platform to CRMs, marketing automation, and email tools.",
}

# Pages that receive E-E-A-T signals: author meta, byline, TechArticle JSON-LD.
# Keys are repo-relative POSIX paths. Values are (datePublished, headline override).
EEAT_PAGES: dict[str, dict] = {
    "ai.html": {
        "datePublished": "2026-02-19",
        "headline": "AI Capabilities: AI That Acts, Not Just Answers",
    },
    "chatbot.html": {
        "datePublished": "2026-02-20",
        "headline": "AI Chatbot Builder: Chatbots That Act on Real Data",
    },
    "mcp-servers.html": {
        "datePublished": "2026-02-19",
        "headline": "MCP Servers: Protocol-Level AI Connectivity",
    },
    "platform/automation-editor.html": {
        "datePublished": "2026-02-19",
        "headline": "Automation Editor: Visual, Powerful, Production-Grade",
    },
    "platform/assembly-editor.html": {
        "datePublished": "2026-02-19",
        "headline": "Assembly Editor and AI Co-Pilot: The AI That Reads API Docs",
    },
}

DATE_MODIFIED = "2026-04-22"
AUTHOR_META_TAG = '<meta content="APIANT Engineering Team" name="author"/>'
AUTHOR_META_RE = re.compile(r'<meta[^>]+name=["\']author["\'][^>]*/?>', re.I)


def is_english_page(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if not rel.parts:
        return False
    first = rel.parts[0]
    if first in {
        "backup", "node_modules", ".git", ".claude", "scripts",
        "appResources", "ai", ".uisnap", "__pycache__",
        "other-pages", "protected-content", "pdf-build",
    }:
        return False
    # Skip locale dirs
    if len(first) == 2 and first.isalpha() and first.islower() and first != "js":
        return False
    # Skip servlet templates. They have {TEMPLATE_*} placeholders the server
    # replaces at serve time. A static canonical or schema would be wrong.
    name = rel.name
    if name in {"servletTemplateConnect.html", "servletTemplateConnections.html"}:
        return False
    return True


def is_indexable(content: str) -> bool:
    return not (NOINDEX_META_RE.search(content) or NOINDEX_META_REV_RE.search(content))


# Directories whose canonical tags must never be rewritten by this script.
# /connect/ and /connections/ are forwarded entirely to Tomcat via mod_jk (the
# static files here are never served), and their pages carry intentional
# cross-page canonicals (e.g. -> /apps.html) that an existing system relies on.
# /connection/ is listed defensively in case such a path is ever added.
CANONICAL_EXCLUDED_DIRS = {"connect", "connection", "connections"}


def is_canonical_excluded(path: Path) -> bool:
    """True if the page lives under an excluded dir, so its canonical is preserved as-is."""
    return path.relative_to(ROOT).parts[0] in CANONICAL_EXCLUDED_DIRS


def url_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return f"{BASE_URL}/"
    if rel.endswith("/index.html"):
        return f"{BASE_URL}/{rel[: -len('index.html')]}"
    if rel.endswith(".html"):
        return f"{BASE_URL}/{rel[: -len('.html')]}"
    return f"{BASE_URL}/{rel}"


def inject_before(content: str, needle_re: re.Pattern, payload: str) -> tuple[str, bool]:
    """Insert payload on its own line immediately before the needle match."""
    m = needle_re.search(content)
    if not m:
        return content, False
    start = m.start()
    line_start = content.rfind("\n", 0, start) + 1
    indent = content[line_start:start]
    new = content[:line_start] + indent + payload + "\n" + content[line_start:]
    return new, True


def inject_before_head_close(content: str, payload: str) -> tuple[str, bool]:
    m = HEAD_CLOSE_RE.search(content)
    if not m:
        return content, False
    idx = m.start()
    return content[:idx] + payload + "\n" + content[idx:], True


def ensure_consent_tag(content: str) -> tuple[str, bool]:
    if CONSENT_TAG in content:
        return content, False
    if COOKIE_TAG_RE.search(content):
        return inject_before(content, COOKIE_TAG_RE, CONSENT_TAG)
    # Page doesn't use the consent banner; skip rather than guessing head placement.
    return content, False


def ensure_canonical(content: str, canonical_url: str, force_if_broken: bool = True) -> tuple[str, bool]:
    existing = CANONICAL_RE.search(content)
    tag = f'<link href="{canonical_url}" rel="canonical"/>'
    if not existing:
        return inject_before_head_close(content, tag)
    if not force_if_broken:
        return content, False
    # Parse the existing href
    href_m = re.search(r'href=["\']([^"\']+)["\']', existing.group(0), re.I)
    if not href_m:
        return content, False
    have = href_m.group(1)
    # Intentional redirect-target canonicals: leave alone if current page is explicitly marked.
    # For self-referential pages, the canonical should equal canonical_url.
    # Allow equivalence: trailing slash vs /index.html.
    def normalize(u: str) -> str:
        u = u.strip()
        if u.endswith("/index.html"):
            u = u[: -len("index.html")]
        if u.startswith("/"):
            u = f"{BASE_URL}{u}"
        return u
    if normalize(have) == normalize(canonical_url):
        return content, False
    # Intentional cross-page canonicals (redirect pages) look like href="/somewhere" on a
    # page whose body has a meta refresh or window.location.replace. Detect that.
    if re.search(r'http-equiv\s*=\s*["\']refresh["\']', content, re.I) or "window.location.replace" in content:
        return content, False
    # Otherwise replace.
    return content.replace(existing.group(0), tag, 1), True


def has_schema_block(content: str) -> bool:
    return SCHEMA_MARKER in content


def schema_block(payloads: list[dict]) -> str:
    parts = [SCHEMA_MARKER]
    for obj in payloads:
        body = json.dumps(obj, indent=2, ensure_ascii=False)
        parts.append(f'<script type="application/ld+json">\n{body}\n</script>')
    return "\n".join(parts)


def org_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "Organization",
        "name": "APIANT",
        "url": "https://apiant.com/",
        "logo": "https://apiant.com/images/apiant-logo.svg",
        "description": "APIANT is a white-label integration platform (iPaaS) for SaaS companies, System Integrators, and enterprises. Dedicated servers, AI co-pilots, embeddable UIs, and a unified data processing engine.",
        "foundingDate": "2014",
        "slogan": "The integration platform builders own.",
        # sameAs: only verified, resolving profiles. linkedin.com/company/apiant
        # returned 404 (WebFetch 2026-04-22). twitter.com/apiant belongs to an
        # unrelated user ("apicellaantonio"). Both removed.
        "sameAs": [
            "https://www.youtube.com/@apiant",
            "https://github.com/apiant",
        ],
    }


def website_schema() -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "WebSite",
        "name": "APIANT",
        "url": "https://apiant.com/",
        "publisher": {"@type": "Organization", "name": "APIANT"},
        "inLanguage": ["en", "es", "fr", "de", "zh", "ja", "pt", "ar", "hi"],
    }


INTEGRATION_LABELS = {
    "activecampaign": "ActiveCampaign",
    "hubspot": "HubSpot",
    "keap": "Keap",
    "klaviyo": "Klaviyo",
    "highlevel": "HighLevel",
    "zoho-crm": "Zoho CRM",
    "salesforce": "Salesforce",
    "shopify": "Shopify",
    "zapier": "Zapier",
    "zoom": "Zoom",
    "calendly": "Calendly",
    "mailchimp": "Mailchimp",
}

PLATFORM_LABELS = {
    "mindbody": "Mindbody",
    "cliniko": "Cliniko",
    "donorperfect": "DonorPerfect",
}


def parse_product_page(path: Path) -> tuple[str, str] | None:
    """Return (platform, integration) e.g. ('mindbody', 'hubspot') or None."""
    stem = path.stem
    parts = path.relative_to(ROOT).parts
    if len(parts) < 3 or parts[0] != "apipartners":
        return None
    platform = parts[1]
    if platform not in PLATFORM_LABELS:
        return None
    m = re.match(rf"{platform}-(.+?)-integration", stem)
    if not m:
        return None
    integration_key = m.group(1)
    if integration_key not in INTEGRATION_LABELS:
        # Handle keys like "zoho-crm"
        alt = integration_key.replace("-", "-")
        if alt not in INTEGRATION_LABELS:
            return None
        integration_key = alt
    return platform, integration_key


def product_schema(path: Path, content: str) -> dict | None:
    parsed = parse_product_page(path)
    if not parsed:
        return None
    platform_key, integration_key = parsed
    platform = PLATFORM_LABELS[platform_key]
    integration = INTEGRATION_LABELS[integration_key]
    name = f"{platform} + {integration} Integration by APIANT"
    desc = find_meta_description(content)
    if not desc:
        desc = f"Bi-directional {platform} and {integration} integration built and maintained by APIANT. Real-time sync of contacts, activity, and custom fields."
    return {
        "@context": "https://schema.org",
        "@type": "Product",
        "name": name,
        "description": desc,
        "brand": {"@type": "Brand", "name": "APIANT"},
        "manufacturer": {"@type": "Organization", "name": "APIANT", "url": "https://apiant.com/"},
        "category": "Integration Platform as a Service",
        "url": url_for(path),
        "audience": {"@type": "BusinessAudience", "audienceType": f"{platform} customers"},
    }


def breadcrumb_schema(path: Path) -> dict | None:
    rel = path.relative_to(ROOT).as_posix()
    parts = rel.split("/")
    if len(parts) < 2:
        return None
    items: list[dict] = [
        {
            "@type": "ListItem",
            "position": 1,
            "name": "APIANT",
            "item": f"{BASE_URL}/",
        }
    ]
    if parts[0] == "apipartners":
        items.append(
            {
                "@type": "ListItem",
                "position": 2,
                "name": "API Partners",
                "item": f"{BASE_URL}/apipartners/",
            }
        )
        # Is this a hub page like mindbody-turnkey-integration-solutions.html?
        if len(parts) == 2 and "turnkey" in parts[1]:
            platform_key = parts[1].split("-")[0]
            if platform_key in PLATFORM_LABELS:
                items.append(
                    {
                        "@type": "ListItem",
                        "position": 3,
                        "name": f"{PLATFORM_LABELS[platform_key]} Integrations",
                        "item": url_for(path),
                    }
                )
        # Is this a product page like apipartners/mindbody/...?
        elif len(parts) == 3 and parts[1] in PLATFORM_LABELS:
            platform_key = parts[1]
            items.append(
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": f"{PLATFORM_LABELS[platform_key]} Integrations",
                    "item": f"{BASE_URL}/apipartners/{platform_key}-turnkey-integration-solutions",
                }
            )
            parsed = parse_product_page(path)
            if parsed:
                _, integration_key = parsed
                items.append(
                    {
                        "@type": "ListItem",
                        "position": 4,
                        "name": f"{PLATFORM_LABELS[platform_key]} + {INTEGRATION_LABELS[integration_key]}",
                        "item": url_for(path),
                    }
                )
        else:
            return None
    elif parts[0] == "platform":
        items.append(
            {
                "@type": "ListItem",
                "position": 2,
                "name": "Platform",
                "item": f"{BASE_URL}/platform/",
            }
        )
        if parts[-1] not in {"index.html", ""}:
            title_match = TITLE_RE.search(path.read_text(encoding="utf-8", errors="ignore")[:2000])
            page_name = (title_match.group(1).split("|")[0].strip() if title_match else parts[-1])
            items.append(
                {
                    "@type": "ListItem",
                    "position": 3,
                    "name": page_name,
                    "item": url_for(path),
                }
            )
    else:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "BreadcrumbList",
        "itemListElement": items,
    }


# Pages that receive a SoftwareApplication JSON-LD block. Keys are repo-relative POSIX.
SOFTWAREAPP_PAGES: dict[str, dict] = {
    "platform/index.html": {
        "name": "APIANT iPaaS",
        "applicationCategory": "BusinessApplication",
        "description": "APIANT is a white-label integration platform (iPaaS) for SaaS companies, System Integrators, and enterprises. Dedicated servers, AI co-pilots, embeddable UIs, and a unified data processing engine.",
        "featureList": [
            "Dedicated infrastructure per customer, no shared multi-tenant servers",
            "Fully white-label down to the embeddable end-user UI",
            "Unified data processing engine for JSON, XML, CSV, EDI, HL7, binary",
            "AI co-pilots for automation authoring and connector generation",
            "Admin console for multi-tenant management and usage monitoring",
            "Deployable in SaaS, customer cloud, or on-premise",
        ],
        "offersUrl": "https://apiant.com/platform/index.html",
    },
    "platform/assembly-editor.html": {
        "name": "APIANT Assembly Editor",
        "applicationCategory": "DeveloperApplication",
        "description": "The Assembly Editor builds and edits API connectors. The AI Co-Pilot reads third-party API documentation and generates working connectors automatically, reducing new-integration build time from weeks to hours.",
        "featureList": [
            "AI Co-Pilot reads API docs and generates connectors",
            "Visual authoring of triggers, actions, and mappings",
            "XPath-based transformations across every supported data format",
            "Version control and commit history per assembly",
            "Reusable connector patterns",
        ],
        "offersUrl": "https://apiant.com/platform/assembly-editor.html",
    },
    "mcp-servers.html": {
        "name": "APIANT MCP Server",
        "applicationCategory": "DeveloperApplication",
        "description": "APIANT MCP Servers expose the integration platform to Claude, ChatGPT, and other LLM agents over the Model Context Protocol, so agents can list, configure, and execute integrations as first-class tools.",
        "featureList": [
            "Model Context Protocol server for LLM agents",
            "Agent-callable integration tools across 500+ connectors",
            "Dev and prod environments with scoped tool access",
            "Works with Claude Code, Claude Desktop, ChatGPT, and other MCP clients",
            "OAuth-scoped tool authorization",
        ],
        "offersUrl": "https://apiant.com/mcp-servers.html",
    },
    "ai-operability.html": {
        "name": "APIANT Claude Code Plugin",
        "applicationCategory": "DeveloperApplication",
        "description": "APIANT's Claude Code plugin exposes 35 skills and 125 MCP tools for building, editing, testing, and deploying integrations from the terminal. The first iPaaS operable end-to-end by Claude Code.",
        "featureList": [
            "Build new automations from natural-language prompts",
            "Build and edit app assemblies (connectors, triggers, actions)",
            "Test automations end-to-end with branch coverage",
            "Deploy dev to prod across linked customer accounts",
            "Diagnose customer issues via execution history and log search",
            "Design and wire Human Interaction forms",
            "Reusable pattern library (chat widgets, CSV mappings, fan-out/fan-in, human moderation, snoozes)",
            "Two-way bidirectional sync with loop prevention",
        ],
        "offersUrl": "https://apiant.com/platform/index.html",
    },
}


def software_application_schema(path: Path) -> dict | None:
    rel = path.relative_to(ROOT).as_posix()
    meta = SOFTWAREAPP_PAGES.get(rel)
    if not meta:
        return None
    return {
        "@context": "https://schema.org",
        "@type": "SoftwareApplication",
        "name": meta["name"],
        "applicationCategory": meta["applicationCategory"],
        "operatingSystem": "Cloud, macOS, Windows, Linux",
        "description": meta["description"],
        "featureList": meta["featureList"],
        "offers": {
            "@type": "Offer",
            "url": meta["offersUrl"],
            "priceCurrency": "USD",
            "availability": "https://schema.org/InStock",
        },
        "publisher": {
            "@type": "Organization",
            "name": "APIANT",
            "url": "https://apiant.com",
        },
    }


def tech_article_schema(path: Path, content: str) -> dict | None:
    rel = path.relative_to(ROOT).as_posix()
    meta = EEAT_PAGES.get(rel)
    if not meta:
        return None
    title_m = TITLE_RE.search(content)
    title_text = title_m.group(1).strip() if title_m else meta.get("headline", "")
    desc_val = find_meta_description(content)
    desc = desc_val.strip() if desc_val else None
    return {
        "@context": "https://schema.org",
        "@type": "TechArticle",
        "headline": meta.get("headline", title_text),
        "name": title_text,
        "description": desc or meta.get("headline", title_text),
        "author": {
            "@type": "Organization",
            "name": "APIANT Engineering Team",
            "url": "https://apiant.com/",
        },
        "publisher": {
            "@type": "Organization",
            "name": "APIANT",
            "url": "https://apiant.com/",
            "logo": {
                "@type": "ImageObject",
                "url": "https://apiant.com/images/apiant-logo.svg",
            },
        },
        "datePublished": meta["datePublished"],
        "dateModified": DATE_MODIFIED,
        "mainEntityOfPage": {
            "@type": "WebPage",
            "@id": url_for(path),
        },
    }


def schemas_for(path: Path, content: str) -> list[dict]:
    rel = path.relative_to(ROOT).as_posix()
    schemas: list[dict] = []
    if rel == "index.html":
        schemas.append(org_schema())
        schemas.append(website_schema())
        return schemas
    # E-E-A-T technical pages: TechArticle + Breadcrumb (if on platform)
    ta = tech_article_schema(path, content)
    if ta:
        schemas.append(ta)
        bs = breadcrumb_schema(path)
        if bs:
            schemas.append(bs)
        # E-E-A-T + SoftwareApplication can coexist (mcp-servers.html, assembly-editor.html)
        sa = software_application_schema(path)
        if sa:
            schemas.append(sa)
        return schemas
    # API App product pages: Product + Breadcrumb
    ps = product_schema(path, content)
    if ps:
        schemas.append(ps)
    bs = breadcrumb_schema(path)
    if bs:
        schemas.append(bs)
    # SoftwareApplication for pages not otherwise covered (platform/index, ai-operability)
    if not schemas:
        sa = software_application_schema(path)
        if sa:
            schemas.append(sa)
            bs = breadcrumb_schema(path)
            if bs:
                schemas.append(bs)
    else:
        # If the page also has a SoftwareApplication entry (e.g. platform/index.html
        # hits breadcrumb only above, so "schemas" already holds the breadcrumb), append SA.
        sa = software_application_schema(path)
        if sa and not any(s.get("@type") == "SoftwareApplication" for s in schemas):
            schemas.append(sa)
    return schemas


def ensure_author_meta(path: Path, content: str) -> tuple[str, bool]:
    """Inject <meta name="author"> on E-E-A-T pages, right after the title tag."""
    rel = path.relative_to(ROOT).as_posix()
    if rel not in EEAT_PAGES:
        return content, False
    if AUTHOR_META_RE.search(content):
        return content, False
    # Insert immediately after the <title>...</title> line.
    m = TITLE_RE.search(content)
    if not m:
        return inject_before_head_close(content, AUTHOR_META_TAG)
    end = m.end()
    return content[:end] + "\n" + AUTHOR_META_TAG + content[end:], True


def ensure_schema(path: Path, content: str) -> tuple[str, bool]:
    rel = path.relative_to(ROOT).as_posix()
    changed_any = False
    # Fast path: nothing yet, write the full block.
    if not has_schema_block(content):
        schemas = schemas_for(path, content)
        if not schemas:
            return content, False
        block = schema_block(schemas)
        return inject_before_head_close(content, block)
    # Schema block exists. If this is an E-E-A-T page that still lacks TechArticle,
    # append only the TechArticle JSON-LD to the existing block.
    if rel in EEAT_PAGES and '"TechArticle"' not in content:
        ta = tech_article_schema(path, content)
        if ta:
            body = json.dumps(ta, indent=2, ensure_ascii=False)
            snippet = f'<script type="application/ld+json">\n{body}\n</script>\n'
            content, ok = inject_before_head_close(content, snippet)
            if ok:
                changed_any = True
    # SoftwareApplication: if the page is eligible and the schema isn't already in the file, add it.
    if rel in SOFTWAREAPP_PAGES and '"SoftwareApplication"' not in content:
        sa = software_application_schema(path)
        if sa:
            body = json.dumps(sa, indent=2, ensure_ascii=False)
            snippet = f'{SOFTWAREAPP_MARKER}\n<script type="application/ld+json">\n{body}\n</script>\n'
            content, ok = inject_before_head_close(content, snippet)
            if ok:
                changed_any = True
    # Homepage: refresh Organization schema if sameAs still lists removed profiles.
    if rel == "index.html" and (
        "linkedin.com/company/apiant" in content or "twitter.com/apiant" in content
    ):
        content, ok = refresh_homepage_schema(content)
        if ok:
            changed_any = True
    return content, changed_any


def ensure_og_url(content: str, canonical_url: str) -> tuple[str, bool]:
    """Inject <meta property="og:url" content="<canonical>"/> on any indexable page."""
    if OGURL_TAG_RE.search(content):
        return content, False
    tag = f'{OGURL_MARKER}\n<meta content="{canonical_url}" property="og:url"/>'
    return inject_before_head_close(content, tag)


def refresh_homepage_schema(content: str) -> tuple[str, bool]:
    """Regenerate the Org+WebSite schema block in-place on the homepage."""
    # Find the schema marker and everything up through the last closing </script>
    # that belongs to the block (the block is <marker>\n<script>..</script>\n<script>..</script>).
    m = re.search(
        r"(<!-- apiant-seo:schema -->\s*(?:<script type=\"application/ld\+json\">.*?</script>\s*)+)",
        content,
        re.DOTALL,
    )
    if not m:
        return content, False
    new_block = schema_block([org_schema(), website_schema()]) + "\n"
    new_content = content[: m.start()] + new_block + content[m.end() :]
    return new_content, True


def clean_html_text(html: str) -> str:
    """Strip tags, collapse whitespace, and decode a handful of common entities."""
    text = TAG_RE.sub('', html)
    text = (text
            .replace('&amp;', '&')
            .replace('&lt;', '<')
            .replace('&gt;', '>')
            .replace('&quot;', '"')
            .replace('&#39;', "'")
            .replace('&rsquo;', "'")
            .replace('&lsquo;', "'")
            .replace('&ldquo;', '"')
            .replace('&rdquo;', '"')
            .replace('&nbsp;', ' ')
            .replace('&ndash;', '-'))
    return re.sub(r'\s+', ' ', text).strip()


def extract_faq_items(content: str) -> list[tuple[str, str]]:
    """Find the first <section class="faq">...</section> and extract (Q, A) pairs."""
    m = FAQ_SECTION_RE.search(content)
    if not m:
        return []
    body = m.group(1)
    items = []
    for im in FAQ_ITEM_RE.finditer(body):
        q = clean_html_text(im.group(1))
        a = clean_html_text(im.group(2))
        if q and a and q.endswith('?'):
            items.append((q, a))
    return items


def faq_schema(items: list[tuple[str, str]]) -> dict:
    return {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": q,
                "acceptedAnswer": {"@type": "Answer", "text": a},
            }
            for q, a in items
        ],
    }


def faq_schema_block(items: list[tuple[str, str]]) -> str:
    body = json.dumps(faq_schema(items), indent=2, ensure_ascii=False)
    return f'{FAQ_SCHEMA_MARKER}\n<script type="application/ld+json">\n{body}\n</script>'


def ensure_faq_schema(content: str) -> tuple[str, bool]:
    items = extract_faq_items(content)
    if not items:
        return content, False
    if FAQ_SCHEMA_MARKER in content:
        # Rebuild if the set of questions has changed so schema stays in sync with copy.
        new_block = faq_schema_block(items)
        pattern = re.compile(
            re.escape(FAQ_SCHEMA_MARKER)
            + r'\s*<script type="application/ld\+json">\s*\{.*?\}\s*</script>',
            re.S,
        )
        updated, n = pattern.subn(new_block, content, count=1)
        if n and updated != content:
            return updated, True
        return content, False
    return inject_before_head_close(content, faq_schema_block(items))


HREFLANG_RE = re.compile(r'<link\b[^>]*hreflang\s*=\s*["\']([^"\']+)["\'][^>]*>', re.I)


def dedupe_hreflang(content: str) -> tuple[str, bool]:
    """Keep the first occurrence of each hreflang value, remove the rest."""
    matches = list(HREFLANG_RE.finditer(content))
    if len(matches) <= 1:
        return content, False
    seen: dict[str, int] = {}
    to_remove: list[tuple[int, int]] = []
    for m in matches:
        lang = m.group(1).lower()
        if lang in seen:
            start = m.start()
            end = m.end()
            line_start = content.rfind("\n", 0, start) + 1
            line_end_idx = content.find("\n", end)
            # Only swallow the whole line if it's just whitespace + the tag
            if line_end_idx != -1:
                between = content[line_start:start]
                after = content[end:line_end_idx]
                if between.strip() == "" and after.strip() == "":
                    to_remove.append((line_start, line_end_idx + 1))
                    continue
            to_remove.append((start, end))
        else:
            seen[lang] = m.start()
    if not to_remove:
        return content, False
    # Apply removals from the end so earlier offsets stay valid.
    for start, end in sorted(to_remove, reverse=True):
        content = content[:start] + content[end:]
    return content, True


def process_file(path: Path) -> dict:
    original = path.read_text(encoding="utf-8")
    if not is_indexable(original):
        return {"path": str(path.relative_to(ROOT)), "skipped": "noindex"}
    content = original
    ops = []
    content, changed = ensure_consent_tag(content)
    if changed:
        ops.append("consent")
    canonical_excluded = is_canonical_excluded(path)
    if not canonical_excluded:
        content, changed = ensure_canonical(content, url_for(path))
        if changed:
            ops.append("canonical")
    content, changed = ensure_og_url(content, url_for(path))
    if changed:
        ops.append("og_url")
    content, changed = ensure_author_meta(path, content)
    if changed:
        ops.append("author_meta")
    content, changed = ensure_schema(path, content)
    if changed:
        ops.append("schema")
    content, changed = ensure_faq_schema(content)
    if changed:
        ops.append("faq_schema")
    content, changed = dedupe_hreflang(content)
    if changed:
        ops.append("hreflang_dedup")
    if content != original:
        path.write_text(content, encoding="utf-8")
    return {
        "path": str(path.relative_to(ROOT)),
        "ops": ops,
        "canonical_excluded": canonical_excluded,
    }


def walk_english_pages() -> list[Path]:
    out = []
    for p in ROOT.rglob("*.html"):
        if not is_english_page(p):
            continue
        out.append(p)
    return sorted(out)


def main() -> int:
    results = []
    for p in walk_english_pages():
        results.append(process_file(p))
    n_changed = sum(1 for r in results if r.get("ops"))
    n_total = len(results)
    print(f"Processed {n_total} English HTML files, modified {n_changed}")
    op_counts = {}
    for r in results:
        for op in r.get("ops", []):
            op_counts[op] = op_counts.get(op, 0) + 1
    for op, n in sorted(op_counts.items()):
        print(f"  {op}: {n}")
    skipped = [r for r in results if r.get("skipped")]
    if skipped:
        print(f"Skipped {len(skipped)} noindex pages")
    canon_excluded = [r for r in results if r.get("canonical_excluded")]
    if canon_excluded:
        print(f"Preserved canonical on {len(canon_excluded)} excluded pages (connect/connection/connections)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
