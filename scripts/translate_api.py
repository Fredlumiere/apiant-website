#!/usr/bin/env python3
"""
API-based translation for APIANT website localization.
Translates only MISSING strings, preserving existing translations.

Supports:
  - DeepL API (better quality for European languages)
  - Google Cloud Translation API (covers all languages)

Usage:
    # Translate missing strings for all languages
    DEEPL_API_KEY=xxx python3 scripts/translate_api.py

    # Translate specific languages only
    DEEPL_API_KEY=xxx python3 scripts/translate_api.py es fr de

    # Use Google instead of DeepL
    GOOGLE_TRANSLATE_API_KEY=xxx python3 scripts/translate_api.py --provider google

    # Dry run (show what would be translated, no API calls)
    python3 scripts/translate_api.py --dry-run

    # After translating, regenerate pages
    python3 scripts/localize.py
"""
import os
import sys
import json
import time
import urllib.request
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).parent.parent
I18N_DIR = ROOT / 'i18n'

LANGUAGES = {
    'es': {'deepl': 'ES', 'google': 'es', 'name': 'Spanish'},
    'fr': {'deepl': 'FR', 'google': 'fr', 'name': 'French'},
    'zh': {'deepl': 'ZH', 'google': 'zh-CN', 'name': 'Chinese'},
    'hi': {'deepl': None, 'google': 'hi', 'name': 'Hindi'},
    'ar': {'deepl': 'AR', 'google': 'ar', 'name': 'Arabic'},
    'he': {'deepl': None, 'google': 'he', 'name': 'Hebrew'},
    'bn': {'deepl': None, 'google': 'bn', 'name': 'Bengali'},
    'pt': {'deepl': 'PT-BR', 'google': 'pt', 'name': 'Portuguese'},
    'ru': {'deepl': 'RU', 'google': 'ru', 'name': 'Russian'},
    'ja': {'deepl': 'JA', 'google': 'ja', 'name': 'Japanese'},
    'de': {'deepl': 'DE', 'google': 'de', 'name': 'German'},
    'ko': {'deepl': 'KO', 'google': 'ko', 'name': 'Korean'},
    'it': {'deepl': 'IT', 'google': 'it', 'name': 'Italian'},
    'nl': {'deepl': 'NL', 'google': 'nl', 'name': 'Dutch'},
    'tr': {'deepl': 'TR', 'google': 'tr', 'name': 'Turkish'},
    'pl': {'deepl': 'PL', 'google': 'pl', 'name': 'Polish'},
    'vi': {'deepl': None, 'google': 'vi', 'name': 'Vietnamese'},
    'th': {'deepl': None, 'google': 'th', 'name': 'Thai'},
    'id': {'deepl': 'ID', 'google': 'id', 'name': 'Indonesian'},
    'sv': {'deepl': 'SV', 'google': 'sv', 'name': 'Swedish'},
}

# Brand names and terms to protect from translation
PROTECTED_TERMS = [
    'APIANT', 'Mindbody', 'Cliniko', 'DonorPerfect', 'HubSpot', 'Salesforce',
    'ActiveCampaign', 'Keap', 'Klaviyo', 'HighLevel', 'Zoho CRM', 'Shopify',
    'Zapier', 'Calendly', 'Zoom', 'Mailchimp', 'CRMConnect', 'ShopConnect',
    'ZoomConnect', 'CalendarConnect', 'AppConnect', 'MailConnect', 'FormApps',
    'MCP Servers', 'iPaaS', 'XPath', 'Co-Pilot',
    # Competitors named on the /compare/ pages. Absent from this list, Google
    # Translate treated them as common nouns and shipped Paragon as 'Dechado' in
    # Spanish, Workato as 'Lavorare' in Italian, Cyclr as 'Pesepeda' in Indonesian
    # and Boomi as a Bengali word for land. A brand name on a page that makes
    # sourced claims about that brand has to survive translation verbatim.
    'Prismatic', 'Tray.ai', 'Workato', 'Paragon', 'n8n', 'Cyclr', 'Boomi',
]

BATCH_SIZE = 50  # Strings per API call


def load_master_strings():
    """Load all translatable strings."""
    path = I18N_DIR / 'translatable_strings.json'
    if not path.exists():
        print('ERROR: Run scripts/extract_strings.py first')
        sys.exit(1)
    with open(path) as f:
        return json.load(f)


def load_existing_translations(lang):
    """Load existing translations for a language."""
    translations = {}

    # Shared UI
    shared_path = I18N_DIR / 'shared_ui.json'
    if shared_path.exists():
        shared = json.load(open(shared_path))
        if lang in shared:
            translations.update(shared[lang])

    # Per-language file
    path = I18N_DIR / f'{lang}.json'
    if path.exists():
        data = json.load(open(path))
        # Cache every entry, including ones whose translation equals the
        # source. Brand names, part numbers and the like translate to
        # themselves; skipping them here dropped them from the cache, so
        # every CI run re-sent ~3.3k strings and paid for identical results.
        translations.update(data)

    return translations


def find_missing(all_strings, existing):
    """Find strings that need translation."""
    missing = []
    for s in all_strings:
        if s not in existing:
            # Skip code-like, purely numeric, or very short strings
            stripped = s.strip()
            if len(stripped) <= 2:
                continue
            if stripped.startswith(('//','/*','```','import ','const ','var ','let ','function ')):
                continue
            missing.append(s)
    return missing


def protect_brands(text):
    """Wrap brand names in non-translatable tags for DeepL."""
    for term in PROTECTED_TERMS:
        text = text.replace(term, f'<keep>{term}</keep>')
    return text


def unprotect_brands(text):
    """Remove protection tags after translation."""
    import re
    text = re.sub(r'<keep>(.*?)</keep>', r'\1', text)
    text = re.sub(r'<keep>(.*?)<\/keep>', r'\1', text)
    return text


def translate_deepl(texts, target_lang, api_key):
    """Translate texts using DeepL API. Returns list of translated strings."""
    lang_code = LANGUAGES[target_lang]['deepl']
    if not lang_code:
        return None  # Language not supported by DeepL

    url = 'https://api-free.deepl.com/v2/translate'
    if not api_key.endswith(':fx'):
        url = 'https://api.deepl.com/v2/translate'

    payload = {
        'text': texts,
        'target_lang': lang_code,
        'source_lang': 'EN',
    }

    data = json.dumps(payload).encode('utf-8')
    req = urllib.request.Request(url, data=data, method='POST')
    req.add_header('Authorization', 'DeepL-Auth-Key ' + api_key)
    req.add_header('Content-Type', 'application/json')

    resp = urllib.request.urlopen(req, timeout=60)
    result = json.loads(resp.read().decode('utf-8'))

    return [t['text'] for t in result['translations']]


def translate_google(texts, target_lang, api_key):
    """Translate texts using Google Cloud Translation API v2."""
    lang_code = LANGUAGES[target_lang]['google']

    base_url = 'https://translation.googleapis.com/language/translate/v2'

    # Google Translate API works best with query parameters + POST body for text
    results = []
    # Process in sub-batches of 25 (Google has URL length limits)
    for i in range(0, len(texts), 25):
        batch = texts[i:i+25]
        params = urllib.parse.urlencode({
            'target': lang_code,
            'source': 'en',
            'format': 'text',
            'key': api_key,
        })
        # Add each text as a separate 'q' parameter
        for t in batch:
            params += '&' + urllib.parse.urlencode({'q': t})

        req = urllib.request.Request(base_url, data=params.encode('utf-8'), method='POST')
        req.add_header('Content-Type', 'application/x-www-form-urlencoded')

        resp = urllib.request.urlopen(req, timeout=30)
        result = json.loads(resp.read().decode('utf-8'))
        results.extend([t['translatedText'] for t in result['data']['translations']])

    return results


def translate_batch(texts, target_lang, provider, api_key):
    """Translate a batch of texts using the specified provider."""
    if provider == 'deepl':
        result = translate_deepl(texts, target_lang, api_key)
        if result is None:
            # DeepL doesn't support this language, fall back to Google
            google_key = os.environ.get('GOOGLE_TRANSLATE_API_KEY')
            if google_key:
                print(f'    (DeepL unsupported, falling back to Google)')
                return translate_google(texts, target_lang, google_key)
            else:
                print(f'    ERROR: DeepL unsupported and no GOOGLE_TRANSLATE_API_KEY set')
                return None
        return result
    else:
        return translate_google(texts, target_lang, api_key)


def translate_language(lang, all_strings, provider, api_key, dry_run=False):
    """Translate all missing strings for a language."""
    existing = load_existing_translations(lang)
    missing = find_missing(all_strings, existing)

    if not missing:
        print(f'  {lang} ({LANGUAGES[lang]["name"]}): fully translated, skipping')
        return 0

    print(f'  {lang} ({LANGUAGES[lang]["name"]}): {len(missing)} strings to translate')

    if dry_run:
        return len(missing)

    # Load existing file to merge into
    lang_path = I18N_DIR / f'{lang}.json'
    if lang_path.exists():
        lang_data = json.load(open(lang_path))
    else:
        lang_data = {}

    translated_count = 0
    for i in range(0, len(missing), BATCH_SIZE):
        batch = missing[i:i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1
        total_batches = (len(missing) + BATCH_SIZE - 1) // BATCH_SIZE

        print(f'    Batch {batch_num}/{total_batches} ({len(batch)} strings)...', end=' ', flush=True)

        try:
            results = translate_batch(batch, lang, provider, api_key)
            if results:
                for original, translated in zip(batch, results):
                    lang_data[original] = translated
                translated_count += len(results)
                print('OK')
            else:
                print('SKIPPED (unsupported)')
                break
        except Exception as e:
            print(f'ERROR: {e}')
            # Save progress so far
            break

        # Rate limiting: small delay between batches
        if i + BATCH_SIZE < len(missing):
            time.sleep(0.5)

    # Save merged translations
    with open(lang_path, 'w', encoding='utf-8') as f:
        json.dump(lang_data, f, ensure_ascii=False, indent=2)

    print(f'    Saved {translated_count} new translations to {lang}.json')
    return translated_count


def main():
    args = sys.argv[1:]
    dry_run = '--dry-run' in args

    # Determine provider
    provider = 'deepl'
    if '--provider' in args:
        idx = args.index('--provider')
        if idx + 1 < len(args):
            provider = args[idx + 1]

    # Remove flags and their values from args, leaving only language codes
    clean_args = []
    skip_next = False
    for a in args:
        if skip_next:
            skip_next = False
            continue
        if a in ('--provider', '--dry-run'):
            if a == '--provider':
                skip_next = True
            continue
        clean_args.append(a)
    args = clean_args

    # Get API key
    if provider == 'deepl':
        api_key = os.environ.get('DEEPL_API_KEY')
        if not api_key and not dry_run:
            print('ERROR: Set DEEPL_API_KEY environment variable')
            print('  Free tier: https://www.deepl.com/pro#developer')
            print('  Or use: --provider google with GOOGLE_TRANSLATE_API_KEY')
            sys.exit(1)
    else:
        api_key = os.environ.get('GOOGLE_TRANSLATE_API_KEY')
        if not api_key and not dry_run:
            print('ERROR: Set GOOGLE_TRANSLATE_API_KEY environment variable')
            sys.exit(1)

    # Load all strings
    all_strings = load_master_strings()
    print(f'Loaded {len(all_strings)} translatable strings')
    print(f'Provider: {provider}' + (' (DRY RUN)' if dry_run else ''))
    print()

    # Target languages
    target_langs = args if args else list(LANGUAGES.keys())

    total_translated = 0
    for lang in target_langs:
        if lang not in LANGUAGES:
            print(f'  {lang}: unknown language, skipping')
            continue
        count = translate_language(lang, all_strings, provider, api_key, dry_run)
        total_translated += count

    print(f'\nTotal: {total_translated} strings {"to translate" if dry_run else "translated"}')
    if not dry_run and total_translated > 0:
        print(f'\nRun "python3 scripts/localize.py" to regenerate pages.')


if __name__ == '__main__':
    main()
