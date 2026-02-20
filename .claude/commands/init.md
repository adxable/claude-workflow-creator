# /setup:init - Claude Workflow Setup Wizard

Install the complete Claude Code workflow into any project — adapted to your stack, interactive, resumable.

## Arguments

- `$ARGUMENTS` - Optional flag: `--fresh` to ignore saved progress and restart from the beginning

## Instructions

### 1. Handle Arguments

If `$ARGUMENTS` contains `--fresh`:
- Delete `.claude/setup-progress.json` if it exists
- Continue to step 2

### 2. Execute Setup Wizard

Read `setup.md` (in the repository root) and execute all phases from the STARTUP section through PHASE 9.

The setup.md file contains complete orchestration for:
- Asking the user where to install the workflow (target project path)
- Progress tracking across sessions (auto-resume if interrupted)
- Interactive questions via AskUserQuestion
- Copying templates from this repo into the target project's `.claude/` directory
- Per-phase confirmation banners and error handling

## Notes

- Progress is saved after each phase to `.claude/setup-progress.json` (in this repo)
- Safe to interrupt — run `/setup:init` again to resume from where you left off
- Check status at any time with `/setup:resume`
- Guides are in `guide/` for deeper explanations of any phase
- Source templates live in this repo under `templates/`, `starter-hooks/`, `guide/`
- Files are installed into `{target_project}/.claude/`

## Workflow Position

```
/setup:init → asks for target project path
    ↓
{target_project}/.claude/ is configured → start using /flow:plan in target project
```
