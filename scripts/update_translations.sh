#!/bin/bash
# Update all localized pages after editing English source files.
# Usage: bash scripts/update_translations.sh
#
# What it does:
# 1. Re-extracts all translatable strings from English pages
# 2. Translates any new/missing strings via DeepL + Google Translate APIs
# 3. Regenerates all 19 language versions from the current English source
# 4. Updates English pages with hreflang tags and language switcher
#
# API keys must be set in ~/.apiant_keys (not committed to git):
#   export DEEPL_API_KEY="your-key"
#   export GOOGLE_TRANSLATE_API_KEY="your-key"

set -e

# Load API keys from local file
if [ -f "$HOME/.apiant_keys" ]; then
  source "$HOME/.apiant_keys"
else
  echo "ERROR: ~/.apiant_keys not found."
  echo "Create it with:"
  echo '  export DEEPL_API_KEY="your-key"'
  echo '  export GOOGLE_TRANSLATE_API_KEY="your-key"'
  exit 1
fi

if [ -z "$DEEPL_API_KEY" ] || [ -z "$GOOGLE_TRANSLATE_API_KEY" ]; then
  echo "ERROR: DEEPL_API_KEY and GOOGLE_TRANSLATE_API_KEY must be set in ~/.apiant_keys"
  exit 1
fi

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
