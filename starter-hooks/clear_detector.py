#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = ["anthropic"]
# ///

"""
Clear Command Detector - Extract memory before /clear wipes context.

Runs on UserPromptSubmit and checks if user typed /clear.
If so, triggers memory extraction before the clear happens.
"""

import json
import subprocess
import sys
from pathlib import Path


def find_transcript(session_id: str, cwd: str) -> Path | None:
    """Find the session transcript file."""
    if not session_id:
        return None

    # Claude stores transcripts in ~/.claude/projects/{encoded-path}/
    # Try to find the transcript by searching common locations
    home = Path.home()
    claude_projects = home / ".claude" / "projects"

    if not claude_projects.exists():
        return None

    # Search for the session transcript across all project dirs
    for project_dir in claude_projects.iterdir():
        if project_dir.is_dir():
            transcript = project_dir / f"{session_id}.jsonl"
            if transcript.exists():
                return transcript

    return None


def main():
    try:
        input_data = json.load(sys.stdin)
        prompt = input_data.get('prompt', '').strip().lower()

        # Check if user is clearing
        if prompt == '/clear' or prompt.startswith('/clear '):
            session_id = input_data.get('session_id', '')
            cwd = input_data.get('cwd', '')

            if not session_id:
                sys.exit(0)

            # Find transcript
            transcript_path = find_transcript(session_id, cwd)

            if transcript_path and transcript_path.exists():
                # Prepare input for memory_extractor
                extractor_input = {
                    'session_id': session_id,
                    'transcript_path': str(transcript_path),
                    'hook_event_name': 'Clear',
                    'cwd': cwd
                }

                # Call memory_extractor
                hooks_dir = Path(__file__).parent
                extractor_path = hooks_dir / 'memory_extractor.py'

                if extractor_path.exists():
                    result = subprocess.run(
                        ['uv', 'run', str(extractor_path)],
                        input=json.dumps(extractor_input),
                        capture_output=True,
                        text=True,
                        cwd=str(hooks_dir.parent.parent)  # Project root
                    )
                    if result.stdout:
                        print(result.stdout)

        sys.exit(0)

    except json.JSONDecodeError:
        sys.exit(0)
    except Exception:
        sys.exit(0)


if __name__ == '__main__':
    main()
