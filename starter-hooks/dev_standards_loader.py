#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Load and inject development standards from CLAUDE.md into prompts.
Ensures coding conventions are always available.
"""

import json
import sys
from pathlib import Path

CLAUDE_MD_FILE = Path('CLAUDE.md')
MEMORY_CLAUDE_MD = Path('.claude/memory/CLAUDE.md')


def load_standards() -> str:
    """Load CLAUDE.md content if exists."""
    # Try main CLAUDE.md first
    if CLAUDE_MD_FILE.exists():
        return CLAUDE_MD_FILE.read_text()

    # Fallback to memory CLAUDE.md
    if MEMORY_CLAUDE_MD.exists():
        return MEMORY_CLAUDE_MD.read_text()

    return ""


def extract_key_sections(content: str) -> str:
    """Extract key sections for context injection."""
    if not content:
        return ""

    # For now, return summary indicator
    # Full content is already loaded by Claude Code from CLAUDE.md
    lines = content.split('\n')
    line_count = len(lines)

    # Find key headers
    headers = [l.strip() for l in lines if l.startswith('#')][:10]

    if not headers:
        return ""

    output = "\n" + "-" * 50 + "\n"
    output += "DEV STANDARDS LOADED (CLAUDE.md)\n"
    output += "-" * 50 + "\n"
    output += f"Lines: {line_count}\n"
    output += "Sections:\n"
    for h in headers:
        output += f"  - {h}\n"
    output += "-" * 50 + "\n"

    return output


def main():
    """Hook entry point - inject on UserPromptSubmit."""
    try:
        input_data = json.load(sys.stdin)
        prompt = input_data.get('prompt', '').lower()

        # Only show for significant prompts
        significant_keywords = [
            'create', 'implement', 'add', 'build', 'fix', 'update',
            '/ship', '/implement', '/plan', '/refactor'
        ]

        if not any(kw in prompt for kw in significant_keywords):
            sys.exit(0)

        content = load_standards()
        if content:
            output = extract_key_sections(content)
            if output:
                print(output)

        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == '__main__':
    main()
