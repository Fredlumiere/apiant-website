#!/usr/bin/env python3
"""
Translate APIANT website strings into Polish (pl), Vietnamese (vi), Thai (th), Indonesian (id).

Usage:
  export ANTHROPIC_API_KEY=sk-ant-...
  python3 translate_batch.py

Reads strings from strings_chunk_{1,2,3}.json, translates in batches via Claude Haiku,
writes output to pl.json, vi.json, th.json, id.json.
"""
import anthropic
import json
import os
import sys
import time
import re

BASE = os.path.dirname(os.path.abspath(__file__))

# ===== CONFIGURATION =====
BATCH_SIZE = 150  # strings per API call (Haiku handles this well)
MODEL = "claude-haiku-4-5"  # cost-effective for translation
MAX_RETRIES = 3
LANGUAGES = {
    "pl": "Polish (professional formal register, business Polish)",
    "vi": "Vietnamese (professional formal register, standard diacritics)",
    "th": "Thai (professional formal register, standard Thai script)",
    "id": "Indonesian (professional formal Bahasa Indonesia, not Malay)",
}

# Brand names and technical terms to keep in English
KEEP_ENGLISH = [
    "APIANT", "Mindbody", "MindBody", "Cliniko", "DonorPerfect", "HubSpot",
    "Salesforce", "ActiveCampaign", "Keap", "Klaviyo", "HighLevel", "Zoho CRM",
    "Shopify", "Zapier", "Calendly", "Zoom", "Mailchimp", "CRMConnect",
    "ShopConnect", "ZoomConnect", "CalendarConnect", "AppConnect", "MailConnect",
    "FormApps", "FormApp", "MCP Servers", "MCP", "iPaaS", "XPath",
    "API", "SDK", "OAuth", "REST", "JSON", "XML", "CSV", "HTTP", "HTTPS",
    "webhook", "endpoint", "SSO", "SAML", "GDPR", "DSAR",
    "Stripe", "Asana", "Discord", "WhatsApp", "Twilio", "Slack",
    "Splunk", "Datadog", "AWS", "Supabase", "Meta",
    "Co-Pilot", "AI Co-Pilot", "Assembly Editor", "Automation Editor",
    "Admin Console", "Exercise Coach", "CodeSync",
    "Sandbox", "Pro", "Scale", "Enterprise",
]


def load_strings():
    """Load all strings from the 3 chunk files."""
    strings = []
    for i in range(1, 4):
        path = os.path.join(BASE, f"strings_chunk_{i}.json")
        with open(path) as f:
            strings.extend(json.load(f))
    return strings


def build_translation_prompt(strings_batch, lang_code, lang_desc):
    """Build the system + user prompt for a batch of strings."""
    system = f"""You are a professional translator for the APIANT website (B2B integration platform).
Translate the following English strings to {lang_desc}.

RULES:
1. Keep brand names EXACTLY as-is: {', '.join(KEEP_ENGLISH[:30])}...
2. Keep technical terms in English where standard: API, SDK, OAuth, REST, JSON, XML, CSV, HTTP, webhook, endpoint
3. Keep code snippets, JSON examples, variable names, CSS class names, URLs, email addresses unchanged
4. Strings that are purely code/numbers/symbols/prices: return them unchanged
5. Keep person names unchanged (e.g. Emily Chen, Eric G., Brad B.)
6. Keep country names in their standard {lang_desc.split('(')[0].strip()} form
7. Preserve any HTML entities, special characters, quotation marks, and formatting
8. Maintain the same tone: professional, direct, technical but accessible
9. Do NOT add or remove content; translate precisely

OUTPUT FORMAT:
Return a JSON array of translated strings, in the EXACT same order as the input.
Each element must be the translated version of the corresponding input string.
Return ONLY the JSON array, no other text."""

    user = f"""Translate these {len(strings_batch)} strings to {lang_desc.split('(')[0].strip()}.
Return a JSON array with exactly {len(strings_batch)} elements.

INPUT:
{json.dumps(strings_batch, ensure_ascii=False, indent=2)}"""

    return system, user


def translate_batch(client, strings_batch, lang_code, lang_desc, batch_num, total_batches):
    """Translate a batch of strings using Claude API."""
    system, user = build_translation_prompt(strings_batch, lang_code, lang_desc)

    for attempt in range(MAX_RETRIES):
        try:
            print(f"  [{lang_code}] Batch {batch_num}/{total_batches} ({len(strings_batch)} strings), attempt {attempt+1}...")

            response = client.messages.create(
                model=MODEL,
                max_tokens=16000,
                system=system,
                messages=[{"role": "user", "content": user}],
            )

            # Extract text
            text = ""
            for block in response.content:
                if block.type == "text":
                    text += block.text

            # Parse JSON from response
            # Sometimes the model wraps in ```json ... ```
            text = text.strip()
            if text.startswith("```"):
                text = re.sub(r'^```\w*\n?', '', text)
                text = re.sub(r'\n?```$', '', text)
                text = text.strip()

            translations = json.loads(text)

            if len(translations) != len(strings_batch):
                print(f"    WARNING: Expected {len(strings_batch)} translations, got {len(translations)}")
                if attempt < MAX_RETRIES - 1:
                    time.sleep(2)
                    continue
                # Pad or truncate
                while len(translations) < len(strings_batch):
                    translations.append(strings_batch[len(translations)])  # fallback to English
                translations = translations[:len(strings_batch)]

            print(f"    OK ({response.usage.input_tokens} in, {response.usage.output_tokens} out)")
            return translations

        except json.JSONDecodeError as e:
            print(f"    JSON parse error: {e}")
            if attempt < MAX_RETRIES - 1:
                time.sleep(2)
                continue
            # Fallback: return English
            print(f"    FALLBACK: returning English for this batch")
            return list(strings_batch)

        except anthropic.RateLimitError:
            wait = 30 * (attempt + 1)
            print(f"    Rate limited, waiting {wait}s...")
            time.sleep(wait)
            continue

        except anthropic.APIStatusError as e:
            if e.status_code >= 500:
                wait = 10 * (attempt + 1)
                print(f"    Server error {e.status_code}, waiting {wait}s...")
                time.sleep(wait)
                continue
            raise

    # All retries exhausted
    print(f"    FALLBACK after {MAX_RETRIES} retries: returning English")
    return list(strings_batch)


def translate_language(client, all_strings, lang_code, lang_desc):
    """Translate all strings for one language."""
    print(f"\n{'='*60}")
    print(f"Translating to {lang_code} ({lang_desc})")
    print(f"{'='*60}")

    all_translations = []
    total_batches = (len(all_strings) + BATCH_SIZE - 1) // BATCH_SIZE

    for i in range(0, len(all_strings), BATCH_SIZE):
        batch = all_strings[i:i + BATCH_SIZE]
        batch_num = i // BATCH_SIZE + 1

        translations = translate_batch(client, batch, lang_code, lang_desc, batch_num, total_batches)
        all_translations.extend(translations)

        # Brief pause between batches to avoid rate limits
        if batch_num < total_batches:
            time.sleep(1)

    # Build the output dict: English -> Translation
    result = {}
    for eng, trans in zip(all_strings, all_translations):
        result[eng] = trans

    return result


def save_translations(translations, lang_code):
    """Save translations to a JSON file."""
    output_path = os.path.join(BASE, f"{lang_code}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(translations, f, ensure_ascii=False, indent=2)
    print(f"\nSaved {len(translations)} translations to {output_path}")


def main():
    # Check for API key
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        print("ERROR: ANTHROPIC_API_KEY environment variable not set.")
        print("Usage: export ANTHROPIC_API_KEY=sk-ant-... && python3 translate_batch.py")
        sys.exit(1)

    client = anthropic.Anthropic()

    # Load strings
    all_strings = load_strings()
    print(f"Loaded {len(all_strings)} strings to translate")

    # Check for existing partial results
    for lang_code, lang_desc in LANGUAGES.items():
        output_path = os.path.join(BASE, f"{lang_code}.json")
        if os.path.exists(output_path):
            with open(output_path) as f:
                existing = json.load(f)
            if len(existing) == len(all_strings):
                print(f"\n{lang_code}.json already exists with {len(existing)} strings. Skipping.")
                print(f"  Delete {output_path} to re-translate.")
                continue

        translations = translate_language(client, all_strings, lang_code, lang_desc)
        save_translations(translations, lang_code)

    print("\n" + "="*60)
    print("DONE. Translation files created:")
    for lang_code in LANGUAGES:
        path = os.path.join(BASE, f"{lang_code}.json")
        if os.path.exists(path):
            with open(path) as f:
                data = json.load(f)
            print(f"  {path}: {len(data)} strings")


if __name__ == "__main__":
    main()
