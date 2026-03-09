# Claude Workflow Setup — Master Orchestration

This is the master setup orchestration document. It is executed by the `/setup:init` command, which reads this file and follows the phases below.

Progress is tracked in `.claude/setup-progress.json` (in this repo). If interrupted, run `/setup:init` again or `/setup:resume` to continue.

---

## Entry Point

Open this repo in Claude Code and run:

```
/setup:init
```

To restart from the beginning:

```
/setup:init --fresh
```

To check status or resume:

```
/setup:resume
```

---

## Path Convention

This wizard uses two base directories:

- **`SOURCE`** = the root of this repo (where `setup.md`, `templates/`, `starter-hooks/`, `guide/` live)
- **`TARGET`** = the user's project root (provided by the user in PHASE 0)

All copy operations follow the pattern:
```
{SOURCE}/templates/...  →  {TARGET}/.claude/...
{SOURCE}/starter-hooks/...  →  {TARGET}/.claude/hooks/...
{SOURCE}/guide/...  →  read for context (not copied)
```

When reading templates, use paths relative to this repo root (e.g., `templates/CLAUDE.md`).
When writing files, use the target path (e.g., `{TARGET}/.claude/CLAUDE.md`).

---

## Instructions for Claude

Follow the phases below in order. Skip any phase already listed in `completed_phases` inside `.claude/setup-progress.json`.

---

### STARTUP: Check Progress

1. Try to read `.claude/setup-progress.json`.

2. **If it exists and has completed phases:**

```
╔══════════════════════════════════════════════════════════╗
║  🔄 Resuming Setup                                        ║
╠══════════════════════════════════════════════════════════╣
║  Target:    {target_path}                                ║
║  Started:   {started}                                    ║
║  Progress:  {N} of {total} phases complete               ║
║  Done:      {completed_phases}                           ║
╚══════════════════════════════════════════════════════════╝
```

Ask (AskUserQuestion):
- "Continue from where I left off" ← Recommended
- "Start fresh — redo everything"

If "Start fresh": delete `.claude/setup-progress.json`, continue to Phase 0.
If "Continue": read `target_path` from the progress file, use it as `TARGET` for all subsequent phases.

3. **If it does not exist:** continue to Phase 0.

---

### PHASE 0: WELCOME & TARGET PATH

**Step 1 — Show welcome banner:**

```
╔══════════════════════════════════════════════════════════╗
║  🚀 Claude Workflow Setup Wizard                         ║
╠══════════════════════════════════════════════════════════╣
║  This wizard installs a complete Claude Code workflow    ║
║  into your project's .claude/ directory.                 ║
║                                                          ║
║  Phase 0  — Where to install (target project path)       ║
║  Phase 1  — Brainstorm your project & team needs         ║
║  Phase 2  — Core pipeline (6 flow commands)              ║
║  Phase 3  — Context detection (FE/BE routing)            ║
║  Phase 4  — Agents (planner, implementer, reviewer...)   ║
║  Phase 4B — Skills from skills.sh (optional)             ║
║  Phase 5  — Memory system (3-layer persistence)          ║
║  Phase 6  — Hooks (event automation)                     ║
║  Phase 7  — Jira integration (optional)                  ║
║  Phase 8  — Browser automation (optional)                ║
║  Phase 8B — Context7 MCP (live documentation)            ║
║                                                          ║
║  Progress saved after each phase.                        ║
║  Safe to interrupt — resume with the same command.       ║
╚══════════════════════════════════════════════════════════╝
```

**Step 2 — Ask for target project path:**

Use AskUserQuestion:
- Header: "Target project"
- Question: "Where should the workflow be installed? Provide the absolute path to your project root."
- Options:
  - label: "Enter path"
    description: "I'll provide the absolute path to my project (e.g., /Users/me/Projects/my-app)"

The user will select "Other" and type their project path (or select "Enter path" and provide it via the description).

**Important:** The user MUST provide an actual filesystem path. After receiving the answer:

1. **Validate the path exists** — use Bash to run `test -d "{path}" && echo "EXISTS" || echo "NOT_FOUND"`
2. **If NOT_FOUND:** show error and ask again:
   ```
   [setup] ⚠ Directory not found: {path}
            Please provide a valid absolute path to your project.
   ```
3. **If EXISTS:** confirm with the user:
   ```
   [setup] Target project: {path}
            Will install to: {path}/.claude/
   ```

Save the validated path as `target_path` in the progress file.

**Step 3 — Write initial progress file** to `.claude/setup-progress.json` (in this repo):
```json
{
  "version": "1.0",
  "started": "{ISO datetime}",
  "last_updated": "{ISO datetime}",
  "target_path": "{validated absolute path}",
  "completed_phases": [],
  "answers": {},
  "files_created": []
}
```

From this point forward:
- **`TARGET`** = the `target_path` value (the user's project)
- **`SOURCE`** = this repo's root (where `templates/`, `starter-hooks/`, `guide/` live)
- All files are **read from `SOURCE`** and **written to `{TARGET}/.claude/`**

Save phase `welcome` to `completed_phases`. Update `last_updated`.

---

### PHASE 1: BRAINSTORM
_Based on: `guide/00-brainstorm.md`_

Read `guide/00-brainstorm.md` (in this repo) for context on what to ask.

Use ONE `AskUserQuestion` call with 3 questions:

**Q1 — Project**
- Header: "Project type"
- Question: "What kind of project is this?"
- Options:
  - "Fullstack — frontend + backend"
  - "Frontend only (React / Vue / Angular / Next.js)"
  - "Backend / API only"
  - "Monorepo — multiple apps"

**Q2 — Frontend stack**
- Header: "Frontend"
- Question: "What frontend technology are you using? (select None if backend-only)"
- Options:
  - "React + TypeScript"
  - "React + JavaScript"
  - "Vue 3 + TypeScript"
  - "Next.js (React)"
  (Other: "Angular", "Svelte", "None", etc.)

**Q3 — Backend stack**
- Header: "Backend"
- Question: "What backend technology are you using? (select None if frontend-only)"
- Options:
  - "Node.js + TypeScript"
  - "Python (FastAPI / Django / Flask)"
  - ".NET / C#"
  - "Go"
  (Other: "Java", "Ruby", "Rust", "None", etc.)

Save to `answers`: `project_type`, `frontend_stack`, `backend_stack`.

Then use a SECOND `AskUserQuestion` call with 3 more questions:

**Q4 — Team**
- Header: "Team"
- Question: "How does your team work?"
- Options:
  - "Solo developer"
  - "Small team (2–5 people)"
  - "Larger team (6+ people)"

**Q5 — Git platform**
- Header: "Git platform"
- Question: "Where does your team host Git repositories?"
- Options:
  - "GitHub"
  - "GitLab"
  - "Bitbucket"
  - "Azure DevOps"
  (Other: self-hosted GitLab, Gitea, etc.)

**Q6 — Issue Tracker**
- Header: "Issue tracker"
- Question: "Which issue tracker does your team use?"
- Options:
  - "Jira"
  - "GitHub Issues"
  - "GitLab Issues"
  - "Linear"
  (Other: "Azure Boards", "Bitbucket Issues", "None", etc.)

**Q7 — Browser testing**
- Header: "Browser testing"
- Question: "Do you want visual browser verification after implementation? (Requires Chrome extension)"
- Options:
  - "Yes — auto-screenshot and verify UI"
  - "No — manual browser testing"

Save to `answers`: `team_size`, `git_platform`, `issue_tracker`, `browser_testing`.

Then use a THIRD `AskUserQuestion` call for exact commands:

**Q7 — Verification commands**
- Header: "Build commands"
- Question: "What commands validate your code? (will be put directly in /flow:verify)"
- Options based on earlier answers:
  - If React/TS + pnpm → "pnpm: tsc --noEmit + eslint + build"
  - If React/TS + npm → "npm: tsc + eslint + build"
  - If Python → "mypy + ruff + pytest"
  - If .NET → "dotnet build + dotnet test"
  (Other: enter custom commands)

If "Other" or unclear, ask follow-up:
```
AskUserQuestion:
  "Enter your exact validation commands (one per line or comma-separated)"
  - Type check: "e.g., pnpm tsc --noEmit"
  - Lint: "e.g., pnpm eslint src/ --max-warnings=0"
  - Build: "e.g., pnpm build"
  - Test (optional): "e.g., pnpm test"
```

Save to `answers.commands`: `typecheck`, `lint`, `build`, `test` (may be empty), `start` (dev server).

Also ask for directory paths if fullstack:

```
AskUserQuestion:
  "Where do your source directories live?"
  - Frontend root: "e.g., frontend/ or src/Shiplex.Web.Frontend"
  - Backend root: "e.g., backend/ or src/api"
```

Save to `answers`: `frontend_dir`, `backend_dir`.

Save phase `brainstorm` to `completed_phases`. Update progress file.

Show summary:
```
[setup] ✓ Phase 1 complete — Brainstorm
         Project:  {project_type}
         Frontend: {frontend_stack} in {frontend_dir}
         Backend:  {backend_stack} in {backend_dir}
         Git:      {git_platform}
         Tracker:  {issue_tracker}
```

---

### PHASE 2: CORE PIPELINE
_Based on: `guide/01-core-flow.md`_

Read `guide/01-core-flow.md` (in this repo) for context.

**Create directory structure in TARGET:**
```bash
mkdir -p {TARGET}/.claude/commands/flow {TARGET}/.claude/commands/utils {TARGET}/.claude/commands/jira {TARGET}/.claude/commands/setup
mkdir -p {TARGET}/.claude/agents {TARGET}/.claude/contexts
mkdir -p {TARGET}/.claude/memory
mkdir -p {TARGET}/.claude/hooks/utils {TARGET}/.claude/plans {TARGET}/.claude/skills {TARGET}/.claude/reviews {TARGET}/.claude/context {TARGET}/.claude/logs
```

**Create `{TARGET}/.claude/CLAUDE.md`:**
Read `templates/CLAUDE.md` (from this repo). Fill in ALL placeholders using answers:
- `{YOUR_PROJECT}` → project name (ask if not captured, or derive from `git -C {TARGET} remote get-url origin`)
- `{FRONTEND_DIR}` → `answers.frontend_dir`
- `{BACKEND_DIR}` → `answers.backend_dir`
- `{React/Vue/Angular/etc}` → `answers.frontend_stack`
- `{Node/Python/.NET/etc}` → `answers.backend_stack`
- `{YOUR_TYPECHECK_COMMAND}` → `answers.commands.typecheck`
- `{YOUR_LINT_COMMAND}` → `answers.commands.lint`
- `{YOUR_BUILD_COMMAND}` → `answers.commands.build`
- `{YOUR_TEST_COMMAND}` → `answers.commands.test` (remove line if empty)
Write to `{TARGET}/.claude/CLAUDE.md`.

**Create all 6 flow commands:**
For each file in `templates/commands/flow/` (this repo), read it, fill in `{YOUR_*}` placeholders, write to `{TARGET}/.claude/commands/flow/`.

Key substitutions in `verify.md`:
- All `{YOUR_*_COMMAND}` → actual commands from answers
- `{YOUR_FRONTEND_DIR}` → `answers.frontend_dir`

Key substitutions in `pr.md` — replace the `gh pr create` call with the correct CLI for the chosen platform:
- **GitHub** → `gh pr create --title "{title}" --body "{body}" --base {base}`
  _(requires: `gh` CLI, `gh auth login`)_
- **GitLab** → `glab mr create --title "{title}" --description "{body}" --target-branch {base}`
  _(requires: `glab` CLI, `glab auth login`)_
- **Bitbucket** → `echo "Open PR at: $(git remote get-url origin)/pull-requests/new?source=$(git branch --show-current)"`
  _(no dedicated CLI; print URL for manual creation)_
- **Azure DevOps** → `az repos pr create --title "{title}" --description "{body}" --target-branch {base}`
  _(requires: `az` CLI with `azure-devops` extension, `az login`)_

Also update the error handling hint in `pr.md` — replace `gh auth login` with the platform-appropriate auth command.

**Create utility commands:**
- Read `templates/commands/utils/refactor.md` (this repo), fill in typecheck + lint commands, write to `{TARGET}/.claude/commands/utils/refactor.md`

**Create setup commands:**
- Read `templates/commands/setup/init.md` → write to `{TARGET}/.claude/commands/setup/init.md`
- Read `templates/commands/setup/resume.md` → write to `{TARGET}/.claude/commands/setup/resume.md`
- Read `templates/commands/setup/skills.md` → write to `{TARGET}/.claude/commands/setup/skills.md`
- Read `templates/commands/setup/audit.md` → write to `{TARGET}/.claude/commands/setup/audit.md`

**Create settings.json:**
- Read `templates/settings.json` (this repo) → write to `{TARGET}/.claude/settings.json`

Add all to `files_created`. Save phase `core_pipeline` to `completed_phases`. Update progress.

Show:
```
[setup] ✓ Phase 2 complete — Core Pipeline
         Target:  {TARGET}
         Created: .claude/CLAUDE.md, .claude/settings.json
         Created: /flow:plan, /flow:implement, /flow:review
                  /flow:verify, /flow:commit, /flow:pr
                  /utils:refactor
                  /setup:init, /setup:resume, /setup:skills
```

---

### PHASE 3: CONTEXT DETECTION
_Based on: `guide/02-context-detector.md`_

Read `guide/02-context-detector.md` (in this repo) for context.

**Skip this phase if** project is "Frontend only" (single context — no routing needed).

Otherwise:

Copy detector:
- Read `templates/contexts/detector.py` (this repo) → write to `{TARGET}/.claude/contexts/detector.py`

**Create `frontend.yaml`** if frontend is not "None":

Read `templates/contexts/context-template.yaml` (this repo). Fill in:
- `{CONTEXT_NAME}` → `frontend`
- Paths based on `answers.frontend_dir` and typical structure for `answers.frontend_stack`
- Extensions based on stack (`.tsx/.ts` for React/TS, `.vue/.ts` for Vue, etc.)
- Keywords for the stack
- `project_root` → `answers.frontend_dir`
- Verify commands from answers
- Agents: `planner: "planner"`, `implementer: "implementer"`, `reviewer: "code-reviewer"`

Write to `{TARGET}/.claude/contexts/frontend.yaml`.

**Create `backend.yaml`** if backend is not "None":

Similar, adapted to backend stack. Write to `{TARGET}/.claude/contexts/backend.yaml`.

Add to `files_created`. Save phase `context_detection` to `completed_phases`. Update progress.

Show:
```
[setup] ✓ Phase 3 complete — Context Detection
         Target:  {TARGET}/.claude/contexts/
         Created: detector.py
         Created: frontend.yaml ({frontend_stack})
         Created: backend.yaml ({backend_stack})
```

---

### PHASE 4: AGENTS
_Based on: `guide/03-agents.md`_

Read `guide/03-agents.md` (in this repo) for context.

**Copy all agent templates** (read from this repo, write to TARGET):

```
# Always installed — generic agents (fallback)
templates/agents/explorer.md       → {TARGET}/.claude/agents/explorer.md
templates/agents/git-automator.md  → {TARGET}/.claude/agents/git-automator.md
templates/agents/refactorer.md     → {TARGET}/.claude/agents/refactorer.md
templates/agents/code-reviewer.md  → {TARGET}/.claude/agents/code-reviewer.md
templates/agents/planner.md        → {TARGET}/.claude/agents/planner.md
templates/agents/implementer.md    → {TARGET}/.claude/agents/implementer.md

# If frontend or fullstack — frontend-specialized agents
templates/agents/planner-fe.md        → {TARGET}/.claude/agents/planner-fe.md
templates/agents/implementer-fe.md    → {TARGET}/.claude/agents/implementer-fe.md
templates/agents/code-reviewer-fe.md  → {TARGET}/.claude/agents/code-reviewer-fe.md

# If backend or fullstack — backend-specialized agents
templates/agents/planner-be.md        → {TARGET}/.claude/agents/planner-be.md
templates/agents/implementer-be.md    → {TARGET}/.claude/agents/implementer-be.md
templates/agents/code-reviewer-be.md  → {TARGET}/.claude/agents/code-reviewer-be.md

# If Jira
templates/agents/jira.md           → {TARGET}/.claude/agents/jira.md

# If browser testing enabled
templates/agents/browser-tester.md → {TARGET}/.claude/agents/browser-tester.md
```

**Specialized agents** contain stack-specific knowledge (glob patterns, validation commands, review checklists, coding conventions). They are used by the context detection system — when the flow commands detect frontend or backend context, they route to the specialized agent (e.g., `planner-fe` instead of `planner`).

**Generic agents** serve as fallbacks when context is ambiguous or for non-FE/BE work.

For **frontend agents** (`planner-fe.md`, `implementer-fe.md`, `code-reviewer-fe.md`), fill in:
- `{YOUR_FRONTEND_DIR}` → `answers.frontend_dir` (e.g., `frontend`)
- `{YOUR_TYPECHECK_COMMAND}` → `answers.commands.typecheck` (e.g., `pnpm tsc --noEmit`)
- `{YOUR_LINT_COMMAND}` → `answers.commands.lint` (e.g., `pnpm eslint src/`)
- `{YOUR_BUILD_COMMAND}` → `answers.commands.build` (e.g., `pnpm build`)
- Frontend stack-specific patterns from `answers.frontend_stack`

For **backend agents** (`planner-be.md`, `implementer-be.md`, `code-reviewer-be.md`), fill in:
- `{YOUR_BACKEND_DIR}` → `answers.backend_dir` (e.g., `backend`)
- `{YOUR_BACKEND_EXT}` → file extension for the backend language (e.g., `java` for Java, `cs` for .NET, `py` for Python)
- `{YOUR_BACKEND_BUILD_COMMAND}` → `answers.commands.backend_build` (e.g., `mvn compile`)
- `{YOUR_BACKEND_TEST_COMMAND}` → `answers.commands.backend_test` (e.g., `mvn test`)
- Backend stack-specific patterns from `answers.backend_stack`

For `browser-tester.md`, fill in:
- `{YOUR_DEV_SERVER_COMMAND}` → `answers.commands.start` (e.g., `pnpm dev`)
- `{YOUR_APP_URL}` → e.g., `http://localhost:5173`

For generic `planner.md` and `implementer.md`, fill in:
- `{YOUR_COMPONENT_GLOB}` → e.g., `{frontend_dir}/src/components/**/*.tsx`
- `{YOUR_FEATURE_GLOB}` → e.g., `{frontend_dir}/src/features/**/*.tsx`
- `{YOUR_TYPECHECK_COMMAND}` → actual command from answers

Add to `files_created`. Save phase `agents` to `completed_phases`. Update progress.

Show:
```
[setup] ✓ Phase 4 complete — Agents
         Target:  {TARGET}/.claude/agents/
         Generic:    planner, implementer, code-reviewer
                     explorer, refactorer, git-automator
         Frontend:   planner-fe, implementer-fe, code-reviewer-fe
         Backend:    planner-be, implementer-be, code-reviewer-be
         {if Jira: + jira}
         {if browser testing: + browser-tester}
```

---

### PHASE 4B: SKILLS (OPTIONAL)
_Based on: https://skills.sh_

**The skills browser command was already copied in Phase 2** to `{TARGET}/.claude/commands/setup/skills.md`.

**Ask the user:**

```
AskUserQuestion:
  question: "Would you like to browse skills.sh and install community skills for your stack?"
  header:   "Skills"
  options:
    - label: "Yes — open skills browser"
      description: "Search skills.sh registry and install relevant skills for your stack (Recommended)"
    - label: "Skip — I'll add skills manually later"
      description: "Continue to the next step, install skills later with /setup:skills"
```

**If "Yes":**

Run the skills browser inline:

1. Use the tech stack from `answers` to build a search query (same logic as in `commands/setup/skills.md` Step 4)
2. Run: `cd {TARGET} && npx --yes skills find {keywords}`
3. Present results and let user pick (multiSelect AskUserQuestion)
4. For each selected skill, install **only for Claude Code** using direct git clone (do NOT use `npx skills add --yes` as it installs to ALL agents and creates dozens of unwanted directories):

```bash
# Clone the skill repo to temp
cd /tmp && git clone --depth 1 https://github.com/{owner}/{repo}.git skill-tmp
# Copy just the skill to Claude's skills directory
cp -r /tmp/skill-tmp/skills/{skill-name} {TARGET}/.claude/skills/{skill-name}
# Clean up
rm -rf /tmp/skill-tmp
```

The skill identifier from skills.sh is `{owner}/{repo}@{skill-name}`, which maps to:
- GitHub repo: `https://github.com/{owner}/{repo}.git`
- Skill directory in repo: `skills/{skill-name}`
- Target: `{TARGET}/.claude/skills/{skill-name}`

5. Show confirmation of installed skills

**IMPORTANT:** Never use `npx skills add --yes` — it creates `.adal`, `.cursor`, `.cline`, `.agents`, and 30+ other agent directories in the project root. Always use the git clone approach above to install only for Claude Code.

**If the git clone fails** (git not available or repo not found):
```
[setup] ⚠ Could not install skill — skipping
         You can install skills manually later: /setup:skills
         Browse: https://skills.sh
```

Save phase `skills` to `completed_phases`. Update progress.

Show:
```
[setup] ✓ Phase 4B complete — Skills
         Target:  {TARGET}/.claude/skills/
         Installed: {N} skill(s) from skills.sh
         Run /setup:skills anytime to install more.
```

---

### PHASE 5: MEMORY SYSTEM
_Based on: `guide/05-memory-system.md`_

Read `guide/05-memory-system.md` (in this repo) for context.

**Copy memory templates** (read from this repo, write to TARGET):

```
templates/memory/README.md       → {TARGET}/.claude/memory/README.md
templates/memory/decisions.md    → {TARGET}/.claude/memory/decisions.md
templates/memory/lessons.md      → {TARGET}/.claude/memory/lessons.md
templates/memory/conventions.md  → {TARGET}/.claude/memory/conventions.md
```

Add project header to each file — insert after the `#` heading:
```markdown
> Project: {project_name} | Setup: {current date}
```

These three markdown files are the core memory system. The `context_loader.py` hook (installed in Phase 6) injects their contents into every significant prompt, giving Claude persistent memory across sessions.

Add to `files_created`. Save phase `memory` to `completed_phases`. Update progress.

Show:
```
[setup] ✓ Phase 5 complete — Memory System
         Target:  {TARGET}/.claude/memory/
         Created: README.md (memory system overview)
         Created: decisions.md, lessons.md, conventions.md
```

---

### PHASE 6: HOOKS
_Based on: `guide/06-hooks.md`_

Read `guide/06-hooks.md` (in this repo) for context.

**Copy hooks** (read from this repo's `starter-hooks/`, write to `{TARGET}/.claude/hooks/`):

```
# Memory injection (UserPromptSubmit)
starter-hooks/context_loader.py        → {TARGET}/.claude/hooks/context_loader.py

# Security (PreToolUse) — blocks rm -rf and .env access
starter-hooks/pre_tool_use.py          → {TARGET}/.claude/hooks/pre_tool_use.py

# Session end (Stop)
starter-hooks/stop.py                  → {TARGET}/.claude/hooks/stop.py
starter-hooks/cost_tracker.py          → {TARGET}/.claude/hooks/cost_tracker.py
```

Also copy the utils directory:
- Read all files from `starter-hooks/utils/` (this repo) → write to `{TARGET}/.claude/hooks/utils/`
- This includes `__init__.py` and `constants.py`

**The `settings.json` was already created in Phase 2** from `templates/settings.json`. It wires the hooks to their events. No changes needed here — just verify it exists at `{TARGET}/.claude/settings.json`.

Add hook files to `files_created`. Save phase `hooks` to `completed_phases`. Update progress.

Show:
```
[setup] ✓ Phase 6 complete — Hooks
         Target:  {TARGET}/.claude/hooks/
         Installed (UserPromptSubmit):
           context_loader     — memory injection (decisions, lessons, conventions)
         Installed (PreToolUse):
           pre_tool_use       — blocks rm -rf + .env access
         Installed (Stop):
           stop               — session logging
           cost_tracker       — daily usage metrics
         ⚠ Restart Claude Code to activate hooks
```

---

### PHASE 7: JIRA INTEGRATION (OPTIONAL)
_Based on: `guide/07-jira-integration.md`_

**Skip if** `answers.issue_tracker` ≠ "Jira".

Read `guide/07-jira-integration.md` (in this repo) for context.

**Step 1 — Install commands and directories in TARGET:**

```bash
mkdir -p {TARGET}/.claude/commands/jira {TARGET}/.claude/commands/pm {TARGET}/.claude/jira {TARGET}/.claude/jira-ready {TARGET}/.claude/screenshots
```

Copy commands (read from this repo, write to TARGET):
```
templates/commands/jira/start.md              → {TARGET}/.claude/commands/jira/start.md
templates/commands/jira/pr-desc.md            → {TARGET}/.claude/commands/jira/pr-desc.md
templates/commands/pm/gen-stories-from-url.md → {TARGET}/.claude/commands/pm/gen-stories-from-url.md
templates/commands/pm/gen-tasks-for-story.md  → {TARGET}/.claude/commands/pm/gen-tasks-for-story.md
templates/commands/pm/prepare.md              → {TARGET}/.claude/commands/pm/prepare.md
templates/commands/pm/push.md                 → {TARGET}/.claude/commands/pm/push.md
```

**Step 2 — Install generic PM skills (fallback templates):**

```bash
mkdir -p {TARGET}/.claude/skills/pm/jira-templates {TARGET}/.claude/skills/pm/story-writing
mkdir -p {TARGET}/.claude/skills/pm/task-breakdown {TARGET}/.claude/skills/pm/estimation
```

Copy skills (read from this repo, write to TARGET):
```
templates/skills/pm/jira-templates/SKILL.md → {TARGET}/.claude/skills/pm/jira-templates/SKILL.md
templates/skills/pm/story-writing/SKILL.md  → {TARGET}/.claude/skills/pm/story-writing/SKILL.md
templates/skills/pm/task-breakdown/SKILL.md → {TARGET}/.claude/skills/pm/task-breakdown/SKILL.md
templates/skills/pm/estimation/SKILL.md     → {TARGET}/.claude/skills/pm/estimation/SKILL.md
```

**Step 3 — Learn from real tickets (optional but highly recommended):**

```
AskUserQuestion:
  question: "Want to customize the Jira templates to match your team's writing style?"
  header: "Jira templates"
  options:
    - label: "Yes — learn from our real tickets (Recommended)"
      description: "Share 2-3 ticket keys; I'll read them and generate templates that match your team's format"
    - label: "Skip — use generic templates for now"
      description: "You can run /setup:init again later to customize with examples"
```

**If "Learn from real tickets":**

Ask via AskUserQuestion (3 separate questions or one with text input):

1. **Story/Feature example** — "Share a key for a well-written Story or Feature ticket (e.g., PROJ-42)"
2. **Bug example** — "Share a key for a well-written Bug ticket (e.g., PROJ-17)" (optional, skip if none)
3. **Task/Subtask example** — "Share a key for a well-written Task or Subtask (e.g., PROJ-88)" (optional)

For each provided key, fetch the ticket:

```
Use mcp__mcp-atlassian__jira_get_issue to fetch each ticket.
```

**Read and analyze each ticket. Extract:**

- Description structure (which bold headers are used, in what order)
- Acceptance criteria style (checkboxes vs dashes vs GIVEN/WHEN/THEN vs numbered)
- Tone and level of detail (brief vs exhaustive, technical vs user-facing)
- Section names (e.g., "ACCEPTANCE CRITERIA" vs "Done when" vs "Definition of Done")
- Any project-specific conventions (e.g., `!! important` markers, `---` separators)
- Issue type names (what is the subtask called — "Sub-task", "Task", "Podzadanie"?)
- Project key and cloud ID (extract from the fetched ticket metadata)

**Generate a customized `pm/jira-templates/SKILL.md`:**

Do NOT use the copied template file — **write a new one from scratch** that:

1. Starts with the frontmatter and a note that it was learned from examples:
   ```markdown
   ---
   name: pm-jira-templates
   description: Jira story and task templates adapted to {PROJECT_NAME} conventions.
   ---
   # PM Skill: Jira Templates
   > Generated from real tickets: {comma-separated ticket keys}
   > Project: {PROJECT_KEY} | Cloud ID: {CLOUD_ID}
   ```

2. Shows the **actual sections** and **actual formatting** observed in the example tickets — not the generic ones from the template

3. Includes one **annotated example** per ticket type (Story, Bug, Task/Subtask) reproduced verbatim from the real ticket but with sensitive content replaced by `[...]` placeholders:
   ```markdown
   ## Story Example (from {PROJ-XX})
   [reproduced structure with real section names and format, content anonymized]
   ```

4. Includes the **MCP creation snippet** filled in with real values:
   ```typescript
   mcp__mcp-atlassian__jira_create_issue({
     cloudId: "{actual cloud ID}",
     projectKey: "{actual project key}",
     issueTypeName: "Story",   // or whatever the team uses
     ...
   })
   ```

Write the generated file to `{TARGET}/.claude/skills/pm/jira-templates/SKILL.md` (overwriting the generic copy).

**If fetching fails** (MCP not connected, ticket not found, etc.):

```
[setup] ⚠ Could not read ticket {key}: {error}
         Falling back to generic templates.
         You can customize later: /setup:init → Phase 7
```

Continue with the generic templates already installed in Step 2.

---

Add to `files_created`. Save phase `jira` to `completed_phases`. Update progress.

Show:

```
[setup] ✓ Phase 7 complete — Jira Integration
         Installed: /jira:start, /jira:pr-desc
         Installed (PM pipeline):
           /pm:gen-stories-from-url  — generate stories from a URL
           /pm:gen-tasks-for-story   — generate tasks from a Jira story
           /pm:prepare               — configure tracker fields
           /pm:push                  — push to Jira
         Installed (PM skills):
           pm/jira-templates  — {customized from {N} examples | generic fallback}
           pm/story-writing   — story writing patterns
           pm/task-breakdown  — task breakdown guidelines
           pm/estimation      — sizing and estimation
         ⚠ Still needed: claude mcp add mcp-atlassian
         Guide: guide/07-jira-integration.md (in this repo)
```

---

### PHASE 8: BROWSER AUTOMATION (OPTIONAL)
_Based on: `guide/08-chrome-extension.md`_

**Skip if** `answers.browser_testing` ≠ "Yes".

Read `guide/08-chrome-extension.md` (in this repo) for context. Show the setup instructions from that guide.

**Install browser-testing skill:**

```bash
mkdir -p {TARGET}/.claude/skills/frontend/browser-testing
```

Read `templates/skills/frontend/browser-testing/SKILL.md` (this repo) → write to `{TARGET}/.claude/skills/frontend/browser-testing/SKILL.md`

**Note:** The `browser-tester` agent was already installed in Phase 4 (conditional on browser testing choice).

Show:
```
[setup] ✓ Phase 8 noted — Browser Automation
         Installed: skills/frontend/browser-testing (Chrome extension patterns)
         Installed: agents/browser-tester (visual verification + fix loop)
         The /flow:review --browser flag triggers browser verification.
         ⚠ Still needed: Install Claude Chrome extension
         Guide: guide/08-chrome-extension.md (in this repo)
```

Save phase `browser` to `completed_phases`. Update progress.

---

### PHASE 8B: CONTEXT7 MCP (OPTIONAL)
_Based on: https://context7.com_

Context7 provides up-to-date library documentation as an MCP server for Claude Code. When Claude needs to reference documentation (React, Spring Boot, etc.), it can query Context7 for current docs instead of relying on training data.

**Ask the user:**

```
AskUserQuestion:
  question: "Would you like to install Context7 MCP for up-to-date library documentation?"
  header:   "Context7"
  options:
    - label: "Yes — install Context7 (Recommended)"
      description: "Adds an MCP server that provides current documentation for React, Spring Boot, and other libraries"
    - label: "Skip — I'll add it manually later"
      description: "You can install later: claude mcp add context7 -- npx -y @upstash/context7-mcp"
```

**If "Yes":**

1. Ask if the user has a Context7 API key:

```
AskUserQuestion:
  question: "Do you have a Context7 API key? (Free at context7.com/dashboard — optional but recommended for higher rate limits)"
  header:   "API key"
  options:
    - label: "No key — install without API key"
      description: "Works with rate limits; get a key later at context7.com/dashboard"
    - label: "I have a key"
      description: "Enter your Context7 API key for higher rate limits"
```

2. Install the MCP server:

**Without API key (local):**
```bash
cd {TARGET} && claude mcp add context7 -- npx -y @upstash/context7-mcp
```

**With API key (remote, recommended):**
```bash
cd {TARGET} && claude mcp add --header "CONTEXT7_API_KEY: {api_key}" --transport http context7 https://mcp.context7.com/mcp
```

**If the command fails** (claude CLI not in PATH or permission error):
```
[setup] Could not auto-install Context7 MCP.
         Install manually:
         claude mcp add context7 -- npx -y @upstash/context7-mcp
         Docs: https://context7.com
```

Show:
```
[setup] Phase 8B complete — Context7 MCP
         Installed: context7 MCP server
         Provides: Up-to-date documentation for React, Spring Boot, and 1000+ libraries
         Usage: Claude will automatically use Context7 when referencing docs
```

Save phase `context7` to `completed_phases`. Update progress.

---

### PHASE 9: FINAL — SUMMARY

**Verify setup commands exist** in `{TARGET}/.claude/commands/setup/` (they should have been copied in Phase 2). If missing, copy them now:

```
templates/commands/setup/init.md   → {TARGET}/.claude/commands/setup/init.md
templates/commands/setup/resume.md → {TARGET}/.claude/commands/setup/resume.md
templates/commands/setup/skills.md → {TARGET}/.claude/commands/setup/skills.md
templates/commands/setup/audit.md  → {TARGET}/.claude/commands/setup/audit.md
```

Add to `files_created` if newly created.

**Mark setup complete in progress file:**
```json
{
  "status": "complete",
  "completed_at": "{ISO datetime}"
}
```

**Show completion banner:**

```
╔══════════════════════════════════════════════════════════════╗
║  ✅ SETUP COMPLETE                                           ║
╠══════════════════════════════════════════════════════════════╣
║  Target:     {TARGET}                                        ║
║  Project:    {project_name}                                  ║
║  Frontend:   {frontend_stack} ({frontend_dir})               ║
║  Backend:    {backend_stack} ({backend_dir})                 ║
║  Integrations: {issue_tracker} {browser_testing}             ║
╠══════════════════════════════════════════════════════════════╣
║  Files installed ({total_count} files):                      ║
║   {TARGET}/.claude/CLAUDE.md                                 ║
║   {TARGET}/.claude/settings.json                             ║
║   {TARGET}/.claude/commands/flow/  (6 commands)              ║
║   {TARGET}/.claude/commands/utils/ (1 command)               ║
║   {TARGET}/.claude/agents/         ({N} agents)              ║
║   {TARGET}/.claude/contexts/       (detector + YAML configs) ║
║   {TARGET}/.claude/memory/         (decisions, lessons, etc) ║
║   {TARGET}/.claude/hooks/          ({N} scripts)             ║
╠══════════════════════════════════════════════════════════════╣
║  ⚠ Open {TARGET} in Claude Code to use the workflow         ║
║  ⚠ Restart Claude Code to activate hooks                    ║
╠══════════════════════════════════════════════════════════════╣
║  START USING THE WORKFLOW (from the target project):         ║
║                                                              ║
║    /flow:plan "first feature description"                    ║
║    → /flow:implement .claude/plans/{name}.md                 ║
║    → /flow:verify                                            ║
║    → /flow:commit                                            ║
║    → /flow:pr                                                ║
║                                                              ║
║  OTHER COMMANDS:                                             ║
║    /utils:refactor        clean up code                      ║
║    /flow:review           code review                        ║
║    /setup:skills          install more skills from skills.sh ║
{if jira}
║    /jira:start PROJ-123   start a Jira ticket                ║
{/if}
║                                                              ║
║  VERIFY:  /setup:audit           verify installation          ║
║  GUIDES:  guide/ (in this repo)                              ║
║  RESUME:  /setup:resume                                      ║
╚══════════════════════════════════════════════════════════════╝
```

---

### ERROR HANDLING

If any file copy or write fails:
1. Show: `[setup] ⚠ Could not create {file}: {error}`
2. Update progress: `"last_error": "{description}"`
3. Continue with the next file — don't stop the whole setup
4. At the end, list any skipped files and how to fix them manually

If a template file is missing:
- Note it: `[setup] ⚠ Template not found: {path} — skipping`
- Continue

If user interrupts mid-phase:
- The progress file already has completed phases saved
- User can restart the same command to resume

---

### RULES FOR CLAUDE

1. **Read each guide before the corresponding phase** — the guides contain the rationale and context that makes customization decisions better
2. **Never leave `{PLACEHOLDER}` in created files** — use actual values or sensible defaults
3. **Save progress after EVERY phase** — not in batch
4. **Use `AskUserQuestion` for all interactions** — not text prompts
5. **When filling templates**, read the full template first, then write the full file with all substitutions applied
6. **Track every file written** in `files_created`
