# /pm:prepare - Configure Tracker Fields

Interactive configuration of issue tracker fields for stories/tasks before pushing.

## Arguments

- `$ARGUMENTS`:
  - **input_file** - Path to stories or tasks markdown file

## Usage

```bash
/pm:prepare .claude/jira/feature-stories.md
/pm:prepare .claude/jira/PROJ-123-tasks.md
```

## Output

Creates: `.claude/jira-ready/{name}-{timestamp}.json`

## Instructions

### 1. Show Start Banner

```
═══════════════════════════════════════════════════
⚙️ PM: Prepare for Tracker
   └─ Input: {input_file}
   └─ Mode: Interactive Configuration
═══════════════════════════════════════════════════
```

### 2. Create Output Directory

```bash
mkdir -p .claude/jira-ready
```

### 3. Read Input File

Parse the input file to extract all stories/tasks and their metadata sections.

### 4. Get Available Projects (Jira)

If Jira MCP is available:

```
Use Task tool with subagent_type: "jira", model: "haiku"

Task: List available Jira projects.

Steps:
1. Use mcp__claude_ai_Atlassian__getVisibleJiraProjects
2. Return project keys and names
```

Otherwise, ask the user for the project key.

### 5. Interactive Configuration

#### Step 5.1: Project Selection

```
AskUserQuestion:
  question: "Which project should these be created in?"
  header: "Project"
  options: (use fetched projects or ask for custom key)
```

#### Step 5.2: Epic Configuration

```
AskUserQuestion:
  question: "Do you want to create or link to an Epic?"
  header: "Epic"
  options:
    - "Create new Epic"
    - "Link to existing Epic (enter key)"
    - "No Epic"
```

#### Step 5.3: Priority (per item or batch)

For each item (or batch if many):

```
AskUserQuestion:
  question: "Set priority for: {item.summary}"
  header: "Priority"
  options:
    - "Highest"
    - "High"
    - "Medium (Recommended)"
    - "Low"
```

#### Step 5.4: Labels (per item)

```
AskUserQuestion:
  question: "Labels for: {item.summary}"
  header: "Labels"
  multiSelect: true
  options: (derive from item metadata + common project labels)
```

#### Step 5.5: Estimation

```
AskUserQuestion:
  question: "Size estimate for: {item.summary}"
  header: "Size"
  options:
    - "S (0.5–1 day)"
    - "M (1–2.5 days)"
    - "L (3–5 days)"
    - "XL (5+ days)"
```

### 6. Build Configuration JSON

```json
{
  "version": "1.0",
  "createdAt": "{ISO timestamp}",
  "source": "{input_file}",
  "project": {
    "key": "{PROJECT_KEY}",
    "name": "{Project Name}"
  },
  "epic": {
    "create": true,
    "summary": "{Epic name}",
    "description": "{Generated description}"
  },
  "items": [
    {
      "type": "story",
      "summary": "{title}",
      "description": "{full formatted description}",
      "priority": "Medium",
      "labels": ["frontend", "backend"],
      "estimation": "M",
      "assignee": null
    },
    {
      "type": "task",
      "parentIndex": 0,
      "summary": "[Frontend] {task title}",
      "description": "{full formatted description}",
      "priority": "Medium",
      "labels": ["frontend"],
      "estimation": "S"
    }
  ]
}
```

### 7. Preview and Confirm

Show a summary table before saving:

```
═══════════════════════════════════════════════════
📋 Configuration Preview
═══════════════════════════════════════════════════

Project: {PROJECT_KEY} — {Project Name}
Epic: "{Epic name}" (to be created)

Items to create:
┌────┬────────┬──────────────────────┬──────────┬──────────┐
│ #  │ Type   │ Summary              │ Priority │ Labels   │
├────┼────────┼──────────────────────┼──────────┼──────────┤
│ 1  │ Story  │ {summary}            │ High     │ frontend │
│ 2  │ Task   │ [Frontend] {summary} │ Medium   │ frontend │
└────┴────────┴──────────────────────┴──────────┴──────────┘

═══════════════════════════════════════════════════
```

```
AskUserQuestion:
  question: "Save this configuration?"
  header: "Confirm"
  options:
    - "Save and continue"
    - "Modify"
    - "Cancel"
```

### 8. Save Configuration

Write to `.claude/jira-ready/{name}-{YYYY-MM-DD}.json`

### 9. Show Completion Banner

```
═══════════════════════════════════════════════════
✅ Configuration Saved
   └─ Output: .claude/jira-ready/{name}-{timestamp}.json
   └─ Project: {project.key}
   └─ Items: {N} ({stories} stories, {tasks} tasks)
═══════════════════════════════════════════════════

Next Step:
  /pm:push .claude/jira-ready/{name}-{timestamp}.json

═══════════════════════════════════════════════════
```

## Batch Mode

For large item sets, offer:

```
AskUserQuestion:
  question: "Configure items individually or apply defaults to all?"
  header: "Mode"
  options:
    - "Batch (Recommended) — apply same settings, customize priority only"
    - "Individual — configure each item separately"
```

## Workflow Position

```
/pm:gen-*  →  /pm:prepare  →  /pm:push
                  ↑
              YOU ARE HERE
```
