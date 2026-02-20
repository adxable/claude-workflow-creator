#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = ["anthropic"]
# ///

"""
Knowledge Ingestor Hook - Stop hook for extracting and storing session learnings.

This hook runs at the end of a Claude session and:
1. Parses the session transcript
2. Uses LLM to extract meaningful learnings (decisions, patterns, lessons, bugs)
3. Saves fragments to pending/ folder for user review
4. Optionally auto-stores low-risk fragments to knowledge store

Event: Stop
Input: Session data including transcript_path
Output: Prints summary of extracted fragments
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

# Paths — memory lives inside the project's .claude/ directory
PROJECT_DIR = Path(__file__).parent.parent
MEMORY_DIR = PROJECT_DIR / "memory"
PENDING_DIR = MEMORY_DIR / "pending"
RULES_FILE = MEMORY_DIR / "rules.json"

# File patterns mentioned in sessions
FILE_PATTERN = re.compile(r'(?:src/|\.claude/|\./)[\w/.-]+\.\w+')

# Minimum session length to process (characters)
MIN_SESSION_LENGTH = 500


def load_rules() -> dict:
    """Load extraction rules from rules.json."""
    if RULES_FILE.exists():
        try:
            return json.loads(RULES_FILE.read_text())
        except Exception:
            pass
    return get_default_rules()


def get_default_rules() -> dict:
    """Default extraction rules if rules.json doesn't exist."""
    return {
        "extract": {
            "categories": {
                "lesson": "Mistakes made and corrected, gotchas discovered",
                "convention": "Codebase-specific coding standards and patterns",
                "decision": "Architectural decisions and their rationale",
                "pattern": "Recurring code patterns specific to this codebase",
                "bug": "Bugs encountered and their root causes"
            },
            "triggers": {
                "include": [
                    "User corrects Claude's mistake",
                    "Claude discovers unexpected behavior",
                    "User explains 'why' something is done a certain way",
                    "Pattern appears 2+ times in conversation",
                    "User says 'remember', 'always', 'never', 'important'"
                ],
                "exclude": [
                    "Generic programming knowledge",
                    "One-off typo fixes",
                    "Information already in CLAUDE.md",
                    "Temporary debugging steps"
                ]
            }
        }
    }


def parse_transcript(transcript_path: str) -> tuple[str, list[dict]]:
    """
    Parse a Claude transcript file (.jsonl format).

    Returns:
        Tuple of (combined text, list of messages)
    """
    if not os.path.exists(transcript_path):
        return "", []

    combined_text = []
    messages = []

    try:
        with open(transcript_path, 'r', encoding='utf-8') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    msg = json.loads(line)
                    messages.append(msg)

                    # Extract text content
                    if 'content' in msg:
                        content = msg['content']
                        if isinstance(content, str):
                            combined_text.append(content)
                        elif isinstance(content, list):
                            for item in content:
                                if isinstance(item, dict) and 'text' in item:
                                    combined_text.append(item['text'])
                                elif isinstance(item, str):
                                    combined_text.append(item)
                except json.JSONDecodeError:
                    continue
    except Exception:
        return "", []

    return "\n".join(combined_text), messages


def extract_files_worked_on(text: str) -> list[str]:
    """Extract file paths mentioned in the session."""
    matches = FILE_PATTERN.findall(text)
    seen = set()
    unique_files = []
    for f in matches:
        if f not in seen:
            seen.add(f)
            unique_files.append(f)
    return unique_files[:20]


def extract_learnings_with_llm(transcript: str, rules: dict) -> list[dict]:
    """Use LLM to extract learnings from conversation transcript."""
    try:
        from utils.llm.anth import call_anthropic
    except ImportError:
        print("Warning: Anthropic API not available, skipping LLM extraction", file=sys.stderr)
        return []

    # Truncate transcript if too long (keep last 15000 chars for context)
    if len(transcript) > 15000:
        transcript = "...[earlier content truncated]...\n\n" + transcript[-15000:]

    categories = rules.get("extract", {}).get("categories", {})
    triggers = rules.get("extract", {}).get("triggers", {})

    prompt = f"""Analyze this Claude Code conversation and extract memory-worthy learnings.

## What to Extract

INCLUDE learnings about:
- Mistakes Claude made that were corrected (valuable for avoiding future errors)
- Codebase-specific patterns discovered (not generic programming knowledge)
- User preferences and conventions explained
- Decisions made with rationale (why X over Y)
- Bugs found and their root causes
- "Always" or "never" rules the user mentioned

EXCLUDE:
- Generic programming knowledge (e.g., "React uses components")
- One-off typo fixes or simple corrections
- Things that would be in standard documentation
- Temporary debugging steps
- Speculation or uncertain information

## Categories
{json.dumps(categories, indent=2)}

## Conversation Transcript
{transcript}

## Output Format
Return a JSON array. Each learning should have:
- "category": one of {list(categories.keys())}
- "title": brief title (max 8 words)
- "content": the learning (max 150 chars, actionable, specific to THIS codebase)
- "context": why this matters (max 80 chars)
- "confidence": "high" | "medium" (only include high/medium confidence items)
- "tags": relevant tags like ["frontend", "api", "ag-grid", "zustand"]

Rules:
- Be VERY selective - only extract truly valuable, reusable learnings
- Maximum 5 learnings per session (quality over quantity)
- Content must be specific and actionable, not vague
- If nothing worth remembering, return empty array: []

Return ONLY valid JSON array, no markdown or explanation."""

    try:
        response = call_anthropic(
            prompt=prompt,
            model="claude-sonnet-4-20250514",
            max_tokens=2000
        )

        # Parse JSON from response
        content = response.strip()

        # Handle markdown code blocks
        if "```" in content:
            # Extract content between code blocks
            match = re.search(r'```(?:json)?\s*([\s\S]*?)\s*```', content)
            if match:
                content = match.group(1)

        learnings = json.loads(content)
        return learnings if isinstance(learnings, list) else []
    except json.JSONDecodeError as e:
        print(f"Warning: Failed to parse LLM response as JSON: {e}", file=sys.stderr)
        return []
    except Exception as e:
        print(f"Warning: LLM extraction failed: {e}", file=sys.stderr)
        return []


def save_to_pending(
    learnings: list[dict],
    session_id: str,
    files_worked_on: list[str]
) -> Path | None:
    """Save extracted learnings to pending folder for review."""
    if not learnings:
        return None

    PENDING_DIR.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d-%H%M")
    filename = f"{timestamp}-{session_id[:8]}.md"
    filepath = PENDING_DIR / filename

    content = f"""# Pending Memory Fragments

> **Session**: {session_id}
> **Extracted**: {datetime.now().strftime("%Y-%m-%d %H:%M")}
> **Files worked on**: {', '.join(files_worked_on[:5]) if files_worked_on else 'N/A'}

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

```bash
/memory review              # Interactive review
/memory approve 1,2,3       # Approve specific fragments
/memory reject 1,2          # Reject specific fragments
/memory promote <id>        # Promote to MEMORY.md (L1)
```
"""

    filepath.write_text(content)
    return filepath


def save_to_knowledge_store(
    learnings: list[dict],
    session_id: str,
    files_worked_on: list[str],
    auto_store_threshold: str = "high"
) -> int:
    """
    Store high-confidence learnings directly to knowledge store.

    Returns number of fragments stored.
    """
    try:
        from utils.knowledge_store import Fragment, DualKnowledgeStore
        store = DualKnowledgeStore()
    except ImportError:
        return 0

    stored_count = 0

    for learning in learnings:
        # Only auto-store high confidence items
        if auto_store_threshold == "high" and learning.get("confidence") != "high":
            continue

        tags = learning.get("tags", [])

        # Add context from files
        for filepath in files_worked_on[:3]:
            if '.tsx' in filepath or '.ts' in filepath:
                if 'frontend' not in tags:
                    tags.append('frontend')
            if '.cs' in filepath:
                if 'backend' not in tags:
                    tags.append('backend')

        try:
            fragment = Fragment(
                content=learning.get("content", ""),
                tags=tags,
                source=f"session:{session_id}",
                scope="shared",
                metadata={
                    "category": learning.get("category"),
                    "title": learning.get("title"),
                    "context": learning.get("context"),
                    "confidence": learning.get("confidence"),
                    "auto_stored": True
                }
            )
            store.add(fragment)
            stored_count += 1
        except Exception:
            continue

    return stored_count


def log_ingestion(
    session_id: str,
    learnings_count: int,
    pending_file: Path | None,
    auto_stored: int,
    files_worked_on: list[str]
) -> None:
    """Log the ingestion results."""
    try:
        log_dir = ensure_session_log_dir(session_id)
        log_file = log_dir / 'knowledge_ingestion.json'

        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'session_id': session_id,
            'learnings_extracted': learnings_count,
            'pending_file': str(pending_file) if pending_file else None,
            'auto_stored': auto_stored,
            'files_worked_on': files_worked_on[:10]
        }

        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    log_data = json.load(f)
            except (json.JSONDecodeError, ValueError):
                log_data = []
        else:
            log_data = []

        log_data.append(log_entry)

        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)
    except Exception:
        pass


def main():
    """Main entry point for the hook."""
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        session_id = input_data.get('session_id', 'unknown')
        transcript_path = input_data.get('transcript_path', '')

        # Skip if no transcript
        if not transcript_path:
            sys.exit(0)

        # Parse transcript
        combined_text, messages = parse_transcript(transcript_path)

        # Skip short sessions
        if not combined_text or len(combined_text) < MIN_SESSION_LENGTH:
            sys.exit(0)

        # Load rules
        rules = load_rules()

        # Extract learnings with LLM
        learnings = extract_learnings_with_llm(combined_text, rules)

        if not learnings:
            sys.exit(0)

        # Extract files worked on
        files_worked_on = extract_files_worked_on(combined_text)

        # Save all to pending for review
        pending_file = save_to_pending(learnings, session_id, files_worked_on)

        # Auto-store high-confidence items to knowledge store
        auto_stored = save_to_knowledge_store(
            learnings,
            session_id,
            files_worked_on,
            auto_store_threshold="high"
        )

        # Log results
        log_ingestion(
            session_id,
            len(learnings),
            pending_file,
            auto_stored,
            files_worked_on
        )

        # Print summary for user
        if pending_file:
            print(f"\n📝 Extracted {len(learnings)} memory fragments")
            print(f"   → Saved to: {pending_file.name}")
            if auto_stored > 0:
                print(f"   → Auto-stored {auto_stored} high-confidence items to L2")
            print(f"   → Run '/memory review' to approve/reject\n")

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception as e:
        print(f"Knowledge ingestor error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()
