# Starter Hooks

Ready-to-use hook implementations for your Claude Code workflow. The setup wizard copies these to `.claude/hooks/` in your project.

## Prerequisites

```bash
# uv (hook runner)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Python 3.11+
python3 --version
```

---

## Included Hooks

| Hook | Event | Purpose |
|------|-------|---------|
| `context_loader.py` | UserPromptSubmit | Injects L1 memory (decisions, lessons, conventions) into prompts |
| `pre_tool_use.py` | PreToolUse | Security — blocks `rm -rf` and `.env` file access |
| `stop.py` | Stop | Session logging and optional transcript export |
| `cost_tracker.py` | Stop | Daily usage metrics (session counts, command breakdown) |

---

## Hook Reference

### `context_loader.py`

**Event:** UserPromptSubmit
**Purpose:** Injects your memory files into every significant prompt.

What it does:
1. Reads `.claude/memory/decisions.md`, `lessons.md`, and `conventions.md`
2. Reads `.claude/context/session_context.json` for previous plans and decisions
3. Outputs formatted context blocks before Claude's response

Triggers only on action-oriented prompts (keywords like `plan`, `implement`, `create`, `fix`, etc.) — skips short conversational messages.

**This is the foundation of the memory system.** Without it, Claude won't "remember" anything across sessions.

---

### `pre_tool_use.py`

**Event:** PreToolUse
**Purpose:** Security guard — blocks dangerous commands before they execute.

What it does:
1. **Blocks dangerous `rm -rf` commands** — comprehensive pattern matching covers `rm -rf`, `rm -fr`, `rm --recursive --force`, and variants targeting `/`, `~`, `$HOME`, `..`, wildcards
2. **Blocks `.env` file access** — prevents reading/writing `.env` files (allows `.env.sample`)
3. **Logs skill activations** — when Claude calls the `Skill` tool, prints a notification to stderr
4. Logs all tool calls to session log directory

**Strongly recommended.** The security rules are lightweight and prevent accidental data loss.

---

### `stop.py`

**Event:** Stop
**Purpose:** Session logging and optional transcript export.

What it does:
1. Logs the stop event payload to session log directory
2. With `--chat` flag: converts the `.jsonl` transcript to a clean `chat.json` array

---

### `cost_tracker.py`

**Event:** Stop
**Purpose:** Logs session usage metrics and prints a daily summary.

What it does:
1. Records the session to `.claude/metrics/daily/{YYYY-MM-DD}.json`
2. Tracks session count and command usage per day
3. Prints a "TODAY'S USAGE" summary at session end

---

## Utilities (`utils/`)

### `constants.py`

Provides `ensure_session_log_dir(session_id)` — creates and returns the session log directory. Used by hooks for consistent log paths.

---

## settings.json Configuration

```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [{ "type": "command", "command": "uv run .claude/hooks/context_loader.py || true" }] }
    ],
    "PreToolUse": [
      { "hooks": [{ "type": "command", "command": "uv run .claude/hooks/pre_tool_use.py || true" }] }
    ],
    "Stop": [
      { "matcher": "", "hooks": [
        { "type": "command", "command": "uv run .claude/hooks/stop.py || true" },
        { "type": "command", "command": "uv run .claude/hooks/cost_tracker.py || true" }
      ]}
    ]
  }
}
```

All hooks use `|| true` to never block Claude from working.
