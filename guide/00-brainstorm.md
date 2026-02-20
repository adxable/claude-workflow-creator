# 00 — Brainstorm: Build Your Claude Workflow

> **START HERE.** This is an interactive guide. Run it with Claude Code in your project.
> Copy the prompt below into Claude Code and answer the questions to get a custom setup plan.

---

## Quick Start Prompt

Paste this into Claude Code in your project:

```
I want to set up a Claude Code workflow for my project. Please ask me a series of questions
to understand my tech stack, team size, and needs — then generate a customized setup plan
pointing to the relevant guides and templates in .claude/claude-init/.

Start with: What kind of project are you working on?
```

---

## What Claude Will Ask You

Claude will walk through these areas:

### 1. Project Type

- What's your tech stack? (React, Vue, Next.js, Angular, plain JS/TS?)
- Do you have a backend? (Node, .NET, Python, Java, Go, Ruby?)
- Is this a monorepo or single-purpose repo?

### 2. Team & Workflow

- Solo developer or a team?
- Do you use Jira, Linear, GitHub Issues, or another issue tracker?
- Do you use feature branches + PRs, or trunk-based development?

### 3. Current Pain Points

- What slows you down most? (planning, implementation, code review, testing?)
- Do you have CI/CD? What does it run? (tests, lint, type checks?)
- Is context loss between sessions a problem?

### 4. Desired Automation Level

- Do you want Claude to auto-commit and push, or confirm everything?
- Should Claude run tests automatically after implementation?
- Do you want browser automation for visual verification?

---

## What You'll Get

Based on your answers, Claude will generate a **custom setup checklist** like:

```
## Your Custom Setup Plan

Tech Stack: React/TypeScript + Node.js backend
Team: 3 developers
Issue Tracker: GitHub Issues

### Step 1: Core Pipeline (2 min)
→ Copy templates/CLAUDE.md and customize for your project
→ Read guide/01-core-flow.md

### Step 2: Context Detection (5 min)
→ Copy templates/contexts/detector.py
→ Copy templates/contexts/context-template.yaml twice (frontend + backend)
→ Read guide/02-context-detector.md

### Step 3: Agents (10 min)
→ Copy templates/agents/planner.md → customize for React
→ Copy templates/agents/implementer.md → customize for Node.js
→ Read guide/03-agents.md

### Step 4: Memory System (5 min)
→ Copy templates/memory/ files
→ Read guide/05-memory-system.md

### Step 5: Hooks (10 min)
→ Copy starter-hooks/ to .claude/hooks/
→ Configure settings.json from templates/settings.json
→ Read guide/06-hooks.md

### Optional: Jira Integration
→ Read guide/07-jira-integration.md

### Optional: Browser Automation
→ Read guide/08-chrome-extension.md
```

---

## Manual Guide Order

If you prefer to set things up manually without the interactive Q&A:

| Order | Guide | What It Sets Up |
|-------|-------|-----------------|
| 1 | `01-core-flow.md` | The `/plan → /implement → /verify` pipeline |
| 2 | `02-context-detector.md` | Auto-detect frontend vs backend work |
| 3 | `03-agents.md` | Specialized agents (planner, implementer, etc.) |
| 4 | `04-commands.md` | Slash commands (`/flow:plan`, `/flow:commit`) |
| 5 | `05-memory-system.md` | 3-layer memory for context persistence |
| 6 | `06-hooks.md` | Event hooks for automation |
| 7 | `07-jira-integration.md` | Jira MCP integration |
| 8 | `08-chrome-extension.md` | Browser automation |

---

## Prerequisites

Before starting, ensure you have:

- [ ] Claude Code installed (`claude` CLI)
- [ ] `uv` installed (for Python hooks) — `curl -LsSf https://astral.sh/uv/install.sh | sh`
- [ ] `gh` installed (for PR creation) — `brew install gh`
- [ ] Python 3.11+ available

---

## Folder Overview

```
.claude/claude-init/
├── guide/              ← You are here — step-by-step setup guides
├── starter-hooks/      ← Ready-to-use hook scripts (copy directly)
└── templates/          ← Generic, customizable starting points
```

**Next Step →** `guide/01-core-flow.md`
