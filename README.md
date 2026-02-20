# Claude Workflow Starter Kit

A portable, customizable Claude Code workflow that any team can copy into their project and adapt to their tech stack.

## What This Is

This kit packages a complete Claude Code development workflow into a single folder. Copy it to your project's `.claude/` directory, customize the templates, and you have:

- **6-command pipeline**: `/flow:plan → /flow:implement → /flow:review → /flow:verify → /flow:commit → /flow:pr`
- **Context detection**: Auto-routes to frontend vs backend tools based on your prompt
- **Specialized agents**: Planner, implementer, explorer, git automator
- **3-layer memory**: Persistent context across sessions (decisions, lessons, knowledge)
- **Event hooks**: Auto-inject context, track costs, extract learnings
- **Skills browser**: Install community skills from [skills.sh](https://skills.sh) via `/setup:skills`
- **Optional add-ons**: Jira MCP integration, browser automation

---

## Prerequisites

```bash
# Claude Code CLI
npm install -g @anthropic-ai/claude-code

# uv (for Python hooks)
curl -LsSf https://astral.sh/uv/install.sh | sh

# gh (for PR creation)
brew install gh && gh auth login

# Python 3.11+
python3 --version
```

---

## Getting Started

**Step 1 — Copy `claude-init` into your project:**

```bash
cp -r path/to/claude-init .claude/claude-init
```

**Step 2 — Bootstrap the setup commands** (one-time, makes `/setup:init` discoverable):

```bash
mkdir -p .claude/commands/setup
cp .claude/claude-init/templates/commands/setup/*.md .claude/commands/setup/
```

**Step 3 — Run the setup wizard:**

```
/setup:init
```

Claude will walk you through the entire setup interactively — asking about your tech stack, team structure, and preferences — then install everything configured for your project.

**Progress is saved** to `.claude/setup-progress.json`. If the session is interrupted, run `/setup:init` again to resume, or `/setup:resume` to check status.

---

## What the Setup Does

The wizard follows 9 phases based on the guides in this folder:

| Phase | What Gets Set Up |
|-------|-----------------|
| 0. Welcome | Shows what will be installed |
| 1. Brainstorm | Asks about your stack, team, and workflow preferences |
| 2. Core Pipeline | CLAUDE.md + 6 flow commands + settings.json |
| 3. Context Detection | Auto-routes frontend vs backend based on your prompt |
| 4. Agents | Installs planner, implementer, explorer, reviewer, git automator |
| 4B. Skills (optional) | Browse & install community skills from [skills.sh](https://skills.sh) |
| 5. Memory | 3-layer persistent context across sessions |
| 6. Hooks | Auto-inject context, track costs, circuit breakers |
| 7. Jira (optional) | Ticket management commands (if you use Jira) |
| 8. Browser (optional) | Chrome extension automation (if applicable) |
| 9. Final | Ensures `/setup:init` + `/setup:resume` + `/setup:skills` are present |

---

## Manual Setup (Alternative)

If you prefer to set things up yourself, follow the guides in order:

```bash
# Read the guides
cat .claude/claude-init/guide/01-core-flow.md      # Pipeline commands
cat .claude/claude-init/guide/02-context-detector.md  # Context detection
cat .claude/claude-init/guide/03-agents.md          # Agents
cat .claude/claude-init/guide/04-commands.md        # Slash commands

# Copy templates
mkdir -p .claude/commands/flow .claude/agents .claude/contexts .claude/memory
mkdir -p .claude/hooks/utils .claude/skills .claude/plans

cp .claude/claude-init/templates/CLAUDE.md .claude/CLAUDE.md
cp .claude/claude-init/templates/settings.json .claude/settings.json
cp .claude/claude-init/templates/commands/flow/*.md .claude/commands/flow/
cp .claude/claude-init/templates/agents/*.md .claude/agents/
cp .claude/claude-init/templates/memory/*.md .claude/memory/

# Hooks (ready-to-use)
mkdir -p .claude/hooks/utils/llm
cp .claude/claude-init/starter-hooks/*.py .claude/hooks/
cp -r .claude/claude-init/starter-hooks/utils/ .claude/hooks/utils/
```

Then replace all `{YOUR_*}` placeholders in the copied files with your actual commands and paths.

---

## Folder Structure

```
.claude/claude-init/
├── README.md                    ← You are here
│
├── guide/                       ← Step-by-step setup guides
│   ├── 00-brainstorm.md        ← START HERE — interactive Q&A
│   ├── 01-core-flow.md         ← plan → implement → verify pipeline
│   ├── 02-context-detector.md  ← Context detection engine
│   ├── 03-agents.md            ← Agent architecture
│   ├── 04-commands.md          ← Slash commands system
│   ├── 05-memory-system.md     ← 3-layer memory
│   ├── 06-hooks.md             ← Event hooks
│   ├── 07-jira-integration.md  ← Jira MCP + PM workflow
│   └── 08-chrome-extension.md  ← Browser automation
│
├── starter-hooks/               ← Ready-to-use hook implementations
│   ├── context_loader.py       ← L1 memory injection
│   ├── knowledge_loader.py     ← Semantic search (L2)
│   ├── cost_tracker.py         ← Token usage tracking
│   ├── circuit_breaker.py      ← Loop protection
│   ├── smart_context_loader.py ← Context-aware skill suggestions
│   ├── clear_detector.py       ← Memory extraction on /clear
│   └── utils/                  ← knowledge_store.py, knowledge_retriever.py
│
└── templates/                   ← Generic, customizable starting points
    ├── CLAUDE.md               ← Starter with {YOUR_PROJECT} placeholders
    ├── settings.json           ← Minimal hook config
    ├── commands/
    │   ├── flow/               ← plan.md, implement.md, verify.md
    │   ├── setup/              ← init.md, resume.md, skills.md (setup wizard commands)
    │   ├── jira/               ← start.md, pr-desc.md
    │   ├── pm/                 ← gen-stories-from-url.md, gen-tasks-for-story.md,
    │   │                          prepare.md, push.md
    │   └── utils/              ← refactor.md
    ├── agents/                 ← planner.md, implementer.md, explorer.md,
    │                              browser-tester.md, ...
    ├── contexts/               ← detector.py + context-template.yaml
    ├── skills/
    │   ├── skill-rules.json    ← keyword → skill activation mapping
    │   ├── frontend/
    │   │   └── browser-testing/SKILL.md  ← Chrome extension testing patterns
    │   └── pm/
    │       ├── jira-templates/SKILL.md   ← Story/task templates (placeholders)
    │       ├── story-writing/SKILL.md    ← User story best practices
    │       ├── task-breakdown/SKILL.md   ← PR-scoped task patterns
    │       └── estimation/SKILL.md       ← Sizing with AI speedup factors
    └── memory/                 ← Empty decisions/lessons/conventions
```

**Two types of content:**
- `starter-hooks/` contains **ready-to-use hook scripts** — copy directly, no modifications needed
- `templates/` contains **generic starting points** — copy these and fill in your values

---

## Read the Guides

| Guide | Time | What You Build |
|-------|------|---------------|
| `guide/01-core-flow.md` | 5 min | The 6-command pipeline |
| `guide/02-context-detector.md` | 5 min | Auto-detect FE vs BE work |
| `guide/03-agents.md` | 10 min | Specialized planner + implementer agents |
| `guide/04-commands.md` | 5 min | Custom slash commands |
| `guide/05-memory-system.md` | 10 min | Persistent context across sessions |
| `guide/06-hooks.md` | 10 min | Event automation |
| `guide/07-jira-integration.md` | 15 min | Jira integration (optional) |
| `guide/08-chrome-extension.md` | 10 min | Browser automation (optional) |

---

## What's in starter-hooks

The `starter-hooks/` folder contains ready-to-use Python hook scripts you can copy directly into `.claude/hooks/`. These are generic implementations that work for any project.

**Notable hooks:**
- `starter-hooks/context_loader.py` — Injects L1 memory (decisions, lessons, conventions) into every prompt
- `starter-hooks/knowledge_loader.py` — Semantic TF-IDF search over L2 knowledge fragments
- `starter-hooks/circuit_breaker.py` — Prevents runaway loops in autonomous pipelines
- `starter-hooks/cost_tracker.py` — Tracks token usage per session
- `starter-hooks/smart_context_loader.py` — Detects work context from prompt and suggests relevant skills
- `starter-hooks/utils/knowledge_store.py` — TF-IDF indexed fragment storage
- `starter-hooks/utils/knowledge_retriever.py` — Query engine for semantic search

---

## Support

- Claude Code docs: [docs.anthropic.com](https://docs.anthropic.com)
- Report issues: [github.com/anthropics/claude-code](https://github.com/anthropics/claude-code/issues)
