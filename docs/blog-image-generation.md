# Generating Blog Images with Nano Banana (Gemini)

Blog hero and inline illustrations are generated with **Nano Banana**, which is
Google's **`gemini-2.5-flash-image`** model, called through the **`@google/genai`**
SDK. This is the same recipe used across Fred's sites (e.g. aipolis.org).

## Prerequisites (already set up on Fred's machine)

- **API key:** `GEMINI_API_KEY` is exported in `~/.zshrc`, so it is present in the
  shell environment for Bash tool calls. Do not print or commit it.
- **Runtime:** `bun` (in `~/.bun/bin`) with `@google/genai` available. If a run
  reports the package is missing, install it: `bun add @google/genai`.
- **Model id:** `gemini-2.5-flash-image` (this is "Nano Banana").

## Generate an image

Write a short bun script (see `scripts/gen_blog_image.mjs` for the canonical one)
and run it with `bun`. The essentials:

```js
import { GoogleGenAI } from "@google/genai";
import { writeFileSync } from "node:fs";

const ai = new GoogleGenAI({ apiKey: process.env.GEMINI_API_KEY });
const res = await ai.models.generateContent({
  model: "gemini-2.5-flash-image",
  contents: "YOUR IMAGE PROMPT HERE",
});
// The image comes back as inline base64 data in the response parts.
for (const part of res.candidates[0].content.parts) {
  if (part.inlineData?.data) {
    writeFileSync("out.png", Buffer.from(part.inlineData.data, "base64"));
  }
}
```

### Prompt art direction (house style)

- Dark background (the blog is dark mode), conceptual editorial-tech illustration.
- One or two accent colors; APIANT green `#1ab759` works well.
- Clean, modern, not cartoony. **No text or words rendered in the image.**
- Wide 16:9 for hero images.

## Convert and host the image

The renderer reads `hero_image_url` (and inline `![](url)` links) from Supabase.
Blog imagery lives in the Supabase Storage **`blog-media`** bucket (public).

1. Convert PNG to AVIF/WebP for weight (heroes on the site are `.avif`):
   `magick out.png -quality 55 hero.avif` (or `cwebp`/`avifenc`).
2. Upload to the `blog-media` bucket via the Supabase Storage REST API using
   `SUPABASE_URL` + `SUPABASE_SERVICE_ROLE_KEY` (both in `~/.apiant_keys`):
   ```bash
   curl -sS -X POST \
     "$SUPABASE_URL/storage/v1/object/blog-media/<slug>/hero.avif" \
     -H "Authorization: Bearer $SUPABASE_SERVICE_ROLE_KEY" \
     -H "Content-Type: image/avif" \
     --data-binary @hero.avif
   ```
   Public URL: `$SUPABASE_URL/storage/v1/object/public/blog-media/<slug>/hero.avif`
3. Put that public URL in the post's `hero_image_url` (and `og_image_url`) column.

## Notes

- Load keys in a Bash call that needs them explicitly if not inherited:
  `set -a; source ~/.apiant_keys; set +a`. `GEMINI_API_KEY` comes from `~/.zshrc`.
- Nano Banana is iterative: regenerate with a refined prompt until the concept
  lands. Cache-bust hosted images by bumping a `?v=N` query param when replacing.
