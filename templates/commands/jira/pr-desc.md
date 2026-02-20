# /jira:pr-desc - Generate PR Description from Jira Ticket

Generate PR title and description from current branch's Jira ticket, then optionally change status to "In Review".

## Arguments

- `$ARGUMENTS` - Optional ticket key (auto-detected from branch name if not provided)

## Instructions

### 1. Show Start Banner

```
═══════════════════════════════════════════════════
📝 Generating PR Description
═══════════════════════════════════════════════════
```

### 2. Extract Ticket Key

If no argument provided:
1. Get current branch: `git branch --show-current`
2. Extract ticket key with regex: `([A-Z]+-\d+)`

Supported branch patterns:
- `PROJ-123-feature-name` → PROJ-123
- `feature/PROJ-456-fix-bug` → PROJ-456
- `PROJ-789-description` → PROJ-789

```
[jira] Detected ticket: {ticket_key} from branch: {branch_name}
```

### 3. Read Ticket

Fetch via `mcp__mcp-atlassian__jira_get_issue`:
- Extract summary, description, acceptance criteria

### 4. Analyze Changes

```bash
git log main..HEAD --oneline
git diff main --stat
```

### 5. Generate PR Title & Description

**Title:** `{ticket_key}: {concise summary}`

**Description:**
```markdown
## Summary

{Brief description derived from ticket + actual changes}

## Jira Ticket

[{ticket_key}]({jira_url}) - {ticket_summary}

## Changes

{Bullet list of key changes from git diff}

## Testing

{How to test, derived from acceptance criteria}

## Checklist

- [ ] {YOUR_TYPE_CHECK_COMMAND}
- [ ] {YOUR_LINT_COMMAND}
- [ ] {YOUR_BUILD_COMMAND}
- [ ] Tested locally
```

### 6. Display Generated Content

```
═══════════════════════════════════════════════════
              📋 GENERATED PR CONTENT
═══════════════════════════════════════════════════

TITLE:
{pr_title}

DESCRIPTION:
{pr_description}

═══════════════════════════════════════════════════
```

### 7. Confirm Status Change

Use `AskUserQuestion`:
```
Should I change ticket status to "In Review"?
- Yes, change status
- No, keep current status
```

### 8. Update Ticket Status (if confirmed)

1. Get transitions via `mcp__mcp-atlassian__jira_get_transitions`
2. Find "In Review" or "Ready for Review" transition
3. Execute via `mcp__mcp-atlassian__jira_transition_issue`

### 9. Show Completion Banner

```
═══════════════════════════════════════════════════
          ✅ PR DESCRIPTION GENERATED
═══════════════════════════════════════════════════

🎫 Ticket: {ticket_key}
📊 Status: In Review

NEXT: Copy the description and create PR with /flow:pr
═══════════════════════════════════════════════════
```

## Customization

Update the description template to match your team's PR format:
- Add required checklist items
- Include your verification commands
- Add design/spec links if needed

## Workflow Position

```
/jira:start → /flow:implement → /flow:verify → /jira:pr-desc → /flow:pr
                                                   ↑
                                              YOU ARE HERE
```

## Related

- **Command**: `/jira:start` - Start working on a ticket
- **Command**: `/flow:pr` - Create the actual PR after this
