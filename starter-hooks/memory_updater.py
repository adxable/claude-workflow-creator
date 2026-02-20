#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Prompt for memory updates after significant sessions.
Suggests updates to decisions.md and lessons.md.
"""

import json
import sys
from pathlib import Path

DECISIONS_FILE = Path('.claude/memory/decisions.md')
LESSONS_FILE = Path('.claude/memory/lessons.md')
REVIEWS_DIR = Path('.claude/reviews')


def check_for_review_findings() -> list:
    """Check if recent review has significant findings."""
    if not REVIEWS_DIR.exists():
        return []

    findings = []

    # Get most recent review
    reviews = sorted(REVIEWS_DIR.glob('*.md'), key=lambda x: x.stat().st_mtime, reverse=True)
    if not reviews:
        return []

    recent_review = reviews[0]
    content = recent_review.read_text()

    # Check for critical/important issues
    if 'CRITICAL' in content or 'Critical' in content:
        findings.append('Critical issues found in review')
    if 'pattern' in content.lower() and ('inconsistent' in content.lower() or 'duplicate' in content.lower()):
        findings.append('Pattern inconsistencies detected')

    return findings


def format_memory_prompt(findings: list) -> str:
    """Format the memory update prompt."""

    output = """
\033[1m==================================================
🧠 MEMORY UPDATE PROMPT
==================================================\033[0m

"""

    if findings:
        output += "Review findings that might be worth remembering:\n"
        for finding in findings:
            output += f"  - {finding}\n"
        output += "\n"

    output += """\033[1mConsider updating:\033[0m

  📝 \033[33mdecisions.md\033[0m - New architectural or pattern decisions?
    Example: "Use queryOptions factory for all TanStack Query"
    Add with: \033[36m/memory decision "description"\033[0m

  💡 \033[33mlessons.md\033[0m - Problems solved worth remembering?
    Example: "Zustand without useShallow causes infinite loops"
    Add with: \033[36m/memory lesson "description"\033[0m

To skip: Just continue with your next task.
\033[1m==================================================\033[0m
"""

    return output


def main():
    """Hook entry point - runs on Stop event."""
    try:
        input_data = json.load(sys.stdin)

        # Stop events provide session_id and transcript_path, not commands.
        # Skip trivial sessions by checking transcript length.
        transcript_path = input_data.get('transcript_path', '')
        if transcript_path:
            try:
                size = Path(transcript_path).stat().st_size
                if size < 2000:
                    sys.exit(0)
            except OSError:
                sys.exit(0)

        # Check for review findings
        findings = check_for_review_findings()

        # Output prompt
        print(format_memory_prompt(findings))

        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == '__main__':
    main()
