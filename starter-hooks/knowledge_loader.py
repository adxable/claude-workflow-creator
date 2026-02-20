#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Knowledge Loader Hook - UserPromptSubmit hook for semantic knowledge retrieval.

This hook reads the user's prompt and retrieves relevant knowledge fragments
from the semantic memory system. It outputs matched fragments as formatted
context that gets injected into Claude's context.

Runs alongside existing hooks (does NOT replace smart_context_loader.py -
that still handles skill suggestions).

Event: UserPromptSubmit
Output: Formatted context injection (stdout)
"""

import json
import os
import sys
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Any

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from utils.constants import ensure_session_log_dir

# Import knowledge retrieval (lazy to avoid slow startup)
_retriever = None


def get_retriever():
    """Lazy-load the retriever to avoid slow startup."""
    global _retriever
    if _retriever is None:
        from utils.knowledge_retriever import KnowledgeRetriever
        _retriever = KnowledgeRetriever()
    return _retriever


def should_retrieve(prompt: str) -> bool:
    """
    Determine if we should attempt knowledge retrieval for this prompt.

    Skip retrieval for very short prompts, commands, or system messages.
    """
    # Skip empty or very short prompts
    if not prompt or len(prompt.strip()) < 10:
        return False

    prompt_lower = prompt.lower().strip()

    # Skip if it's a command
    if prompt_lower.startswith('/'):
        return False

    # Skip common non-question patterns
    skip_patterns = [
        'yes', 'no', 'ok', 'okay', 'thanks', 'thank you',
        'continue', 'proceed', 'go ahead', 'stop', 'cancel',
        'good', 'great', 'perfect', 'nice', 'cool'
    ]
    if prompt_lower in skip_patterns:
        return False

    return True


def format_output(
    fragments: List[Any],
    scores: List[float],
    prompt_preview: str
) -> str:
    """Format the knowledge fragments for output."""
    if not fragments:
        return ""

    lines = [
        "",
        "-" * 50,
        "RELEVANT KNOWLEDGE (L2)",
        "-" * 50,
        ""
    ]

    for fragment, score in zip(fragments, scores):
        # Show scope indicator and tags
        scope_icon = "📁" if fragment.scope == "shared" else "👤"
        tag_str = f" [{', '.join(fragment.tags)}]" if fragment.tags else ""

        lines.append(f"{scope_icon}{tag_str}")
        lines.append(fragment.content)
        lines.append("")

    lines.append("-" * 50)

    return "\n".join(lines)


def log_retrieval(
    session_id: str,
    prompt: str,
    fragments: List[Any],
    scores: List[float]
) -> None:
    """Log the retrieval for debugging and analytics."""
    try:
        log_dir = ensure_session_log_dir(session_id)
        log_file = log_dir / 'knowledge_retrieval.json'

        # Read existing log data
        if log_file.exists():
            try:
                with open(log_file, 'r') as f:
                    log_data = json.load(f)
            except (json.JSONDecodeError, ValueError):
                log_data = []
        else:
            log_data = []

        # Create log entry
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'prompt_preview': prompt[:200] + '...' if len(prompt) > 200 else prompt,
            'fragments_retrieved': len(fragments),
            'fragments': [
                {
                    'id': f.id,
                    'score': score,
                    'scope': f.scope,
                    'tags': f.tags
                }
                for f, score in zip(fragments, scores)
            ]
        }

        log_data.append(log_entry)

        # Keep only last 100 entries
        log_data = log_data[-100:]

        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)

    except Exception:
        pass  # Don't fail the hook if logging fails


def main():
    """Main entry point for the hook."""
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        session_id = input_data.get('session_id', 'unknown')
        prompt = input_data.get('prompt', '')

        # Check if we should retrieve
        if not should_retrieve(prompt):
            sys.exit(0)

        # Get the retriever
        retriever = get_retriever()

        # Retrieve relevant fragments
        results = retriever.retrieve(
            prompt=prompt,
            top_k=5,  # Limit to 5 to avoid context bloat
            min_score=0.15,  # Minimum relevance threshold
            include_personal=True
        )

        if not results:
            sys.exit(0)

        # Extract fragments and scores
        fragments = [f for f, _ in results]
        scores = [s for _, s in results]

        # Log retrieval
        log_retrieval(session_id, prompt, fragments, scores)

        # Format and output
        output = format_output(
            fragments,
            scores,
            prompt[:50] + '...' if len(prompt) > 50 else prompt
        )

        if output:
            print(output)

        # Mark fragments as accessed (async-safe: just update access tracking)
        try:
            retriever.mark_retrieved(fragments)
        except Exception:
            pass  # Don't fail if tracking update fails

        sys.exit(0)

    except json.JSONDecodeError:
        # No valid JSON input
        sys.exit(0)
    except ImportError as e:
        # Knowledge store not available - silently skip
        # This can happen if the store hasn't been initialized
        sys.exit(0)
    except Exception as e:
        # Log error but don't fail the hook
        print(f"Knowledge loader error: {e}", file=sys.stderr)
        sys.exit(0)


if __name__ == '__main__':
    main()
