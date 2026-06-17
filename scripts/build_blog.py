#!/usr/bin/env python3
"""build_blog.py — render blog posts from Supabase to static HTML.

Triggered by GitHub Actions on `repository_dispatch` type `blog_publish`,
which the Supabase publish trigger fires when a post transitions to status
'publishing'. Can also be run locally:

  SUPABASE_URL=... SUPABASE_SERVICE_ROLE_KEY=... \
    python3 scripts/build_blog.py --post-id <uuid>

  python3 scripts/build_blog.py --all       # rebuild every live post + hub

Flow:
  1. Fetch the target post (or all live posts) via Supabase REST.
  2. Render body markdown to HTML (Python-Markdown + pymdownx extensions).
  3. Extract a TOC from H2/H3 in the rendered HTML.
  4. Render the post template and write /blog/posts/<slug>/index.html.
  5. Always rebuild the hub (/blog/index.html) and category landing pages
     from the full set of live posts.
  6. Write /blog/feed.xml (RSS 2.0, 50 most recent).
  7. POST /functions/v1/blog-mark-live to flip the post's status to 'live'
     or 'failed' (the GitHub Action commits + deploys the resulting files).
"""
from __future__ import annotations

import argparse
import html
import json
import os
import re
import sys
import textwrap
import traceback
from datetime import datetime, timezone
from pathlib import Path

import markdown as md
import requests

ROOT = Path(__file__).resolve().parent.parent
BLOG_DIR = ROOT / "blog"
POSTS_DIR = BLOG_DIR / "posts"
CATEGORY_DIR = BLOG_DIR / "category"
TEMPLATES_DIR = BLOG_DIR / "_templates"
BASE_URL = "https://apiant.com"
SITE_NAME = "APIANT Blog"

WORDS_PER_MINUTE = 220

# ---------- Supabase REST helpers ----------

SUPABASE_URL = os.environ.get("SUPABASE_URL", "").rstrip("/")
SERVICE_KEY = os.environ.get("SUPABASE_SERVICE_ROLE_KEY", "")


def sb_headers() -> dict:
    if not SUPABASE_URL or not SERVICE_KEY:
        raise SystemExit(
            "SUPABASE_URL and SUPABASE_SERVICE_ROLE_KEY env vars required"
        )
    return {
        "apikey": SERVICE_KEY,
        "Authorization": f"Bearer {SERVICE_KEY}",
        "Content-Type": "application/json",
        "Accept": "application/json",
    }


def sb_get(path: str, params: dict | None = None) -> list:
    url = f"{SUPABASE_URL}/rest/v1{path}"
    r = requests.get(url, headers=sb_headers(), params=params or {}, timeout=30)
    r.raise_for_status()
    return r.json()


POST_SELECT = (
    "id,slug,title,subtitle,excerpt,body_md,hero_image_url,hero_image_alt,"
    "seo_title,seo_description,canonical_url,og_image_url,status,"
    "published_at,scheduled_for,created_at,updated_at,"
    "category:blog_categories(id,slug,name,description),"
    "author:blog_authors(id,slug,display_name,role_title,avatar_url,bio),"
    "tags:blog_post_tags(blog_tags(id,slug,name))"
)


def fetch_post(post_id: str) -> dict | None:
    rows = sb_get("/blog_posts", {"id": f"eq.{post_id}", "select": POST_SELECT})
    return rows[0] if rows else None


def fetch_live_posts() -> list[dict]:
    return sb_get(
        "/blog_posts",
        {
            "status": "eq.live",
            "select": POST_SELECT,
            "order": "published_at.desc.nullslast",
        },
    )


def fetch_categories() -> list[dict]:
    return sb_get(
        "/blog_categories",
        {"select": "id,slug,name,description,sort_order", "order": "sort_order.asc"},
    )


def mark_live(post_id: str, status: str, msg: str | None = None) -> None:
    """Best-effort. Failure here doesn't roll back HTML writes."""
    url = f"{SUPABASE_URL}/functions/v1/blog-mark-live"
    try:
        r = requests.post(
            url,
            headers={
                "Authorization": f"Bearer {SERVICE_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps({"id": post_id, "status": status, "msg": msg}),
            timeout=15,
        )
        if not r.ok:
            print(f"WARN blog-mark-live non-2xx ({r.status_code}): {r.text[:300]}")
    except Exception as e:
        print(f"WARN blog-mark-live exception: {e}")


# ---------- Template helpers ----------

def load_template(name: str) -> str:
    return (TEMPLATES_DIR / name).read_text(encoding="utf-8")


def sub(template: str, vars: dict) -> str:
    out = template
    for k, v in vars.items():
        out = out.replace("{{" + k + "}}", v)
    # Strip any remaining placeholders so we don't leak {{X}} into HTML.
    out = re.sub(r"\{\{[A-Z_]+\}\}", "", out)
    return out


def normalize(s: str | None) -> str:
    return (s or "").strip()


def js(value):
    """JSON-encode a value for safe inline use in <script>."""
    return json.dumps(value if value is not None else "")


def slugify_anchor(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", text.lower()).strip()
    return re.sub(r"[-\s]+", "-", s) or "section"


# ---------- Markdown + TOC ----------

def render_markdown(body_md: str) -> tuple[str, list[tuple[int, str, str]]]:
    """Render markdown to HTML and return (html, toc_entries).

    toc_entries: list of (level, anchor_id, text) for H2 (level=2) and H3 (level=3).
    """
    extensions = [
        "markdown.extensions.fenced_code",
        "markdown.extensions.tables",
        "markdown.extensions.smarty",
        "markdown.extensions.attr_list",
        "markdown.extensions.toc",
        "pymdownx.superfences",
    ]
    extension_configs = {
        "markdown.extensions.toc": {
            "slugify": lambda value, sep: slugify_anchor(value),
            "toc_depth": "2-3",
        },
    }
    rendered = md.markdown(body_md or "", extensions=extensions, extension_configs=extension_configs)

    toc: list[tuple[int, str, str]] = []
    for m in re.finditer(r'<h([23])\s+id="([^"]+)"[^>]*>(.*?)</h\1>', rendered, flags=re.DOTALL):
        level = int(m.group(1))
        anchor = m.group(2)
        text = re.sub(r"<[^>]+>", "", m.group(3)).strip()
        toc.append((level, anchor, text))
    return rendered, toc


def estimate_read_minutes(body_md: str) -> int:
    words = len(re.findall(r"\b\w+\b", body_md or ""))
    return max(1, round(words / WORDS_PER_MINUTE))


# ---------- HTML blocks ----------

def head_for_post(post: dict) -> str:
    head_tmpl = load_template("_head.html")
    title = normalize(post["title"])
    excerpt = normalize(post.get("excerpt")) or f"{title} — APIANT Blog"
    seo_title = normalize(post.get("seo_title")) or f"{title} | APIANT Blog"
    canonical = normalize(post.get("canonical_url")) or f"{BASE_URL}/blog/posts/{post['slug']}/"
    og_image = normalize(post.get("og_image_url")) or normalize(post.get("hero_image_url")) or f"{BASE_URL}/images/Apiant-iso1-02.png"
    # Social scrapers (Facebook, LinkedIn, X) don't decode AVIF, so an .avif
    # og:image renders as no image on shares. og_image_url must be jpg/png:
    # keep the page hero as .avif and upload a JPEG sibling for sharing.
    if og_image.lower().split("?")[0].endswith(".avif"):
        print(f"WARN og:image for '{post['slug']}' is .avif; social shares will "
              f"show no preview image. Set og_image_url to a jpg/png copy.")
    return sub(head_tmpl, {
        "TITLE_TAG": html.escape(seo_title),
        "META_DESCRIPTION": html.escape(excerpt),
        "OG_TITLE": html.escape(title),
        "OG_IMAGE_URL": html.escape(og_image),
        "OG_TYPE": "article",
        "CANONICAL_URL": html.escape(canonical),
        "EXTRA_HEAD": "",
    })


def head_for_hub(title: str, description: str, url: str) -> str:
    head_tmpl = load_template("_head.html")
    return sub(head_tmpl, {
        "TITLE_TAG": html.escape(title),
        "META_DESCRIPTION": html.escape(description),
        "OG_TITLE": html.escape(title),
        "OG_IMAGE_URL": f"{BASE_URL}/images/Apiant-iso1-02.png",
        "OG_TYPE": "website",
        "CANONICAL_URL": html.escape(url),
        "EXTRA_HEAD": "",
    })


def render_post_card(post: dict) -> str:
    cat = post.get("category") or {}
    hero = post.get("hero_image_url") or ""
    hero_html = (
        f'<div class="blog-card-image"><img alt="{html.escape(post.get("hero_image_alt") or post["title"])}" loading="lazy" src="{html.escape(hero)}"/></div>'
        if hero else
        '<div class="blog-card-image"></div>'
    )
    excerpt = html.escape(normalize(post.get("excerpt")) or "")
    published = format_date(post.get("published_at") or post.get("updated_at"))
    author = (post.get("author") or {}).get("display_name", "")
    # Tag slugs as a space-separated data attribute so blog-search.js can
    # filter cards by tag without re-rendering the grid.
    tag_slugs = []
    for t in (post.get("tags") or []):
        inner = t.get("blog_tags") if isinstance(t, dict) else None
        if inner and inner.get("slug"):
            tag_slugs.append(inner["slug"])
    data_tags = html.escape(" ".join(tag_slugs))
    return (
        f'<a class="blog-card" data-tags="{data_tags}" href="/blog/posts/{html.escape(post["slug"])}/">'
        f'{hero_html}'
        f'<div class="blog-card-body">'
        f'<div class="blog-category-chip">{html.escape(cat.get("name", ""))}</div>'
        f'<h3 class="blog-card-title">{html.escape(post["title"])}</h3>'
        f'<p class="blog-card-excerpt">{excerpt}</p>'
        f'<div class="blog-card-meta">'
        f'<span class="notranslate">{html.escape(author)}</span>'
        f'<span>{html.escape(published)}</span>'
        f'</div></div></a>'
    )


def render_category_pills(categories: list[dict], active_slug: str | None) -> str:
    pills = [(
        f'<a class="blog-pill{" active" if active_slug is None else ""}" href="/blog/">All</a>'
    )]
    for c in categories:
        active = " active" if c["slug"] == active_slug else ""
        pills.append(
            f'<a class="blog-pill{active}" href="/blog/category/{html.escape(c["slug"])}">'
            f'{html.escape(c["name"])}</a>'
        )
    return "\n".join(pills)


def render_tag_filter(posts: list[dict], category_slug: str) -> str:
    """Return the empty container div for the tag-pill row.
    blog-search.js fills it at runtime from the data-tags attributes on
    the visible cards. Empty server-rendered div survives locale auto-
    regen (which has been observed to strip inline-rendered tag pills
    during BS4 roundtrip)."""
    return (
        '<div class="blog-tag-filter" '
        'data-category="' + html.escape(category_slug) + '" '
        'role="group" aria-label="Filter by tag"></div>'
    )


def render_featured(post: dict) -> str:
    cat = post.get("category") or {}
    hero = post.get("hero_image_url") or ""
    # Carry the same data-tags as a card so blog-search.js can include the
    # featured post in tag filtering (without it the featured post is invisible
    # to every ?tag= filter).
    tag_slugs = []
    for t in (post.get("tags") or []):
        inner = t.get("blog_tags") if isinstance(t, dict) else None
        if inner and inner.get("slug"):
            tag_slugs.append(inner["slug"])
    data_tags = html.escape(" ".join(tag_slugs))
    hero_html = (
        f'<div class="blog-featured-image"><img alt="{html.escape(post.get("hero_image_alt") or post["title"])}" src="{html.escape(hero)}"/></div>'
        if hero else
        '<div class="blog-featured-image"></div>'
    )
    return (
        f'<section class="blog-featured" data-tags="{data_tags}">'
        f'{hero_html}'
        '<div class="blog-featured-body">'
        f'<div class="blog-category-chip">{html.escape(cat.get("name", ""))}</div>'
        f'<h2 class="blog-featured-title"><a href="/blog/posts/{html.escape(post["slug"])}/">{html.escape(post["title"])}</a></h2>'
        f'<p class="blog-featured-excerpt">{html.escape(normalize(post.get("excerpt")) or "")}</p>'
        '</div></section>'
    )


def render_toc(toc: list[tuple[int, str, str]]) -> str:
    if not toc:
        return ""
    items = []
    for level, anchor, text in toc:
        items.append(
            f'<li class="lvl-{level}"><a href="#{html.escape(anchor)}">{html.escape(text)}</a></li>'
        )
    return (
        '<aside class="blog-toc">'
        '<div class="blog-toc-heading">In this article</div>'
        '<ul class="blog-toc-list">' + "".join(items) + '</ul>'
        '</aside>'
    )


def render_tags(tags: list[dict]) -> str:
    if not tags:
        return ""
    chips = "".join(
        f'<a class="blog-tag" href="/blog/?tag={html.escape(t["slug"])}">#{html.escape(t["name"])}</a>'
        for t in tags
    )
    return f'<div class="blog-post-tags">{chips}</div>'


def render_related(posts: list[dict]) -> str:
    if not posts:
        return ""
    cards = "".join(render_post_card(p) for p in posts)
    return (
        '<section class="blog-related">'
        '<h2 class="blog-related-heading">Keep reading</h2>'
        f'<div class="blog-grid">{cards}</div>'
        '</section>'
    )


def render_api_apps_cta() -> str:
    """Three tiny cards at the foot of every post, one per turnkey vertical
    hub. Replaces the old single 'browse the full catalog' text link."""
    cards = [
        ("Mindbody Solutions",
         "Fitness and wellness integrations",
         "/apipartners/mindbody-turnkey-integration-solutions"),
        ("Cliniko Solutions",
         "Healthcare and allied-health integrations",
         "/apipartners/cliniko-turnkey-integration-solutions"),
        ("DonorPerfect Solutions",
         "Nonprofit and fundraising integrations",
         "/apipartners/donorperfect-turnkey-integration-solutions"),
    ]
    items = "".join(
        f'<a class="blog-apps-cta-card" href="{html.escape(url)}">'
        f'<span class="blog-apps-cta-name">{html.escape(name)}</span>'
        f'<span class="blog-apps-cta-desc">{html.escape(desc)}</span>'
        f'<span class="blog-apps-cta-arrow">Explore &rarr;</span>'
        f'</a>'
        for name, desc, url in cards
    )
    return (
        '<aside class="blog-apps-cta">'
        '<div class="blog-apps-cta-heading">Browse the full API Apps catalog</div>'
        f'<div class="blog-apps-cta-grid">{items}</div>'
        '</aside>'
    )


def is_shopconnect_post(post: dict, tag_slugs: set) -> bool:
    """True for ShopConnect (Mindbody + Shopify) posts. Prefers the explicit
    tags, falls back to the slug because a few posts are mistagged in the CMS
    (e.g. the booking-widget post carries crmconnect/highlevel tags)."""
    if "shopconnect" in tag_slugs or "shopify" in tag_slugs:
        return True
    slug = (post.get("slug") or "").lower()
    return "shopify" in slug and "mindbody" in slug


def render_shopconnect_cta() -> str:
    """Free-trial CTA rendered just above the catalog cards on ShopConnect
    posts, pointing at the Mindbody + Shopify integration page."""
    url = "/apipartners/mindbody/mindbody-shopify-integration-and-automation-apiant"
    return (
        '<aside class="blog-trial-cta">'
        '<div class="blog-trial-cta-eyebrow">ShopConnect &middot; Shopify + Mindbody</div>'
        '<h2 class="blog-trial-cta-title">Run Shopify and Mindbody as one system</h2>'
        '<p class="blog-trial-cta-text">ShopConnect keeps your Shopify store and Mindbody '
        'account in sync automatically: orders, products, inventory, taxes, and client '
        'records line up without anyone re-keying them. Spin it up and watch it run on '
        'your own data.</p>'
        f'<a class="blog-trial-cta-btn" href="{url}">Start your free ShopConnect trial '
        '<span aria-hidden="true">&rarr;</span></a>'
        '<span class="blog-trial-cta-note">See it working end to end before you commit. '
        'Plans start at $79/mo.</span>'
        '</aside>'
    )


VERTICAL_NAMES = {"mindbody": "Mindbody", "cliniko": "Cliniko", "donorperfect": "DonorPerfect"}
PARTNER_NAMES = {
    "hubspot": "HubSpot", "activecampaign": "ActiveCampaign", "keap": "Keap",
    "klaviyo": "Klaviyo", "highlevel": "HighLevel", "zoho-crm": "Zoho CRM",
    "shopify": "Shopify", "zapier": "Zapier", "zoom": "Zoom", "calendly": "Calendly",
    "salesforce": "Salesforce", "mailchimp": "Mailchimp",
}

_PRODUCT_MAP = None


def product_map() -> dict:
    """(vertical, partner) -> /apipartners/<vertical>/<file> path, scanned from
    the repo so the odd filenames (e.g. cliniko-hubspot has no '-and-') resolve
    on their own."""
    global _PRODUCT_MAP
    if _PRODUCT_MAP is not None:
        return _PRODUCT_MAP
    m = {}
    for vert in VERTICAL_NAMES:
        d = ROOT / "apipartners" / vert
        if not d.is_dir():
            continue
        for f in d.glob("*.html"):
            core = f.stem.split("-integration")[0]   # mindbody-hubspot / mindbody-zoho-crm
            if not core.startswith(vert + "-"):
                continue
            partner = core[len(vert) + 1:]
            if partner in PARTNER_NAMES:
                m[(vert, partner)] = f"/apipartners/{vert}/{f.stem}"
    _PRODUCT_MAP = m
    return m


def detect_product(post: dict, tag_slugs: set):
    """Map a use-case post to its specific product page via the vertical +
    partner in its slug. Returns (url, vertical_name, partner_name) or None."""
    slug = (post.get("slug") or "").lower()
    s = f"-{slug}-"
    vertical = next((v for v in VERTICAL_NAMES if f"-{v}-" in s or slug.startswith(v + "-")), None)
    if not vertical:
        return None
    # Longest partner slug first so 'zoho-crm' is matched before any short token.
    partner = next((p for p in sorted(PARTNER_NAMES, key=len, reverse=True) if f"-{p}-" in s), None)
    if not partner:
        return None
    url = product_map().get((vertical, partner))
    if not url:
        return None
    return url, VERTICAL_NAMES[vertical], PARTNER_NAMES[partner]


def render_product_cta(url: str, vertical: str, partner: str) -> str:
    """Targeted 'this exact integration' CTA, linking a use-case post to its
    specific product page. Reuses the .blog-trial-cta styles."""
    v, p = html.escape(vertical), html.escape(partner)
    return (
        '<aside class="blog-trial-cta">'
        f'<div class="blog-trial-cta-eyebrow">{v} + {p}</div>'
        f'<h2 class="blog-trial-cta-title">Run {v} and {p} as one system</h2>'
        f'<p class="blog-trial-cta-text">This use case runs on APIANT’s deep, two-way '
        f'{v} and {p} integration: it keeps both systems in sync automatically, with no '
        're-keying and no spreadsheets. See exactly what it syncs and how it works.</p>'
        f'<a class="blog-trial-cta-btn" href="{html.escape(url)}">Explore the {v} + {p} '
        'integration <span aria-hidden="true">&rarr;</span></a>'
        '</aside>'
    )


def render_post_ctas(post: dict, tag_slugs: set) -> str:
    """Foot-of-post CTAs: a specific product CTA when the post maps to one
    (ShopConnect keeps its dedicated trial CTA), always followed by the
    three vertical catalog cards."""
    if is_shopconnect_post(post, tag_slugs):
        return render_shopconnect_cta() + render_api_apps_cta()
    prod = detect_product(post, tag_slugs)
    if prod:
        return render_product_cta(*prod) + render_api_apps_cta()
    return render_api_apps_cta()


# Temporary override: inject demo screenshots into specific posts whose CMS
# body_md does not yet carry them. The proper home for these is the Supabase
# post body; once added there, drop the slug entry below. Each image is placed
# immediately before the named section heading (markdown rendered as a figure).
_DOCS_IMG = "https://lptryjqgqoknvmzotyvz.supabase.co/storage/v1/object/public/images/docs-images"
POST_BODY_IMAGES = {
    "add-mindbody-booking-widget-to-shopify": [
        ("## When you can't take payment through Mindbody",
         f"![The Book Now page customers use: a green how-to-book panel beside the live Mindbody class schedule, embedded right on the Shopify store]({_DOCS_IMG}/1780676074264-shopconnect-demo-book-now-page-styled.webp)"),
        ("## Kill the confusing password email",
         f"![The Shopify thank-you page with a green banner explaining how to book: open the Book Now page, pick a class, and the Mindbody sign-in takes over]({_DOCS_IMG}/1780676526661-shopconnect-demo-thank-you-page-banner-inline.webp)"),
        ("## What ShopConnect is doing in the middle",
         f"![The Mindbody create-account screen appearing inline at booking, name and email already prefilled, asking the customer to set a password]({_DOCS_IMG}/1780676082583-mindbody-create-account-set-password.webp)"),
        ("## What closing the gap is worth",
         f"![The Mindbody profile schedule showing the Intro to Yoga class with status Booked]({_DOCS_IMG}/1780676527275-mindbody-booked-classes-profile.webp)"),
    ],
}


def inject_body_images(slug: str, body_md: str) -> str:
    spec = POST_BODY_IMAGES.get(slug)
    if not spec:
        return body_md
    for anchor, img_md in spec:
        if anchor in body_md:
            body_md = body_md.replace(anchor, img_md + "\n\n" + anchor, 1)
    return body_md


def render_hero_image(post: dict) -> str:
    hero = normalize(post.get("hero_image_url"))
    if not hero:
        return ""
    alt = html.escape(post.get("hero_image_alt") or post["title"])
    return (
        f'<div class="blog-post-hero-image"><img alt="{alt}" src="{html.escape(hero)}"/></div>'
    )


def format_date(value) -> str:
    if not value:
        return ""
    try:
        dt = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except Exception:
        return ""
    return dt.strftime("%b %-d, %Y") if sys.platform != "win32" else dt.strftime("%b %#d, %Y")


# ---------- Renderers per page type ----------

def write_post_page(post: dict, related: list[dict]) -> Path:
    body_html, toc = render_markdown(inject_body_images(post["slug"], post["body_md"]))
    cat = post.get("category") or {}
    author = post.get("author") or {}
    tags = [t["blog_tags"] for t in (post.get("tags") or []) if t.get("blog_tags")]
    tag_slugs = {(t.get("slug") or "").lower() for t in tags}
    canonical = normalize(post.get("canonical_url")) or f"{BASE_URL}/blog/posts/{post['slug']}/"
    category_url = f"{BASE_URL}/blog/category/{cat.get('slug', '')}"
    published_iso = post.get("published_at") or post.get("created_at") or ""
    updated_iso = post.get("updated_at") or published_iso
    hero_image_for_jsonld = normalize(post.get("hero_image_url")) or normalize(post.get("og_image_url"))

    template = load_template("post.html")
    rendered = sub(template, {
        "HEAD": head_for_post(post),
        "NAV": load_template("_nav.html"),
        "FOOTER": load_template("_footer.html"),
        "TITLE": html.escape(post["title"]),
        "SUBTITLE_BLOCK": (
            f'<p class="blog-post-subtitle">{html.escape(post["subtitle"])}</p>'
            if normalize(post.get("subtitle")) else ""
        ),
        "CATEGORY_SLUG": html.escape(cat.get("slug", "")),
        "CATEGORY_NAME": html.escape(cat.get("name", "")),
        "AUTHOR_NAME": html.escape(author.get("display_name", "")),
        "AUTHOR_SLUG": html.escape(author.get("slug", "")),
        "PUBLISHED_DISPLAY": format_date(published_iso),
        "READ_TIME": str(estimate_read_minutes(post["body_md"])),
        "HERO_IMAGE_BLOCK": render_hero_image(post),
        "BODY_HTML": body_html,
        "API_APPS_CTA": render_post_ctas(post, tag_slugs),
        "TOC_BLOCK": render_toc(toc),
        "TAGS_BLOCK": render_tags(tags),
        "RELATED_BLOCK": render_related(related),
        # JSON-LD fields (json-encoded)
        "JSON_TITLE": js(post["title"]),
        "JSON_DESCRIPTION": js(post.get("excerpt") or ""),
        "JSON_HERO_IMAGE": js(hero_image_for_jsonld or f"{BASE_URL}/images/Apiant-iso1-02.png"),
        "JSON_PUBLISHED_AT": js(published_iso),
        "JSON_UPDATED_AT": js(updated_iso),
        "JSON_AUTHOR_NAME": js(author.get("display_name", "")),
        "JSON_AUTHOR_URL": js(f"{BASE_URL}/blog/?author={author.get('slug', '')}"),
        "JSON_CANONICAL": js(canonical),
        "JSON_CATEGORY_NAME": js(cat.get("name", "")),
        "JSON_CATEGORY_URL": js(category_url),
    })

    out_dir = POSTS_DIR / post["slug"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "index.html"
    out_path.write_text(rendered, encoding="utf-8")
    return out_path


def write_hub(posts: list[dict], categories: list[dict]) -> Path:
    template = load_template("index.html")
    cards = "".join(render_post_card(p) for p in posts[1:]) if posts else ""
    featured = render_featured(posts[0]) if posts else ""

    rendered = sub(template, {
        "HEAD": head_for_hub(
            "APIANT Blog — Builder notes from the integration trenches",
            "Use cases, customer stories, and platform deep dives from the APIANT integration platform.",
            f"{BASE_URL}/blog/",
        ),
        "NAV": load_template("_nav.html"),
        "FOOTER": load_template("_footer.html"),
        "HERO_TITLE": "Builder notes from the integration trenches.",
        "HERO_SUB": "Real integration problems solved with the APIANT platform, and the AI Co-Pilot that built it.",
        "CATEGORY_PILLS": render_category_pills(categories, None),
        "FEATURED_BLOCK": featured,
        "POST_CARDS": cards,
        "PAGINATION_BLOCK": "",  # Pagination kicks in at 10+ posts; v1 ships flat.
    })

    out_path = BLOG_DIR / "index.html"
    out_path.write_text(rendered, encoding="utf-8")
    return out_path


def write_category(category: dict, posts: list[dict], all_categories: list[dict]) -> Path:
    template = load_template("category.html")
    cards = "".join(render_post_card(p) for p in posts)
    cat_url = f"{BASE_URL}/blog/category/{category['slug']}"

    rendered = sub(template, {
        "HEAD": head_for_hub(
            f'{category["name"]} — APIANT Blog',
            normalize(category.get("description")) or f'Posts in {category["name"]}.',
            cat_url,
        ),
        "NAV": load_template("_nav.html"),
        "FOOTER": load_template("_footer.html"),
        "CATEGORY_NAME": html.escape(category["name"]),
        "CATEGORY_NAME_UPPER": html.escape(category["name"].upper()),
        "CATEGORY_DESCRIPTION": html.escape(normalize(category.get("description")) or ""),
        "CATEGORY_PILLS": render_category_pills(all_categories, category["slug"]),
        "TAG_FILTER": render_tag_filter(posts, category["slug"]),
        "POST_CARDS": cards if cards else '<div class="blog-empty"><h2>No posts yet</h2><p>Check back soon.</p></div>',
        "PAGINATION_BLOCK": "",
        "JSON_CATEGORY_NAME": js(category["name"]),
        "JSON_CATEGORY_DESCRIPTION": js(category.get("description") or ""),
        "JSON_CATEGORY_URL": js(cat_url),
    })

    out_dir = CATEGORY_DIR / category["slug"]
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "index.html"
    out_path.write_text(rendered, encoding="utf-8")
    return out_path


def write_rss(posts: list[dict]) -> Path:
    now = datetime.now(timezone.utc).strftime("%a, %d %b %Y %H:%M:%S +0000")
    items = []
    for p in posts[:50]:
        pub = ""
        if p.get("published_at"):
            try:
                pub = datetime.fromisoformat(p["published_at"].replace("Z", "+00:00")).strftime("%a, %d %b %Y %H:%M:%S +0000")
            except Exception:
                pub = ""
        link = f"{BASE_URL}/blog/posts/{p['slug']}/"
        title = html.escape(p["title"])
        desc = html.escape(normalize(p.get("excerpt")) or "")
        items.append(
            f"<item><title>{title}</title><link>{link}</link>"
            f"<guid isPermaLink=\"true\">{link}</guid>"
            f"<pubDate>{pub}</pubDate>"
            f"<description>{desc}</description></item>"
        )
    rss = textwrap.dedent(f"""<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom">
        <channel>
        <title>{SITE_NAME}</title>
        <link>{BASE_URL}/blog/</link>
        <atom:link href="{BASE_URL}/blog/feed.xml" rel="self" type="application/rss+xml"/>
        <description>Use cases, customer stories, and platform deep dives from APIANT.</description>
        <language>en</language>
        <lastBuildDate>{now}</lastBuildDate>
        {''.join(items)}
        </channel>
        </rss>
    """).strip()
    out_path = BLOG_DIR / "feed.xml"
    out_path.write_text(rss, encoding="utf-8")
    return out_path


# ---------- Orchestration ----------

def pick_related(post: dict, all_live: list[dict], limit: int = 3) -> list[dict]:
    """Pick related posts: same category first, then most recent."""
    cat_id = (post.get("category") or {}).get("id")
    same_cat = [p for p in all_live if p["id"] != post["id"] and (p.get("category") or {}).get("id") == cat_id]
    others = [p for p in all_live if p["id"] != post["id"] and p not in same_cat]
    return (same_cat + others)[:limit]


def plain_text_from_md(body_md: str) -> str:
    """Strip markdown/HTML to plain words for the search index."""
    t = body_md or ""
    t = re.sub(r"```.*?```", " ", t, flags=re.S)        # fenced code
    t = re.sub(r"`[^`]*`", " ", t)                       # inline code
    t = re.sub(r"!\[[^\]]*\]\([^)]*\)", " ", t)          # images
    t = re.sub(r"\[([^\]]*)\]\([^)]*\)", r"\1", t)       # links -> text
    t = re.sub(r"<[^>]+>", " ", t)                        # html tags
    t = re.sub(r"[#>*_~|`=+-]", " ", t)                   # md punctuation
    t = re.sub(r"\s+", " ", t).strip()
    return t


def write_search_index(posts: list[dict]) -> Path:
    """Emit a flat JSON index used by client-side Fuse.js search on the hub.
    Includes a `search_text` blob (title + de-hyphenated slug + subtitle +
    tags + excerpt + capped body) so queries match the article's actual
    wording and slug, not just the SEO title.
    """
    index = []
    for p in posts:
        cat = p.get("category") or {}
        tags = [t["blog_tags"] for t in (p.get("tags") or []) if t.get("blog_tags")]
        slug_words = (p["slug"] or "").replace("-", " ")
        body_plain = plain_text_from_md(p.get("body_md"))[:600]
        search_text = " ".join(filter(None, [
            p.get("title") or "",
            slug_words,
            p.get("subtitle") or "",
            " ".join(t.get("name", "") for t in tags),
            p.get("excerpt") or "",
            body_plain,
        ]))
        index.append({
            "slug": p["slug"],
            "title": p["title"],
            "excerpt": (p.get("excerpt") or "")[:280],
            "category": cat.get("slug", ""),
            "category_name": cat.get("name", ""),
            "tags": [t["slug"] for t in tags],
            "tag_names": [t["name"] for t in tags],
            "search_text": search_text,
            "hero_image_url": p.get("hero_image_url") or "",
            "url": f"/blog/posts/{p['slug']}/",
            "published_at": p.get("published_at"),
        })
    out_path = BLOG_DIR / "search-index.json"
    out_path.write_text(json.dumps(index, separators=(",", ":")), encoding="utf-8")
    return out_path


def rebuild_all_hubs() -> None:
    categories = fetch_categories()
    live = fetch_live_posts()
    write_hub(live, categories)
    for c in categories:
        in_cat = [p for p in live if (p.get("category") or {}).get("id") == c["id"]]
        write_category(c, in_cat, categories)
    write_rss(live)
    write_search_index(live)


def build_one(post_id: str) -> None:
    post = fetch_post(post_id)
    if not post:
        print(f"ERROR post {post_id} not found")
        sys.exit(1)
    try:
        # Re-fetch all live posts to pick related and to rebuild hubs in one go.
        all_live = fetch_live_posts()
        # Make sure the post we're publishing is in the related-source if it's now live.
        related = pick_related(post, all_live)
        path = write_post_page(post, related)
        # The post itself isn't 'live' yet until we mark it; mark first so the
        # next hub rebuild includes it.
        mark_live(post_id, "live")
        rebuild_all_hubs()
        print(f"OK wrote {path.relative_to(ROOT)}")
    except Exception as e:
        traceback.print_exc()
        mark_live(post_id, "failed", str(e)[:500])
        sys.exit(1)


def build_all() -> None:
    rebuild_all_hubs()
    live = fetch_live_posts()
    for p in live:
        related = pick_related(p, live)
        write_post_page(p, related)
    print(f"OK rebuilt {len(live)} posts + hub + categories + RSS")


def main() -> int:
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--post-id", help="single post UUID to publish")
    g.add_argument("--all", action="store_true", help="rebuild every live post + hub + categories + RSS")
    args = ap.parse_args()

    BLOG_DIR.mkdir(parents=True, exist_ok=True)
    POSTS_DIR.mkdir(parents=True, exist_ok=True)
    CATEGORY_DIR.mkdir(parents=True, exist_ok=True)

    if args.post_id:
        build_one(args.post_id)
    else:
        build_all()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
