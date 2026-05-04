#!/usr/bin/env python3
"""
APIANT Website Localization Generator

Reads English HTML pages, applies translations, and generates localized copies
in /{lang}/ subdirectories. Adds hreflang tags, language switcher, RTL support.

Usage:
    python3 scripts/localize.py                  # Generate all languages
    python3 scripts/localize.py es fr de          # Generate specific languages
    python3 scripts/localize.py --add-hreflang    # Add hreflang to English pages
    python3 scripts/localize.py --add-switcher    # Add language switcher to English pages
"""
import os
import sys
import json
import re
import copy
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment, Doctype

ROOT = Path(__file__).parent.parent
I18N_DIR = ROOT / 'i18n'

# Mirror the translatable-attribute set from extract_strings.py so the two
# halves of the pipeline stay in sync. Import is guarded so this script can
# still run if extract_strings is ever moved or refactored.
try:
    sys.path.insert(0, str(Path(__file__).parent))
    from extract_strings import TRANSLATABLE_ATTRS  # type: ignore
except Exception:
    TRANSLATABLE_ATTRS = {
        'data-when',
        'data-example',
        'data-prod-desc',
        'data-desc',
        'data-title',
    }

LANGUAGES = {
    'es': {'name': 'Español', 'native': 'ES', 'dir': 'ltr'},
    'fr': {'name': 'Français', 'native': 'FR', 'dir': 'ltr'},
    'zh': {'name': '\u4e2d\u6587', 'native': 'ZH', 'dir': 'ltr'},
    'hi': {'name': '\u0939\u093f\u0928\u094d\u0926\u0940', 'native': 'HI', 'dir': 'ltr'},
    'ar': {'name': '\u0627\u0644\u0639\u0631\u0628\u064a\u0629', 'native': 'AR', 'dir': 'rtl'},
    'he': {'name': '\u05e2\u05d1\u05e8\u05d9\u05ea', 'native': 'HE', 'dir': 'rtl'},
    'bn': {'name': '\u09ac\u09be\u0982\u09b2\u09be', 'native': 'BN', 'dir': 'ltr'},
    'pt': {'name': 'Português', 'native': 'PT', 'dir': 'ltr'},
    'ru': {'name': '\u0420\u0443\u0441\u0441\u043a\u0438\u0439', 'native': 'RU', 'dir': 'ltr'},
    'ja': {'name': '\u65e5\u672c\u8a9e', 'native': 'JA', 'dir': 'ltr'},
    'de': {'name': 'Deutsch', 'native': 'DE', 'dir': 'ltr'},
    'ko': {'name': '\ud55c\uad6d\uc5b4', 'native': 'KO', 'dir': 'ltr'},
    'it': {'name': 'Italiano', 'native': 'IT', 'dir': 'ltr'},
    'nl': {'name': 'Nederlands', 'native': 'NL', 'dir': 'ltr'},
    'tr': {'name': 'Türkçe', 'native': 'TR', 'dir': 'ltr'},
    'pl': {'name': 'Polski', 'native': 'PL', 'dir': 'ltr'},
    'vi': {'name': 'Tiếng Việt', 'native': 'VI', 'dir': 'ltr'},
    'th': {'name': '\u0e44\u0e17\u0e22', 'native': 'TH', 'dir': 'ltr'},
    'id': {'name': 'Bahasa Indonesia', 'native': 'ID', 'dir': 'ltr'},
    'sv': {'name': 'Svenska', 'native': 'SV', 'dir': 'ltr'},
}

PAGES = [
    'index.html',
    'index2.html',
    'pricing.html',
    'ai.html',
    'ai-operability.html',
    'apps.html',
    'chatbot.html',
    'formapps.html',
    'mcp-servers.html',
    'for-saas.html',
    'for-si.html',
    'for-enterprises.html',
    '404.html',
    'platform/index.html',
    'platform/automation-editor.html',
    'platform/assembly-editor.html',
    'platform/admin-console.html',
    'apipartners/mindbody-turnkey-integration-solutions.html',
    'apipartners/cliniko-turnkey-integration-solutions.html',
    'apipartners/donorperfect-turnkey-integration-solutions.html',
    'apipartners/mindbody/mindbody-hubspot-integration-and-automation-apiant.html',
    'apipartners/mindbody/mindbody-activecampaign-integration-and-automation-apiant.html',
    'apipartners/mindbody/mindbody-keap-integration-and-automation-apiant.html',
    'apipartners/mindbody/mindbody-klaviyo-integration-and-automation-apiant.html',
    'apipartners/mindbody/mindbody-highlevel-integration-and-automation-apiant.html',
    'apipartners/mindbody/mindbody-zoho-crm-integration-and-automation-apiant.html',
    'apipartners/mindbody/mindbody-shopify-integration-and-automation-apiant.html',
    'apipartners/mindbody/mindbody-zapier-integration-and-automation-apiant.html',
    'apipartners/mindbody/mindbody-calendly-integration-and-automation-apiant.html',
    'apipartners/mindbody/mindbody-zoom-integration-and-automation-apiant.html',
    'apipartners/cliniko/cliniko-hubspot-integration-automation-apiant.html',
    'apipartners/cliniko/cliniko-salesforce-integration-and-automation-apiant.html',
    'apipartners/cliniko/cliniko-activecampaign-integration-and-automation-apiant.html',
    'apipartners/donorperfect/donorperfect-hubspot-integration-and-automation-apiant.html',
    'apipartners/donorperfect/donorperfect-activecampaign-integration-and-automation-apiant.html',
    'apipartners/donorperfect/donorperfect-keap-integration-and-automation-apiant.html',
    'apipartners/donorperfect/donorperfect-mailchimp-integration-and-automation-apiant.html',
    'privacy.html',
    'cookie-policy.html',
    'tos.html',
    'dpa.html',
]

LOCALIZED_SET = set(PAGES)

SKIP_TAGS = frozenset(['script', 'style', 'code', 'pre', 'svg', 'noscript', 'math'])

# Tags whose text content should NOT be translated
SKIP_TRANSLATE_CLASSES = frozenset(['w-embed', 'notranslate'])


def should_skip_translate(el):
    """Return True if the element (or any ancestor) should not be translated.
    Respects class="notranslate", class="w-embed", and translate="no" attribute.
    """
    node = el
    while node is not None and hasattr(node, 'get'):
        classes = node.get('class') or []
        if any(c in SKIP_TRANSLATE_CLASSES for c in classes):
            return True
        if (node.get('translate') or '').lower() == 'no':
            return True
        node = node.parent
    return False

BASE_URL = 'https://apiant.com'


def strip_html_ext(url):
    """Convert a URL ending in .html to the extensionless form.

    Any URL ending in /index.html becomes trailing-slash form (matching the
    canonical homepage convention https://apiant.com/), so /es/index.html
    becomes /es/, /platform/index.html becomes /platform/, etc.
    """
    if url.endswith('/index.html'):
        return url[:-len('index.html')]
    if url.endswith('.html'):
        return url[:-len('.html')]
    return url

# Language switcher HTML template - placed inline in nav between links and CTA
SWITCHER_HTML = '''<div class="lang-switcher" style="position:relative;display:flex;align-items:center;margin-left:4px;">
<button class="lang-switcher-btn" style="background:transparent;border:1px solid rgba(255,255,255,0.15);border-radius:6px;padding:6px 10px;color:rgba(255,255,255,0.7);font-size:13px;cursor:pointer;display:flex;align-items:center;gap:5px;font-family:'DM Sans',sans-serif;white-space:nowrap;transition:border-color 0.2s,color 0.2s;">
<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
<span class="lang-switcher-current">{LANG_CODE}</span>
<svg width="10" height="10" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M6 9l6 6 6-6"/></svg>
</button>
<div class="lang-switcher-dropdown"></div>
</div>'''

SWITCHER_CSS = '''
.lang-switcher-btn:hover{border-color:rgba(255,255,255,0.35);color:#fff;}
.lang-switcher-dropdown{display:none;position:absolute;top:calc(100% + 4px);right:0;background:#1a1a2e;border:1px solid rgba(255,255,255,0.1);border-radius:8px;padding:4px;min-width:170px;z-index:9999;max-height:420px;overflow-y:auto;box-shadow:0 8px 32px rgba(0,0,0,0.4);}
.lang-switcher-dropdown.open{display:block;}
.lang-option{display:flex;align-items:center;gap:8px;padding:7px 12px;color:rgba(255,255,255,0.7);text-decoration:none;font-size:13px;border-radius:4px;transition:background 0.15s,color 0.15s;font-family:'DM Sans',sans-serif;}
.lang-option:hover{background:rgba(255,255,255,0.08);color:#fff;}
.lang-option.active{color:#1ab759;font-weight:600;}
.lang-option-code{font-size:11px;opacity:0.5;min-width:20px;}
.lang-option-name{white-space:nowrap;}
.lang-switcher-dropdown::-webkit-scrollbar{width:4px;}
.lang-switcher-dropdown::-webkit-scrollbar-track{background:transparent;}
.lang-switcher-dropdown::-webkit-scrollbar-thumb{background:rgba(255,255,255,0.15);border-radius:2px;}
.white-mode .lang-switcher-btn,.nav-menu.white-mode .lang-switcher-btn{border-color:rgba(0,0,0,0.2)!important;color:rgba(0,0,0,0.6)!important;}
.white-mode .lang-switcher-btn:hover,.nav-menu.white-mode .lang-switcher-btn:hover{border-color:rgba(0,0,0,0.4)!important;color:#000!important;}
.white-mode .lang-switcher-dropdown,.nav-menu.white-mode .lang-switcher-dropdown{background:#fff;border-color:rgba(0,0,0,0.1);box-shadow:0 8px 32px rgba(0,0,0,0.15);}
.white-mode .lang-option,.nav-menu.white-mode .lang-option{color:rgba(0,0,0,0.6);}
.white-mode .lang-option:hover,.nav-menu.white-mode .lang-option:hover{background:rgba(0,0,0,0.05);color:#000;}
.white-mode .lang-option.active,.nav-menu.white-mode .lang-option.active{color:#0d7a3a;}
@media(max-width:991px){.lang-switcher{margin:8px 0 0 0!important;order:10;}.lang-switcher-dropdown{right:auto;left:0;}}
.listed-addons{width:100%!important;min-width:0!important;max-width:100%!important;overflow:visible!important;box-sizing:border-box!important;height:auto!important;max-height:none!important;}.listed-addons label.checkbox-field.list{width:100%!important;max-width:100%!important;box-sizing:border-box!important;}.listed-addons .addon-tick.list{max-width:calc(100% - 40px)!important;}.listed-addons .addon-tick.list p,.listed-addons .addon-tick.list .small-price{white-space:normal!important;word-break:break-word!important;overflow-wrap:break-word!important;}.listed-addons .addon-wrapper{max-width:100%!important;box-sizing:border-box!important;}.listed-addons .checkbox-field.list{flex-wrap:wrap!important;gap:8px 12px!important;}.listed-addons .addon-tick{padding-left:0!important;padding-right:0!important;}.listed-addons .addon-tick.list{flex-wrap:wrap!important;}.listed-addons .addon-tick.list .dark-paragraph{white-space:normal!important;word-break:break-word!important;}.listed-addons .addon-wrapper{flex-wrap:wrap!important;width:100%!important;}.listed-addons .addon-description{min-width:0!important;}.listed-addons .addon-description .dark-paragraph{white-space:normal!important;word-break:break-word!important;}.listed-addons{overflow:visible!important;}.listed-addons .custom-checkbox.horizontal{display:none!important;}.custom-checkbox.horizontal{display:none!important;width:0!important;height:0!important;}.listed-addons .qty{width:60px!important;min-width:0!important;flex:none!important;}
.addon-description .dark-paragraph{white-space:normal!important;word-break:break-word;}
.pricing-holder{flex-wrap:nowrap!important;max-width:1060px;margin-left:auto;margin-right:auto;align-items:flex-start!important;gap:20px!important;border:none!important;padding:0!important;}.pricing-holder>.pricing-container{flex:1;border:2px solid #e8e8e8;border-radius:14px;padding:19px;}.addon-container-copy{background:#f0f4f3!important;border:2px solid rgba(26,183,89,0.25)!important;border-radius:14px!important;flex:0 0 220px!important;position:sticky!important;top:100px!important;align-self:flex-start!important;padding:20px 16px!important;}.addon-container-copy .final-price-text{color:#0d7a3a!important;font-size:32px!important;}.addon-container-copy .btn-primary,.addon-container-copy .button.nav{background:#1ab759!important;color:#fff!important;border:none!important;border-radius:8px!important;padding:10px 16px!important;font-size:14px!important;width:100%!important;text-align:center!important;}@media(max-width:991px){.pricing-holder{flex-direction:column!important;max-width:100%!important;}.pricing-holder>.pricing-container{width:100%;}.addon-container-copy{flex:none!important;width:100%!important;position:relative!important;}}
'''


def load_translations(lang):
    """Load translation dictionary for a language, merging shared UI + per-language."""
    translations = {}

    # 1. Load shared UI translations (high-priority, hand-curated)
    shared_path = I18N_DIR / 'shared_ui.json'
    if shared_path.exists():
        with open(shared_path, 'r', encoding='utf-8') as f:
            shared = json.load(f)
        if lang in shared:
            translations.update(shared[lang])

    # 2. Load per-language translations (agent-generated, bulk content)
    path = I18N_DIR / f'{lang}.json'
    if path.exists():
        with open(path, 'r', encoding='utf-8') as f:
            lang_data = json.load(f)
        # Only add entries that are actually translated (different from key)
        for k, v in lang_data.items():
            if k != v:
                translations[k] = v

    # 3. Shared UI overrides agent translations for critical UI strings
    if shared_path.exists():
        with open(shared_path, 'r', encoding='utf-8') as f:
            shared = json.load(f)
        if lang in shared:
            translations.update(shared[lang])

    if not translations:
        print(f'  WARNING: No translations found for {lang}')

    return translations


def translate_text(text, translations):
    """Look up a translation. Returns original if not found."""
    stripped = text.strip()
    if not stripped:
        return text
    if stripped in translations:
        leading = text[:len(text) - len(text.lstrip())]
        trailing = text[len(text.rstrip()):]
        return leading + translations[stripped] + trailing
    return text


def is_relative(url):
    """Check if URL is relative."""
    return url and not url.startswith(('http', '//', '#', 'data:', 'mailto:', 'tel:', 'javascript:', '/'))


def resolve_url(url, page_dir):
    """Resolve a relative URL to an absolute path from root."""
    if page_dir:
        resolved = os.path.normpath(os.path.join(page_dir, url))
    else:
        resolved = os.path.normpath(url)
    # Remove any leading ./
    resolved = resolved.lstrip('./')
    return resolved


def fix_asset_url(url, page_dir):
    """Convert relative asset URL to absolute from root."""
    if not is_relative(url):
        return url
    return '/' + resolve_url(url, page_dir)


def fix_srcset(srcset, page_dir):
    """Fix srcset attribute URLs."""
    parts = srcset.split(',')
    fixed = []
    for part in parts:
        tokens = part.strip().split()
        if tokens and is_relative(tokens[0]):
            tokens[0] = '/' + resolve_url(tokens[0], page_dir)
        fixed.append(' '.join(tokens))
    return ', '.join(fixed)


def fix_urls(soup, lang, page_path):
    """Fix all URLs in the page for the localized context."""
    page_dir = os.path.dirname(page_path)

    # Fix asset URLs (CSS, JS, images, video, fonts)
    for tag in soup.find_all(['link', 'img', 'video', 'source']):
        for attr in ['href', 'src']:
            val = tag.get(attr)
            if val and is_relative(val):
                tag[attr] = fix_asset_url(val, page_dir)
        if tag.get('srcset'):
            tag['srcset'] = fix_srcset(tag['srcset'], page_dir)

    for tag in soup.find_all('script'):
        src = tag.get('src')
        if src and is_relative(src):
            tag['src'] = fix_asset_url(src, page_dir)

    # Fix background video data attributes
    for tag in soup.find_all(attrs={'data-video-urls': True}):
        urls = tag['data-video-urls']
        parts = urls.split(',')
        fixed = []
        for u in parts:
            u = u.strip()
            if is_relative(u):
                fixed.append(fix_asset_url(u, page_dir))
            else:
                fixed.append(u)
        tag['data-video-urls'] = ','.join(fixed)

    poster_tag = soup.find(attrs={'data-poster-url': True})
    if poster_tag:
        val = poster_tag['data-poster-url']
        if is_relative(val):
            poster_tag['data-poster-url'] = fix_asset_url(val, page_dir)

    # Fix background-image in inline styles
    for tag in soup.find_all(style=True):
        style = tag['style']
        def fix_bg(m):
            url = m.group(1).strip('"\'')
            if is_relative(url):
                return f'url("{fix_asset_url(url, page_dir)}")'
            return m.group(0)
        tag['style'] = re.sub(r'url\(([^)]+)\)', fix_bg, style)

    # Fix internal page links
    for a_tag in soup.find_all('a'):
        href = a_tag.get('href')
        if not href or not is_relative(href):
            continue

        # Split hash
        if '#' in href:
            page_part, hash_part = href.split('#', 1)
            hash_suffix = '#' + hash_part
        else:
            page_part = href
            hash_suffix = ''

        if page_part.endswith('.html'):
            resolved = resolve_url(page_part, page_dir)
            if resolved in LOCALIZED_SET:
                # Link to localized version
                a_tag['href'] = '/' + lang + '/' + resolved + hash_suffix
            else:
                # Link to English root version
                a_tag['href'] = '/' + resolved + hash_suffix
        elif page_part:
            # Non-HTML relative links
            a_tag['href'] = fix_asset_url(page_part, page_dir) + hash_suffix

    return soup


def add_hreflang_tags(soup, page_path):
    """Add hreflang link tags to <head>. Idempotent. Removes any existing
    hreflang link tags first so this can be re-run without duplicating."""
    head = soup.find('head')
    if not head:
        return

    # Remove existing hreflang tags to keep this idempotent.
    for existing in soup.find_all('link', attrs={'hreflang': True}):
        existing.decompose()

    # x-default (English)
    tag = soup.new_tag('link', rel='alternate', hreflang='x-default')
    tag['href'] = strip_html_ext(f'{BASE_URL}/{page_path}')
    head.append('\n')
    head.append(tag)

    # English
    tag = soup.new_tag('link', rel='alternate', hreflang='en')
    tag['href'] = strip_html_ext(f'{BASE_URL}/{page_path}')
    head.append('\n')
    head.append(tag)

    # All other languages
    for lc in LANGUAGES:
        tag = soup.new_tag('link', rel='alternate', hreflang=lc)
        tag['href'] = strip_html_ext(f'{BASE_URL}/{lc}/{page_path}')
        head.append('\n')
        head.append(tag)

    head.append('\n')


def add_language_switcher(soup, lang_code):
    """Insert language switcher into the navigation bar."""
    # Remove any existing switchers and their CSS (from previous runs)
    for existing in soup.find_all(class_='lang-switcher'):
        existing.decompose()
    for existing in soup.find_all('style'):
        css = existing.string or ''
        if '.lang-switcher' not in css:
            continue
        # Strip only the lang-switcher rules (and their media queries) from this block,
        # preserving any unrelated page-specific CSS that happens to share the block.
        cleaned = re.sub(
            r'(?:^|\n)[^\n]*\.lang-switcher[^{\n]*\{[^}]*\}',
            '',
            css,
            flags=re.MULTILINE,
        )
        # Also handle switcher rules inside @media blocks: just remove the switcher bit.
        cleaned = re.sub(
            r'(@media[^{]*\{)([^}]*\.lang-switcher[^{]*\{[^}]*\})+([^}]*\})',
            lambda m: m.group(1) + m.group(3),
            cleaned,
        )
        cleaned = cleaned.strip()
        if cleaned:
            existing.string = cleaned
        else:
            existing.decompose()
    for existing in soup.find_all('script', attrs={'src': True}):
        if 'i18n.js' in (existing.get('src') or ''):
            existing.decompose()

    # Add CSS
    head = soup.find('head')
    if head:
        style_tag = soup.new_tag('style')
        style_tag.string = SWITCHER_CSS
        head.append(style_tag)

    # Add switcher to the navigation
    code = LANGUAGES.get(lang_code, {}).get('native', 'EN') if lang_code != 'en' else 'EN'
    html = SWITCHER_HTML.replace('{LANG_CODE}', code)

    # Detect white-mode (partner) pages: switcher goes outside nav, next to menu button
    nav_menu = soup.find('nav', class_='white-mode')
    if nav_menu:
        # White-mode page: use dark colors for the button
        html = html.replace('rgba(255,255,255,0.15)', 'rgba(0,0,0,0.2)')
        html = html.replace('rgba(255,255,255,0.7)', 'rgba(0,0,0,0.6)')
        switcher = BeautifulSoup(html, 'html.parser')
        # Place after nav-menu-holder, before menu-button
        menu_btn = soup.find(class_='menu-button')
        if menu_btn:
            menu_btn.insert_before(switcher)
        else:
            nav_holder = soup.find(class_='nav-holder')
            if nav_holder:
                nav_holder.append(switcher)
    else:
        # Dark-mode page: place inside navlinks-holder
        navlinks = soup.find(class_='navlinks-holder')
        if navlinks:
            switcher = BeautifulSoup(html, 'html.parser')
            navlinks.append(switcher)
        else:
            # Fallback for pages without navlinks-holder (e.g. legal pages):
            # place before subscribed-visitor or append to nav-holder
            switcher = BeautifulSoup(html, 'html.parser')
            sub_visitor = soup.find(class_='subscribed-visitor')
            if sub_visitor:
                sub_visitor.insert_before(switcher)
            else:
                nav_holder = soup.find(class_='nav-holder')
                if nav_holder:
                    nav_holder.append(switcher)

    # Add i18n.js script before </body>
    body = soup.find('body')
    if body:
        script_tag = soup.new_tag('script', src='/js/i18n.js')
        body.append(script_tag)


def translate_dom(element, translations):
    """Recursively translate text nodes in the DOM tree."""
    if isinstance(element, (Comment, Doctype)):
        return
    if isinstance(element, NavigableString):
        if element.parent and element.parent.name in SKIP_TAGS:
            return
        # Skip if any ancestor has notranslate / w-embed class or translate="no"
        if element.parent and should_skip_translate(element.parent):
            return
        text = str(element)
        if text.strip():
            translated = translate_text(text, translations)
            if translated != text:
                element.replace_with(NavigableString(translated))
        return

    if hasattr(element, 'children'):
        for child in list(element.children):
            translate_dom(child, translations)


def translate_meta(soup, translations):
    """Translate meta tags, title, alt text, placeholders."""
    # Title
    title = soup.find('title')
    if title and title.string:
        title.string = translate_text(title.string, translations)

    # Meta description and OG tags
    for meta in soup.find_all('meta'):
        content = meta.get('content')
        name = meta.get('name', '') or meta.get('property', '')
        if content and name in ('description', 'og:title', 'og:description', 'twitter:title', 'twitter:description'):
            translated = translate_text(content, translations)
            if translated != content:
                meta['content'] = translated

    # Alt text
    for img in soup.find_all('img'):
        alt = img.get('alt', '')
        if alt and alt.strip():
            translated = translate_text(alt, translations)
            if translated != alt:
                img['alt'] = translated

    # Placeholders
    for inp in soup.find_all(['input', 'textarea']):
        ph = inp.get('placeholder', '')
        if ph and ph.strip():
            translated = translate_text(ph, translations)
            if translated != ph:
                inp['placeholder'] = translated

    # Button values
    for btn in soup.find_all('input', {'type': ['submit', 'button']}):
        val = btn.get('value', '')
        if val and val.strip():
            translated = translate_text(val, translations)
            if translated != val:
                btn['value'] = translated


def translate_data_attrs(soup, translations):
    """Translate content-bearing data-* attributes (drawer depth content, etc.)."""
    for attr in TRANSLATABLE_ATTRS:
        for el in soup.find_all(attrs={attr: True}):
            if should_skip_translate(el):
                continue
            val = el.get(attr)
            if not isinstance(val, str) or not val.strip():
                continue
            translated = translate_text(val, translations)
            if translated != val:
                el[attr] = translated


def process_page(html_content, lang, translations, page_path):
    """Process a single page: translate, fix URLs, add hreflang, add switcher."""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Set lang attribute
    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = lang
        if LANGUAGES[lang]['dir'] == 'rtl':
            html_tag['dir'] = 'rtl'
        else:
            # Remove dir if present
            if html_tag.get('dir'):
                del html_tag['dir']

    # Add RTL stylesheet for Arabic
    if LANGUAGES[lang]['dir'] == 'rtl':
        head = soup.find('head')
        if head:
            rtl_link = soup.new_tag('link', rel='stylesheet', href='/css/rtl.css', type='text/css')
            head.append(rtl_link)

    # Add hreflang tags
    add_hreflang_tags(soup, page_path)

    # Fix URLs (assets to absolute, internal links to localized)
    fix_urls(soup, lang, page_path)

    # Translate meta tags, title, alt, placeholders
    translate_meta(soup, translations)

    # Translate content-bearing data-* attributes (drawer depth content)
    translate_data_attrs(soup, translations)

    # Translate DOM text nodes
    body = soup.find('body')
    if body:
        translate_dom(body, translations)

    # Add language switcher and i18n.js
    add_language_switcher(soup, lang)

    # Set canonical URL (remove any inherited canonicals from the source first)
    head = soup.find('head')
    if head:
        for existing in soup.find_all('link', rel='canonical'):
            existing.decompose()
        canonical = soup.new_tag('link', rel='canonical')
        canonical['href'] = strip_html_ext(f'{BASE_URL}/{lang}/{page_path}')
        head.append(canonical)

    return str(soup)


def update_english_page(html_content, page_path):
    """Add hreflang tags and language switcher to English pages."""
    soup = BeautifulSoup(html_content, 'html.parser')

    # Set lang="en"
    html_tag = soup.find('html')
    if html_tag:
        html_tag['lang'] = 'en'

    # Add hreflang tags
    add_hreflang_tags(soup, page_path)

    # Add language switcher
    add_language_switcher(soup, 'en')

    return str(soup)


def generate_languages(target_langs=None):
    """Generate localized pages for specified languages (or all)."""
    langs = target_langs or list(LANGUAGES.keys())

    for lang in langs:
        if lang not in LANGUAGES:
            print(f'ERROR: Unknown language {lang}')
            continue

        print(f'\nGenerating {lang} ({LANGUAGES[lang]["name"]})...')
        translations = load_translations(lang)
        if not translations:
            print(f'  No translations loaded, pages will have English content')

        translated_count = 0
        for page in PAGES:
            src_path = ROOT / page
            if not src_path.exists():
                print(f'  SKIP: {page} (not found)')
                continue

            html = src_path.read_text(encoding='utf-8')
            result = process_page(html, lang, translations, page)

            dst_path = ROOT / lang / page
            dst_path.parent.mkdir(parents=True, exist_ok=True)
            dst_path.write_text(result, encoding='utf-8')
            translated_count += 1

        print(f'  Generated {translated_count} pages in /{lang}/')

    print(f'\nDone! Generated {len(langs)} language(s).')


def update_english_pages():
    """Add hreflang tags and language switcher to all English pages."""
    print('Updating English pages with hreflang tags and language switcher...')
    count = 0
    for page in PAGES:
        src_path = ROOT / page
        if not src_path.exists():
            continue

        html = src_path.read_text(encoding='utf-8')
        result = update_english_page(html, page)
        src_path.write_text(result, encoding='utf-8')
        count += 1
        print(f'  Updated {page}')

    print(f'Updated {count} English pages.')


def main():
    args = sys.argv[1:]

    if '--add-hreflang' in args or '--add-switcher' in args:
        update_english_pages()
        return

    if '--english' in args:
        update_english_pages()
        args.remove('--english')

    target_langs = [a for a in args if not a.startswith('-')]
    generate_languages(target_langs if target_langs else None)


if __name__ == '__main__':
    main()
