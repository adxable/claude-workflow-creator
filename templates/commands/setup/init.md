# /setup:init - Claude Workflow Setup Wizard

Install the complete Claude Code workflow into your project — adapted to your stack, interactive, resumable.

## Arguments

- `$ARGUMENTS` - Optional flag: `--fresh` to ignore saved progress and restart from the beginning

## Instructions

### 1. Handle Arguments

If `$ARGUMENTS` contains `--fresh`:
- Delete `.claude/setup-progress.json` if it exists
- Continue to step 2

### 2. Execute Setup Wizard

Read `.claude/claude-init/setup.md` and execute all phases from the STARTUP section through PHASE 9.

The setup.md file contains complete orchestration for:
- Progress tracking across sessions (auto-resume if interrupted)
- Interactive questions via AskUserQuestion
- File creation for CLAUDE.md, commands, agents, contexts, memory, and hooks
- Per-phase confirmation banners and error handling

## Notes

- Progress is saved after each phase to `.claude/setup-progress.json`
- Safe to interrupt — run `/setup:init` again to resume from where you left off
- Check status at any time with `/setup:resume`
- Guides are in `.claude/claude-init/guide/` for deeper explanations of any phase

## Workflow Position

```
/setup:init → /setup:resume (check status)
    ↓
.claude/ is configured → start using /flow:plan
```
