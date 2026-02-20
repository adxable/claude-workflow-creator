#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Load and inject session context and L1 memory into prompts.
Provides continuity across sessions and core project knowledge.

L1 Memory Files (always loaded for significant prompts):
- decisions.md - Architectural decisions
- lessons.md - Lessons learned
- conventions.md - Code conventions
"""

import json
import sys
from pathlib import Path
from datetime import datetime

CONTEXT_FILE = Path('.claude/context/session_context.json')
MEMORY_DIR = Path('.claude/memory')

# L1 files to always load
L1_FILES = [
    'decisions.md',
    'lessons.md',
    'conventions.md',
]


def load_context() -> dict:
    """Load session context if exists."""
    if CONTEXT_FILE.exists():
        return json.loads(CONTEXT_FILE.read_text())
    return {}


def save_context(context: dict):
    """Save updated context."""
    CONTEXT_FILE.parent.mkdir(parents=True, exist_ok=True)
    context['lastUpdated'] = datetime.now().isoformat()
    CONTEXT_FILE.write_text(json.dumps(context, indent=2))


def load_l1_memory() -> dict[str, str]:
    """Load L1 memory files."""
    l1_content = {}
    for filename in L1_FILES:
        filepath = MEMORY_DIR / filename
        if filepath.exists():
            l1_content[filename] = filepath.read_text()
    return l1_content


def format_l1_summary(l1_content: dict[str, str]) -> str:
    """Format L1 memory for injection - actual content, truncated per file."""
    if not l1_content:
        return ""

    MAX_LINES_PER_FILE = 80

    output_parts = []
    output_parts.append("")
    output_parts.append("-" * 50)
    output_parts.append("L1 MEMORY (Core Knowledge)")
    output_parts.append("-" * 50)

    for filename, content in l1_content.items():
        lines = content.split('\n')
        name = filename.replace('.md', '').title()

        output_parts.append(f"\n### {name}")

        truncated = lines[:MAX_LINES_PER_FILE]
        output_parts.extend(truncated)

        if len(lines) > MAX_LINES_PER_FILE:
            output_parts.append(f"\n... ({len(lines) - MAX_LINES_PER_FILE} more lines, see .claude/memory/{filename})")

    output_parts.append("")
    output_parts.append("-" * 50)

    return "\n".join(output_parts)


def format_context_summary(context: dict) -> str:
    """Format session context for injection into prompt."""
    if not context:
        return ""

    output_parts = []

    # Recent plans
    plans = context.get('previousPlans', [])[-3:]  # Last 3
    if plans:
        output_parts.append("Recent Plans:")
        for plan in plans:
            status = plan.get('status', 'unknown')
            summary = plan.get('summary', 'No summary')
            output_parts.append(f"  - {summary} ({status})")

    # Key decisions
    decisions = context.get('decisions', [])[-5:]  # Last 5
    if decisions:
        output_parts.append("\nKey Decisions:")
        for d in decisions:
            decision = d.get('decision', '')
            reason = d.get('reason', '')
            output_parts.append(f"  - {decision}: {reason}")

    # Established patterns
    patterns = context.get('patterns', {})
    if patterns:
        output_parts.append("\nEstablished Patterns:")
        for name, pattern in patterns.items():
            output_parts.append(f"  - {name}: {pattern}")

    # Blocked patterns
    blocked = context.get('blockedPatterns', [])
    if blocked:
        output_parts.append("\nDo NOT use:")
        for b in blocked:
            pattern = b.get('pattern', '')
            reason = b.get('reason', '')
            output_parts.append(f"  - {pattern} ({reason})")

    # Recent lessons
    lessons = context.get('recentLessons', [])[-3:]  # Last 3
    if lessons:
        output_parts.append("\nRecent Lessons:")
        for lesson in lessons:
            output_parts.append(f"  - {lesson.get('lesson', '')}")

    if not output_parts:
        return ""

    header = "\n" + "-" * 50 + "\n"
    header += "SESSION CONTEXT (from previous sessions)\n"
    header += "-" * 50 + "\n"

    return header + "\n".join(output_parts) + "\n" + "-" * 50 + "\n"


def main():
    """Hook entry point - inject context on UserPromptSubmit."""
    try:
        input_data = json.load(sys.stdin)
        prompt = input_data.get('prompt', '').lower()

        # Keywords that trigger context loading
        relevant_keywords = [
            'plan', 'implement', 'create', 'add', 'build', 'feature',
            'fix', 'refactor', 'update', 'change', 'modify',
            '/ship', '/plan', '/implement', '/flow', '/pipe'
        ]

        if not any(kw in prompt for kw in relevant_keywords):
            sys.exit(0)

        output_parts = []

        # Load and format session context
        context = load_context()
        if context:
            context_output = format_context_summary(context)
            if context_output:
                output_parts.append(context_output)

        # Load and format L1 memory (summary only)
        l1_content = load_l1_memory()
        if l1_content:
            l1_output = format_l1_summary(l1_content)
            if l1_output:
                output_parts.append(l1_output)

        if output_parts:
            print("\n".join(output_parts))

        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == '__main__':
    main()
