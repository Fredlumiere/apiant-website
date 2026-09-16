#!/usr/bin/env python3
"""Regenerate the allowlists behind apache-connect-redirect.conf.

The legacy apiant.com /connect/ and /connections/ pages can only be redirected
to apiant.ai where the corresponding apiant.ai page actually exists. apiant.ai
runs a different, newer app catalog, so most of them do not. This script
measures the overlap rather than assuming it, and writes three RewriteMap
files:

    apiant-ai-apps.txt              apps present on apiant.ai   -> /connections/
    apiant-ai-connect-sources.txt   apps that expose a trigger  -> left of -to-
    apiant-ai-connect-targets.txt   apps that expose an action  -> right of -to-

Method:
  1. Read the legacy app catalog out of apiant.com's sitemap.
  2. Probe every legacy slug against https://apiant.ai/connections/<slug>.
  3. Probe every ordered pair of the survivors against
     https://apiant.ai/connect/<a>-to-<b>.
  4. Derive the source and target capability lists from the live pairs, then
     assert that those two lists reproduce the probed set exactly. If they do
     not, apiant.ai's pair rule has changed and the Apache config needs
     revisiting rather than a regenerated map.

Non-200 responses are retried once before being treated as real, so a single
transient failure cannot silently drop a page from the allowlist.

Usage:  python3 scripts/probe_apiant_ai_catalog.py [--out-dir .] [--jobs 8]

Takes a few minutes and makes a few thousand requests; run it when apiant.ai's
catalog has grown, not on every deploy.
"""

import argparse
import itertools
import json
import os
import re
import subprocess
import sys
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from datetime import date

SITEMAP = "https://apiant.com/sitemap/sitemap0.xml"
AI = "https://apiant.ai"


def fetch_legacy_apps():
    with urllib.request.urlopen(SITEMAP, timeout=180) as r:
        xml = r.read().decode("utf-8", "replace")
    slugs = {m.lower() for m in re.findall(r"https://apiant\.com/connections/([^\]<\s]+)", xml)}
    if len(slugs) < 50:
        sys.exit(f"ERROR: parsed only {len(slugs)} app slugs from the sitemap; the format probably changed.")
    return sorted(slugs)


def status(url, timeout=30):
    r = subprocess.run(
        ["curl", "-sS", "-o", "/dev/null", "-w", "%{http_code}", "-m", str(timeout), url],
        capture_output=True, text=True,
    )
    return r.stdout.strip()


def probe(urls, jobs, label):
    """Return {url: status}, retrying every non-200 once."""
    print(f"  {label}: {len(urls)} requests ...", flush=True)
    with ThreadPoolExecutor(max_workers=jobs) as ex:
        res = dict(zip(urls, ex.map(status, urls)))
    retry = [u for u, c in res.items() if c != "200"]
    if retry:
        print(f"  {label}: retrying {len(retry)} non-200 ...", flush=True)
        with ThreadPoolExecutor(max_workers=max(2, jobs // 2)) as ex:
            res.update(zip(retry, ex.map(lambda u: status(u, 40), retry)))
    ok = sum(1 for c in res.values() if c == "200")
    print(f"  {label}: {ok} live of {len(urls)}", flush=True)
    return res


HEADER = """# {name}
#
# Apache RewriteMap read by apache-connect-redirect.conf.
# {note}
#
# Generated {today} by scripts/probe_apiant_ai_catalog.py, from a live probe of
# every legacy app slug and every candidate pair against apiant.ai.
# Entries: {count}
#
# Format: <key> <value>. Key is the lowercased legacy apiant.com slug, value is
# the apiant.ai slug. They are identical today, so a rename on apiant.ai is a
# value edit rather than a rule change.
#
"""

NOTES = {
    "apiant-ai-apps.txt":
        "Apps that exist on apiant.ai at all. Drives the /connections/<A> redirect,\n"
        "# which needs no trigger or action.",
    "apiant-ai-connect-sources.txt":
        "Apps that can appear on the LEFT of /connect/<A>-to-<B> on apiant.ai.\n"
        "# An app is listed only if it exposes a trigger there; without one, apiant.ai\n"
        "# has no <A>-to-anything page and the redirect would 404.",
    "apiant-ai-connect-targets.txt":
        "Apps that can appear on the RIGHT of /connect/<A>-to-<B> on apiant.ai.\n"
        "# An app is listed only if it exposes an action there; without one, apiant.ai\n"
        "# has no anything-to-<B> page and the redirect would 404.",
}


def write_map(out_dir, name, slugs):
    path = os.path.join(out_dir, name)
    with open(path, "w") as f:
        f.write(HEADER.format(name=name, note=NOTES[name], today=date.today().isoformat(), count=len(slugs)))
        for s in slugs:
            f.write(f"{s} {s}\n")
    print(f"  wrote {path} ({len(slugs)} entries)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default=".")
    ap.add_argument("--jobs", type=int, default=8)
    args = ap.parse_args()

    print(f"Reading legacy catalog from {SITEMAP}")
    legacy = fetch_legacy_apps()
    print(f"  legacy apps on apiant.com: {len(legacy)} "
          f"(implies {len(legacy) * (len(legacy) - 1)} /connect/ pages)")

    print("Probing apiant.ai app pages")
    app_res = probe([f"{AI}/connections/{s}" for s in legacy], args.jobs, "apps")
    apps = sorted(s for s in legacy if app_res[f"{AI}/connections/{s}"] == "200")

    print("Probing apiant.ai pair pages")
    pairs = list(itertools.permutations(apps, 2))
    pair_res = probe([f"{AI}/connect/{a}-to-{b}" for a, b in pairs], args.jobs, "pairs")
    live = {(a, b) for a, b in pairs if pair_res[f"{AI}/connect/{a}-to-{b}"] == "200"}

    sources = sorted({a for a, _ in live})
    targets = sorted({b for _, b in live})
    model = {(a, b) for a, b in itertools.product(sources, targets) if a != b}
    if model != live:
        sys.exit(
            "ERROR: the source/target model no longer reproduces the probed pairs "
            f"(+{len(model - live)} would 404, -{len(live - model)} would be missed).\n"
            "apiant.ai's pair rule has changed. Revisit apache-connect-redirect.conf "
            "before regenerating the maps."
        )
    print(f"  model reproduces the probed set exactly: {len(live)} pairs")

    write_map(args.out_dir, "apiant-ai-apps.txt", apps)
    write_map(args.out_dir, "apiant-ai-connect-sources.txt", sources)
    write_map(args.out_dir, "apiant-ai-connect-targets.txt", targets)

    total = len(legacy) * (len(legacy) - 1)
    print(f"\nRedirectable: {len(live)} of {total} /connect/ pages "
          f"({len(live) / total * 100:.1f}%), {len(apps)} of {len(legacy)} /connections/ pages.")
    print("Everything else keeps serving from apiant.com.")


if __name__ == "__main__":
    main()
