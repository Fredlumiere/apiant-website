#!/usr/bin/env python3
"""Apply performance optimizations to every English HTML page.

Idempotent. Safe to run repeatedly. What it does per page:

  1. Ensure <link rel="preconnect" href="https://fonts.googleapis.com"> and
     <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin> exist
     near the top of <head>.
  2. Replace the Google WebFont loader <script> (major LCP blocker) with
     native <link rel="preload" as="style"> + <link rel="stylesheet"
     ...&display=swap> for Lato, Open Sans, DM Sans, Inter.
  3. Add loading="lazy" and decoding="async" to below-the-fold <img> tags
     that don't already have them (first 2 body images are left eager so
     we don't hurt LCP).
  4. Add <link rel="preload" as="image" fetchpriority="high"> for an obvious
     hero image when one is clearly the LCP (img with class containing
     "hero-animation-image" and a populated src). Conservative, skips when
     uncertain.

Run after editing English pages. Follow with scripts/inject_seo.py and
scripts/localize.py (or bash scripts/update_translations.sh) to regenerate
localized copies.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

# Shared locale/skip rules match inject_seo.py behavior.
SKIP_TOP_DIRS = {
    "backup", "node_modules", ".git", ".claude", "scripts",
    "appResources", "ai", ".uisnap", "__pycache__",
    "other-pages", "protected-content", "pdf-build",
    "i18n", "supabase", "private", "docs", "video", "videos",
    "images", "css", "js", "fonts", "appResources",
}
LOCALE_DIRS = {
    "es", "fr", "de", "zh", "ja", "pt", "ar", "hi", "bn", "ru",
    "ko", "it", "nl", "tr", "pl", "vi", "th", "id", "sv", "he",
}
SKIP_FILES = {
    "servletTemplateConnect.html",
    "servletTemplateConnections.html",
}
# Only skip these when they live at the repo root (they are admin/test/
# scaffolding pages). `platform/admin-console.html` is a legitimate product
# page that happens to start with "admin", so we guard on relative depth.
SKIP_ROOT_PREFIXES = (
    "admin", "test", "temp", "architecture-illustration",
    "401", "404",
)

PRECONNECT_GOOGLEAPIS = '<link href="https://fonts.googleapis.com" rel="preconnect"/>'
PRECONNECT_GSTATIC = '<link crossorigin="anonymous" href="https://fonts.gstatic.com" rel="preconnect"/>'

# Single combined Google Fonts URL covering the four families WebFont was loading.
FONTS_HREF = (
    "https://fonts.googleapis.com/css2"
    "?family=DM+Sans:wght@300;400;500;600;700"
    "&family=Inter:wght@300;400;500;600;700"
    "&family=Lato:ital,wght@0,100;0,300;0,400;0,700;0,900;1,100;1,300;1,400;1,700;1,900"
    "&family=Open+Sans:ital,wght@0,300;0,400;0,600;0,700;0,800;1,300;1,400;1,600;1,700;1,800"
    "&display=swap"
)
FONTS_PRELOAD = f'<link rel="preload" as="style" href="{FONTS_HREF}"/>'
FONTS_STYLESHEET = f'<link rel="stylesheet" href="{FONTS_HREF}" media="print" onload="this.media=\'all\'"/>'
FONTS_NOSCRIPT = f'<noscript><link rel="stylesheet" href="{FONTS_HREF}"/></noscript>'

PERF_FONT_MARKER = "<!-- apiant-perf:fonts -->"
PERF_HERO_MARKER = "<!-- apiant-perf:hero-preload -->"

HEAD_OPEN_RE = re.compile(r"<head\b[^>]*>", re.I)
HEAD_CLOSE_RE = re.compile(r"</head>", re.I)
BODY_OPEN_RE = re.compile(r"<body\b[^>]*>", re.I)

WEBFONT_SCRIPT_RE = re.compile(
    r'<script[^>]*src=["\']https://ajax\.googleapis\.com/ajax/libs/webfont/[^"\']+["\'][^>]*>\s*</script>\s*'
    r'<script[^>]*>\s*(?:WebFont|!\s*function).*?WebFont\.load\s*\(\s*\{.*?\}\s*\)\s*;?\s*</script>',
    re.I | re.S,
)
# Fallback for pages where the two scripts are separated: strip just the WebFont.load block and the loader.
WEBFONT_LOADER_TAG_RE = re.compile(
    r'<script[^>]*src=["\']https://ajax\.googleapis\.com/ajax/libs/webfont/[^"\']+["\'][^>]*>\s*</script>',
    re.I,
)
WEBFONT_LOAD_INLINE_RE = re.compile(
    r'<script[^>]*>\s*WebFont\.load\s*\(\s*\{.*?\}\s*\)\s*;?\s*</script>',
    re.I | re.S,
)

# Match <img ...> tags (self-closing or not). Group 0 is full tag. Used for
# below-the-fold lazy-loading. Does not attempt to be a general HTML parser.
IMG_TAG_RE = re.compile(r"<img\b[^>]*/?>", re.I)


def is_english_page(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    parts = rel.parts
    if not parts:
        return False
    first = parts[0]
    if first in SKIP_TOP_DIRS:
        return False
    if first in LOCALE_DIRS:
        return False
    # Skip generic 2-letter locale dirs (catch-all for future additions).
    if len(first) == 2 and first.isalpha() and first.islower():
        return False
    name = rel.name
    if name in SKIP_FILES:
        return False
    # Root-level only: scaffolding/admin pages.
    if len(parts) == 1:
        for prefix in SKIP_ROOT_PREFIXES:
            if name.startswith(prefix):
                return False
    return True


def ensure_preconnects(content: str) -> tuple[str, bool]:
    changed = False
    # If already present (exact string), no-op. Webflow output varies slightly, so
    # we normalize: look for "fonts.googleapis.com" with rel="preconnect" nearby.
    has_goog = bool(re.search(
        r'<link\b[^>]*rel=["\']preconnect["\'][^>]*fonts\.googleapis\.com|fonts\.googleapis\.com[^>]*rel=["\']preconnect["\']',
        content, re.I,
    ))
    has_gstatic = bool(re.search(
        r'<link\b[^>]*rel=["\']preconnect["\'][^>]*fonts\.gstatic\.com|fonts\.gstatic\.com[^>]*rel=["\']preconnect["\']',
        content, re.I,
    ))
    # Insert missing ones right after the <head> opening tag (or after the
    # charset/title cluster if we can find it). We chain the inserts so they
    # stay adjacent.
    to_insert = []
    if not has_goog:
        to_insert.append(PRECONNECT_GOOGLEAPIS)
    if not has_gstatic:
        to_insert.append(PRECONNECT_GSTATIC)
    if not to_insert:
        return content, False
    m = HEAD_OPEN_RE.search(content)
    if not m:
        return content, False
    insert_at = m.end()
    block = "\n" + "\n".join(to_insert)
    return content[:insert_at] + block + content[insert_at:], True


def replace_webfont_loader(content: str) -> tuple[str, bool]:
    """Swap the WebFont.load script for native <link> stylesheets."""
    if PERF_FONT_MARKER in content:
        return content, False
    replacement = (
        f"{PERF_FONT_MARKER}\n"
        f"{FONTS_PRELOAD}\n"
        f"{FONTS_STYLESHEET}\n"
        f"{FONTS_NOSCRIPT}"
    )
    # Try combined match first.
    new = WEBFONT_SCRIPT_RE.sub(replacement, content, count=1)
    if new != content:
        return new, True
    # Fallback: remove loader script and the inline WebFont.load block separately.
    had_loader = bool(WEBFONT_LOADER_TAG_RE.search(content))
    had_inline = bool(WEBFONT_LOAD_INLINE_RE.search(content))
    if not (had_loader or had_inline):
        return content, False
    new = WEBFONT_LOADER_TAG_RE.sub("", content, count=1)
    new = WEBFONT_LOAD_INLINE_RE.sub(replacement, new, count=1)
    # If only the loader tag was present (no inline .load block), we still need
    # to inject the stylesheet. Insert before </head>.
    if PERF_FONT_MARKER not in new:
        close = HEAD_CLOSE_RE.search(new)
        if close:
            new = new[:close.start()] + replacement + "\n" + new[close.start():]
    return new, True


def lazy_load_below_fold_images(content: str) -> tuple[str, int]:
    """Add loading="lazy" decoding="async" to <img> tags below the fold.

    "Below the fold" heuristic: skip the first 2 body <img> tags; lazy-load
    the rest. Images already marked eager or lazy are left alone. Images with
    width/height attributes missing are untouched otherwise (we only add
    two attributes).
    """
    body_m = BODY_OPEN_RE.search(content)
    if not body_m:
        return content, 0
    body_start = body_m.end()
    head_part = content[:body_start]
    body_part = content[body_start:]

    count_seen = 0
    count_changed = 0

    def rewrite(match: re.Match) -> str:
        nonlocal count_seen, count_changed
        tag = match.group(0)
        count_seen += 1
        # Keep first 2 images eager to preserve LCP.
        if count_seen <= 2:
            return tag
        # Already has loading attribute.
        if re.search(r'\bloading\s*=\s*["\'][^"\']*["\']', tag, re.I):
            has_loading = True
        else:
            has_loading = False
        if re.search(r'\bdecoding\s*=\s*["\'][^"\']*["\']', tag, re.I):
            has_decoding = True
        else:
            has_decoding = False
        if has_loading and has_decoding:
            return tag
        # Insert attributes just before the closing > (respect self-closing />).
        if tag.endswith("/>"):
            closing = "/>"
            inner = tag[:-2].rstrip()
        else:
            closing = ">"
            inner = tag[:-1].rstrip()
        additions = []
        if not has_loading:
            additions.append('loading="lazy"')
        if not has_decoding:
            additions.append('decoding="async"')
        new_tag = inner + " " + " ".join(additions) + closing
        count_changed += 1
        return new_tag

    body_part_new = IMG_TAG_RE.sub(rewrite, body_part)
    if count_changed == 0:
        return content, 0
    return head_part + body_part_new, count_changed


HERO_IMG_RE = re.compile(
    r'<img\b[^>]*class=["\'][^"\']*hero-animation-image[^"\']*["\'][^>]*src=["\']([^"\']+)["\'][^>]*>',
    re.I,
)


def preload_hero_image(content: str) -> tuple[str, bool]:
    if PERF_HERO_MARKER in content:
        return content, False
    m = HERO_IMG_RE.search(content)
    if not m:
        return content, False
    tag = m.group(0)
    # Skip if the hero img is hidden (Webflow `hide` class is applied on many
    # pages where the element is a fallback for a background video).
    class_m = re.search(r'class=["\']([^"\']+)["\']', tag, re.I)
    if class_m and re.search(r'\bhide\b', class_m.group(1)):
        return content, False
    src = m.group(1)
    # Skip data URIs and transparent spacer gifs.
    if src.startswith("data:") or src.endswith(".svg"):
        return content, False
    # Look for a srcset so we can preload the responsive variant.
    srcset_m = re.search(r'srcset=["\']([^"\']+)["\']', m.group(0), re.I)
    sizes_m = re.search(r'sizes=["\']([^"\']+)["\']', m.group(0), re.I)
    attrs = [
        f'href="{src}"',
        'rel="preload"',
        'as="image"',
        'fetchpriority="high"',
    ]
    if srcset_m:
        attrs.append(f'imagesrcset="{srcset_m.group(1)}"')
    if sizes_m:
        attrs.append(f'imagesizes="{sizes_m.group(1)}"')
    tag = f"{PERF_HERO_MARKER}\n<link {' '.join(attrs)}/>"
    close = HEAD_CLOSE_RE.search(content)
    if not close:
        return content, False
    return content[:close.start()] + tag + "\n" + content[close.start():], True


def process_file(path: Path) -> dict:
    original = path.read_text(encoding="utf-8")
    content = original
    ops: list[str] = []

    content, changed = ensure_preconnects(content)
    if changed:
        ops.append("preconnect")

    content, changed = replace_webfont_loader(content)
    if changed:
        ops.append("fonts")

    content, n_lazy = lazy_load_below_fold_images(content)
    if n_lazy:
        ops.append(f"lazy:{n_lazy}")

    content, changed = preload_hero_image(content)
    if changed:
        ops.append("hero_preload")

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
    n_changed = sum(1 for r in results if r["ops"])
    n_total = len(results)
    print(f"perf_fixes: processed {n_total} English HTML files, modified {n_changed}")
    op_counts: dict[str, int] = {}
    for r in results:
        for op in r["ops"]:
            key = op.split(":", 1)[0]
            op_counts[key] = op_counts.get(key, 0) + 1
    for op, n in sorted(op_counts.items()):
        print(f"  {op}: {n}")
    # Surface heavy-lazy pages for inspection.
    lazy_pages = [(r["path"], int(op.split(":", 1)[1])) for r in results for op in r["ops"] if op.startswith("lazy:")]
    lazy_pages.sort(key=lambda x: -x[1])
    if lazy_pages[:5]:
        print("top lazy counts:")
        for p, n in lazy_pages[:5]:
            print(f"  {n:4d}  {p}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
