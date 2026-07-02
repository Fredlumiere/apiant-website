// Generate a blog image with Nano Banana (Gemini gemini-2.5-flash-image).
// Usage: GEMINI_API_KEY=... bun scripts/gen_blog_image.mjs "<prompt>" out.png
// See docs/blog-image-generation.md for the full recipe.
import { GoogleGenAI } from "@google/genai";
import { writeFileSync } from "node:fs";

const [prompt, outPath = "out.png"] = process.argv.slice(2);
if (!prompt) {
  console.error('Usage: bun scripts/gen_blog_image.mjs "<prompt>" out.png');
  process.exit(1);
}
const apiKey = process.env.GEMINI_API_KEY;
if (!apiKey) {
  console.error("GEMINI_API_KEY not set (it lives in ~/.zshrc).");
  process.exit(1);
}

const ai = new GoogleGenAI({ apiKey });
const res = await ai.models.generateContent({
  model: "gemini-2.5-flash-image",
  contents: prompt,
});

let wrote = false;
for (const part of res.candidates?.[0]?.content?.parts ?? []) {
  if (part.inlineData?.data) {
    writeFileSync(outPath, Buffer.from(part.inlineData.data, "base64"));
    console.log("wrote", outPath, "(" + part.inlineData.mimeType + ")");
    wrote = true;
  } else if (part.text) {
    console.log("model text:", part.text);
  }
}
if (!wrote) {
  console.error("No image returned. Full response:");
  console.error(JSON.stringify(res, null, 2).slice(0, 2000));
  process.exit(2);
}
