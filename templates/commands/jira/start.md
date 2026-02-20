# /jira:start - Start a Jira Ticket

Read a Jira ticket, create an implementation plan, change status to "In Progress", and assign to you.

## Arguments

- `$ARGUMENTS` - Jira ticket key (e.g., PROJ-123)

## Prerequisites

- Atlassian MCP configured (see `guide/07-jira-integration.md`)
- `mcp-atlassian` server enabled in settings.json

## Instructions

### 1. Show Start Banner

```
═══════════════════════════════════════════════════
🎫 Starting Jira Ticket: {$ARGUMENTS}
═══════════════════════════════════════════════════
```

### 2. Initialize Jira Connection

1. Get accessible Atlassian resources (cloudId) via `mcp__mcp-atlassian__jira_get_issue`
2. Note your account ID for assignment

### 3. Read Ticket Details

Fetch the ticket and extract:
- Summary, description, acceptance criteria
- Current status and assignee

Display:
```
📋 Ticket: {key}
📝 Summary: {summary}
👤 Assignee: {current_assignee or "Unassigned"}
📊 Status: {current_status}
```

### 4. Check for Missing Context

If description is vague or missing acceptance criteria:
- Use `AskUserQuestion` to clarify requirements
- Ask about expected behavior and edge cases

### 5. Update Ticket Status

If status is NOT already "In Progress":

1. Get available transitions via `mcp__mcp-atlassian__jira_get_transitions`
2. Find transition to "In Progress" (or similar: "Start Progress", "Begin Work")
3. Execute transition via `mcp__mcp-atlassian__jira_transition_issue`

```
[jira] Transitioning: {old_status} → In Progress
```

### 6. Assign Ticket

If not already assigned to current user:
- Update assignee via `mcp__mcp-atlassian__jira_update_issue`

```
[jira] Assigning to: {your_name}
```

### 7. Create Implementation Plan

Invoke the `planner` agent:
- Ticket summary as the task description
- Full ticket description as context
- Acceptance criteria as validation requirements

Plan file: `.claude/plans/{ticket_key}-{slug}.md`

### 8. Create Git Branch (Optional)

If not already on a ticket branch, suggest:
```bash
git checkout -b {ticket_key}-{slug}
```

### 9. Show Completion Banner

```
═══════════════════════════════════════════════════
           ✅ TICKET STARTED SUCCESSFULLY
═══════════════════════════════════════════════════

🎫 Ticket: {key} - {summary}
📊 Status: In Progress
👤 Assigned: {your_name}
📄 Plan: {plan_file_path}

═══════════════════════════════════════════════════
              SUGGESTED NEXT STEPS
═══════════════════════════════════════════════════

1. Review the plan
2. Start implementation:

   /flow:implement {plan_file_path}

═══════════════════════════════════════════════════
```

## Workflow Position

```
/jira:start → /flow:implement → /flow:verify → /jira:pr-desc → /flow:pr
    ↑
YOU ARE HERE
```

## Related

- **Agent**: `jira` - Jira operations (reads/writes tickets)
- **Command**: `/jira:pr-desc` - Generate PR description from ticket
- **Command**: `/flow:implement` - Execute the generated plan
