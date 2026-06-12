#!/usr/bin/env python3
"""delete_blog_post.py — unpublish or fully delete a blog post.

The blog is rendered from Supabase (see build_blog.py), so taking a post off
the site means changing Supabase AND removing the already-generated HTML
directories from the repo (English + every locale). The deploy workflow's
"Sync blog tree with --delete" rsync step then removes the folders from
apiant.com on the next push.

Usage:
  python3 scripts/delete_blog_post.py --slug <slug> --unpublish   # back to draft
  python3 scripts/delete_blog_post.py --slug <slug> --delete      # remove row + media
  python3 scripts/delete_blog_post.py --slug <slug> --delete --keep-media
  add --yes to skip the confirmation prompt

What each mode does:
  --unpublish  Sets status back to 'saved' (a CMS draft). Keeps the row, tags,
               and media so the post can be re-published later.
  --delete     Deletes the blog_posts row (tag links cascade) and the post's
               blog-media/<slug>/ storage folder (unless --keep-media).

Both modes then:
  1. Remove blog/posts/<slug>/ and <locale>/blog/posts/<slug>/ from the
     working tree.
  2. Run build_blog.py --all so the hub, category pages, feed, and search
     index no longer reference the post.
  3. Print the git commands to commit and push (push triggers deploy, which
     rsyncs the removals to apiant.com). This script never commits for you.

Credentials: SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY from the environment,
falling back to ~/.apiant_keys (same convention as update_translations.sh).
"""
from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

import requests

ROOT = Path(__file__).resolve().parent.parent


def load_keys() -> tuple[str, str]:
    url = os.environ.get("SUPABASE_URL", "")
    key = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")
    if not (url and key):
        keyfile = Path.home() / ".apiant_keys"
        if keyfile.exists():
            for line in keyfile.read_text().splitlines():
                m = re.match(r'\s*export\s+(\w+)\s*=\s*"?([^"\n]+)"?', line)
                if not m:
                    continue
                if m.group(1) == "SUPABASE_URL" and not url:
                    url = m.group(2)
                if m.group(1) == "SUPABASE_SERVICE_ROLE_KEY" and not key:
                    key = m.group(2)
    if not (url and key):
        raise SystemExit("SUPABASE_URL / SUPABASE_SERVICE_ROLE_KEY not found "
                         "in env or ~/.apiant_keys")
    return url.rstrip("/"), key


SB, KEY = "", ""


def hdrs() -> dict:
    return {"apikey": KEY, "Authorization": f"Bearer {KEY}",
            "Content-Type": "application/json"}


def fetch_post(slug: str) -> dict | None:
    r = requests.get(f"{SB}/rest/v1/blog_posts",
                     params={"slug": f"eq.{slug}",
                             "select": "id,slug,title,status,published_at"},
                     headers=hdrs(), timeout=30)
    r.raise_for_status()
    rows = r.json()
    return rows[0] if rows else None


def unpublish(post_id: str) -> None:
    r = requests.patch(f"{SB}/rest/v1/blog_posts", params={"id": f"eq.{post_id}"},
                       json={"status": "saved"}, headers=hdrs(), timeout=30)
    r.raise_for_status()
    print("OK status -> saved (draft)")


def delete_row(post_id: str) -> None:
    r = requests.delete(f"{SB}/rest/v1/blog_posts", params={"id": f"eq.{post_id}"},
                        headers=hdrs(), timeout=30)
    r.raise_for_status()
    print("OK blog_posts row deleted (tag links cascade)")


def delete_media(slug: str) -> None:
    r = requests.post(f"{SB}/storage/v1/object/list/blog-media",
                      json={"prefix": f"{slug}/", "limit": 1000},
                      headers=hdrs(), timeout=30)
    r.raise_for_status()
    names = [f"{slug}/{o['name']}" for o in r.json() if o.get("name")]
    if not names:
        print("No storage objects under blog-media/%s/" % slug)
        return
    r = requests.delete(f"{SB}/storage/v1/object/blog-media",
                        json={"prefixes": names}, headers=hdrs(), timeout=30)
    r.raise_for_status()
    print(f"OK deleted {len(names)} object(s) from blog-media/{slug}/")


def remove_local_dirs(slug: str) -> list[Path]:
    removed = []
    candidates = [ROOT / "blog" / "posts" / slug]
    for entry in ROOT.iterdir():
        if entry.is_dir() and re.fullmatch(r"[a-z]{2}", entry.name):
            candidates.append(entry / "blog" / "posts" / slug)
    for d in candidates:
        if d.is_dir():
            shutil.rmtree(d)
            removed.append(d.relative_to(ROOT))
    return removed


def main() -> int:
    global SB, KEY
    ap = argparse.ArgumentParser(description="Unpublish or delete a blog post")
    ap.add_argument("--slug", required=True)
    mode = ap.add_mutually_exclusive_group(required=True)
    mode.add_argument("--unpublish", action="store_true",
                      help="set status back to 'saved' (draft); keeps row and media")
    mode.add_argument("--delete", action="store_true",
                      help="delete the row and its blog-media storage folder")
    ap.add_argument("--keep-media", action="store_true",
                    help="with --delete: keep the blog-media/<slug>/ images")
    ap.add_argument("--yes", action="store_true", help="skip confirmation")
    args = ap.parse_args()

    SB, KEY = load_keys()

    post = fetch_post(args.slug)
    if not post:
        print(f"No blog_posts row with slug '{args.slug}'.")
        # The row may already be gone while HTML lingers; still offer cleanup.
        if not args.yes:
            resp = input("Remove any generated HTML directories anyway? [y/N] ")
            if resp.strip().lower() != "y":
                return 1
    else:
        action = "UNPUBLISH (status -> saved)" if args.unpublish else \
            "DELETE row + media" if not args.keep_media else "DELETE row (keeping media)"
        print(f"Post:   {post['title']}")
        print(f"Status: {post['status']}  Published: {post.get('published_at')}")
        print(f"Action: {action}")
        if not args.yes:
            resp = input("Proceed? [y/N] ")
            if resp.strip().lower() != "y":
                print("Aborted.")
                return 1
        if args.unpublish:
            unpublish(post["id"])
        else:
            delete_row(post["id"])
            if not args.keep_media:
                delete_media(args.slug)

    removed = remove_local_dirs(args.slug)
    for d in removed:
        print(f"removed {d}")
    if not removed:
        print("No generated HTML directories found for this slug.")

    print("Rebuilding hub/categories/feed/search from live posts...")
    env = dict(os.environ, SUPABASE_URL=SB, SUPABASE_SERVICE_ROLE_KEY=KEY)
    subprocess.run([sys.executable, str(ROOT / "scripts" / "build_blog.py"), "--all"],
                   check=True, env=env)

    print("\nDone. To ship the removal to apiant.com:")
    print(f'  git add -A && git commit -m "Remove blog post {args.slug}" && git push')
    print("The deploy workflow's scoped rsync --delete removes the folders "
          "from the server.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
