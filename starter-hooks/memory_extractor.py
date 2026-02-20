#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["anthropic"]
# ///

"""
Unified Memory Extractor - Extract learnings before context is lost.

Triggered by:
- PreCompact: Before context compaction (auto or manual)
- Stop: Before session ends
- Clear: Before /clear command (via PreToolUse matcher)

Extracts valuable learnings using LLM and saves to pending/ for review.
"""

import json
import os
import re
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.constants import ensure_session_log_dir

# Paths — use project's custom memory dir (tracked in git)
MEMORY_DIR = Path('.claude/memory')
PENDING_DIR = MEMORY_DIR / "pending"
RULES_FILE = MEMORY_DIR / "rules.json"

# Minimum content to process
MIN_TRANSCRIPT_LENGTH = 1000
MAX_TRANSCRIPT_LENGTH = 20000


def load_rules() -> dict:
    """Load extraction rules from rules.json."""
    if RULES_FILE.exists():
        try:
            return json.loads(RULES_FILE.read_text())
        except Exception:
            pass
    return {
        "extract": {
            "categories": {
                "lesson": "Mistakes made and corrected, gotchas discovered",
                "convention": "Codebase-specific coding standards",
                "decision": "Architectural decisions with rationale",
                "pattern": "Recurring code patterns",
                "bug": "Bugs and their root causes"
            }
        }
    }


def parse_transcript(transcript_path: str) -> str:
    """Parse transcript file and extract text content."""
    if not transcript_path or not os.path.exists(transcript_path):
        return ""

    combined_text = []

    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                    role = msg.get('role', 'unknown')

                    # Extract text content
                    if 'content' in msg:
                        content = msg['content']
                        if isinstance(content, str):
                            combined_text.append(f"[{role}]: {content}")
                        elif isinstance(content, list):
                            text_parts = []
                            for item in content:
                                if isinstance(item, dict) and 'text' in item:
                                    text_parts.append(item['text'])
                                elif isinstance(item, str):
                                    text_parts.append(item)
                            if text_parts:
                                combined_text.append(f"[{role}]: {' '.join(text_parts)}")
                except json.JSONDecodeError:
                    continue
    except Exception as e:
        print(f"Error parsing transcript: {e}", file=sys.stderr)
        return ""

    return "\n\n".join(combined_text)


def extract_learnings_with_llm(transcript: str, rules: dict, trigger: str) -> list[dict]:
    """Use LLM to extract learnings from conversation."""
    try:
        from utils.llm.anth import call_anthropic
    except ImportError:
        print("Warning: Anthropic API not available", file=sys.stderr)
        return []

    # Truncate if too long
    if len(transcript) > MAX_TRANSCRIPT_LENGTH:
        transcript = transcript[-MAX_TRANSCRIPT_LENGTH:]
        transcript = "...[earlier content truncated]...\n\n" + transcript

    categories = rules.get("extract", {}).get("categories", {})

    prompt = f"""Analyze this Claude Code conversation and extract memory-worthy learnings.

## Trigger: {trigger}
The conversation is about to be {'compacted' if trigger == 'PreCompact' else 'cleared/ended'}.
Extract any valuable learnings before context is lost.

## What to Extract (be VERY selective)

INCLUDE:
- Mistakes Claude made that were corrected
- Codebase-specific patterns discovered
- User preferences and conventions explained
- Decisions made with rationale (why X over Y)
- Bugs found and their root causes

EXCLUDE:
- Generic programming knowledge
- One-off fixes or typos
- Information in standard documentation
- Temporary debugging steps

## Categories
{json.dumps(categories, indent=2)}

## Conversation
{transcript}

## Output
Return a JSON array. Each learning:
- "category": one of {list(categories.keys())}
- "title": brief title (max 8 words)
- "content": the learning (max 150 chars, specific and actionable)
- "context": why this matters (max 80 chars)
- "confidence": "high" | "medium"
- "tags": relevant tags ["frontend", "api", "zustand", etc.]

Rules:
- Maximum 5 learnings (quality over quantity)
- Only high/medium confidence items
- Must be specific to THIS codebase
- If nothing valuable, return: []

Return ONLY valid JSON array."""

    try:
        response = call_anthropic(
            prompt=prompt,
            model="claude-sonnet-4-20250514",
            max_tokens=2000
        )

        content = response.strip()

        # Handle markdown code blocks
        if "```" in content:
            match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', content)
            if match:
                content = match.group(1)

        learnings = json.loads(content)
        return learnings if isinstance(learnings, list) else []
    except Exception as e:
        print(f"LLM extraction error: {e}", file=sys.stderr)
        return []


def save_to_pending(
    learnings: list[dict],
    session_id: str,
    trigger: str
) -> Path | None:
    """Save extracted learnings to pending folder."""
    if not learnings:
        return None

    PENDING_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    filename = f"{timestamp}-{trigger.lower()}-{session_id[:8]}.md"
    filepath = PENDING_DIR / filename

    content = f"""# Pending Memory Fragments

> **Trigger**: {trigger}
> **Session**: {session_id}
> **Extracted**: {datetime.now().strftime("%Y-%m-%d %H:%M")}

---

"""

    for i, learning in enumerate(learnings, 1):
        category = learning.get("category", "unknown").upper()
        title = learning.get("title", "Untitled")
        body = learning.get("content", "")
        context = learning.get("context", "")
        confidence = learning.get("confidence", "medium")
        tags = learning.get("tags", [])

        content += f"""## {i}. [{category}] {title}

**Confidence**: {confidence}
**Tags**: {', '.join(tags) if tags else 'none'}

{body}

> {context}

---

"""

    content += """
## Review Commands

```
/memory review          # Interactive review
/memory approve 1,2     # Approve to L2 (searchable)
/memory promote 1,2     # Promote to L1 (MEMORY.md)
/memory reject 1,2      # Archive
```
"""

    filepath.write_text(content)
    return filepath


def auto_store_high_confidence(learnings: list[dict], session_id: str) -> int:
    """Store high-confidence learnings to L2 automatically."""
    try:
        from utils.knowledge_store import Fragment, DualKnowledgeStore
        store = DualKnowledgeStore()
    except ImportError:
        return 0

    stored = 0
    for learning in learnings:
        if learning.get("confidence") != "high":
            continue

        try:
            fragment = Fragment(
                content=learning.get("content", ""),
                tags=learning.get("tags", []),
                source=f"auto:{session_id[:8]}",
                scope="shared",
                metadata={
                    "category": learning.get("category"),
                    "title": learning.get("title"),
                    "auto_stored": True
                }
            )
            store.add(fragment)
            stored += 1
        except Exception:
            continue

    return stored


def log_extraction(session_id: str, trigger: str, learnings: int, pending_file: Path | None):
    """Log the extraction event."""
    try:
        log_dir = ensure_session_log_dir(session_id)
        log_file = log_dir / 'memory_extraction.json'

        entry = {
            'timestamp': datetime.now().isoformat(),
            'trigger': trigger,
            'learnings_extracted': learnings,
            'pending_file': str(pending_file) if pending_file else None
        }

        data = []
        if log_file.exists():
            try:
                data = json.loads(log_file.read_text())
            except Exception:
                pass

        data.append(entry)
        log_file.write_text(json.dumps(data, indent=2))
    except Exception:
        pass


def main():
    """Main entry point."""
    try:
        input_data = json.load(sys.stdin)

        session_id = input_data.get('session_id', 'unknown')
        transcript_path = input_data.get('transcript_path', '')
        trigger = input_data.get('hook_event_name', 'Unknown')

        # Parse transcript
        transcript = parse_transcript(transcript_path)

        if len(transcript) < MIN_TRANSCRIPT_LENGTH:
            sys.exit(0)

        # Load rules
        rules = load_rules()

        # Extract learnings
        learnings = extract_learnings_with_llm(transcript, rules, trigger)

        if not learnings:
            sys.exit(0)

        # Save to pending
        pending_file = save_to_pending(learnings, session_id, trigger)

        # Auto-store high confidence
        auto_stored = auto_store_high_confidence(learnings, session_id)

        # Log
        log_extraction(session_id, trigger, len(learnings), pending_file)

        # Output for user
        if pending_file:
            print(f"\n📝 Memory: Extracted {len(learnings)} learnings ({trigger})")
            if auto_stored > 0:
                print(f"   ✓ Auto-stored {auto_stored} high-confidence to L2")
            print(f"   → Review with '/memory review'\n")

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:
        print(f"Memory extractor error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()
