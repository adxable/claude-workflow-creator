# /setup:resume - Check Setup Status or Resume

Check the current state of the Claude workflow setup and continue if incomplete.

## Instructions

### 1. Read Progress File

Read `.claude/setup-progress.json`.

**If it does not exist:**

```
╔══════════════════════════════════════════════════════════╗
║  ⚠ No setup progress found                               ║
╠══════════════════════════════════════════════════════════╣
║  Setup has not been started yet.                         ║
║  Run: /setup:init                                        ║
╚══════════════════════════════════════════════════════════╝
```

Stop here.

### 2. Show Status

Display progress with a phase checklist:

```
╔══════════════════════════════════════════════════════════╗
║  📋 Setup Status                                          ║
╠══════════════════════════════════════════════════════════╣
║  Started:   {started}                                    ║
║  Updated:   {last_updated}                               ║
║  Files:     {files_created.length} created               ║
╠══════════════════════════════════════════════════════════╣
║  Phases:                                                 ║
║   {✓ or ○} welcome          — Welcome                   ║
║   {✓ or ○} brainstorm       — Project & stack questions  ║
║   {✓ or ○} core_pipeline    — Commands & CLAUDE.md       ║
║   {✓ or ○} context_detection — Frontend/backend routing  ║
║   {✓ or ○} agents           — Planner, implementer, etc. ║
║   {✓ or ○} memory           — 3-layer knowledge store    ║
║   {✓ or ○} hooks            — Event automation           ║
║   {✓ or ○} jira             — Jira integration           ║
║   {✓ or ○} browser          — Browser automation         ║
╠══════════════════════════════════════════════════════════╣
║  Stack:     {answers.frontend_stack} / {answers.backend_stack} ║
║  Tracker:   {answers.issue_tracker}                      ║
╚══════════════════════════════════════════════════════════╝
```

Use ✓ for completed phases and ○ for pending ones.

### 3. Decide Next Action

**If `status === "complete"`:**

Show the workflow cheatsheet:

```
╔══════════════════════════════════════════════════════════╗
║  ✅ Setup is complete                                     ║
╠══════════════════════════════════════════════════════════╣
║  WORKFLOW CHEATSHEET:                                    ║
║                                                          ║
║    /flow:plan "feature description"                      ║
║    → /flow:implement .claude/plans/{name}.md             ║
║    → /flow:verify                                        ║
║    → /flow:commit                                        ║
║    → /flow:pr                                            ║
║                                                          ║
║  OTHER:                                                  ║
║    /utils:refactor        clean up code                  ║
║    /flow:review           code review                    ║
║    /jira:start PROJ-123   start a ticket (if Jira)       ║
╚══════════════════════════════════════════════════════════╝
```

**If phases are incomplete:**

Use AskUserQuestion:
- "Continue setup from last completed phase" (Recommended)
- "Just show me the status — I'll continue manually"

If "Continue": read `.claude/claude-init/setup.md` and resume from the first incomplete phase.

## Workflow Position

```
/setup:init → (interrupted) → /setup:resume → continue
                                   ↓
                          (complete) → /flow:plan
```
