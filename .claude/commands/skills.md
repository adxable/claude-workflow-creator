# /setup:skills - Browse and Install Skills from skills.sh

Discover and install community skills from the [skills.sh](https://skills.sh) registry into your project.

## Arguments

- `$ARGUMENTS` - Optional: search keyword override, e.g. `/setup:skills react`

## Usage

```bash
/setup:skills              # Auto-detect stack and suggest relevant skills
/setup:skills react        # Search for React-specific skills
/setup:skills backend      # Search for backend skills
/setup:skills testing      # Search for testing skills
```

## Instructions

### 1. Show Start Banner

```
═══════════════════════════════════════════════════
📦 Skills Browser — skills.sh
   Discover and install community skills
═══════════════════════════════════════════════════
```

### 2. Show Installed Skills

Glob `.claude/skills/**/*.md` (only SKILL.md files, i.e. `**/SKILL.md`).

Extract the `name` from each file's YAML frontmatter. If no frontmatter, use the directory name.

Display:

```
Currently installed (N skills):
  frontend/   react-best-practices, react-tables, react-forms ...
  backend/    dotnet-services, csharp-patterns ...
  workflow/   code-quality-rules, human-like-writing
  pm/         jira-templates, story-writing ...
```

If `.claude/skills/` is empty, show: `No skills installed yet.`

### 3. Detect or Ask Tech Stack

**Check** `.claude/setup-progress.json` for `answers.frontend_stack` and `answers.backend_stack`.

**If found**, show:
```
Detected stack: {frontend_stack} + {backend_stack}
```

**If not found** (standalone use), ask via AskUserQuestion:

```
Question: "What's your tech stack? (used to find relevant skills)"
Header:   "Stack"
Options:
  - "React + TypeScript (frontend)"
  - "React + JavaScript (frontend)"
  - "Vue / Angular / Svelte (frontend)"
  - "Node.js (backend)"
  - ".NET / C# (backend)"
  - "Python (backend)"
  - "Go (backend)"
  - "Fullstack — let me pick both"
```

If `$ARGUMENTS` provided, skip this step and use it directly as the search query.

### 4. Build Search Queries

Map stack to skills.sh keywords:

| Stack | Search Keywords |
|-------|----------------|
| React + TypeScript | `react typescript` |
| React + JavaScript | `react javascript` |
| Vue 3 | `vue typescript` |
| Next.js | `nextjs react` |
| .NET / C# | `dotnet csharp` |
| Node.js | `nodejs typescript` |
| Python | `python fastapi` |
| Go | `golang` |
| Generic frontend | `frontend javascript` |
| Generic backend | `backend api` |

If `$ARGUMENTS` provided, use it verbatim as the keyword.

### 5. Search skills.sh Registry

Run the search command:

```bash
npx --yes skills find {keywords}
```

This outputs a list of available skills with their install identifiers.

**If the command fails** (npx not available, network error, etc.), show:
```
⚠ Could not reach skills.sh registry.
  Try manually: npx skills find {keywords}
  Browse:       https://skills.sh
```
Then skip to Step 7.

**Parse the output** — each result typically looks like:
```
owner/repo@skill-name  — Description of the skill
```

Extract a list of `{ id: "owner/repo@skill-name", description: "..." }` entries.
Filter out skills that are already installed (match by name).

### 6. Present Results and Let User Select

If no results found:
```
No skills found for "{keywords}" on skills.sh.
Try a different keyword: /setup:skills {other keyword}
Browse the full registry: https://skills.sh
```

Otherwise, show count and present with AskUserQuestion (multiSelect: true):

```
Question: "Which skills do you want to install? ({N} found for '{keywords}')"
Header:   "Skills"
Options: (up to 4, prioritize most relevant)
  - label: "{skill-name}"
    description: "{description from registry}"
```

If more than 4 results, include a "Show more results" option and re-run with `--limit` or an offset query.

Also include:
- label: "None — skip for now"
  description: "Close the browser without installing"

### 7. Install Selected Skills

For each selected skill (skip if "None" selected):

```bash
npx --yes skills add {owner/repo@skill-name}
```

Show progress:
```
  Installing react-best-practices...  ✓
  Installing react-tables...          ✓
  Installing csharp-patterns...       ✗ (already installed, skipped)
```

**On error:** show `⚠ Failed to install {skill}: {error}` and continue with the rest.

Skills install to `.claude/skills/{skill-name}/SKILL.md`.

### 8. Show Summary and Next Steps

```
═══════════════════════════════════════════════════
  ✅ Skills Installation Complete

  Installed: {N} new skills
  Location:  .claude/skills/

  Your skills are now available to agents and
  can be loaded into any conversation.
═══════════════════════════════════════════════════
  NEXT:
    /setup:skills {other keyword}   Install more skills
    /flow:plan "feature"            Start using the workflow
    https://skills.sh               Browse the full registry
═══════════════════════════════════════════════════
```

### 9. Offer to Search Again

AskUserQuestion:

```
Question: "What would you like to do next?"
Header:   "Action"
Options:
  - "Search for more skills"  → go back to Step 3
  - "Create my own skill"     → show npx skills init instructions
  - "Done — close browser"    → end
```

**If "Create my own skill":**

```
To create a skill for your project:

  npx skills init

This creates a new skill in the current directory with the
correct SKILL.md frontmatter. Skills are auto-published via
usage telemetry — no submission needed.

Your skill directory should be placed at:
  .claude/skills/{skill-name}/SKILL.md

Format:
  ---
  name: your-skill-name
  description: What this skill provides
  ---

  # Your Skill Title

  [skill content]
```

## Notes

- Skills are installed to `.claude/skills/` which Claude Code reads automatically
- The `npx --yes` flag installs the skills CLI without prompting
- Skills already installed are detected by matching directory names under `.claude/skills/`
- Browse the full registry at https://skills.sh

## Workflow Position

```
/setup:init → /setup:skills → /flow:plan → /flow:implement
    ↑               ↑
Setup wizard    Standalone skill browser (run anytime)
```

## Related

- **Command**: `/setup:init` - Full setup wizard (includes skills step)
- **Command**: `/setup:resume` - Check setup progress
- **Registry**: https://skills.sh - Browse all available skills
