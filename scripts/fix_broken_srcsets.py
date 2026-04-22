#!/usr/bin/env python3
"""Strip broken srcset entries across the repo.

Webflow's export inserted responsive srcset entries of the form
`<basename>_1<basename>.<ext>` (e.g., `cliniko-app_1cliniko-app.avif`) that
were never actually generated as files. The result: 404 console errors on
every page that loaded those images and lighthouse best-practices penalties.

This script walks every indexable English HTML page (localized copies
regenerate from English via scripts/localize.py, so we don't edit them),
parses each <img srcset="...">, drops entries whose file doesn't exist
relative to /images/, and removes the srcset attribute entirely if
everything is broken. The <src> attribute stays untouched as the browser
fallback.

Idempotent.
"""
import re
import sys
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent.parent
IMAGES_DIR = ROOT / "images"

SRCSET_RE = re.compile(r'\ssrcset="([^"]+)"', re.I)


def resolve_to_repo(url: str, page_path: Path) -> Path | None:
    """Resolve a relative or absolute URL to a path under /images/."""
    parsed = urlparse(url.strip())
    if parsed.scheme or parsed.netloc:
        return None  # external, leave alone
    path = parsed.path
    if path.startswith("/"):
        return ROOT / path.lstrip("/")
    # Relative: resolve against the page's directory
    candidate = (page_path.parent / path).resolve()
    # Guard against escaping the repo
    try:
        candidate.relative_to(ROOT)
    except ValueError:
        return None
    return candidate


def split_srcset_entries(srcset: str) -> list[tuple[str, str]]:
    """Parse srcset into list of (url, descriptor) pairs."""
    out = []
    for raw in srcset.split(","):
        raw = raw.strip()
        if not raw:
            continue
        # Split once on whitespace
        parts = raw.split(None, 1)
        url = parts[0]
        descriptor = parts[1] if len(parts) > 1 else ""
        out.append((url, descriptor))
    return out


def filter_srcset(srcset: str, page_path: Path) -> tuple[str, int]:
    """Return (new_srcset, removed_count)."""
    entries = split_srcset_entries(srcset)
    kept = []
    removed = 0
    for url, desc in entries:
        resolved = resolve_to_repo(url, page_path)
        if resolved is None:
            kept.append((url, desc))  # external, keep
            continue
        if resolved.exists():
            kept.append((url, desc))
        else:
            removed += 1
    new = ", ".join((u + (" " + d if d else "")) for u, d in kept)
    return new, removed


def process_file(path: Path) -> dict:
    original = path.read_text(encoding="utf-8", errors="ignore")
    changed = 0
    total_removed = 0

    def replace(m):
        nonlocal changed, total_removed
        srcset = m.group(1)
        new, removed = filter_srcset(srcset, path)
        if removed == 0:
            return m.group(0)
        changed += 1
        total_removed += removed
        if not new.strip():
            # Drop the whole attribute
            return ""
        return f' srcset="{new}"'

    new_content = SRCSET_RE.sub(replace, original)
    if new_content != original:
        path.write_text(new_content, encoding="utf-8")
    return {
        "path": str(path.relative_to(ROOT)),
        "srcsets_fixed": changed,
        "entries_removed": total_removed,
    }


LOCALES = {
    "es", "fr", "zh", "hi", "ar", "bn", "pt", "ru", "ja", "de",
    "ko", "it", "nl", "tr", "pl", "vi", "th", "id", "sv", "he",
}
EXCLUDE_DIRS = {
    "backup", "node_modules", ".git", ".claude", "scripts",
    "appResources", "ai", ".uisnap", "__pycache__",
    "other-pages", "protected-content", "pdf-build",
}


def is_english_page(path: Path) -> bool:
    rel = path.relative_to(ROOT)
    if not rel.parts:
        return False
    first = rel.parts[0]
    if first in EXCLUDE_DIRS:
        return False
    if first in LOCALES:
        return False
    return True


def main() -> int:
    results = []
    for p in ROOT.rglob("*.html"):
        if not is_english_page(p):
            continue
        r = process_file(p)
        if r["entries_removed"]:
            results.append(r)
    total_pages = len(results)
    total_entries = sum(r["entries_removed"] for r in results)
    print(f"Pages modified: {total_pages}")
    print(f"Srcset entries removed: {total_entries}")
    if results:
        print("Top offenders:")
        for r in sorted(results, key=lambda x: -x["entries_removed"])[:10]:
            print(f"  {r['entries_removed']:3d} entries across {r['srcsets_fixed']} srcsets  in  {r['path']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
