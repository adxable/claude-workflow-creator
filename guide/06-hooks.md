# 06 — Hooks: Event-Driven Automation

Hooks are shell commands that run automatically at lifecycle events. They turn Claude Code from a reactive chat tool into a proactive workflow system.

## Hook Events

| Event | When It Fires | Common Use |
|-------|---------------|------------|
| `UserPromptSubmit` | Before Claude processes your prompt | Inject context, validate input |
| `PreToolUse` | Before Claude calls any tool | Security, validation |
| `Stop` | When Claude finishes responding | Logging, metrics |

---

## Hook File Format (settings.json)

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/context_loader.py || true"
          },
          {
            "type": "command",
            "command": "uv run .claude/hooks/context_detector.py || true"
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/pre_tool_use.py || true"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/stop.py || true"
          },
          {
            "type": "command",
            "command": "uv run .claude/hooks/cost_tracker.py || true"
          }
        ]
      }
    ]
  }
}
```

The `|| true` ensures hook failures never block Claude from working.

---

## Starter Hooks

**Ready-to-use hooks:** `starter-hooks/`
**Full config example:** see `templates/settings.json`

| Hook | Event | What It Does |
|------|-------|-------------|
| `context_loader.py` | UserPromptSubmit | Injects memory (decisions, lessons, conventions) into prompts |
| `context_detector.py` | UserPromptSubmit | Detects frontend/backend context, injects routing info |
| `pre_tool_use.py` | PreToolUse | Security — blocks `rm -rf` and `.env` access |
| `stop.py` | Stop | Session logging and optional transcript export |
| `cost_tracker.py` | Stop | Daily usage metrics (session counts, commands) |

---

## Setting Up Hooks

Copy the starter hooks and configure settings:

```bash
mkdir -p .claude/hooks/utils
cp starter-hooks/*.py .claude/hooks/
cp -r starter-hooks/utils/ .claude/hooks/utils/
cp templates/settings.json .claude/settings.json
```

The hooks use `uv run` for dependency management. Each hook file has its dependencies declared in a `# /// script` header block.

---

## Writing Your Own Hook

A hook is a Python script that:
1. Reads JSON input from stdin
2. Optionally prints context to inject into the prompt (stdout)
3. Exits with code 0 (OK), 1 (warn), or 2 (block)

**Minimal hook template:**

```python
#!/usr/bin/env -S uv run --script
# /// script
# requires-python = ">=3.11"
# dependencies = []
# ///

import json
import sys

def main():
    try:
        input_data = json.load(sys.stdin)
        prompt = input_data.get('prompt', '')

        # Your logic here
        # Print context to inject (optional):
        # print("Context to inject into the prompt")

        sys.exit(0)
    except Exception:
        sys.exit(0)  # Never fail loudly

if __name__ == '__main__':
    main()
```

**To block a prompt (exit code 2):**
```python
print("Reason for blocking", file=sys.stderr)
sys.exit(2)
```

---

**Next Step ->** `guide/07-jira-integration.md` (if you use Jira) or `guide/08-chrome-extension.md` (if you want browser automation)
