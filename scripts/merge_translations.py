#!/usr/bin/env python3
"""
Merge partial translation files into complete ones.
Handles cases where translations were generated in chunks (e.g., fr_part1.json, fr_part2.json, fr_part3.json -> fr.json)
"""
import json
import sys
from pathlib import Path

I18N_DIR = Path(__file__).parent.parent / 'i18n'

LANGUAGES = ['es', 'fr', 'zh', 'hi', 'ar', 'bn', 'pt', 'ru', 'ja', 'de', 'ko', 'it', 'nl', 'tr', 'pl', 'vi', 'th', 'id', 'sv']

def merge_lang(lang):
    """Merge partial files for a language into one complete file."""
    merged = {}
    parts_found = 0

    # Check for part files
    for i in range(1, 10):
        part_path = I18N_DIR / f'{lang}_part{i}.json'
        if part_path.exists():
            with open(part_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            merged.update(data)
            parts_found += 1
            print(f'  Loaded {part_path.name}: {len(data)} entries')

    if parts_found == 0:
        # Check if complete file already exists
        complete_path = I18N_DIR / f'{lang}.json'
        if complete_path.exists():
            with open(complete_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            print(f'  {lang}.json already exists with {len(data)} entries')
            return len(data)
        else:
            print(f'  No files found for {lang}')
            return 0

    # Write merged file
    out_path = I18N_DIR / f'{lang}.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(merged, f, ensure_ascii=False, indent=2)

    print(f'  Merged {parts_found} parts -> {out_path.name}: {len(merged)} total entries')

    # Clean up part files
    for i in range(1, 10):
        part_path = I18N_DIR / f'{lang}_part{i}.json'
        if part_path.exists():
            part_path.unlink()
            print(f'  Removed {part_path.name}')

    return len(merged)


def main():
    target = sys.argv[1:] if len(sys.argv) > 1 else LANGUAGES

    for lang in target:
        print(f'\n{lang}:')
        merge_lang(lang)


if __name__ == '__main__':
    main()
