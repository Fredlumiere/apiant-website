#!/usr/bin/env python3
"""Fix 'openPopup is not defined' and 'resetAll is not defined' on the 3 HubSpot
integration product pages.

Both are cross-script-block hoisting issues:

1. resetAll: declared with `const resetAll` inside a DOMContentLoaded handler,
   referenced by a sibling pageshow handler OUTSIDE that scope. Fix: move the
   pageshow handler inside the DOMContentLoaded callback.

2. openPopup: defined as `function openPopup(id)` in a later <script> block,
   but monkey-patched earlier via `var origOpenPopup = openPopup;` before the
   declaration block has executed. Fix: wrap the monkey-patch block in a
   DOMContentLoaded listener so it runs after all script blocks have parsed.

Idempotent.
"""
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent

PAGES = [
    "apipartners/cliniko/cliniko-hubspot-integration-automation-apiant.html",
    "apipartners/donorperfect/donorperfect-hubspot-integration-and-automation-apiant.html",
    "apipartners/mindbody/mindbody-hubspot-integration-and-automation-apiant.html",
]

# --- resetAll fix: move pageshow listener into DOMContentLoaded scope -------

RESET_ALL_BAD = re.compile(
    r'(                            wait\(\);\s*\n'
    r'                          \}\);\s*\n'
    r')(                          window\.addEventListener\(\'pageshow\', \(\) => \{\s*\n'
    r'                            resetAll\(\);\s*\n'
    r'                          \}\);)',
    re.M,
)


def fix_resetAll(content: str) -> tuple[str, bool]:
    m = RESET_ALL_BAD.search(content)
    if not m:
        # Already patched, or the pattern doesn't exist on this page
        return content, False
    replacement = (
        "                            wait();\n"
        "                            window.addEventListener('pageshow', () => { resetAll(); });\n"
        "                          });"
    )
    new_content = content[: m.start()] + replacement + content[m.end() :]
    return new_content, True


# --- openPopup fix: wrap monkey-patch block in DOMContentLoaded ------------

OPEN_POPUP_MARKER_START = "    // Reset qualification flow when popup opens\n    var origOpenPopup = openPopup;"
OPEN_POPUP_PATCHED_MARKER = "document.addEventListener('DOMContentLoaded', function cqPatchOpenPopup() {"


def fix_openPopup(content: str) -> tuple[str, bool]:
    """Wrap the openPopup monkey-patch block in DOMContentLoaded.

    Strategy: find the start ('var origOpenPopup = openPopup;') and the end
    (the closing of the assigned function, marked by 'origOpenPopup(id);\n      }\n    };').
    Replace the bare IIFE-style code with a DOMContentLoaded-wrapped version.
    """
    if OPEN_POPUP_PATCHED_MARKER in content:
        return content, False
    start_idx = content.find(OPEN_POPUP_MARKER_START)
    if start_idx == -1:
        return content, False
    # Find the closing of the assigned function: look for '    };' that closes openPopup assignment
    # The pattern: after '};\n' we usually see a new top-level statement or a close of the outer script.
    # Search forward for the closing '};' matching openPopup = function(id) { ... };
    # Simpler: search for 'origOpenPopup(id);' followed by the closing braces.
    end_marker = "      origOpenPopup(id);\n    };\n"
    end_idx = content.find(end_marker, start_idx)
    if end_idx == -1:
        return content, False
    block_end = end_idx + len(end_marker)

    block = content[start_idx:block_end]
    # Wrap
    wrapped = (
        "    // Reset qualification flow when popup opens. Wrapped in\n"
        "    // DOMContentLoaded so `openPopup` (declared in a later <script>\n"
        "    // block) has been defined before we monkey-patch it.\n"
        "    document.addEventListener('DOMContentLoaded', function cqPatchOpenPopup() {\n"
        "      if (typeof openPopup !== 'function') return;\n"
        + "    "  # indent the block one more level
        + block[4:].replace("\n    ", "\n      ").replace(
            "    // Reset qualification flow when popup opens\n    var origOpenPopup = openPopup;",
            "  var origOpenPopup = openPopup;",
        )
        + "    });\n"
    )

    # Simpler: minimal wrapping without reindent, rely on existing indent
    wrapped = (
        "    // Reset qualification flow when popup opens. Wrapped in\n"
        "    // DOMContentLoaded so `openPopup` (declared in a later <script>\n"
        "    // block) has been defined before we monkey-patch it.\n"
        "    document.addEventListener('DOMContentLoaded', function cqPatchOpenPopup() {\n"
        "      if (typeof openPopup !== 'function') return;\n"
        + block
        + "    });\n"
    )

    new_content = content[:start_idx] + wrapped + content[block_end:]
    return new_content, True


def process_file(path: Path) -> dict:
    original = path.read_text(encoding="utf-8")
    content = original
    ops = []
    content, changed = fix_resetAll(content)
    if changed:
        ops.append("resetAll")
    content, changed = fix_openPopup(content)
    if changed:
        ops.append("openPopup")
    if content != original:
        path.write_text(content, encoding="utf-8")
    return {"path": str(path.relative_to(ROOT)), "ops": ops}


def main() -> int:
    for rel in PAGES:
        p = ROOT / rel
        if not p.exists():
            print(f"MISSING: {rel}")
            continue
        r = process_file(p)
        ops = r["ops"]
        if ops:
            print(f"Fixed: {rel}  ({', '.join(ops)})")
        else:
            print(f"Already patched: {rel}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
