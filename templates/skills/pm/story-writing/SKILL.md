---
name: pm-story-writing
description: Best practices for writing user stories with INVEST criteria, sizing guidelines, splitting strategies, and module-specific patterns for shipping software teams.
---

# PM Skill: User Story Writing

Best practices and patterns for writing effective user stories.

## User Story Format

### Standard Template

```
As a [user role]
I want to [action/feature]
So that [benefit/value]
```

### Examples

**Good:**
```
As a fleet operator
I want to filter shipments by status
So that I can quickly find relevant items for my team
```

**Better (with context):**
```
As a fleet operator managing multiple vessel types
I want to filter the shipments list by status (Active, Pending, Completed)
So that I can focus on relevant items without scrolling through hundreds of entries
```

## Acceptance Criteria Patterns

### GIVEN-WHEN-THEN Format

```
GIVEN I am on the shipments list page
WHEN I select "Active" from the status filter
THEN only active shipments are displayed
AND the filter selection is visually indicated
AND the results count updates to show filtered count
```

### Checklist Format

```
Acceptance Criteria:
- [ ] Status dropdown appears in filter bar
- [ ] Dropdown contains all relevant status values
- [ ] Selecting a status filters the grid immediately
- [ ] "All" option clears the filter
- [ ] Filter state persists on page refresh
- [ ] Filter works in combination with other filters
```

## Story Sizing Guidelines

### Size Definitions

| Size | Story Points | Time | Characteristics |
|------|--------------|------|-----------------|
| **S** | 1-3 | 0-3 days | Single component, simple logic |
| **M** | 5 | 4-6 days | Multiple components, moderate logic |
| **L** | 8 | 7-13 days | Feature + API, complex logic |
| **XL** | 13+ | 2+ weeks | Major feature, needs splitting |

### Story Sizing Rules

**Golden Rule:** A story should produce **2-4 developer tasks**.

| Story Tasks | Assessment | Action |
|-------------|------------|--------|
| 1 task | Too small | Combine with related stories |
| 2-4 tasks | ✅ Ideal | Keep as-is |
| 5+ tasks | Too big | Split into multiple stories |

### When to Combine Stories

Combine if:
- Stories are on same page/screen
- Each story would only have 1 task
- Stories share common components
- Stories are naturally implemented together

**Example - Too Granular:**
```
❌ Story: Add search input
❌ Story: Add filter dropdown
❌ Story: Add export button
```

**Example - Better:**
```
✅ Story: List view search and export functionality
   - Search input with debounced filtering
   - Export to Excel/CSV
   - All grid utilities
```

### When to Split Stories

Split if:
- Estimate > 8 points (XXL)
- Would produce 5+ tasks
- Multiple distinct user workflows
- Both FE and BE are substantial (>2 days each)
- Different teams would work on parts

### Splitting Strategies

1. **By Page/View** (preferred)
   - "Jobs List View" + "Jobs Calendar View"

2. **By Layer** (when significant work both sides)
   - "Jobs API" + "Jobs UI"

3. **By User Workflow**
   - "View and filter items" + "Initiate action on item"

## Story Quality Checklist

### INVEST Criteria

- [ ] **I**ndependent - Can be developed separately
- [ ] **N**egotiable - Details open for discussion
- [ ] **V**aluable - Delivers user value
- [ ] **E**stimable - Team can estimate effort
- [ ] **S**mall - Fits in a sprint (< 8 points)
- [ ] **T**estable - Has clear acceptance criteria

### Anti-Patterns to Avoid

❌ **Technical Stories**
```
As a developer, I want to refactor the API...
```
→ Technical tasks belong in subtasks, not stories

❌ **Vague Criteria**
```
- [ ] Works correctly
- [ ] Good performance
```
→ Be specific and measurable

❌ **Solution in Story**
```
I want a dropdown with React Select...
```
→ Describe the need, not the implementation

❌ **Multiple Features**
```
I want to filter, sort, and export items...
```
→ Split into separate stories

## Module-Aware Stories

Always identify the application module in the story title:

```
[{MODULE}] As a {role}, I want to {feature}...
```

Example:
```
[Orders] As a warehouse manager, I want to filter orders by status...
[Auth] As a user, I want to reset my password by email...
```

### Label Conventions

| Label | Use Case |
|-------|----------|
| `{module-name}` | Module identifier (e.g., `orders`, `auth`, `inventory`) |
| `frontend` | React/UI work |
| `backend` | API/service work |
| `database` | Schema changes |
| `bug` | Defect fix |
| `enhancement` | Improvement |
| `new-feature` | New capability |

### Priority Guidelines

| Priority | Criteria |
|----------|----------|
| **Critical** | Blocks release, data loss risk, security |
| **High** | Core functionality, committed features |
| **Medium** | Important but not blocking |
| **Low** | Nice-to-have, future consideration |

## Templates for Common Story Types

### Filter Feature

```
As a [module] user
I want to filter the [entity] list by [field]
So that I can quickly find specific [entities]

Acceptance Criteria:
- [ ] Filter control appears in filter bar
- [ ] Filter options come from [source]
- [ ] Filter applies immediately on selection
- [ ] Filter works with other filters
- [ ] Filter state persists in URL
- [ ] "Clear" removes filter
```

### Export Feature

```
As a [module] user
I want to export [entity] data to [format]
So that I can [use case]

Acceptance Criteria:
- [ ] Export button visible in toolbar
- [ ] Export includes currently filtered data
- [ ] Export format is [Excel/PDF/CSV]
- [ ] Column order matches grid
- [ ] Large datasets handled (pagination/streaming)
- [ ] Download starts within [X] seconds
```

### Edit Form

```
As a [module] user
I want to edit [entity] details
So that I can update information

Acceptance Criteria:
- [ ] Edit form opens from grid row
- [ ] All editable fields are present
- [ ] Validation shows inline errors
- [ ] Save updates the record
- [ ] Cancel discards changes
- [ ] Grid refreshes after save
```

## Related

- **Skill**: `pm/task-breakdown` - Task breakdown patterns
- **Skill**: `pm/estimation` - Sizing and estimation
- **Skill**: `pm/jira-templates` - Tracker issue templates
