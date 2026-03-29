#!/bin/bash
# Upload protected page content to Supabase Storage bucket "protected-pages"
# Requires SUPABASE_SERVICE_ROLE_KEY env var

set -euo pipefail

SUPABASE_URL="https://kereljzjgeerrdnssttu.supabase.co"
BUCKET="protected-pages"
CONTENT_DIR="$(dirname "$0")/../protected-content"

if [ -z "${SUPABASE_SERVICE_ROLE_KEY:-}" ]; then
  echo "Error: SUPABASE_SERVICE_ROLE_KEY not set"
  exit 1
fi

for file in "$CONTENT_DIR"/*.html; do
  filename=$(basename "$file")
  echo "Uploading $filename..."

  curl -s -X POST \
    "${SUPABASE_URL}/storage/v1/object/${BUCKET}/${filename}" \
    -H "Authorization: Bearer ${SUPABASE_SERVICE_ROLE_KEY}" \
    -H "Content-Type: text/html" \
    -H "x-upsert: true" \
    --data-binary "@${file}" \
    -o /dev/null -w "  %{http_code}\n"
done

echo "Done."
