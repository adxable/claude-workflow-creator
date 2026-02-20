# 06 — Hooks: Event-Driven Automation

Hooks are shell commands that run automatically at lifecycle events. They turn Claude Code from a reactive chat tool into a proactive workflow system.

## Hook Events

| Event | When It Fires | Common Use |
|-------|---------------|------------|
| `UserPromptSubmit` | Before Claude processes your prompt | Inject context, validate input |
| `PreToolUse` | Before Claude calls any tool | Logging, validation |
| `PostToolUse` | After a tool call completes | Track changes |
| `Stop` | When Claude finishes responding | Save learnings, summarize |
| `SubagentStop` | When a subagent completes | Track agent results |
| `PreCompact` | Before context compression | Save important context |
| `Notification` | Desktop notification events | macOS/Linux notifications |

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

## Starter Hook Stack

**Ready-to-use hooks:** `starter-hooks/`
**Full config example:** see `templates/settings.json`

### UserPromptSubmit Hooks (run before every prompt)

| Hook | What It Does |
|------|-------------|
| `clear_detector.py` | Clear context detection cache |
| `dev_standards_loader.py` | Inject dev standards based on context |
| `context_loader.py` | Load L1 memory + session context |
| `smart_context_loader.py` | Smart context injection based on file activity |
| `knowledge_loader.py` | Semantic search + inject relevant L2 fragments |
| `skill-activation-prompt.py` | Suggest relevant skills based on prompt |
| `circuit_breaker.py` | Stop runaway loops (cost protection) |
| `cost_advisor.py` | Show estimated cost before heavy operations |
| `user_prompt_submit.py` | Log prompt for session analysis |

### Stop Hooks (run when Claude finishes)

| Hook | What It Does |
|------|-------------|
| `context_updater.py` | Update session context with new decisions/patterns |
| `cost_tracker.py` | Track token usage and costs |
| `memory_updater.py` | Update L1 memory files |
| `memory_extractor.py` | Extract learnings into L2 fragments |
| `stop.py` | Chat summary + session logging |

### Other Hooks

| Hook | Event | What It Does |
|------|-------|-------------|
| `pre_tool_use.py` | PreToolUse | Log tool calls |
| `post_tool_use.py` | PostToolUse | Track file changes |
| `notification.py` | Notification | macOS desktop notifications |
| `pre_compact.py` | PreCompact | Save context before compression |
| `subagent_stop.py` | SubagentStop | Log subagent completions |

---

## Setting Up Hooks

### Minimal Setup (3 hooks)

If you want the most value with least complexity, start with these three:

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
            "command": "uv run .claude/hooks/knowledge_loader.py || true"
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
            "command": "uv run .claude/hooks/cost_tracker.py || true"
          }
        ]
      }
    ]
  }
}
```

This gives you: memory injection + cost tracking.

### Full Setup

Copy the starter hooks and configure settings:

```bash
cp .claude/claude-init/templates/settings.json .claude/settings.json
mkdir -p .claude/hooks/utils/llm
cp .claude/claude-init/starter-hooks/*.py .claude/hooks/
cp -r .claude/claude-init/starter-hooks/utils/ .claude/hooks/utils/
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

## Important Hook: circuit_breaker.py

The circuit breaker prevents runaway loops where Claude keeps calling tools repeatedly. It tracks tool call counts per session and can block the prompt if thresholds are exceeded.

**See implementation:** `starter-hooks/circuit_breaker.py`

This is particularly important for autonomous pipelines like `/pipe:ship`.

---

## Cost Tracking

The `cost_tracker.py` hook tracks token usage per session and writes to `.claude/context/costs.json`. This lets you see how much each session costs.

**See implementation:** `starter-hooks/cost_tracker.py`

---

**Next Step →** `guide/07-jira-integration.md` (if you use Jira) or `guide/08-chrome-extension.md` (if you want browser automation)
