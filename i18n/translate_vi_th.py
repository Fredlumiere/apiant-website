#!/usr/bin/env python3
"""
Translate APIANT website strings to Vietnamese and Thai using Google Translate.
"""

import json
import re
import time
import sys
from deep_translator import GoogleTranslator

def should_passthrough(s):
    """Check if string should be kept unchanged."""
    stripped = s.strip()
    # Pure numbers, timestamps, codes, symbols
    if re.match(r'^[\d\.\,\:\;\$\%\+\-\/\*\#\@\!\?\&\=\<\>\|\~\^\[\]\(\)\{\}\\\s"\'→•–✓✗✔]+$', stripped):
        return True
    if re.match(r'^[\d\.]+s$', stripped):
        return True
    if re.match(r'^\$[\d\.\,\+kKmM\s\/\-–]+(/mo(nth)?)?$', stripped):
        return True
    if re.match(r'^/[\w/\{\}\.\-]+$', stripped):
        return True
    if re.match(r'^"?[\w\.\-\+]+@[\w\.\-]+"?$', stripped):
        return True
    if re.match(r'^"[\w\-\@\.]+\"$', stripped):
        return True
    if re.match(r'^v[\d\.]+$', stripped):
        return True
    if stripped in ('200 OK', '185/10s', '/mo', '/month', 'APIANT'):
        return True
    if len(stripped) <= 2 and not stripped.isalpha():
        return True
    return False


def translate_all(lang_code):
    """Translate all strings to target language."""
    base = '/Users/fredericlumiere/apiant-website/i18n'
    all_strings = []
    for i in range(1, 4):
        with open(f'{base}/strings_chunk_{i}.json') as f:
            all_strings.extend(json.load(f))

    translator = GoogleTranslator(source='en', target=lang_code)
    result = {}
    total = len(all_strings)
    translated_count = 0
    passthrough_count = 0
    error_count = 0

    for idx, s in enumerate(all_strings):
        if idx % 100 == 0:
            print(f'[{lang_code}] Progress: {idx}/{total} (translated={translated_count}, passthrough={passthrough_count}, errors={error_count})', flush=True)

        if should_passthrough(s):
            result[s] = s
            passthrough_count += 1
            continue

        # Try to translate
        retries = 0
        success = False
        while retries < 3 and not success:
            try:
                translated = translator.translate(s)
                if translated and translated.strip():
                    result[s] = translated
                    translated_count += 1
                    success = True
                else:
                    result[s] = s
                    passthrough_count += 1
                    success = True
            except Exception as e:
                retries += 1
                if retries < 3:
                    time.sleep(2 * retries)
                else:
                    print(f'  ERROR at {idx}: {str(e)[:80]}', flush=True)
                    result[s] = s
                    error_count += 1

        # Small delay to avoid rate limiting (every 10 strings)
        if idx % 10 == 0:
            time.sleep(0.1)

    print(f'[{lang_code}] DONE: {total} total, {translated_count} translated, {passthrough_count} passthrough, {error_count} errors', flush=True)
    return result


def main():
    base = '/Users/fredericlumiere/apiant-website/i18n'
    lang = sys.argv[1] if len(sys.argv) > 1 else 'both'

    if lang in ('vi', 'both'):
        print('=== Translating to Vietnamese ===', flush=True)
        vi = translate_all('vi')
        with open(f'{base}/vi.json', 'w', encoding='utf-8') as f:
            json.dump(vi, f, ensure_ascii=False, indent=2)
        print(f'Wrote vi.json with {len(vi)} entries', flush=True)

    if lang in ('th', 'both'):
        print('=== Translating to Thai ===', flush=True)
        th = translate_all('th')
        with open(f'{base}/th.json', 'w', encoding='utf-8') as f:
            json.dump(th, f, ensure_ascii=False, indent=2)
        print(f'Wrote th.json with {len(th)} entries', flush=True)

    print('Done!', flush=True)


if __name__ == '__main__':
    main()
