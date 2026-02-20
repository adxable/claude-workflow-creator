# Claude Workflow Starter Kit

A portable, customizable Claude Code workflow that any team can install into their project through an interactive setup wizard.

## Getting Started

**Step 1 — Open this repo in Claude Code:**

```bash
claude /path/to/claude-workflow-wizard
```

**Step 2 — Run the setup wizard:**

```
/setup:init
```

The wizard will ask where to install the workflow, then walk you through everything interactively — asking about your tech stack, team structure, and preferences.

**Progress is saved** after each phase. If interrupted, run `/setup:init` again to resume.

---

## What Gets Installed

- **6-command pipeline**: `/flow:plan → /flow:implement → /flow:review → /flow:verify → /flow:commit → /flow:pr`
- **Context detection**: Auto-routes to frontend vs backend tools based on your prompt
- **Specialized agents**: Planner, implementer, explorer, reviewer, git automator
- **3-layer memory**: Persistent context across sessions (decisions, lessons, knowledge)
- **Event hooks**: Auto-inject context, track costs, extract learnings
- **Skills browser**: Install community skills from [skills.sh](https://skills.sh) via `/setup:skills`
- **Optional add-ons**: Jira MCP integration, browser automation

---

## Prerequisites

```bash
# Claude Code CLI
npm install -g @anthropic-ai/claude-code

# Python 3.11+
brew install python@3.11

# uv (for Python hooks)
curl -LsSf https://astral.sh/uv/install.sh | sh

# gh (for PR creation)
brew install gh && gh auth login
```

---

## Setup Phases

| Phase | What Gets Set Up |
|-------|-----------------|
| 0. Welcome | Asks for target project path |
| 1. Brainstorm | Asks about your stack, team, and workflow preferences |
| 2. Core Pipeline | CLAUDE.md + 6 flow commands + settings.json |
| 3. Context Detection | Auto-routes frontend vs backend based on your prompt |
| 4. Agents | Installs planner, implementer, explorer, reviewer, git automator |
| 4B. Skills (optional) | Browse & install community skills from [skills.sh](https://skills.sh) |
| 5. Memory | 3-layer persistent context across sessions |
| 6. Hooks | Auto-inject context, track costs, circuit breakers |
| 7. Jira (optional) | Ticket management commands (if you use Jira) |
| 8. Browser (optional) | Chrome extension automation (if applicable) |

---

## Manual Setup (Optional)

If you prefer to set things up yourself without the wizard:

```bash
TARGET=/path/to/your/project
SOURCE=/path/to/claude-workflow-wizard

mkdir -p $TARGET/.claude/{commands/flow,agents,contexts,memory,hooks/utils,skills,plans}

cp $SOURCE/templates/CLAUDE.md $TARGET/.claude/CLAUDE.md
cp $SOURCE/templates/settings.json $TARGET/.claude/settings.json
cp $SOURCE/templates/commands/flow/*.md $TARGET/.claude/commands/flow/
cp $SOURCE/templates/agents/*.md $TARGET/.claude/agents/
cp $SOURCE/templates/memory/*.md $TARGET/.claude/memory/
cp $SOURCE/starter-hooks/*.py $TARGET/.claude/hooks/
cp -r $SOURCE/starter-hooks/utils/ $TARGET/.claude/hooks/utils/
```

Then replace all `{YOUR_*}` placeholders with your actual values.

---

## Support

- Claude Code docs: [docs.anthropic.com](https://docs.anthropic.com)
- Report issues: [github.com/anthropics/claude-code](https://github.com/anthropics/claude-code/issues)
