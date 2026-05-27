#!/usr/bin/env python3
"""Apply accessibility fixes across every English HTML page.

Idempotent. What it does:

  1. Heading order: walk the document in source order. Any heading whose
     level exceeds (previous_level + 1) is promoted (upshifted) to fit the
     sequence. For example h1 -> h4 becomes h1 -> h2, and a following h4
     staying at the same visual level becomes h3 accordingly. We only
     modify the tag name and its matching closer. Class names and inline
     styles stay exactly the same.
  2. Unnamed <a> links whose only content is an <img> with empty alt: set
     the img alt to a value derived from the href filename when it is
     obviously a logo or icon, otherwise add aria-label="app link" as a
     last resort. Links with no visible text and no image are flagged by
     adding aria-label="decorative link" only when href="#" and the link
     has zero content (prevents breaking real behavior).
  3. Form labels: for pages containing the contact popup and forum form,
     audit every <input> / <textarea> / <select> that has no associated
     <label for="..."> in the same page. Add aria-label derived from
     placeholder or name attribute.
  4. CSS muted text colors: bump any `color: rgba(255,255,255,0.X)` with X
     in 0.0 to 0.74 up to 0.75 so WCAG AA contrast on dark backgrounds
     holds. This applies to css/apiant.css, css/components.css,
     css/normalize.css, css/cookie-consent.css, AND inline <style> blocks
     inside English HTML pages.

Run after perf_fixes.py and before inject_seo.py / localize.py.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

SKIP_TOP_DIRS = {
    "backup", "node_modules", ".git", ".claude", "scripts",
    "appResources", "ai", ".uisnap", "__pycache__",
    "other-pages", "protected-content", "pdf-build",
    "i18n", "supabase", "private", "docs", "video", "videos",
    "images", "css", "js", "fonts",
}
LOCALE_DIRS = {
    "es", "fr", "de", "zh", "ja", "pt", "ar", "hi", "bn", "ru",
    "ko", "it", "nl", "tr", "pl", "vi", "th", "id", "sv", "he",
}
SKIP_FILES = {
    "servletTemplateConnect.html",
    "servletTemplateConnections.html",
}
SKIP_ROOT_PREFIXES = (
    "admin", "test", "temp", "architecture-illustration",
    "401", "404",
)

# --- Heading order -----------------------------------------------------

HEADING_RE = re.compile(r"<(/?)(h[1-6])\b", re.I)
SCRIPT_STYLE_RE = re.compile(r"<(script|style)\b[^>]*>.*?</\1>", re.I | re.S)


def fix_heading_order(content: str) -> tuple[str, int]:
    """Walk headings in source order, promote any that skip levels.

    We operate on a copy of the content where <script> and <style> blocks
    are masked out so their text content never contaminates matches.
    Replacements happen on the real content using the same offsets.
    """
    # Build a mask: replace script/style bodies with same-length spaces so
    # that regex offsets on the mask mirror the real content.
    mask_chars = list(content)
    for m in SCRIPT_STYLE_RE.finditer(content):
        for i in range(m.start(), m.end()):
            if mask_chars[i] != "\n":
                mask_chars[i] = " "
    mask = "".join(mask_chars)

    replacements: list[tuple[int, int, str]] = []
    prev_level = 0
    # Track level remapping. When we promote a heading, we also keep a stack
    # so that when we later see a heading that was "correctly" lower in the
    # hierarchy, we can promote it consistently. Keep it simple: clamp
    # level to prev_level + 1. Don't lower anything.
    for m in HEADING_RE.finditer(mask):
        closing = bool(m.group(1))
        tag = m.group(2).lower()
        level = int(tag[1])
        if closing:
            # We don't pair up openings and closings here; the closers are
            # rewritten in a separate pass that mirrors the opener list.
            continue
        if prev_level == 0:
            # First heading: accept as-is (typically h1). Capture level.
            prev_level = level
            continue
        if level > prev_level + 1:
            new_level = prev_level + 1
            # Replace the opening tag level.
            start = m.start()
            # The matched substring is "<h3" or "<h4" etc. We want to
            # preserve case of original file. Use original content.
            orig_tag_segment = content[start : start + len(m.group(0))]
            # Swap the digit at index after "<h".
            digit_idx = orig_tag_segment.lower().find("h") + 1
            absolute_digit_idx = start + digit_idx
            # Build replacement: same slice with digit swapped.
            replacements.append((absolute_digit_idx, absolute_digit_idx + 1, str(new_level)))
            prev_level = new_level
        else:
            prev_level = level

    if not replacements:
        return content, 0

    # We now also need to fix the matching </hN> closer for each opener we
    # modified. Simplest correct approach: walk the document and keep a
    # stack of open heading levels (with their new level). Apply the
    # opener changes first, then do a stack-based second pass to rewrite
    # closers accordingly.
    # Apply opener changes to a working copy.
    working = list(content)
    for start, end, new_char in sorted(replacements, key=lambda r: -r[0]):
        working[start:end] = list(new_char)
    opener_adjusted = "".join(working)

    # Now walk the adjusted doc and match openers to closers. For each
    # open heading, we need its position. Track original level from the
    # *unadjusted* mask so we can recover the closer target level.
    # Strategy: iterate HEADING_RE over unadjusted mask, keep a stack of
    # (original_level_for_closer_match, new_level). When we see a closer
    # tag in the unadjusted mask whose level matches the top of stack
    # original, rewrite its digit in the working content to the new_level
    # we promoted the opener to.
    stack: list[tuple[int, int]] = []  # (original_open_level, new_open_level)
    closer_replacements: list[tuple[int, int, str]] = []
    # Iterate again, this time paying attention to closers.
    # Reset prev_level and remap logic matches opener logic.
    prev_level = 0
    for m in HEADING_RE.finditer(mask):
        closing = bool(m.group(1))
        tag = m.group(2).lower()
        level = int(tag[1])
        if not closing:
            if prev_level == 0:
                stack.append((level, level))
                prev_level = level
                continue
            if level > prev_level + 1:
                new_level = prev_level + 1
                stack.append((level, new_level))
                prev_level = new_level
            else:
                stack.append((level, level))
                prev_level = level
        else:
            # Find the topmost stack entry with matching original level.
            # Pop everything above it (they were unclosed siblings).
            idx = None
            for i in range(len(stack) - 1, -1, -1):
                if stack[i][0] == level:
                    idx = i
                    break
            if idx is None:
                continue  # stray closer, skip
            _, new_level = stack[idx]
            # Pop stack down to and including idx.
            stack = stack[:idx]
            if new_level != level:
                # Rewrite the digit in the closer.
                start = m.start()
                orig_tag_segment = content[start : start + len(m.group(0))]
                digit_idx = orig_tag_segment.lower().find("h") + 1
                absolute_digit_idx = start + digit_idx
                closer_replacements.append((absolute_digit_idx, absolute_digit_idx + 1, str(new_level)))

    if closer_replacements:
        working = list(opener_adjusted)
        for start, end, new_char in sorted(closer_replacements, key=lambda r: -r[0]):
            working[start:end] = list(new_char)
        opener_adjusted = "".join(working)

    return opener_adjusted, len(replacements)


# --- Unnamed links -----------------------------------------------------

# Match <a ...>...</a> blocks (non-greedy). Tolerates nested tags but not nested <a>.
A_BLOCK_RE = re.compile(r"<a\b([^>]*)>(.*?)</a>", re.I | re.S)


def link_has_accessible_name(attrs: str, inner: str) -> bool:
    if re.search(r'\baria-label\s*=\s*["\'][^"\']+["\']', attrs, re.I):
        return True
    if re.search(r'\btitle\s*=\s*["\'][^"\']+["\']', attrs, re.I):
        return True
    # Visible text (strip tags, entities roughly).
    stripped = re.sub(r"<[^>]+>", "", inner)
    stripped = re.sub(r"&[a-z]+;", " ", stripped, flags=re.I)
    if stripped.strip():
        return True
    # img with non-empty alt.
    for img_m in re.finditer(r"<img\b([^>]*)>", inner, re.I):
        img_attrs = img_m.group(1)
        alt = re.search(r'\balt\s*=\s*["\']([^"\']*)["\']', img_attrs, re.I)
        if alt and alt.group(1).strip():
            return True
    # SVG with title child.
    if re.search(r"<svg[\s\S]*?<title\b[^>]*>[^<]+</title>", inner, re.I):
        return True
    return False


def derive_link_label(attrs: str, inner: str) -> str | None:
    """Return a best-effort aria-label for an unnamed link, or None."""
    href_m = re.search(r'\bhref\s*=\s*["\']([^"\']+)["\']', attrs, re.I)
    href = href_m.group(1) if href_m else ""
    if href.startswith("javascript:") or href == "#":
        return None
    # Brand/nav logos typically link to index.html or the root.
    clean_href = re.sub(r"[?#].*$", "", href).rstrip("/")
    class_m = re.search(r'\bclass\s*=\s*["\']([^"\']*)["\']', attrs, re.I)
    classes = class_m.group(1).lower() if class_m else ""
    is_brand = ("brand" in classes) or ("logo" in classes) or ("w-nav-brand" in classes)
    if is_brand and (clean_href.endswith("index.html") or clean_href in {"", "/"}):
        return "APIANT home"
    # Social media links, detect by href host.
    social_map = {
        "linkedin.com": "APIANT on LinkedIn",
        "twitter.com": "APIANT on X",
        "x.com": "APIANT on X",
        "youtube.com": "APIANT on YouTube",
        "github.com": "APIANT on GitHub",
        "facebook.com": "APIANT on Facebook",
    }
    for host, label in social_map.items():
        if host in href:
            return label
    # Use alt attribute of inner image if present but empty was the trigger.
    img_m = re.search(r"<img\b([^>]*)>", inner, re.I)
    if img_m:
        src_m = re.search(r'\bsrc\s*=\s*["\']([^"\']+)["\']', img_m.group(1), re.I)
        if src_m:
            base = src_m.group(1).rstrip("/").split("/")[-1]
            base = re.sub(r"\.[a-z0-9]+$", "", base, flags=re.I)
            base = re.sub(r"[-_]+", " ", base).strip()
            # Discard "APIANT LOGO V4 Dark Mode" style dumps, prefer href.
            if base and len(base) < 40 and "logo" not in base.lower():
                return base.title()
    # Last resort: href filename stem.
    if clean_href:
        last = clean_href.split("/")[-1]
        last = re.sub(r"\.(html|htm|php|jsp)$", "", last)
        if last:
            words = re.sub(r"[-_]+", " ", last).strip()
            if words and len(words) < 60:
                return words.title()
    return None


def fix_unnamed_links(content: str) -> tuple[str, int]:
    fixed = 0

    def rewrite(match: re.Match) -> str:
        nonlocal fixed
        attrs = match.group(1)
        inner = match.group(2)
        if link_has_accessible_name(attrs, inner):
            return match.group(0)
        label = derive_link_label(attrs, inner)
        if not label:
            return match.group(0)
        # Inject aria-label into attrs.
        new_attrs = attrs.rstrip() + f' aria-label="{label}"'
        fixed += 1
        return f"<a{new_attrs}>{inner}</a>"

    return A_BLOCK_RE.sub(rewrite, content), fixed


# --- Form labels -------------------------------------------------------

INPUT_TAG_RE = re.compile(r"<(input|textarea|select)\b([^>]*)>", re.I)


def extract_attr(attrs: str, name: str) -> str | None:
    m = re.search(rf'\b{name}\s*=\s*["\']([^"\']*)["\']', attrs, re.I)
    return m.group(1) if m else None


def fix_form_labels(content: str) -> tuple[str, int]:
    # Build a set of IDs referenced by labels via for="...".
    labelled_ids = set(re.findall(r'<label\b[^>]*\bfor\s*=\s*["\']([^"\']+)["\']', content, re.I))
    # Also count inputs that are nested inside a <label>...</label> (implicit
    # label association). Track the IDs so we don't double-label them.
    wrapped_ids: set[str] = set()
    for lm in re.finditer(r"<label\b[^>]*>(.*?)</label>", content, re.I | re.S):
        for im in re.finditer(r"<(input|textarea|select)\b([^>]*)>", lm.group(1), re.I):
            id_m = re.search(r'\bid\s*=\s*["\']([^"\']+)["\']', im.group(2), re.I)
            if id_m:
                wrapped_ids.add(id_m.group(1))
    # Inputs without an id but wrapped in a label are effectively labeled, but
    # our rewriter skips based on id anyway; we just extend labelled_ids.
    labelled_ids.update(wrapped_ids)
    fixed = 0

    def rewrite(match: re.Match) -> str:
        nonlocal fixed
        tag = match.group(1)
        attrs = match.group(2)
        # Skip type=hidden inputs (no UX surface).
        typ = extract_attr(attrs, "type")
        if tag.lower() == "input" and typ and typ.lower() == "hidden":
            return match.group(0)
        # Skip type=submit / button (not a labelable control in the a11y sense).
        if tag.lower() == "input" and typ and typ.lower() in {"submit", "reset", "button"}:
            return match.group(0)
        id_ = extract_attr(attrs, "id")
        aria_label = extract_attr(attrs, "aria-label")
        aria_by = extract_attr(attrs, "aria-labelledby")
        if aria_label or aria_by:
            return match.group(0)
        if id_ and id_ in labelled_ids:
            return match.group(0)
        # Derive label from placeholder or name.
        label = extract_attr(attrs, "placeholder") or extract_attr(attrs, "name")
        if not label:
            # title can count, but the rule above handles title on a > link
            # not here. Try data-field-label or fallback.
            label = extract_attr(attrs, "title")
        if not label:
            return match.group(0)
        # Sanitize label (strip e.g. leading "e.g.").
        label = label.strip()
        if label.lower().startswith("e.g."):
            label = label[4:].strip() or label
        # Truncate overly long placeholders to a reasonable label size.
        if len(label) > 80:
            label = label[:77].rstrip() + "..."
        new_attrs = attrs.rstrip() + f' aria-label="{label}"'
        fixed += 1
        return f"<{tag}{new_attrs}>"

    new_content = INPUT_TAG_RE.sub(rewrite, content)
    return new_content, fixed


# --- CSS contrast ------------------------------------------------------

# Match `color: rgba(255,255,255,0.NN)` where NN makes the alpha under 0.75.
# Also match `color: rgba(247,248,248,0.NN)` (heading color fallback). Only the
# text `color` property, not `border-color` / `background-color` / etc. We
# anchor with a look-behind that rejects a leading letter, hyphen, or digit
# (word-boundary \b alone is not sufficient because \b matches after a
# hyphen which is common in `border-color:`).
COLOR_RGBA_RE = re.compile(
    r"(?<![\w-])"                          # not preceded by letter/digit/_/-
    r"(color\s*:\s*rgba\(\s*(?:255\s*,\s*255\s*,\s*255|247\s*,\s*248\s*,\s*248)\s*,\s*)"
    r"(0?\.\d+)"
    r"(\s*\))",
    re.I,
)


def bump_low_opacity_colors(content: str) -> tuple[str, int]:
    """Bump alpha on `color: rgba(white, <0.75)` up to 0.75."""
    fixed = 0

    def rewrite(m: re.Match) -> str:
        nonlocal fixed
        alpha_str = m.group(2)
        try:
            alpha = float(alpha_str)
        except ValueError:
            return m.group(0)
        if alpha >= 0.75:
            return m.group(0)
        fixed += 1
        return f"{m.group(1)}0.75{m.group(3)}"

    new = COLOR_RGBA_RE.sub(rewrite, content)
    return new, fixed


# --- File walking ------------------------------------------------------

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
    if len(first) == 2 and first.isalpha() and first.islower():
        return False
    name = rel.name
    if name in SKIP_FILES:
        return False
    if len(parts) == 1:
        for prefix in SKIP_ROOT_PREFIXES:
            if name.startswith(prefix):
                return False
    return True


def walk_english_pages() -> list[Path]:
    out = []
    for p in ROOT.rglob("*.html"):
        if not is_english_page(p):
            continue
        out.append(p)
    return sorted(out)


def process_html(path: Path) -> dict:
    original = path.read_text(encoding="utf-8")
    content = original
    ops: list[str] = []

    content, n_headings = fix_heading_order(content)
    if n_headings:
        ops.append(f"headings:{n_headings}")

    content, n_links = fix_unnamed_links(content)
    if n_links:
        ops.append(f"links:{n_links}")

    content, n_inputs = fix_form_labels(content)
    if n_inputs:
        ops.append(f"inputs:{n_inputs}")

    content, n_color = bump_low_opacity_colors(content)
    if n_color:
        ops.append(f"color:{n_color}")

    if content != original:
        path.write_text(content, encoding="utf-8")
    return {"path": str(path.relative_to(ROOT)), "ops": ops}


def process_css(path: Path) -> dict:
    original = path.read_text(encoding="utf-8")
    content, n_color = bump_low_opacity_colors(original)
    ops = []
    if n_color:
        ops.append(f"color:{n_color}")
    if content != original:
        path.write_text(content, encoding="utf-8")
    return {"path": str(path.relative_to(ROOT)), "ops": ops}


def main() -> int:
    results = []
    for p in walk_english_pages():
        results.append(process_html(p))
    css_files = [
        ROOT / "css" / "apiant.css",
        ROOT / "css" / "components.css",
        ROOT / "css" / "normalize.css",
        ROOT / "css" / "cookie-consent.css",
    ]
    for p in css_files:
        if p.exists():
            results.append(process_css(p))
    n_changed = sum(1 for r in results if r["ops"])
    n_total = len(results)
    print(f"a11y_fixes: processed {n_total} files, modified {n_changed}")
    op_counts: dict[str, int] = {}
    for r in results:
        for op in r["ops"]:
            key = op.split(":", 1)[0]
            op_counts[key] = op_counts.get(key, 0) + 1
    for op, n in sorted(op_counts.items()):
        print(f"  {op}: {n}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
