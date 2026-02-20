# Starter Hooks

Ready-to-use hook implementations for your Claude Code workflow. Copy these to `.claude/hooks/` in your project.

## Prerequisites

```bash
# uv (hook runner)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Python 3.11+
python3 --version
```

---

## Which Hooks to Install

The setup wizard installs a **recommended default set**. Some hooks are **optional** and only useful in specific scenarios.

| Hook | Event | Default | Notes |
|------|-------|---------|-------|
| `context_loader.py` | UserPromptSubmit | ✅ | Core — L1 memory injection |
| `knowledge_loader.py` | UserPromptSubmit | ✅ | Core — L2 semantic search |
| `smart_context_loader.py` | UserPromptSubmit | ✅ | Skill suggestions from prompt |
| `cost_advisor.py` | UserPromptSubmit | ✅ | Token cost warnings |
| `clear_detector.py` | UserPromptSubmit | ✅ | Memory extraction before /clear |
| `user_prompt_submit.py` | UserPromptSubmit | ✅ | Prompt logging scaffold |
| `pre_tool_use.py` | PreToolUse | ✅ | Security — blocks rm -rf + .env |
| `post_tool_use.py` | PostToolUse | ✅ | Token tracking for cost_advisor |
| `stop.py` | Stop | ✅ | Session logging |
| `context_updater.py` | Stop | ✅ | Updates session context |
| `cost_tracker.py` | Stop | ✅ | Daily usage metrics |
| `memory_updater.py` | Stop | ✅ | Prompts memory updates |
| `knowledge_ingestor.py` | Stop | ✅ | LLM learning extraction (needs API key) |
| `subagent_stop.py` | SubagentStop | ✅ | Subagent session logging |
| `pre_compact.py` | PreCompact | ✅ | Logging before context compaction |
| `memory_extractor.py` | PreCompact | ✅ | LLM extraction before compaction (needs API key) |
| `circuit_breaker.py` | UserPromptSubmit | ⚙️ Optional | Only for autonomous `/ralph` loops |
| `checkpoint.py` | UserPromptSubmit | ⚙️ Optional | Only for `/ship` with rollback |
| `skill-activation-prompt.py` | UserPromptSubmit | ⚙️ Optional | Only after `skill-rules.json` configured |
| `dev_standards_loader.py` | UserPromptSubmit | ⚙️ Optional | Claude reads CLAUDE.md already |
| `notification.py` | Notification | ⚙️ Optional | Empty — must customize for your OS |

**API key hooks** (`knowledge_ingestor.py`, `memory_extractor.py`, `clear_detector.py`) require `ANTHROPIC_API_KEY` in your environment. They silently skip if not set.

---

## Hook Reference

### UserPromptSubmit Hooks

These run before Claude sees your message and can inject extra context into the prompt.

---

#### `context_loader.py`

**Event:** UserPromptSubmit
**Purpose:** Injects your L1 memory (decisions, lessons, conventions) and session history into every significant prompt.

What it does:
1. Reads `.claude/memory/decisions.md`, `lessons.md`, and `conventions.md`
2. Reads `.claude/context/session_context.json` for previous plans, decisions, blocked patterns, and recent lessons
3. Outputs both as formatted context blocks injected before Claude's response

Triggers only on action-oriented prompts (keywords like `plan`, `implement`, `create`, `fix`, etc.) — skips short conversational messages.

Files read:
- `.claude/memory/decisions.md`
- `.claude/memory/lessons.md`
- `.claude/memory/conventions.md`
- `.claude/context/session_context.json`

When to enable: **Always** — this is the foundation of the memory system. Without it, Claude won't "remember" anything across sessions.

---

#### `knowledge_loader.py`

**Event:** UserPromptSubmit
**Purpose:** Semantic search — retrieves relevant knowledge fragments from L2 (the TF-IDF knowledge store) and injects them as context.

What it does:
1. Takes your prompt and runs TF-IDF semantic matching against stored knowledge fragments
2. Returns the top 5 most relevant fragments (min relevance score: 0.15)
3. Formats and injects them as a "RELEVANT KNOWLEDGE (L2)" block

Skips very short prompts, single-word answers, and slash commands.

Files read:
- `.claude/memory/knowledge/` (TF-IDF index built by `knowledge_store.py`)

Logs retrieval to `.claude/logs/{session_id}/knowledge_retrieval.json`

When to enable: Enable if you use the knowledge store. Disable if you haven't populated L2 yet (it will just silently skip).

---

#### `smart_context_loader.py`

**Event:** UserPromptSubmit
**Purpose:** Detects what type of work the prompt is about and suggests relevant skills.

What it does:
1. Matches the prompt against `CONTEXT_RULES` defined at the top of the file
2. Each rule has keywords + regex patterns → maps to skill names + a context note
3. Outputs a "SMART CONTEXT DETECTED" block showing suggested skills and notes

Built-in rules cover: forms, tables/grids, API/data fetching, styling, components, performance, TypeScript, testing, browser verification, refactoring, state management, routing, documentation, project structure.

**To customize:** Edit the `CONTEXT_RULES` list at the top of the file — replace skill names with your own skill file names.

```python
CONTEXT_RULES = [
    {
        "name": "forms",
        "keywords": ["form", "validation"],
        "skills": ["your-forms-skill"],     # ← Replace with your skill name
        "context": "Use YourFormLibrary",   # ← Replace with your note
        "priority": "high"
    }
]
```

Logs detections to `.claude/logs/{session_id}/smart_context.json`

When to enable: Enable once you have skills set up. Before that, it still works but suggestions won't match your files.

---

#### `skill-activation-prompt.py`

**Event:** UserPromptSubmit
**Purpose:** Reads your `skill-rules.json` file and tells Claude which skills to load before responding.

What it does:
1. Reads `.claude/skills/skill-rules.json`
2. Matches your prompt against each skill's `keywords` and `intentPatterns`
3. Groups matches by priority (critical → high → medium → low)
4. Outputs a "SKILL ACTIVATION CHECK" block with a direct instruction: "Use Skill tool BEFORE responding"

**Difference from `smart_context_loader.py`:** This hook reads from an external JSON config file, making it easier to add skills without editing Python. The other hook has rules hardcoded in Python.

Config file format (`.claude/skills/skill-rules.json`):
```json
{
  "skills": {
    "react-forms": {
      "promptTriggers": {
        "keywords": ["form", "validation", "submit"],
        "intentPatterns": ["create.*form", "add.*input"]
      },
      "priority": "high",
      "enforcement": "suggest"
    }
  }
}
```

Logs activations to `.claude/logs/{session_id}/skill_activation.json`

When to enable: Use this if you want to manage skill rules in a config file rather than Python code.

---

#### `dev_standards_loader.py`

**Event:** UserPromptSubmit
**Purpose:** Reminds Claude that your CLAUDE.md exists and what sections it contains.

What it does:
1. Reads `CLAUDE.md` (or `.claude/memory/CLAUDE.md` as fallback)
2. Extracts the first 10 section headers
3. Outputs a "DEV STANDARDS LOADED" banner listing them

Only triggers on action-oriented prompts. Note: Claude Code already reads CLAUDE.md automatically — this hook adds a visible reminder in the context, useful if Claude tends to forget conventions mid-session.

When to enable: Optional. Most useful if you have a long CLAUDE.md and Claude sometimes ignores sections.

---

#### `cost_advisor.py`

**Event:** UserPromptSubmit
**Purpose:** Warns about potentially expensive operations before Claude starts running them.

What it does:
1. Analyzes your prompt for expensive patterns (e.g., "refactor everything", "fix all")
2. Categorizes slash commands as expensive/moderate/cheap
3. Checks session token usage against configurable thresholds
4. Counts daily sessions and warns if high
5. Outputs a "COST ADVISOR" block with warnings and suggestions

Configuration via `.claude/hooks/cost_config.json` (created on first use with defaults):
```json
{
  "session_token_warn_threshold": 500000,
  "session_token_hard_warn_threshold": 1000000,
  "expensive_commands": ["/pipe:ship", "/pipe:ralph"],
  "suggest_sonnet_for_simple": true
}
```

Warning levels:
- `! [COST]` — expensive operation, consider narrowing scope
- `! [BUDGET]` — session token usage is high
- `o [INFO]` — informational, no action needed
- `i [TIP]` — suggested improvement

Tracks session usage in `.claude/metrics/sessions/{session_id}.json`

When to enable: Enable for teams where API cost is a concern. Individual developers may find it noisy.

---

#### `circuit_breaker.py`

**Event:** UserPromptSubmit
**Purpose:** Prevents autonomous loops (like `/ralph` or `/pipe:ship`) from running indefinitely.

What it does:
1. Only activates when the prompt contains `/ralph`
2. Tracks iterations, API calls per hour, consecutive loops with no file changes, and repeated errors
3. Trips the circuit (blocks execution) when any threshold is exceeded:
   - 50 iterations (default)
   - 100 API calls/hour (default)
   - 3 loops with no file changes (stagnation)
   - Same error repeated 5 times

Three states:
- `CLOSED` — normal operation
- `HALF_OPEN` — testing after recovery attempt
- `OPEN` — stopped, requires manual reset

Flags supported in the prompt:
- `/ralph --status` — shows current state
- `/ralph --reset` — resets the breaker to allow continuation

State persists in `.claude/circuit_breaker_state.json`

When to enable: Only needed if you use autonomous pipeline commands (`/ralph`, `/pipe:ship`). Irrelevant for normal interactive use.

---

#### `user_prompt_submit.py`

**Event:** UserPromptSubmit
**Purpose:** Logging scaffold — records every prompt to a session log file.

What it does:
1. Logs the full input payload to `.claude/logs/{session_id}/user_prompt_submit.json`
2. Optionally validates prompts against blocked patterns (via `--validate` flag)
3. Optionally blocks prompts that match patterns (exit code 2 blocks the prompt)

Flags:
- `--validate` — enable validation against `blocked_patterns` list
- `--log-only` — log but never block, even if validation is enabled

The `blocked_patterns` list is empty by default — add patterns to block specific inputs:
```python
blocked_patterns = [
    ('rm -rf /', 'Dangerous command detected'),
    # Add your own
]
```

When to enable: Useful as a foundation for adding custom validation logic. The logging itself is lightweight and safe to always enable.

---

#### `clear_detector.py`

**Event:** UserPromptSubmit
**Purpose:** Extracts memory from the session transcript before `/clear` deletes the context.

What it does:
1. Detects if the user typed `/clear`
2. Finds the session transcript file (`.jsonl` in `~/.claude/projects/`)
3. Calls `memory_extractor.py` as a subprocess, passing the transcript
4. The extractor uses LLM to pull out learnings, saves them to `.claude/memory/pending/`

This is a "save before wipe" mechanism — when you clear context, valuable learnings from the session are preserved for review.

**Requires:** `anthropic` package (installed automatically by `uv` via the script header).

When to enable: Enable if you use `/clear` regularly and want to preserve session learnings. Pairs with `memory_extractor.py`.

---

### Stop Hooks

These run after Claude finishes a response.

---

#### `stop.py`

**Event:** Stop
**Purpose:** Session logging and optional transcript export.

What it does:
1. Logs the stop event payload to `.claude/logs/{session_id}/stop.json`
2. With `--chat` flag: converts the `.jsonl` transcript to a clean `chat.json` array for easier reading

The `--chat` flag creates `.claude/logs/{session_id}/chat.json` — a formatted JSON array of all messages, easier to read than raw `.jsonl`.

When to enable: Always safe to enable. The `--chat` flag is optional but useful for debugging long sessions.

---

#### `context_updater.py`

**Event:** Stop
**Purpose:** Scans the `.claude/plans/` directory and updates session context with any new plan files found.

What it does:
1. Reads `.claude/context/session_context.json`
2. Scans `.claude/plans/*.md` for new plan files not yet tracked
3. Adds new plans to the `previousPlans` list (keeps last 10)
4. Saves the updated context

Also exposes utility functions (`add_decision`, `add_pattern`, `add_lesson`) that can be called programmatically by other scripts to record session learnings.

When to enable: Enable if you use the planning pipeline (`/flow:plan`). The context it maintains feeds into `context_loader.py`.

---

#### `cost_tracker.py`

**Event:** Stop
**Purpose:** Logs session usage metrics and prints a daily summary.

What it does:
1. Records the session to `.claude/metrics/daily/{YYYY-MM-DD}.json`
2. Tracks session count and command usage per day
3. Prints a "TODAY'S USAGE" summary at session end: session count and command breakdown

Also provides weekly and monthly reports (accessible via the `CostTracker` class directly).

Output example:
```
--------------------------------------------------
TODAY'S USAGE
--------------------------------------------------
Sessions: 3
Commands:
  - /flow:plan: 2
  - /flow:implement: 1
--------------------------------------------------
```

Note: This tracks session/command counts, not actual API token costs. For token-level tracking, see `cost_advisor.py`.

When to enable: Enable if you want a lightweight session counter. Disable if the end-of-session output is noisy.

---

#### `memory_updater.py`

**Event:** Stop
**Purpose:** Reminds you to update your memory files after significant sessions.

What it does:
1. Checks the transcript size — skips trivial sessions (< 2KB)
2. Scans recent review files for "Critical" findings or pattern inconsistencies
3. Prints a "MEMORY UPDATE PROMPT" with suggestions to run `/memory decision` or `/memory lesson`

This hook doesn't update memory itself — it prompts you to do it manually.

When to enable: Enable if you want a nudge to capture learnings. Disable if the reminders become repetitive.

---

#### `memory_extractor.py`

**Event:** Stop / PreCompact / Clear (via `clear_detector.py`)
**Purpose:** Uses an LLM to automatically extract learnings from the conversation and save them for review.

What it does:
1. Parses the session transcript (`.jsonl` format)
2. Sends the transcript to Claude (sonnet model) with a selective extraction prompt
3. LLM identifies: mistakes corrected, codebase-specific patterns, user preferences, decisions, bugs
4. Saves results to `.claude/memory/pending/{timestamp}-{trigger}-{session_id}.md`
5. Auto-stores high-confidence items directly to L2 knowledge store
6. Prints: "Extracted N learnings → Review with '/memory review'"

Extraction rules are configurable via `.claude/memory/rules.json`:
```json
{
  "extract": {
    "categories": {
      "lesson": "Mistakes made and corrected",
      "convention": "Codebase-specific coding standards",
      "decision": "Architectural decisions with rationale",
      "pattern": "Recurring code patterns",
      "bug": "Bugs and their root causes"
    }
  }
}
```

**Requires:** `anthropic` package. Each extraction makes one API call (claude-sonnet).

When to enable: Enable if you want automated memory extraction. Disable if you prefer to maintain memory manually or want to save on API calls.

---

#### `knowledge_ingestor.py`

**Event:** Stop
**Purpose:** Extracts and stores session learnings to the L2 knowledge store. Companion to `memory_extractor.py` with more detail.

What it does:
1. Parses the session transcript
2. Extracts file paths mentioned in the session (`.ts`, `.tsx`, `.cs` patterns)
3. Calls LLM to extract learnings (same extraction logic as `memory_extractor.py`)
4. Saves all learnings to `.claude/memory/pending/` for review
5. Auto-stores high-confidence items to `.claude/memory/knowledge/` (TF-IDF store)
6. Tags fragments with `frontend`/`backend` based on file extensions in the session

Key difference from `memory_extractor.py`: This is more focused on populating L2 (searchable knowledge store) and includes file path context. `memory_extractor.py` is more focused on the L1/prompt injection use case.

**Requires:** `anthropic` package.

When to enable: Enable one of `knowledge_ingestor.py` or `memory_extractor.py` — they overlap significantly. `knowledge_ingestor.py` is better if your primary goal is building L2 search, `memory_extractor.py` if you want richer control via `rules.json`.

---

### Other Hooks

---

#### `pre_tool_use.py`

**Event:** PreToolUse
**Purpose:** Security guard — blocks dangerous commands before they execute.

What it does:
1. **Blocks dangerous `rm -rf` commands** — comprehensive pattern matching covers `rm -rf`, `rm -fr`, `rm --recursive --force`, and variants targeting `/`, `~`, `$HOME`, `..`, wildcards
2. **Blocks `.env` file access** — prevents reading/writing `.env` files (allows `.env.sample`)
3. **Logs skill activations** — when Claude calls the `Skill` tool, prints a cyan notification to stderr
4. Logs all tool calls to `.claude/logs/{session_id}/pre_tool_use.json`

Exit code 2 blocks the tool call and shows the error message to Claude.

When to enable: **Strongly recommended.** The security rules are lightweight and prevent accidental data loss.

---

#### `post_tool_use.py`

**Event:** PostToolUse
**Purpose:** Tracks token usage from tool responses.

What it does:
1. Reads `totalTokens` from the tool response payload
2. Accumulates token counts per session in `.claude/metrics/sessions/{session_id}.json`
3. Logs all tool responses to `.claude/logs/{session_id}/post_tool_use.json`

The token data is consumed by `cost_advisor.py` for session-level budget warnings.

When to enable: Enable alongside `cost_advisor.py`. Standalone it just provides logging.

---

#### `pre_compact.py`

**Event:** PreCompact
**Purpose:** Logs context compaction events.

What it does: Logs the pre-compact payload to `.claude/logs/{session_id}/pre_compact.json`. This is a minimal logging hook — a scaffold for adding behavior before compaction (e.g., triggering memory extraction).

To trigger memory extraction on compaction: add a call to `memory_extractor.py` here, similar to how `clear_detector.py` calls it.

When to enable: Enable if you want to log compaction events or use it as a base for adding pre-compaction logic.

---

#### `subagent_stop.py`

**Event:** SubagentStop
**Purpose:** Logs when subagents (spawned via the Task tool) complete.

What it does:
1. Logs the stop event for each subagent to `.claude/logs/{session_id}/subagent_stop.json`
2. With `--chat` flag: converts the subagent transcript to a clean `chat.json` for inspection

Mirrors `stop.py` but for subagents. Useful for debugging multi-agent pipelines (e.g., why did the planner agent stop early?).

When to enable: Enable if you use agents (`/flow:plan`, `/flow:implement`) and want visibility into subagent behavior.

---

#### `notification.py`

**Event:** Notification
**Purpose:** Notification scaffold — logs notification events.

What it does: Logs notification payloads to `.claude/logs/{session_id}/notification.json`. The `--notify` flag exists but the TTS/desktop notification implementation is left intentionally blank for you to fill in.

To add desktop notifications on macOS:
```python
if args.notify:
    subprocess.run(['osascript', '-e', f'say "Claude finished"'])
    # or: subprocess.run(['terminal-notifier', '-message', 'Claude finished'])
```

When to enable: Enable as a base if you want to add system notifications when Claude finishes a task.

---

#### `checkpoint.py`

**Event:** UserPromptSubmit (for `/ship` commands)
**Purpose:** Creates git-based restore points during the `/ship` pipeline so you can resume or rollback.

What it does:
1. Activates only when the prompt contains `/ship`
2. After each pipeline phase completes, saves the current `git HEAD` SHA to `.claude/checkpoints/{ship_id}.json`
3. Provides resume capability — reads the last completed phase and tells Claude where to continue

Supported flags:
- `/ship --status` — shows which phases completed and the next resume point
- `/ship --continue` — shows resume instructions
- `/ship --rollback {phase}` — runs `git reset --hard {sha}` to the phase checkpoint

Phases tracked: `plan → implement → refactor → verify → review → commit → pr`

When to enable: Only useful with a `/ship` pipeline command. Disable if you run each pipeline step manually.

---

## Utilities (`utils/`)

### `constants.py`

Provides `ensure_session_log_dir(session_id)` — creates and returns `.claude/logs/{session_id}/`. Used by every hook for consistent log paths.

### `knowledge_store.py`

TF-IDF indexed fragment storage. Manages the L2 knowledge store at `.claude/memory/knowledge/`:
- `DualKnowledgeStore` — handles both shared (`.claude/memory/knowledge/`) fragments
- `Fragment` dataclass — content, tags, scope, source, metadata
- Builds and maintains TF-IDF index for semantic search
- Supports adding, updating, and removing fragments

### `knowledge_retriever.py`

Query engine for the knowledge store:
- `KnowledgeRetriever.retrieve(prompt, top_k, min_score)` — returns ranked fragments
- Uses TF-IDF cosine similarity
- Supports tag-based filtering and personal vs shared scope

### `llm/anth.py`

Thin wrapper for calling the Anthropic API from hooks:
```python
from utils.llm.anth import call_anthropic
response = call_anthropic(prompt="...", model="claude-sonnet-4-20250514", max_tokens=2000)
```
Reads `ANTHROPIC_API_KEY` from environment. Used by `memory_extractor.py` and `knowledge_ingestor.py`.

### `llm/oai.py`

Same interface for OpenAI (optional, for teams using GPT models for hook extraction).

---

## Minimal Setup (3 hooks)

If you want just the essentials:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [{ "type": "command", "command": "uv run .claude/hooks/context_loader.py || true" }] },
      { "hooks": [{ "type": "command", "command": "uv run .claude/hooks/knowledge_loader.py || true" }] }
    ],
    "Stop": [
      { "matcher": "", "hooks": [{ "type": "command", "command": "uv run .claude/hooks/cost_tracker.py || true" }] }
    ]
  }
}
```

## Full Setup

For the complete stack:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      { "hooks": [{ "type": "command", "command": "uv run .claude/hooks/context_loader.py || true" }] },
      { "hooks": [{ "type": "command", "command": "uv run .claude/hooks/knowledge_loader.py || true" }] },
      { "hooks": [{ "type": "command", "command": "uv run .claude/hooks/smart_context_loader.py || true" }] },
      { "hooks": [{ "type": "command", "command": "uv run .claude/hooks/cost_advisor.py || true" }] },
      { "hooks": [{ "type": "command", "command": "uv run .claude/hooks/circuit_breaker.py || true" }] },
      { "hooks": [{ "type": "command", "command": "uv run .claude/hooks/clear_detector.py || true" }] },
      { "hooks": [{ "type": "command", "command": "uv run .claude/hooks/user_prompt_submit.py || true" }] }
    ],
    "PreToolUse": [
      { "hooks": [{ "type": "command", "command": "uv run .claude/hooks/pre_tool_use.py || true" }] }
    ],
    "PostToolUse": [
      { "hooks": [{ "type": "command", "command": "uv run .claude/hooks/post_tool_use.py || true" }] }
    ],
    "Stop": [
      { "matcher": "", "hooks": [{ "type": "command", "command": "uv run .claude/hooks/stop.py || true" }] },
      { "matcher": "", "hooks": [{ "type": "command", "command": "uv run .claude/hooks/context_updater.py || true" }] },
      { "matcher": "", "hooks": [{ "type": "command", "command": "uv run .claude/hooks/cost_tracker.py || true" }] },
      { "matcher": "", "hooks": [{ "type": "command", "command": "uv run .claude/hooks/memory_updater.py || true" }] },
      { "matcher": "", "hooks": [{ "type": "command", "command": "uv run .claude/hooks/knowledge_ingestor.py || true" }] }
    ],
    "SubagentStop": [
      { "matcher": "", "hooks": [{ "type": "command", "command": "uv run .claude/hooks/subagent_stop.py || true" }] }
    ],
    "PreCompact": [
      { "hooks": [{ "type": "command", "command": "uv run .claude/hooks/pre_compact.py || true" }] }
    ]
  }
}
```

## Customizing `smart_context_loader.py`

Edit `CONTEXT_RULES` at the top of the file to match your project's skills and patterns:

```python
CONTEXT_RULES = [
    {
        "name": "forms",
        "keywords": ["form", "input", "validation"],  # Add your keywords
        "skills": ["your-forms-skill"],                # Match your skill names
        "context": "Form handling - use YourFramework", # Your context note
        "priority": "high"
    },
    # Add more rules...
]
```

## Customizing `skill-activation-prompt.py`

This hook reads from `.claude/skills/skill-rules.json`. Create that file to define which skills get suggested for which prompts:

```json
{
  "version": "1.0",
  "skills": {
    "your-skill-name": {
      "promptTriggers": {
        "keywords": ["your", "keywords"],
        "intentPatterns": ["create.*thing", "add.*feature"]
      },
      "priority": "high",
      "enforcement": "suggest"
    }
  }
}
```
