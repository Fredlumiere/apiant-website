#!/bin/bash
# Update all localized pages after editing English source files.
# Usage: bash scripts/update_translations.sh
#
# What it does:
# 1. Re-extracts all translatable strings from English pages
# 2. Translates any new/missing strings via DeepL + Google Translate APIs
# 3. Regenerates all 19 language versions from the current English source
# 4. Updates English pages with hreflang tags and language switcher

set -e

export DEEPL_API_KEY="REDACTED"
export GOOGLE_TRANSLATE_API_KEY="REDACTED"

echo "=== Step 1: Extract strings ==="
python3 scripts/extract_strings.py

echo ""
echo "=== Step 2: Translate missing strings ==="
python3 scripts/translate_api.py

echo ""
echo "=== Step 3: Regenerate all localized pages ==="
python3 scripts/localize.py --english

echo ""
echo "Done. All 19 languages updated. Review and commit when ready."
