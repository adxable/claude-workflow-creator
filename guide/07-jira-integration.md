# 07 — Jira Integration: PM Workflow

The Jira integration connects Claude Code to your project management workflow. It uses the Atlassian MCP server to read tickets, update statuses, and create issues directly from the CLI.

## Prerequisites

1. Install the MCP Atlassian server:
   - Follow setup at: https://github.com/sooperset/mcp-atlassian
   - Or use the Atlassian Cloud MCP: `claude mcp add mcp-atlassian`

2. Configure in settings.json:
```json
{
  "enabledMcpjsonServers": ["mcp-atlassian"]
}
```

---

## Developer Workflow Commands

### `/jira:start` — Begin a ticket

```bash
/jira:start YOUR-123
```

This command:
1. Reads the Jira ticket details
2. Moves ticket status to "In Progress"
3. Assigns to you
4. Creates an implementation plan from the ticket description

**How to adapt for your project:**
```markdown
# In .claude/commands/jira/start.md:

## Instructions

1. Use mcp__mcp-atlassian__jira_get_issue to read ticket {$ARGUMENTS}
2. Use mcp__mcp-atlassian__jira_transition_issue to move to "In Progress"
3. Create a plan based on the ticket description
   → /flow:plan "{ticket summary}"
```

### `/jira:status` — Change ticket status

```bash
/jira:status YOUR-123
```

Shows available transitions and lets you pick one interactively.

### `/jira:pr-desc` — Auto-generate PR description from ticket

```bash
/jira:pr-desc
```

Extracts ticket key from branch name (e.g., `YOUR-123-feature-name` → YOUR-123), reads the ticket, and generates a structured PR description.

---

## PM Workflow: Story & Task Generation

This kit includes a 3-stage PM workflow for product managers. You can adapt this for any Jira setup.

### Stage 1: Generate Stories/Tasks

```bash
# From a URL (browser investigation)
/pm:gen-stories-from-url http://your-app.com/feature "Add filtering by status"

# From an image/mockup
/pm:gen-stories-from-img "Dashboard redesign" /path/to/mockup.png

# From an existing Jira story
/pm:gen-tasks-for-story YOUR-STORY-KEY
```

Output: Markdown files in `.claude/jira/`

### Stage 2: Configure for Jira

```bash
/pm:prepare .claude/jira/feature-stories.md
```

Interactive configuration:
- Project selection
- Epic linking
- Priority per item
- Labels/components
- Assignee

Output: JSON files in `.claude/jira-ready/`

### Stage 3: Push to Jira

```bash
/pm:push .claude/jira-ready/feature-2026-02-19.json
```

Creates all stories and tasks in Jira with proper hierarchy.

---

## Jira Story Template

```markdown
**DESIGN:** {figma link or "N/A"}

**USER STORY:** As a {role}, I want to {action}, so that I can {benefit}.

**SHORT DESCRIPTION:** This story requires {brief description}.

**ACCEPTANCE CRITERIA:**
• {criterion 1}
• {criterion 2}
• {criterion 3}
```

## Jira Task Template

```markdown
**SCENARIO:**
GIVEN {initial context}
WHEN {user action}
THEN {expected outcome}

**[Frontend/Backend] USER STORY:** As a {role}, I want to {action}.

**CRITERIA/DESCRIPTION:**

**{Section 1}:**
{Detailed requirements}

**[Visual Reference]:** {link or "See parent story"}
```

---

## Available MCP Tools

When the Atlassian MCP is configured, these tools are available:

| Tool | What It Does |
|------|-------------|
| `mcp__mcp-atlassian__jira_get_issue` | Read a ticket |
| `mcp__mcp-atlassian__jira_create_issue` | Create a ticket |
| `mcp__mcp-atlassian__jira_update_issue` | Update ticket fields |
| `mcp__mcp-atlassian__jira_transition_issue` | Change ticket status |
| `mcp__mcp-atlassian__jira_get_transitions` | List available transitions |
| `mcp__mcp-atlassian__jira_search` | Search tickets with JQL |
| `mcp__mcp-atlassian__jira_add_comment` | Add comment to ticket |
| `mcp__mcp-atlassian__jira_get_all_projects` | List projects |
| `mcp__mcp-atlassian__jira_get_sprints_from_board` | List sprints |

---

## Branch Auto-Detection

The `/jira:pr-desc` command extracts the ticket key from your branch name:

| Branch Name | Detected Key |
|-------------|-------------|
| `YOUR-123-add-filter` | YOUR-123 |
| `feature/YOUR-456-fix-bug` | YOUR-456 |
| `PROJ-789-description` | PROJ-789 |

Implement this with a regex:

```python
import re
branch = "YOUR-123-add-user-filter"
match = re.search(r'([A-Z]+-\d+)', branch)
if match:
    ticket_key = match.group(1)  # → "YOUR-123"
```

---

## Minimal Jira Setup

If you just want ticket reading + status updates (no PM pipeline):

1. Install Atlassian MCP
2. Create `.claude/commands/jira/start.md` with:
   - Read ticket
   - Transition to "In Progress"
   - Show ticket details
3. Create `.claude/commands/jira/pr-desc.md` with:
   - Extract key from branch
   - Read ticket
   - Generate PR description

---

**Next Step →** `guide/08-chrome-extension.md`
