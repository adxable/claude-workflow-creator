# 03 — Agents: Specialized Workers

Agents are the execution layer of the workflow. Each agent is a markdown file in `.claude/agents/` that defines a specialist with specific tools, a model, and a task scope.

## Architecture

```
Command (/flow:plan)
    ↓
Detects context (frontend)
    ↓
Invokes Task tool with subagent_type: "planner-fe"
    ↓
Claude reads .claude/agents/fe/planner-fe.md
    ↓
Agent executes with given tools + model
```

Agents run as subprocesses ("subagents") via Claude's Task tool, which keeps their work isolated from the main conversation window.

---

## Agent File Format

Every agent is a markdown file with a YAML front matter header:

```markdown
---
name: planner-fe
description: Research and create implementation plans for React/TypeScript features.
tools: Read, Grep, Glob, Write
model: opus
---

# Frontend Planner Agent

{Instructions for what this agent does and how}
```

**Key fields:**
- `name` — The subagent_type identifier (used in Task tool calls)
- `description` — What Claude Code shows when selecting agents
- `tools` — Comma-separated list of allowed tools
- `model` — `opus` (most capable), `sonnet` (balanced), `haiku` (fast/cheap)

---

## Agent Types

### Planner Agents (model: opus)

Research the codebase before implementation. They:
- Search for similar patterns using Glob + Grep
- Read existing files for context
- Write a structured plan file to `.claude/plans/`
- **Never modify source code**

The `templates/agents/planner.md` file provides a generic starting point — copy and customize for your tech stack.

### Implementer Agents (model: sonnet)

Execute plan files step by step. They:
- Read the plan file
- Load relevant skills
- Create and modify source files
- Run validation commands after changes
- Report blockers without guessing

The `templates/agents/implementer.md` file provides a generic starting point — copy and customize for your stack.

### Explorer Agent (model: haiku)

Fast, read-only codebase search. Used by other agents when they need to quickly find a file or pattern without reading everything.

The `templates/agents/explorer.md` provides a minimal read-only agent to start with.

### Git Automator Agent (model: sonnet/haiku)

Handles all git operations: commits, branches, PRs. Reads git history to match your commit style. This is a general-purpose agent — see the Claude Code built-in `git-automator` subagent type.

---

## Setting Up Agents for Your Stack

### Step 1: Choose your agent directory structure

```bash
mkdir -p .claude/agents/fe
mkdir -p .claude/agents/be
mkdir -p .claude/agents/shared
```

Or flat if single-context:

```bash
mkdir -p .claude/agents
```

### Step 2: Copy and customize templates

```bash
# Core pipeline agents
cp .claude/claude-init/templates/agents/planner.md .claude/agents/planner.md
cp .claude/claude-init/templates/agents/implementer.md .claude/agents/implementer.md
cp .claude/claude-init/templates/agents/explorer.md .claude/agents/explorer.md

# Code quality agents
cp .claude/claude-init/templates/agents/refactorer.md .claude/agents/refactorer.md
cp .claude/claude-init/templates/agents/code-reviewer.md .claude/agents/code-reviewer.md

# Git and DevOps
cp .claude/claude-init/templates/agents/git-automator.md .claude/agents/git-automator.md

# Optional: Jira (requires Atlassian MCP)
cp .claude/claude-init/templates/agents/jira.md .claude/agents/jira.md
```

**Context-specific setup** (if you have FE/BE split):
```bash
mkdir -p .claude/agents/fe .claude/agents/be
cp .claude/claude-init/templates/agents/planner.md .claude/agents/fe/planner-fe.md
cp .claude/claude-init/templates/agents/planner.md .claude/agents/be/planner-be.md
# etc.
```

### Step 3: Customize for your stack

Edit `planner-fe.md` — update the research patterns section:

```markdown
### 1. Find Similar Patterns

# Replace these with YOUR project's patterns:
Glob: "src/components/**/*.tsx"      → YOUR component path
Glob: "src/hooks/**/*.ts"            → YOUR hook path
Grep: "export function"              → YOUR export pattern
```

Edit `implementer-fe.md` — update validation commands:

```markdown
## Validation

After each file change:
npm run typecheck 2>&1 | head -20    → YOUR type check
npm run lint 2>&1 | head -20         → YOUR lint
```

---

## Agent Design Principles

### Tool Restrictions

Give each agent only the tools it needs:

| Agent | Tools |
|-------|-------|
| Planner | Read, Grep, Glob, Write (for plan file) |
| Implementer | Read, Write, Edit, Grep, Glob, Bash |
| Explorer | Read, Grep, Glob (read-only!) |
| Reviewer | Read, Grep, Glob, Bash |
| Git Automator | Bash, Read, Grep |

### Model Selection

| Agent | Model | Why |
|-------|-------|-----|
| Planner | opus | Complex reasoning, architecture decisions |
| Implementer | sonnet | Balanced: good code quality, reasonable speed |
| Explorer | haiku | Fast, cheap — just needs to find files |
| Git Automator | haiku | Simple string operations |

### Terminal Output Convention

All agents should show consistent terminal output:

```markdown
**On Start:**
┌─────────────────────────────────────────────────┐
│  📋 AGENT: planner-fe                           │
│  📋 Task: {brief description}                   │
│  ⚡ Model: opus                                 │
└─────────────────────────────────────────────────┘

**During Execution:**
[planner-fe] Searching for patterns...
[planner-fe] Found: {description}
[planner-fe] Creating plan...

**On Complete:**
[planner-fe] ✓ Complete (Plan: {file_path})
```

---

## Calling Agents from Commands

In your command files, invoke agents like this:

```markdown
### 3. Invoke Planner Agent

Use Task tool with subagent_type: "planner-fe", model: "opus"

Task: Research the codebase and create an implementation plan for: {description}

Search paths:
- YOUR_COMPONENT_PATH/**/*.tsx
- YOUR_HOOKS_PATH/**/*.ts

Create plan at: .claude/plans/fe/{type}-{name}.md
```

---

## Complete Agent Template List

| Template | Subagent Type | Model | Purpose |
|----------|---------------|-------|---------|
| `templates/agents/planner.md` | `planner` | opus | Research codebase + create plan |
| `templates/agents/implementer.md` | `implementer` | sonnet | Execute plan step by step |
| `templates/agents/explorer.md` | `explorer` | haiku | Fast read-only codebase search |
| `templates/agents/refactorer.md` | `refactorer` | sonnet | Clean up code quality issues |
| `templates/agents/code-reviewer.md` | `code-reviewer` | opus | Code review + quality report |
| `templates/agents/git-automator.md` | `git-automator` | haiku | Commits, branches, PRs |
| `templates/agents/jira.md` | `jira` | sonnet | Jira ticket operations (MCP) |

---

**Next Step →** `guide/04-commands.md`
