---
name: pm-jira-templates
description: Jira story and task templates with GIVEN-WHEN-THEN acceptance criteria patterns, MCP tool invocation examples, and label/priority conventions.
---

# PM Skill: Jira Templates

> **This is the generic fallback template.** For best results, re-run `/setup:init` → Phase 7 and
> provide real ticket examples — Claude will read them and generate a version adapted to your
> team's actual section names, acceptance criteria style, and formatting conventions.
>
> **Manual setup:** Replace `{PROJECT_KEY}`, `{CLOUD_ID}`, and `{SUBTASK_TYPE}` with your values.
> Find your Cloud ID at: Jira Settings → Products → API information

## Project Configuration

| Field | Value |
|-------|-------|
| **Project Key** | `{PROJECT_KEY}` |
| **Cloud ID** | `{CLOUD_ID}` |
| **Issue Types** | Story, `{SUBTASK_TYPE}` (Subtask), Task, Bug |

---

## STORY Template

Stories represent user-facing features. They should be high-level and focus on user value.

### Required Sections

1. **Link to Design** - Figma/mockup link (required)
2. **User Story** - "As a [role], I need [feature] so that I can [benefit]"
3. **Description** - Detailed explanation of the view/feature and its structure
4. **Important** - Key responsibilities and critical business rules (use `!!` for constraints)
5. **Acceptance Criteria** - Dash-list of what "done" looks like

### Template

```markdown
**LINK TO DESIGN:**
[Paste Figma/design link here or "N/A"]
---
**USER STORY:**
As a [user role], I need [functionality/feature] so that I can [benefit/value].

**DESCRIPTION:**
The [view/feature name] provides a complete interface for [purpose]. The view consists of [high-level structure description].

**IMPORTANT:**
This [view/feature] is responsible for [key responsibility].
!! [Critical business rule or constraint]
[Additional important notes]

**ACCEPTANCE CRITERIA:**
- [Criterion 1 - user-visible outcome]
- [Criterion 2 - user-visible outcome]
- [Criterion 3 - user-visible outcome]
- [Criterion 4 - user-visible outcome]
```

### Example

```markdown
**LINK TO DESIGN:**
https://www.figma.com/design/xxxxx
---
**USER STORY:**
As a user, I need a comprehensive Edit Component view for managing all aspects of a component instance, so that I can view and maintain component information, associated items, and attachments in a centralised interface.

**DESCRIPTION:**
The Edit Component view provides a complete interface for managing a component instance. The view consists of a header section displaying the component identity and status, a toolbar with available actions, and a tabbed interface for accessing different aspects of the component data.

**IMPORTANT:**
This editing view is responsible for updating the instances of components from the Component Library.
!! This view must enforce specific business rules regarding which fields are mandatory and which remain read-only once a component is created.

**ACCEPTANCE CRITERIA:**
- The Edit Component view shall display the component header with name, status, type.
- The toolbar shall provide Save, Save & Close, Delete, and Share actions.
- The tabbed interface shall include Summary and Detail tabs.
- The Summary tab shall be the default active tab upon entering the Edit Component view.
- All sections within the Summary tab shall be collapsible/expandable.
```

---

## TASK (Subtask) Template

Tasks are developer-facing implementation units. They should be specific and actionable.

### Required Sections

1. **Link to Design** - Figma/mockup link (required)
2. **Description** - What needs to be implemented and in what context
3. **Acceptance Criteria** - Detailed criteria with embedded SCENARIOs where applicable
4. **Screens** - Reference to mockups/screenshots

### Template

```markdown
**LINK TO DESIGN:**
[Paste Figma/design link here or "See parent story"]
---
**DESCRIPTION:**
This view requires [implementing/creating] the [feature/component name] within the [parent view/context], [brief description of functionality and states].

**ACCEPTANCE CRITERIA:**
- [Criterion with specific UI/UX detail]
- [Criterion with specific UI/UX detail]
  - SCENARIO:
    GIVEN [precondition]
    WHEN [action]
    THEN [expected result]
- [Criterion for empty/alternative state]
  - SCENARIO:
    GIVEN [precondition]
    WHEN [action]
    THEN [expected result]
- [Additional criterion]

**SCREENS:**
[Attach relevant screenshots/mockups]
```

### Example

```markdown
**LINK TO DESIGN:**
https://www.figma.com/design/xxxxx
---
**DESCRIPTION:**
This view requires implementing the Items tab within the Component Edit view, displaying a list of assigned items when available, or showing guidance for adding new items when the list is empty.

**ACCEPTANCE CRITERIA:**
- When the user navigates to the Items tab, the system displays "Assigned Items" as the section title
- If items are assigned, a data grid displays the list with relevant columns
- If items are assigned, a data grid displays the total number of assigned items
  - SCENARIO:
    GIVEN I am viewing a component in Edit mode
    WHEN I click on the "Items" tab
    THEN I see a data grid showing all assigned items with relevant columns
- If no items are assigned, an empty state message is shown: "No items assigned to this component"
- An "+ Add Item" button is always visible in the top right header area
  - SCENARIO:
    GIVEN I am viewing a component with no assigned items
    WHEN I click on the "Items" tab
    THEN I see an empty state with guidance to add the first item
- The user can add, edit, or remove items from the component

**SCREENS:**
[Attach relevant screenshots/mockups]
```

---

## Task Template - Backend

For backend/API tasks, adapt the template with technical details:

```markdown
**LINK TO DESIGN:**
[API documentation link or "N/A"]
---
**DESCRIPTION:**
This task requires implementing [API/service capability] to support [feature/functionality]. The endpoint will [brief description of purpose].

**ACCEPTANCE CRITERIA:**
- The API endpoint [HTTP method] [route] shall be available
  - SCENARIO:
    GIVEN [API context]
    WHEN [API call/action]
    THEN [expected response/behavior]
- Request parameters shall include: [parameter list]
- Response shall include: [field list]
- Validation shall enforce: [validation rules]
- Error handling shall return appropriate status codes:
  - [Error case 1]: [HTTP status + response]
  - [Error case 2]: [HTTP status + response]

**SCREENS:**
N/A (Backend task)
```

---

## Quick Reference: Section Headers

### For Stories
- `**LINK TO DESIGN:**` (followed by `---` separator)
- `**USER STORY:**`
- `**DESCRIPTION:**`
- `**IMPORTANT:**` (with `!!` for critical constraints)
- `**ACCEPTANCE CRITERIA:**`

### For Tasks
- `**LINK TO DESIGN:**` (followed by `---` separator)
- `**DESCRIPTION:**`
- `**ACCEPTANCE CRITERIA:**` (with nested `SCENARIO:` blocks)
- `**SCREENS:**`

---

## Labels

| Label | Use When |
|-------|----------|
| `frontend` | React/UI implementation |
| `backend` | API/service implementation |
| `database` | Schema changes |
| `bug` | Defect fix |
| `critical` | High priority |

## Priority

| Priority | When to Use |
|----------|-------------|
| **Highest** | Blocking other work, critical path |
| **High** | Important for current sprint |
| **Medium** | Standard priority |
| **Low** | Can wait, nice-to-have |
| **Lowest** | Backlog, future consideration |

---

## Creating Issues via MCP

### Create Story

```typescript
mcp__mcp-atlassian__jira_create_issue({
  cloudId: "{CLOUD_ID}",
  projectKey: "{PROJECT_KEY}",
  issueTypeName: "Story",
  summary: "[Module] - Feature Name",
  description: `**LINK TO DESIGN:**
[link]
---
**USER STORY:**
As a [role], I need [feature] so that I can [benefit].

**DESCRIPTION:**
The [view] provides [purpose]. The view consists of [structure].

**IMPORTANT:**
This [view] is responsible for [responsibility].
!! [Critical constraint]

**ACCEPTANCE CRITERIA:**
- Criterion 1
- Criterion 2
- Criterion 3`
})
```

### Create Subtask

```typescript
mcp__mcp-atlassian__jira_create_issue({
  cloudId: "{CLOUD_ID}",
  projectKey: "{PROJECT_KEY}",
  issueTypeName: "{SUBTASK_TYPE}",
  summary: "[Frontend/Backend] Task Name",
  description: `**LINK TO DESIGN:**
[link or "See parent story"]
---
**DESCRIPTION:**
This view requires implementing [feature] within [context], [description].

**ACCEPTANCE CRITERIA:**
- Criterion with detail
  - SCENARIO:
    GIVEN [precondition]
    WHEN [action]
    THEN [result]
- Additional criterion

**SCREENS:**
[Attach mockups]`,
  parent: "{PROJECT_KEY}-XX"  // Parent story key
})
```

---

## Related

- **Command**: `/pm:gen-stories-from-url` - Generate stories from URL
- **Command**: `/pm:gen-tasks-for-story` - Generate tasks for a story
- **Command**: `/pm:push` - Push to Jira
- **Skill**: `pm/story-writing` - Story writing patterns
- **Skill**: `pm/task-breakdown` - Task breakdown guidelines
