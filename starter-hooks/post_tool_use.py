#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

import json
import os
import sys
from pathlib import Path
from datetime import datetime

from utils.constants import ensure_session_log_dir

SESSION_USAGE_DIR = Path('.claude/metrics/sessions')


def update_token_tracking(session_id: str, input_data: dict):
    """Track token usage from tool responses for cost advisor."""
    tool_response = input_data.get('tool_response', {})
    if not isinstance(tool_response, dict):
        return

    total_tokens = tool_response.get('totalTokens', 0)
    if total_tokens == 0:
        return

    SESSION_USAGE_DIR.mkdir(parents=True, exist_ok=True)
    usage_file = SESSION_USAGE_DIR / f'{session_id}.json'

    if usage_file.exists():
        try:
            usage = json.loads(usage_file.read_text())
        except (json.JSONDecodeError, ValueError):
            usage = {}
    else:
        usage = {'started': datetime.now().isoformat(), 'prompt_count': 0}

    usage['total_tokens'] = usage.get('total_tokens', 0) + total_tokens
    usage['tool_call_count'] = usage.get('tool_call_count', 0) + 1
    usage['last_tool_use'] = datetime.now().isoformat()

    usage_file.write_text(json.dumps(usage, indent=2))


def main():
    try:
        # Read JSON input from stdin
        input_data = json.load(sys.stdin)

        # Extract session_id
        session_id = input_data.get('session_id', 'unknown')

        # Ensure session log directory exists
        log_dir = ensure_session_log_dir(session_id)
        log_path = log_dir / 'post_tool_use.json'

        # Read existing log data or initialize empty list
        if log_path.exists():
            with open(log_path, 'r') as f:
                try:
                    log_data = json.load(f)
                except (json.JSONDecodeError, ValueError):
                    log_data = []
        else:
            log_data = []

        # Append new data
        log_data.append(input_data)

        # Write back to file with formatting
        with open(log_path, 'w') as f:
            json.dump(log_data, f, indent=2)

        # Track token usage for cost advisor
        update_token_tracking(session_id, input_data)

        sys.exit(0)
        
    except json.JSONDecodeError:
        # Handle JSON decode errors gracefully
        sys.exit(0)
    except Exception:
        # Exit cleanly on any other error
        sys.exit(0)

if __name__ == '__main__':
    main()