#!/usr/bin/env python3
"""
Context Detector for Claude Workflow

Detects whether the current work is frontend, backend, or another context based on:
1. File paths mentioned in the prompt
2. File extensions
3. Keywords in the prompt

Reads configuration from YAML files in the same directory.
"""

import os
import re
import sys
from pathlib import Path
from typing import Optional

# Try to import yaml, fall back to basic parsing
try:
    import yaml
    HAS_YAML = True
except ImportError:
    HAS_YAML = False


def load_context_config(context_name: str) -> dict:
    """Load a context configuration file."""
    config_path = Path(__file__).parent / f"{context_name}.yaml"
    if not config_path.exists():
        return {}

    if HAS_YAML:
        with open(config_path, 'r') as f:
            return yaml.safe_load(f)

    # Basic fallback: parse simple key: value lines
    # Not recommended for production — install pyyaml
    return {}


def score_context(text: str, config: dict) -> int:
    """Score a context based on how well the text matches its indicators."""
    indicators = config.get('indicators', {})
    score = 0
    text_lower = text.lower()

    # Path indicators (strong signal: +10 each)
    for path in indicators.get('paths', []):
        if path.lower() in text_lower:
            score += 10

    # Extension indicators (medium signal: +5 each)
    for ext in indicators.get('extensions', []):
        if re.search(rf'\w+{re.escape(ext)}|{re.escape(ext)}\s+file', text, re.IGNORECASE):
            score += 5

    # Keyword indicators (weak signal: +3 each)
    for keyword in indicators.get('keywords', []):
        if keyword.lower() in text_lower:
            score += 3

    return score


def detect_context(prompt: str, changed_files: Optional[list] = None) -> dict:
    """
    Detect the context based on prompt and optionally changed files.

    Returns:
        dict with:
        - context: 'frontend' | 'backend' | 'unknown'
        - confidence: 0-100
        - scores: {context: score}
    """
    # Find all available context configs
    config_dir = Path(__file__).parent
    context_names = [
        f.stem for f in config_dir.glob('*.yaml')
        if f.stem not in ('base',)
    ]

    if not context_names:
        return {
            'context': 'unknown',
            'confidence': 0,
            'details': 'No context configurations found',
            'scores': {}
        }

    # Combine prompt with changed files
    text = prompt
    if changed_files:
        text += " " + " ".join(changed_files)

    # Score each context
    scores = {}
    for ctx_name in context_names:
        config = load_context_config(ctx_name)
        scores[ctx_name] = score_context(text, config)

    max_score = max(scores.values()) if scores else 0

    if max_score == 0:
        return {
            'context': 'unknown',
            'confidence': 0,
            'details': 'No context indicators found',
            'scores': scores
        }

    detected = max(scores, key=scores.get)
    confidence = min(100, max_score * 5)  # Scale to 0-100

    return {
        'context': detected,
        'confidence': confidence,
        'details': f"Detected {detected} context",
        'scores': scores
    }


if __name__ == '__main__':
    test_prompt = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "Create a new component"
    result = detect_context(test_prompt)
    print(f"Prompt: {test_prompt}")
    print(f"Detected: {result['context']} (confidence: {result['confidence']}%)")
    print(f"Scores: {result['scores']}")
