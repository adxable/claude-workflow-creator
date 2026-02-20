# /pm:push - Push to Issue Tracker

Push configured stories/tasks to Jira from a prepared JSON file.

## Arguments

- `$ARGUMENTS`:
  - **config_file** - Path to prepared JSON configuration file
  - **--dry-run** (optional) - Preview what would be created without actually creating

## Usage

```bash
/pm:push .claude/jira-ready/feature-2026-01-29.json
/pm:push .claude/jira-ready/feature-2026-01-29.json --dry-run
```

## Input

Expects the JSON file created by `/pm:prepare`:

```json
{
  "version": "1.0",
  "project": { "key": "PROJ" },
  "epic": { "create": true, "summary": "..." },
  "items": [...]
}
```

## Instructions

### 1. Show Start Banner

```
═══════════════════════════════════════════════════
🚀 PM: Push to Tracker
   └─ Config: {config_file}
   └─ Mode: {Live | Dry Run}
═══════════════════════════════════════════════════
```

### 2. Read and Validate Configuration

Read `{config_file}` and validate the JSON structure. If invalid, show the error and exit.

### 3. Dry Run Mode

If `$ARGUMENTS` contains `--dry-run`:

Show a preview table of what would be created and exit without creating anything.

### 4. Create Issues in Jira

Use the jira agent:

```
Use Task tool with subagent_type: "jira", model: "sonnet"

Task: Create Jira issues from the prepared configuration.

Configuration: {config JSON}

Steps:

1. Create Epic (if config.epic.create is true)
   Use mcp__claude_ai_Atlassian__createJiraIssue with issueTypeName: "Epic"
   Store the created Epic key.

2. Create Stories
   For each item with type "story":
   - Use mcp__claude_ai_Atlassian__createJiraIssue with issueTypeName: "Story"
   - Link to Epic if created (set parent or Epic Link field)
   - Apply labels and priority from config
   - Store created key with its index

3. Create Tasks/Subtasks
   For each item with type "task":
   - Use mcp__claude_ai_Atlassian__createJiraIssue with issueTypeName: "Subtask"
     (Note: some Jira instances use "Sub-task" — check your project's issue type names)
   - Set parent to the Story key via parentIndex mapping
   - Apply labels and priority

4. Return results: epic key, story keys with indices, task keys with parent mappings

Notes:
- Use projectKey: {config.project.key}
- Add small delays between requests if hitting rate limits
```

### 5. Show Progress During Creation

```
═══════════════════════════════════════════════════
🚀 Creating Issues...
═══════════════════════════════════════════════════

[1/6] Creating Epic: {epic name}
      ✅ Created: PROJ-100

[2/6] Creating Story: {story title}
      ✅ Created: PROJ-101 → Linked to PROJ-100

[3/6] Creating Task: [Frontend] {task title}
      ✅ Created: PROJ-102 → Parent: PROJ-101

...
```

### 6. Update Configuration File

Add the created keys to the config file under a `pushed` key:

```json
{
  ...existing config...,
  "pushed": {
    "at": "{ISO timestamp}",
    "epicKey": "PROJ-100",
    "items": [
      { "index": 0, "key": "PROJ-101", "url": "https://your-jira.atlassian.net/browse/PROJ-101" },
      { "index": 1, "key": "PROJ-102", "parent": "PROJ-101" }
    ]
  }
}
```

### 7. Show Completion Banner

```
═══════════════════════════════════════════════════
✅ PUSHED TO JIRA
═══════════════════════════════════════════════════

Project: {PROJECT_KEY}

EPIC
──────────────────────────────────────────────────
{PROJ-100}: {Epic name}

STORIES & TASKS
──────────────────────────────────────────────────
{PROJ-101}: {Story title}
   └─ {PROJ-102}: [Frontend] {task title}
   └─ {PROJ-103}: [Backend] {task title}

{PROJ-104}: {Story title 2}
   └─ {PROJ-105}: [Frontend] {task title}

SUMMARY
──────────────────────────────────────────────────
Epic:     1 created
Stories:  {N} created
Tasks:    {N} created
Total:    {N} issues

Config updated: {config_file}

═══════════════════════════════════════════════════

Next step for developers:
  /jira:start {PROJ-101}

═══════════════════════════════════════════════════
```

### 8. Screenshot Attachment Reminder

If the source file had associated screenshots:

```
═══════════════════════════════════════════════════
📸 SCREENSHOTS — ATTACH MANUALLY
═══════════════════════════════════════════════════

Jira API doesn't support file uploads.

📁 Location: .claude/screenshots/{feature-slug}/before/
📎 Attach to: {PROJ-100} (the Epic)

Drag & drop files directly into the Jira ticket.

═══════════════════════════════════════════════════
```

## Error Handling

If an issue creation fails:

```
❌ Failed: {item.summary}
   Error: {message}

Options:
1. Skip this item and continue
2. Abort — progress saved to {config_file}
```

## Workflow Position

```
/pm:gen-*  →  /pm:prepare  →  /pm:push
                                  ↑
                              YOU ARE HERE
```

## Related

- **Agent**: `jira` - Creates issues via Jira MCP
- **Command**: `/jira:start PROJ-101` - Start working on a created story
