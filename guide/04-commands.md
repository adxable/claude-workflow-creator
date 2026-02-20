# 04 — Commands: The Slash Command System

Commands are the user-facing entry points of your workflow. Each command is a markdown file in `.claude/commands/` that Claude reads and follows when you type `/command-name`.

## Directory Structure

```
.claude/commands/
├── flow/               ← Core development pipeline
│   ├── plan.md
│   ├── implement.md
│   ├── verify.md
│   ├── review.md
│   ├── commit.md
│   └── pr.md
├── jira/               ← Issue tracker commands (optional)
│   ├── start.md
│   └── pr-desc.md
├── utils/              ← Utility commands
│   ├── refactor.md
│   └── memory.md
└── {context}/          ← Context-specific commands (optional)
    └── build.md
```

Subdirectory commands use the `:` separator: `flow/plan.md` → `/flow:plan`

---

## Command File Format

A command file is just markdown with instructions for Claude:

```markdown
# /flow:plan - Context-Aware Planning

Short description of what this command does.

## Arguments

- `$ARGUMENTS` - What the user passes after the command

## Usage

/flow:plan "Add search to the products page"
/flow:plan [frontend] "Add filters to orders list"

## Instructions

### 1. Show Start Banner
...

### 2. Detect Context
...

### 3. Invoke Agent
Use Task tool with subagent_type: "planner"
...
```

The key patterns are:
1. **`$ARGUMENTS`** — Placeholder for user's input
2. **Numbered steps** — Claude follows them in order
3. **Agent invocation** — Delegates work to specialized agents
4. **Banners** — Structured output so users know where they are

---

## The 6 Core Pipeline Commands

### Planning Phase

**`/flow:plan`** — Creates an implementation plan
- Calls: `planner` agent (context-appropriate)
- Output: `.claude/plans/{name}.md`
- Template: `templates/commands/flow/plan.md`

**`/flow:implement`** — Executes the plan
- Calls: `implementer` agent (context-appropriate)
- Input: Plan file path
- Template: `templates/commands/flow/implement.md`

### Quality Phase

**`/flow:review`** — Code review with checklists
- Calls: `code-reviewer` agent
- Output: `.claude/reviews/review-{date}.md`
- Template: `templates/commands/flow/review.md`

**`/flow:verify`** — Run validation suite
- Runs: your type checks, lint, build, tests
- Template: `templates/commands/flow/verify.md`

### Ship Phase

**`/flow:commit`** — Conventional commit
- Calls: `git-automator` agent
- Format: `feat(scope): description`
- Template: `templates/commands/flow/commit.md`

**`/flow:pr`** — Create pull request
- Calls: `git-automator` agent
- Uses: `gh pr create`
- Template: `templates/commands/flow/pr.md`

---

## Jira Commands (Optional)

Requires Atlassian MCP configured. See `guide/07-jira-integration.md`.

### `/jira:start` — Begin a ticket

```bash
/jira:start PROJ-123
```

1. Reads the Jira ticket
2. Moves status to "In Progress"
3. Assigns to you
4. Creates an implementation plan via `/flow:plan`

**Template:** `templates/commands/jira/start.md`

### `/jira:pr-desc` — Generate PR description from ticket

```bash
/jira:pr-desc
```

1. Auto-detects ticket key from branch name (`PROJ-123-feature` → PROJ-123)
2. Reads ticket for context
3. Analyzes git diff for actual changes
4. Generates PR title + description
5. Optionally transitions ticket to "In Review"

**Template:** `templates/commands/jira/pr-desc.md`

### Full Jira Developer Flow

```bash
/jira:start PROJ-123
→ /flow:implement .claude/plans/PROJ-123-feature.md
→ /flow:verify
→ /jira:pr-desc
→ /flow:pr
```

---

## Utility Commands

### `/utils:refactor` — Code cleanup

```bash
/utils:refactor                        # All changed files on branch
/utils:refactor src/features/auth/     # Specific directory
```

Calls the `refactorer` agent to:
- Remove `any` types and fix type safety
- Remove dead code and unused imports
- Split oversized files
- Fix code quality issues

**Template:** `templates/commands/utils/refactor.md`

### `/utils:memory` — Memory management

```bash
/utils:memory add "Always use useSuspenseQuery for data fetching" --tags react,data
/utils:memory search "suspense"
/utils:memory show
```

### `/utils:discover` — Codebase exploration

```bash
/utils:discover "how is authentication handled"
/utils:discover "show all API endpoint definitions"
```

---

## Writing a New Command

Here's a minimal command template:

```markdown
# /mycommand:name - Short Description

What this command does.

## Arguments

- `$ARGUMENTS` - Description of expected input

## Usage

/mycommand:name "some argument"

## Instructions

### 1. Show Start Banner

═══════════════════════════════
🚀 Starting {Name}
   └─ Task: {$ARGUMENTS}
═══════════════════════════════

### 2. Do the Work

{Step-by-step instructions for Claude}

### 3. Show Completion

═══════════════════════════════
✅ {NAME} COMPLETE
═══════════════════════════════

NEXT STEPS:
1. Next command to run
```

---

## Context Override Syntax

All pipeline commands support manual context override using bracketed prefixes:

```bash
/flow:plan [frontend] "Add filtering"   # Force frontend context
/flow:plan [backend] "Add API endpoint" # Force backend context
/flow:plan "Add filtering"              # Auto-detect context
```

Implement this in command files by checking `$ARGUMENTS` first:

```markdown
### 2. Detect Context

**Priority order:**
1. Manual override: `[frontend]` or `[backend]` in $ARGUMENTS
2. Auto-detect from description keywords
3. Ask user if ambiguous

| Indicators | Context |
|------------|---------|
| component, hook, tsx, React | Frontend |
| service, endpoint, controller, cs | Backend |
```

---

## Command Naming Conventions

| Pattern | Example | When to Use |
|---------|---------|-------------|
| `flow:*` | `/flow:plan` | Core pipeline steps |
| `{context}:*` | `/frontend:build` | Context-specific tools |
| `utils:*` | `/utils:memory` | Utility commands |
| `pm:*` | `/pm:stories` | Product management |
| `jira:*` | `/jira:start` | Issue tracker commands |

---

## Complete Template List

| Template | Command | What It Does |
|----------|---------|-------------|
| `templates/commands/flow/plan.md` | `/flow:plan` | Research + plan implementation |
| `templates/commands/flow/implement.md` | `/flow:implement` | Execute plan step by step |
| `templates/commands/flow/review.md` | `/flow:review` | Code review with checklists |
| `templates/commands/flow/verify.md` | `/flow:verify` | Type check, lint, build |
| `templates/commands/flow/commit.md` | `/flow:commit` | Conventional git commit |
| `templates/commands/flow/pr.md` | `/flow:pr` | Create pull request |
| `templates/commands/jira/start.md` | `/jira:start` | Start Jira ticket + create plan |
| `templates/commands/jira/pr-desc.md` | `/jira:pr-desc` | PR description from ticket |
| `templates/commands/utils/refactor.md` | `/utils:refactor` | Code cleanup |

---

**Next Step →** `guide/05-memory-system.md`
