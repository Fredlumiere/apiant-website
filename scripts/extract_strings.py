#!/usr/bin/env python3
"""
Extract all translatable strings from APIANT website HTML pages.
Outputs a JSON file with all unique strings grouped by page.
"""
import os
import sys
import json
import re
from pathlib import Path
from bs4 import BeautifulSoup, NavigableString, Comment

ROOT = Path(__file__).parent.parent

PAGES = [
    'index.html',
    'pricing.html',
    'ai.html',
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
]

SKIP_TAGS = {'script', 'style', 'code', 'pre', 'svg', 'math', 'noscript'}

def extract_strings(html_content):
    """Extract all translatable text strings from HTML."""
    soup = BeautifulSoup(html_content, 'html.parser')
    strings = set()

    # Extract title
    title = soup.find('title')
    if title and title.string:
        s = title.string.strip()
        if s:
            strings.add(s)

    # Extract meta content
    for meta in soup.find_all('meta'):
        content = meta.get('content', '')
        name = meta.get('name', '') or meta.get('property', '')
        if content and name in ('description', 'og:title', 'og:description', 'twitter:title', 'twitter:description'):
            s = content.strip()
            if s:
                strings.add(s)

    # Extract alt text
    for img in soup.find_all('img'):
        alt = img.get('alt', '').strip()
        if alt and alt not in ('', 'Drop Down Icon'):
            strings.add(alt)

    # Extract placeholder text
    for inp in soup.find_all(['input', 'textarea']):
        ph = inp.get('placeholder', '').strip()
        if ph:
            strings.add(ph)

    # Extract button/submit values
    for btn in soup.find_all('input', {'type': ['submit', 'button']}):
        val = btn.get('value', '').strip()
        if val:
            strings.add(val)

    # Walk DOM for text nodes
    def walk(element):
        if isinstance(element, Comment):
            return
        if isinstance(element, NavigableString):
            if element.parent and element.parent.name in SKIP_TAGS:
                return
            text = str(element).strip()
            # Skip empty, purely numeric, or very short strings
            if text and len(text) > 1 and not text.replace('.', '').replace(',', '').isdigit():
                # Skip strings that look like code/URLs/emails
                if not re.match(r'^[\w\-\.]+@[\w\-\.]+$', text) and \
                   not re.match(r'^https?://', text) and \
                   not re.match(r'^[\d\.\,\%\$\+\-\/\*\=\#]+$', text) and \
                   not re.match(r'^[A-Z0-9\-_]+$', text):
                    strings.add(text)
            return
        for child in element.children:
            walk(child)

    body = soup.find('body')
    if body:
        walk(body)

    return strings


def main():
    all_strings = set()
    page_strings = {}

    for page in PAGES:
        path = ROOT / page
        if not path.exists():
            print(f'WARNING: {page} not found', file=sys.stderr)
            continue
        html = path.read_text(encoding='utf-8')
        strings = extract_strings(html)
        page_strings[page] = sorted(strings)
        all_strings.update(strings)
        print(f'{page}: {len(strings)} strings', file=sys.stderr)

    # Sort all strings
    sorted_strings = sorted(all_strings)

    # Output
    output = {
        'total_unique_strings': len(sorted_strings),
        'all_strings': sorted_strings,
        'per_page': page_strings
    }

    out_path = ROOT / 'i18n' / 'strings_master.json'
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=2)

    print(f'\nTotal unique strings: {len(sorted_strings)}', file=sys.stderr)
    print(f'Output: {out_path}', file=sys.stderr)


if __name__ == '__main__':
    main()
