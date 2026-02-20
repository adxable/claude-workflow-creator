#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# ///

"""
Cost Advisor Hook - UserPromptSubmit

Warns users about potential high-cost operations and suggests
cost-efficient alternatives. Designed for enterprise teams
where extended thinking can drive up API costs.

Configuration: .claude/hooks/cost_config.json
"""

import json
import sys
from pathlib import Path
from datetime import datetime, date

CONFIG_FILE = Path('.claude/hooks/cost_config.json')
SESSION_USAGE_DIR = Path('.claude/metrics/sessions')

# Default config if cost_config.json doesn't exist
DEFAULT_CONFIG = {
    'warn_thinking_enabled': True,
    'session_token_warn_threshold': 500_000,
    'session_token_hard_warn_threshold': 1_000_000,
    'session_prompt_warn_threshold': 30,
    'daily_session_warn_threshold': 20,
    'suggest_sonnet_for_simple': True,
    'vague_prompt_min_words': 5,
    'expensive_keywords': [
        'refactor everything',
        'rewrite all',
        'fix all',
        'update everything',
        'check all files',
        'review entire',
        'scan the whole',
        'go through all'
    ],
    'simple_task_keywords': [
        'typo',
        'rename',
        'change string',
        'update text',
        'fix import',
        'add comment',
        'remove console.log'
    ],
    # Slash commands that spawn multiple agents and use heavy token budgets
    'expensive_commands': [
        '/pipe:ship',
        '/pipe:ralph',
        '/flow:ship',
        '/pm:ship-feature'
    ],
    # Slash commands that use moderate resources (single agent + tools)
    'moderate_commands': [
        '/flow:plan',
        '/flow:implement',
        '/flow:review',
        '/flow:verify',
        '/fe:refactor',
        '/pm:gen-stories-from-url',
        '/pm:gen-stories-from-img',
        '/pm:gen-tasks-for-stories'
    ],
    # Slash commands that are cheap (git ops, simple queries)
    'cheap_commands': [
        '/flow:commit',
        '/flow:pr',
        '/jira:status',
        '/jira:pr-desc',
        '/jira:start',
        '/pm:push',
        '/pm:prepare',
        '/utils:costs'
    ]
}


def load_config() -> dict:
    """Load config from file or return defaults."""
    if CONFIG_FILE.exists():
        try:
            user_config = json.loads(CONFIG_FILE.read_text())
            merged = {**DEFAULT_CONFIG, **user_config}
            return merged
        except (json.JSONDecodeError, ValueError):
            pass
    return DEFAULT_CONFIG


def get_session_usage(session_id: str) -> dict:
    """Get accumulated usage for current session."""
    usage_file = SESSION_USAGE_DIR / f'{session_id}.json'
    if usage_file.exists():
        try:
            return json.loads(usage_file.read_text())
        except (json.JSONDecodeError, ValueError):
            pass
    return {'prompt_count': 0, 'total_tokens': 0, 'started': datetime.now().isoformat()}


def update_session_usage(session_id: str, usage: dict):
    """Update session usage tracking."""
    SESSION_USAGE_DIR.mkdir(parents=True, exist_ok=True)
    usage_file = SESSION_USAGE_DIR / f'{session_id}.json'
    usage['prompt_count'] = usage.get('prompt_count', 0) + 1
    usage['last_prompt'] = datetime.now().isoformat()
    usage_file.write_text(json.dumps(usage, indent=2))


def count_daily_sessions() -> int:
    """Count unique sessions today."""
    if not SESSION_USAGE_DIR.exists():
        return 0
    today = date.today().isoformat()
    count = 0
    for f in SESSION_USAGE_DIR.glob('*.json'):
        try:
            data = json.loads(f.read_text())
            if data.get('started', '').startswith(today):
                count += 1
        except (json.JSONDecodeError, ValueError):
            continue
    return count


def extract_command(prompt: str) -> tuple:
    """Extract slash command and its arguments from a prompt.

    Returns (command, args) where command is e.g. '/flow:verify'
    and args is the rest of the prompt. Returns (None, prompt) if
    no slash command found.
    """
    stripped = prompt.strip()
    if not stripped.startswith('/'):
        return None, stripped
    parts = stripped.split(None, 1)
    command = parts[0].lower()
    args = parts[1] if len(parts) > 1 else ''
    return command, args


def analyze_prompt(prompt: str, config: dict) -> list:
    """Analyze prompt for cost concerns. Returns list of warnings."""
    warnings = []
    prompt_lower = prompt.strip().lower()
    word_count = len(prompt.split())

    command, args = extract_command(prompt)

    # --- Slash command analysis ---
    if command is not None:
        # Check expensive pipeline commands
        for exp_cmd in config.get('expensive_commands', []):
            if command == exp_cmd.lower():
                warnings.append({
                    'level': 'cost',
                    'message': f'Expensive pipeline: {command}',
                    'suggestion': 'This runs multiple agents (plan+implement+verify+review+commit). '
                                  'Consider running individual steps (/flow:plan, /flow:implement) '
                                  'for more control over token usage.'
                })
                break

        # Check moderate commands
        for mod_cmd in config.get('moderate_commands', []):
            if command == mod_cmd.lower():
                warnings.append({
                    'level': 'info',
                    'message': f'Moderate cost command: {command}',
                    'suggestion': 'Uses agents and multiple tool calls. Ensure your description is specific.'
                })
                break

        # Analyze the arguments of slash commands for broad/vague patterns
        if args:
            args_lower = args.lower()
            for keyword in config['expensive_keywords']:
                if keyword in args_lower:
                    warnings.append({
                        'level': 'cost',
                        'message': f'Broad scope in arguments: "{keyword}"',
                        'suggestion': 'Narrow the scope to specific files or modules to reduce token usage.'
                    })
                    break
        elif command not in [c.lower() for c in config.get('cheap_commands', [])]:
            # Slash command with no arguments (and not a cheap command)
            # Some commands need args to be efficient
            needs_args = ['/flow:plan', '/flow:implement', '/pipe:ship', '/pipe:ralph',
                          '/pm:gen-stories-from-url', '/pm:gen-tasks-for-story']
            if command in [c.lower() for c in needs_args]:
                warnings.append({
                    'level': 'tip',
                    'message': f'{command} called without arguments.',
                    'suggestion': 'Add a specific description to avoid expensive exploration.'
                })

        return warnings

    # --- Free-text prompt analysis ---

    # Check for vague/short prompts
    if word_count < config['vague_prompt_min_words']:
        warnings.append({
            'level': 'tip',
            'message': 'Short prompt detected. More specific prompts reduce unnecessary exploration and save tokens.',
            'suggestion': 'Add details: what file, what behavior, what the expected result is.'
        })

    # Check for expensive broad operations
    for keyword in config['expensive_keywords']:
        if keyword in prompt_lower:
            warnings.append({
                'level': 'cost',
                'message': f'Broad operation detected: "{keyword}"',
                'suggestion': 'Consider narrowing scope to specific files or modules to reduce token usage.'
            })
            break

    # Suggest Sonnet for simple tasks
    if config['suggest_sonnet_for_simple']:
        for keyword in config['simple_task_keywords']:
            if keyword in prompt_lower:
                warnings.append({
                    'level': 'tip',
                    'message': f'Simple task detected ("{keyword}").',
                    'suggestion': 'Consider using /model sonnet or low effort level for simple changes.'
                })
                break

    return warnings


def check_session_budget(usage: dict, config: dict) -> list:
    """Check session-level budget thresholds."""
    warnings = []

    total_tokens = usage.get('total_tokens', 0)
    prompt_count = usage.get('prompt_count', 0)

    # Token thresholds
    if total_tokens >= config['session_token_hard_warn_threshold']:
        warnings.append({
            'level': 'budget',
            'message': f'High token usage: ~{total_tokens:,} tokens this session.',
            'suggestion': 'Consider starting a new session with /clear or narrowing your task scope.'
        })
    elif total_tokens >= config['session_token_warn_threshold']:
        warnings.append({
            'level': 'info',
            'message': f'Session token usage: ~{total_tokens:,} tokens.',
            'suggestion': 'Keep prompts focused to manage costs.'
        })

    # Prompt count threshold
    if prompt_count >= config['session_prompt_warn_threshold']:
        warnings.append({
            'level': 'info',
            'message': f'{prompt_count} prompts in this session.',
            'suggestion': 'Long sessions accumulate context. Consider /clear for unrelated tasks.'
        })

    return warnings


def format_warnings(warnings: list) -> str:
    """Format warnings for display."""
    if not warnings:
        return ''

    icons = {
        'cost': '!',
        'budget': '!',
        'tip': 'i',
        'info': 'o'
    }

    lines = ['--------------------------------------------------']
    lines.append('COST ADVISOR')
    lines.append('--------------------------------------------------')

    for w in warnings:
        icon = icons.get(w['level'], 'o')
        lines.append(f'   {icon} [{w["level"].upper()}] {w["message"]}')
        if w.get('suggestion'):
            lines.append(f'     -> {w["suggestion"]}')

    lines.append('--------------------------------------------------')
    return '\n'.join(lines)


def main():
    try:
        input_data = json.load(sys.stdin)

        session_id = input_data.get('session_id', 'unknown')
        prompt = input_data.get('prompt', '')

        config = load_config()
        all_warnings = []

        # 1. Analyze the prompt itself
        prompt_warnings = analyze_prompt(prompt, config)
        all_warnings.extend(prompt_warnings)

        # 2. Check session-level budget
        usage = get_session_usage(session_id)
        budget_warnings = check_session_budget(usage, config)
        all_warnings.extend(budget_warnings)

        # 3. Check daily session count
        daily_count = count_daily_sessions()
        if daily_count >= config['daily_session_warn_threshold']:
            all_warnings.append({
                'level': 'info',
                'message': f'{daily_count} sessions today.',
                'suggestion': 'Consider batching related tasks into fewer sessions.'
            })

        # 4. Update session tracking
        update_session_usage(session_id, usage)

        # 5. Output warnings (printed to stdout = injected as context)
        if all_warnings:
            output = format_warnings(all_warnings)
            print(output)

        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == '__main__':
    main()
