#!/usr/bin/env python3
"""Generate /sitemap.xml for apiant.com.

Walks the repo, collects indexable HTML pages, emits a canonical sitemap with
hreflang alternates for the 20 supported locales. Run before every deploy.

Excluded from the sitemap:
  - backup/, node_modules/, scripts/, .git/, ai/ working dirs
  - *-next-steps.html and admin/401/404 (noindex)
  - architecture-illustration-v*.html (internal iterations)
  - servlet templates (TEMPLATE_* placeholders)
  - apps2.html, ADOPTION-PLAN.html (internal / deprecated)
"""
import os
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parent.parent
BASE_URL = "https://apiant.com"

LOCALES = [
    "es", "fr", "zh", "hi", "ar", "bn", "pt", "ru", "ja", "de",
    "ko", "it", "nl", "tr", "pl", "vi", "th", "id", "sv", "he",
]

EXCLUDE_DIRS = {
    "backup", "node_modules", ".git", ".claude", "scripts",
    "appResources", "ai", ".uisnap", "__pycache__",
    "connect", "connections",
    "other-pages", "protected-content", "pdf-build",
}

EXCLUDE_FILES = {
    "401.html", "404.html",
    "admin.html", "admin-disabled.html",
    "appconnect-next-steps.html",
    "shopconnect-next-steps.html",
    "mailconnect-next-steps.html",
    "zoomconnect-nextsteps.html",
    "apps2.html",
    "index2.html",
    "temp.html",
    "ADOPTION-PLAN.html",
    "servlettemplateconnect.html",
    "servlettemplateconnections.html",
    "ai-operability.html",
    "workshop-appointment-confirmation.html",
}

EXCLUDE_PATTERNS = [
    re.compile(r"^architecture-illustration(-v\d+)?\.html$"),
    re.compile(r"^index-v\d+\.html$"),
]

PRIORITY_OVERRIDES = {
    "index.html": 1.0,
    "platform/index.html": 0.9,
    "pricing.html": 0.9,
    "ai.html": 0.85,
    "for-saas.html": 0.85,
    "for-si.html": 0.85,
    "for-enterprises.html": 0.85,
    "apps.html": 0.8,
}


def is_locale_dir(name: str) -> bool:
    return name in LOCALES


def should_skip(path: Path) -> bool:
    name = path.name
    if name in EXCLUDE_FILES:
        return True
    for p in EXCLUDE_PATTERNS:
        if p.match(name):
            return True
    return False


def page_has_noindex(path: Path) -> bool:
    try:
        head = path.read_text(encoding="utf-8", errors="ignore")[:8000]
    except OSError:
        return False
    for m in re.finditer(r"<meta\b[^>]*>", head, re.I):
        tag = m.group(0)
        if not re.search(r'name\s*=\s*["\']robots["\']', tag, re.I):
            continue
        if re.search(r'content\s*=\s*["\'][^"\']*noindex', tag, re.I):
            return True
    return False


def url_from_path(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel.endswith("/index.html"):
        rel = rel[: -len("index.html")]
    elif rel == "index.html":
        rel = ""
    return f"{BASE_URL}/{rel}" if rel else f"{BASE_URL}/"


def collect_english_pages() -> list[Path]:
    pages = []
    for dirpath, dirnames, filenames in os.walk(ROOT):
        rel_dir = Path(dirpath).relative_to(ROOT)
        parts = rel_dir.parts
        if parts and parts[0] in EXCLUDE_DIRS:
            dirnames[:] = []
            continue
        if parts and is_locale_dir(parts[0]):
            dirnames[:] = []
            continue
        dirnames[:] = [d for d in dirnames if d not in EXCLUDE_DIRS and not is_locale_dir(d)]
        for fn in filenames:
            if not fn.endswith(".html"):
                continue
            p = Path(dirpath) / fn
            if should_skip(p):
                continue
            if page_has_noindex(p):
                continue
            pages.append(p)
    return sorted(pages)


def locale_url_for(english_path: Path, locale: str) -> str | None:
    """Return the URL of the localized equivalent if it exists."""
    rel = english_path.relative_to(ROOT)
    localized = ROOT / locale / rel
    if not localized.exists():
        return None
    rel_str = rel.as_posix()
    if rel_str.endswith("/index.html"):
        rel_str = rel_str[: -len("index.html")]
    elif rel_str == "index.html":
        rel_str = ""
    return f"{BASE_URL}/{locale}/{rel_str}" if rel_str else f"{BASE_URL}/{locale}/"


def priority_for(path: Path) -> float:
    rel = path.relative_to(ROOT).as_posix()
    if rel in PRIORITY_OVERRIDES:
        return PRIORITY_OVERRIDES[rel]
    if "apipartners/" in rel and rel.count("/") == 1:
        return 0.8
    if "apipartners/" in rel:
        return 0.7
    if rel in {"privacy.html", "cookie-policy.html", "tos.html", "dpa.html"}:
        return 0.3
    return 0.6


def changefreq_for(path: Path) -> str:
    rel = path.relative_to(ROOT).as_posix()
    if rel == "index.html" or rel == "pricing.html":
        return "weekly"
    if rel in {"privacy.html", "cookie-policy.html", "tos.html"}:
        return "yearly"
    return "monthly"


def lastmod_for(path: Path) -> str:
    ts = path.stat().st_mtime
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d")


def build_sitemap(pages: list[Path]) -> str:
    out = ['<?xml version="1.0" encoding="UTF-8"?>']
    out.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"')
    out.append('        xmlns:xhtml="http://www.w3.org/1999/xhtml">')
    for p in pages:
        en_url = url_from_path(p)
        alternates: list[tuple[str, str]] = [("en", en_url)]
        for loc in LOCALES:
            lu = locale_url_for(p, loc)
            if lu:
                alternates.append((loc, lu))
        alternates.append(("x-default", en_url))
        out.append("  <url>")
        out.append(f"    <loc>{escape(en_url)}</loc>")
        out.append(f"    <lastmod>{lastmod_for(p)}</lastmod>")
        out.append(f"    <changefreq>{changefreq_for(p)}</changefreq>")
        out.append(f"    <priority>{priority_for(p):.2f}</priority>")
        for hreflang, url in alternates:
            out.append(
                f'    <xhtml:link rel="alternate" hreflang="{hreflang}" href="{escape(url)}"/>'
            )
        out.append("  </url>")
    out.append("</urlset>")
    return "\n".join(out) + "\n"


def main() -> int:
    pages = collect_english_pages()
    xml = build_sitemap(pages)
    out_path = ROOT / "sitemap.xml"
    out_path.write_text(xml, encoding="utf-8")
    print(f"Wrote {out_path} with {len(pages)} English URLs")
    print(f"Locale alternates checked: {len(LOCALES)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
