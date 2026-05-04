#!/usr/bin/env python3
"""Strip .html from URLs in apiant-website pages.

Targets:
  <link rel="canonical">
  <meta property="og:url">
  <link rel="alternate" hreflang="...">
  <script type="application/ld+json"> ... </script>  (Schema.org @id, url, etc.)
  <a href="..."> body links to internal (apiant.com) pages

Skips: external links, mailto:/tel:/javascript:/data:, anchor-only (#section).

Index handling: any URL ending /index.html becomes the trailing-slash form,
matching the existing English root convention (https://apiant.com/).

Dry run: python3 scripts/strip_html_ext.py
Apply:   python3 scripts/strip_html_ext.py --apply
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

CANONICAL = re.compile(r'<link\b[^>]*\brel="canonical"[^>]*/>', re.IGNORECASE)
OG_URL    = re.compile(r'<meta\b[^>]*\bproperty="og:url"[^>]*/>', re.IGNORECASE)
HREFLANG  = re.compile(r'<link\b(?=[^>]*\brel="alternate")(?=[^>]*\bhreflang=)[^>]*/>', re.IGNORECASE)
JSONLD    = re.compile(r'<script\b[^>]*\btype="application/ld\+json"[^>]*>.*?</script>', re.IGNORECASE | re.DOTALL)
A_HREF    = re.compile(r'(<a\b[^>]*\bhref=")([^"]*)("[^>]*>)', re.IGNORECASE)

INDEX_HTML = re.compile(r'(https://apiant\.com/(?:[^"]*/)?)index\.html(?=")')
HTML_EXT   = re.compile(r'(https://apiant\.com/[^"]+?)\.html(?=")')

SKIP_SCHEMES = ('mailto:', 'tel:', 'javascript:', 'data:')

LANG_DIRS = ['ar', 'bn', 'de', 'es', 'fr', 'he', 'hi', 'id', 'it', 'ja',
             'ko', 'nl', 'pl', 'pt', 'ru', 'sv', 'th', 'tr', 'vi', 'zh']

def fix_url_in_tag(tag):
    new, n1 = INDEX_HTML.subn(r'\1', tag)
    new, n2 = HTML_EXT.subn(r'\1', new)
    return new, n1 + n2

def transform_internal_href(href):
    """Strip .html from an internal href value. Returns (new_href, changed_count)."""
    if not href or href.startswith('#') or href.startswith(SKIP_SCHEMES):
        return href, 0
    if href.startswith(('http://', 'https://')):
        if 'apiant.com' not in href.split('/', 3)[2]:
            return href, 0
    m = re.match(r'^([^?#]*)([?#].*)?$', href)
    if not m:
        return href, 0
    base = m.group(1)
    rest = m.group(2) or ''
    if base.endswith('/index.html'):
        new_base = base[:-len('index.html')]
    elif base == 'index.html':
        return href, 0
    elif base.endswith('.html'):
        new_base = base[:-len('.html')]
    else:
        return href, 0
    return new_base + rest, 1

def fix_file(path, apply):
    content = path.read_text(encoding='utf-8', errors='ignore')
    new_content = content
    urls = [0]
    for pat in (CANONICAL, OG_URL, HREFLANG, JSONLD):
        def repl(m, u=urls):
            t = m.group(0)
            n, count = fix_url_in_tag(t)
            u[0] += count
            return n
        new_content = pat.sub(repl, new_content)
    def repl_a(m, u=urls):
        prefix, href, suffix = m.group(1), m.group(2), m.group(3)
        new_href, n = transform_internal_href(href)
        u[0] += n
        return prefix + new_href + suffix
    new_content = A_HREF.sub(repl_a, new_content)
    if apply and urls[0] > 0:
        path.write_text(new_content, encoding='utf-8')
    return urls[0]

SCAN_DIRS = ['apipartners', 'platform', 'connect', 'connections']

def collect_files():
    files = sorted(ROOT.glob('*.html'))
    for d in SCAN_DIRS:
        sub = ROOT / d
        if sub.exists():
            files.extend(sorted(sub.rglob('*.html')))
    for d in LANG_DIRS:
        sub = ROOT / d
        if sub.exists():
            files.extend(sorted(sub.rglob('*.html')))
    return files

def main():
    apply = '--apply' in sys.argv
    files = collect_files()
    total_tags = 0
    changed = 0
    samples = []
    for f in files:
        n = fix_file(f, apply=apply)
        if n > 0:
            changed += 1
            total_tags += n
            if len(samples) < 5:
                samples.append((f.relative_to(ROOT), n))
    mode = "APPLIED" if apply else "DRY RUN"
    print(f"[{mode}] files scanned  : {len(files)}")
    print(f"[{mode}] files changed  : {changed}")
    print(f"[{mode}] tag URLs flipped: {total_tags}")
    print(f"[{mode}] first 5 samples:")
    for rel, n in samples:
        print(f"   {n:3d} tags  {rel}")

if __name__ == '__main__':
    main()
