#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.8"
# dependencies = [
#     "pyyaml",
# ]
# ///

"""
Detect frontend/backend context from the user's prompt and inject
routing info (tools, agents, project root) so flow commands know
which stack to target.

Reads YAML context configs from .claude/contexts/*.yaml.
Skips silently when no configs exist (e.g. frontend-only projects).
"""

import json
import sys
import re
from pathlib import Path

try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False

CONTEXTS_DIR = Path('.claude/contexts')
MIN_CONFIDENCE = 15  # minimum score to inject context


def load_configs() -> dict[str, dict]:
    """Load all YAML context configs."""
    if not HAS_YAML or not CONTEXTS_DIR.exists():
        return {}

    configs = {}
    for f in CONTEXTS_DIR.glob('*.yaml'):
        try:
            configs[f.stem] = yaml.safe_load(f.read_text()) or {}
        except Exception:
            continue
    return configs


def score_context(text: str, config: dict) -> int:
    """Score how well the prompt matches a context's indicators."""
    indicators = config.get('indicators', {})
    score = 0
    text_lower = text.lower()

    for path in indicators.get('paths', []):
        if path.lower() in text_lower:
            score += 10

    for ext in indicators.get('extensions', []):
        if re.search(rf'\w+{re.escape(ext)}|{re.escape(ext)}\b', text, re.IGNORECASE):
            score += 5

    for keyword in indicators.get('keywords', []):
        if keyword.lower() in text_lower:
            score += 3

    return score


def check_manual_override(prompt: str, config_names: list[str]) -> str | None:
    """Check for [frontend] or [backend] manual override in prompt."""
    for name in config_names:
        if f'[{name}]' in prompt.lower():
            return name
    return None


def format_context_output(name: str, config: dict, confidence: int) -> str:
    """Format detected context for injection into the prompt."""
    parts = []
    parts.append("")
    parts.append("-" * 50)
    parts.append(f"DETECTED CONTEXT: {name} (confidence: {confidence}%)")
    parts.append("-" * 50)

    project_root = config.get('project_root', '')
    if project_root:
        parts.append(f"Project root: {project_root}")

    tools = config.get('tools', {})
    verify_cmds = tools.get('verify', [])
    if verify_cmds:
        parts.append("Verify commands:")
        if isinstance(verify_cmds, list):
            for cmd in verify_cmds:
                parts.append(f"  - {cmd}")
        else:
            parts.append(f"  - {verify_cmds}")

    test_cmd = tools.get('test', '')
    if test_cmd:
        parts.append(f"Test: {test_cmd}")

    agents = config.get('agents', {})
    if agents:
        parts.append("Preferred agents:")
        for role, agent in agents.items():
            parts.append(f"  - {role}: {agent}")

    parts.append("-" * 50)
    parts.append("")
    return "\n".join(parts)


def main():
    try:
        input_data = json.load(sys.stdin)
        prompt = input_data.get('prompt', '')

        if not prompt or len(prompt.strip()) < 3:
            sys.exit(0)

        configs = load_configs()
        if not configs:
            sys.exit(0)

        config_names = list(configs.keys())

        # Check manual override first
        override = check_manual_override(prompt, config_names)
        if override and override in configs:
            output = format_context_output(override, configs[override], 100)
            print(output)
            sys.exit(0)

        # Score each context
        scores = {}
        for name, config in configs.items():
            scores[name] = score_context(prompt, config)

        max_score = max(scores.values()) if scores else 0
        if max_score < MIN_CONFIDENCE:
            sys.exit(0)

        detected = max(scores, key=scores.get)
        confidence = min(100, max_score * 5)

        output = format_context_output(detected, configs[detected], confidence)
        print(output)

        sys.exit(0)

    except Exception:
        sys.exit(0)


if __name__ == '__main__':
    main()
