#!/usr/bin/env python3
"""Acceptance checks for canonical URL generation in inject_seo.py.

Run:  python3 scripts/test_inject_seo_canonical.py
Exits non-zero on any failure. No third-party deps.
"""
from pathlib import Path

import inject_seo as seo

ROOT = seo.ROOT
FAILS: list[str] = []


def check(label: str, got, want) -> None:
    ok = got == want
    print(f"  [{'PASS' if ok else 'FAIL'}] {label}: got {got!r}")
    if not ok:
        FAILS.append(f"{label}: expected {want!r}, got {got!r}")


def main() -> int:
    print("url_for(): clean, https, apiant.com, .html stripped, query-free")
    # Normal page -> strips trailing .html
    check("apps.html", seo.url_for(ROOT / "apps.html"), "https://apiant.com/apps")
    check(
        "platform/admin-console.html",
        seo.url_for(ROOT / "platform" / "admin-console.html"),
        "https://apiant.com/platform/admin-console",
    )
    # Root index -> bare domain (established site convention)
    check("index.html", seo.url_for(ROOT / "index.html"), "https://apiant.com/")
    # Section index -> trailing slash
    check(
        "platform/index.html",
        seo.url_for(ROOT / "platform" / "index.html"),
        "https://apiant.com/platform/",
    )
    # Force HTTPS + apiant.com host
    for label in ("apps.html", "ai.html", "mcp-servers.html"):
        u = seo.url_for(ROOT / label)
        check(f"{label} scheme/host", u.startswith("https://apiant.com/"), True)
    # Query-string-free by construction
    check("no query string", "?" in seo.url_for(ROOT / "apps.html"), False)

    print("\nensure_canonical(): missing tag is added inside <head>")
    no_canon = "<head><title>x</title></head>"
    out, changed = seo.ensure_canonical(no_canon, "https://apiant.com/foo")
    check("adds when missing (changed)", changed, True)
    check(
        "adds before </head>",
        '<link href="https://apiant.com/foo" rel="canonical"/>' in out and out.index("rel=\"canonical\"") < out.index("</head>"),
        True,
    )
    print("ensure_canonical(): self-referential tag left untouched")
    has_canon = '<head><link href="https://apiant.com/foo" rel="canonical"/></head>'
    _, changed = seo.ensure_canonical(has_canon, "https://apiant.com/foo")
    check("no change when correct", changed, False)

    print("\nExclusions: /connect/, /connection/, /connections/")
    check("connect excluded", seo.is_canonical_excluded(ROOT / "connect" / "connect.html"), True)
    check(
        "connections excluded",
        seo.is_canonical_excluded(ROOT / "connections" / "connections.html"),
        True,
    )
    check("connection excluded", seo.is_canonical_excluded(ROOT / "connection" / "x.html"), True)
    check("normal page not excluded", seo.is_canonical_excluded(ROOT / "apps.html"), False)

    print("\nExcluded pages keep their authored canonical (no rewrite on disk)")
    for rel in ("connect/connect.html", "connections/connections.html"):
        p = ROOT / rel
        if not p.exists():
            print(f"  [SKIP] {rel} not present")
            continue
        before = p.read_text(encoding="utf-8")
        seo.process_file(p)
        after = p.read_text(encoding="utf-8")
        # Canonical must still point at the authored cross-page target, unchanged.
        check(f"{rel} canonical preserved", after == before, True)
        check(f"{rel} still -> /apps.html", 'href="https://apiant.com/apps.html" rel="canonical"' in after, True)

    print()
    if FAILS:
        print(f"FAILED ({len(FAILS)}):")
        for f in FAILS:
            print(f"  - {f}")
        return 1
    print("All canonical acceptance checks passed.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
