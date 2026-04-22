#!/usr/bin/env python3
"""Inject SEO + GEO foundation into every English HTML page in the repo.

Idempotent — safe to run repeatedly. For each indexable English page:
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
SCHEMA_MARKER = '<!-- apiant-seo:schema -->'

APP_HUB_DESCRIPTIONS = {
    "mindbody": "Turnkey Mindbody integrations connecting your studio platform to CRMs, email marketing, commerce, and video conferencing.",
    "cliniko": "Turnkey Cliniko integrations connecting your clinical practice platform to CRMs and sales pipelines.",
    "donorperfect": "Turnkey DonorPerfect integrations connecting your fundraising platform to CRMs, marketing automation, and email tools.",
}


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
    # Skip servlet templates — they have {TEMPLATE_*} placeholders the server
    # replaces at serve time. A static canonical or schema would be wrong.
    name = rel.name
    if name in {"servlettemplateconnect.html", "servlettemplateconnections.html"}:
        return False
    return True


def is_indexable(content: str) -> bool:
    return not (NOINDEX_META_RE.search(content) or NOINDEX_META_REV_RE.search(content))


def url_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html":
        return f"{BASE_URL}/"
    if rel.endswith("/index.html"):
        return f"{BASE_URL}/{rel[: -len('index.html')]}"
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
        "sameAs": [
            "https://www.linkedin.com/company/apiant",
            "https://twitter.com/apiant",
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
    desc = None
    m = META_DESC_RE.search(content)
    if m:
        desc = m.group(1)
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
                    "item": f"{BASE_URL}/apipartners/{platform_key}-turnkey-integration-solutions.html",
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


def schemas_for(path: Path, content: str) -> list[dict]:
    rel = path.relative_to(ROOT).as_posix()
    schemas: list[dict] = []
    if rel == "index.html":
        schemas.append(org_schema())
        schemas.append(website_schema())
        return schemas
    # API App product pages: Product + Breadcrumb
    ps = product_schema(path, content)
    if ps:
        schemas.append(ps)
    bs = breadcrumb_schema(path)
    if bs:
        schemas.append(bs)
    return schemas


def ensure_schema(path: Path, content: str) -> tuple[str, bool]:
    if has_schema_block(content):
        return content, False
    schemas = schemas_for(path, content)
    if not schemas:
        return content, False
    block = schema_block(schemas)
    return inject_before_head_close(content, block)


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
    content, changed = ensure_canonical(content, url_for(path))
    if changed:
        ops.append("canonical")
    content, changed = ensure_schema(path, content)
    if changed:
        ops.append("schema")
    content, changed = dedupe_hreflang(content)
    if changed:
        ops.append("hreflang_dedup")
    if content != original:
        path.write_text(content, encoding="utf-8")
    return {"path": str(path.relative_to(ROOT)), "ops": ops}


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
    return 0


if __name__ == "__main__":
    sys.exit(main())
