# 01 — Core Flow: plan → implement → verify

The foundation of the workflow is a 6-command pipeline that takes a task from idea to merged PR.

## The Pipeline

```
/flow:plan → /flow:implement → /flow:review → /flow:verify → /flow:commit → /flow:pr
```

Each command is a markdown file in `.claude/commands/flow/`. Claude reads the file and follows its instructions when you run the slash command.

---

## How Each Command Works

### `/flow:plan`

**What it does:** Researches your codebase and creates a structured plan file.

**Under the hood:**
1. Detects context (frontend vs backend) from your description
2. Invokes a specialized `planner` agent (e.g., `planner-fe` or `planner-be`)
3. The agent searches for similar patterns in your codebase
4. Outputs a structured `.claude/plans/{context}/{name}.md` file

**Template:** `templates/commands/flow/plan.md`

**Usage:**
```bash
/flow:plan "Add user authentication"
/flow:plan [frontend] "Add filters to the orders list"
/flow:plan [backend] "Add export endpoint for reports"
```

---

### `/flow:implement`

**What it does:** Reads the plan file and executes each step.

**Under the hood:**
1. Detects context from plan file metadata
2. Invokes a specialized `implementer` agent
3. The agent creates/modifies files following your patterns
4. Runs incremental validation after each file change
5. Reports blockers instead of guessing

**Template:** `templates/commands/flow/implement.md`

**Usage:**
```bash
/flow:implement .claude/plans/fe/feature-auth.md
/flow:implement [frontend] "Quick fix for button style"
```

---

### `/flow:review`

**What it does:** Context-aware code review with checklists.

**Under the hood:**
1. Detects changed files from git diff
2. Invokes a code reviewer agent (e.g., `code-reviewer-fe`)
3. Reviews against your project's quality checklist
4. Optionally adds browser verification (`--browser` flag)
5. Outputs a review report to `.claude/reviews/`

**Template:** `templates/commands/flow/review.md`

---

### `/flow:verify`

**What it does:** Runs type checks, linting, build, and tests.

**Under the hood:**
1. Detects context from changed files
2. Runs context-specific validation commands
3. Shows structured pass/fail output
4. Suggests `--fix` for auto-fixable lint errors

**Template:** `templates/commands/flow/verify.md`

**Validation commands by context:**

| Context | Commands |
|---------|----------|
| React/TS | `pnpm tsc --noEmit`, `pnpm eslint`, `pnpm build` |
| .NET | `dotnet build`, `dotnet test` |
| Node.js | `npm run typecheck`, `npm run lint`, `npm test` |
| Python | `mypy`, `ruff check`, `pytest` |

---

### `/flow:commit`

**What it does:** Stages all changes and creates a conventional commit.

**Under the hood:**
1. Detects context from changed file paths
2. Invokes `git-automator` agent
3. Analyzes changes to determine commit type + scope
4. Uses HEREDOC format for the commit message
5. Includes `Co-Authored-By: Claude` attribution

**Template:** `templates/commands/flow/commit.md`

---

### `/flow:pr`

**What it does:** Creates a pull request with a structured description.

**Under the hood:**
1. Analyzes all commits on the branch
2. Generates a PR title and body
3. Pushes branch and creates PR via `gh pr create`

**Template:** `templates/commands/flow/pr.md`

---

## Setting Up the Pipeline

### Step 1: Create the commands directory

```bash
mkdir -p .claude/commands/flow
```

### Step 2: Copy and customize templates

```bash
cp .claude/claude-init/templates/commands/flow/plan.md .claude/commands/flow/plan.md
cp .claude/claude-init/templates/commands/flow/implement.md .claude/commands/flow/implement.md
cp .claude/claude-init/templates/commands/flow/verify.md .claude/commands/flow/verify.md
```

Copy all remaining pipeline commands from templates:

```bash
cp .claude/claude-init/templates/commands/flow/review.md .claude/commands/flow/review.md
cp .claude/claude-init/templates/commands/flow/commit.md .claude/commands/flow/commit.md
cp .claude/claude-init/templates/commands/flow/pr.md .claude/commands/flow/pr.md
```

### Step 3: Customize verification commands

Edit `.claude/commands/flow/verify.md` and replace the verification commands with your stack's:

```markdown
# Replace these with YOUR stack's commands:

## Frontend Verification
pnpm tsc --noEmit        → YOUR type check command
pnpm eslint src/         → YOUR lint command
pnpm build               → YOUR build command

## Backend Verification
dotnet build             → YOUR build command
dotnet test              → YOUR test command
```

### Step 4: Register in CLAUDE.md

Add the commands table to your `CLAUDE.md`:

```markdown
## Commands

| Command | Description |
|---------|-------------|
| `/flow:plan {desc}` | Research codebase and create plan |
| `/flow:implement {plan}` | Execute plan step by step |
| `/flow:review` | Code review with checklists |
| `/flow:verify` | Run type checks, lint, build, tests |
| `/flow:commit` | Conventional commit |
| `/flow:pr` | Create pull request |
```

---

## Minimal Setup (No Context Detection)

If you don't want context detection, you can use a single flat command file instead of separate FE/BE commands. Replace the agent dispatch in `plan.md` with a direct instruction:

```markdown
## Instructions

Invoke the `planner` agent:

Use Task tool with subagent_type: "adx:planner"

Task: Research the codebase and create an implementation plan for: {$ARGUMENTS}
Search for similar patterns and generate a plan file at: .claude/plans/{name}.md
```

---

**Next Step →** `guide/02-context-detector.md` (or skip to `03-agents.md` if you don't need FE/BE detection)
