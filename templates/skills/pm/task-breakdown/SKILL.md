---
name: pm-task-breakdown
description: Patterns for breaking down user stories into PR-ready developer tasks with balanced scope and minimal dependencies.
---

# PM Skill: Developer Task Breakdown

Patterns for breaking down user stories into actionable developer tasks.

## Task Breakdown Philosophy

### Goals
1. **PR-Ready Scope** - Each task = one meaningful PR
2. **Complete Features** - Task delivers working functionality, not fragments
3. **Reviewable Size** - Can be reviewed in one sitting (max ~500 lines changed)
4. **Includes Tests** - Testing is part of the task, not separate

### Story vs Task Sizing

**The Golden Rule:** A well-scoped story should produce **2-4 tasks**.

| If Story Has | Problem | Solution |
|--------------|---------|----------|
| **1 task** | Story too small | Combine with related stories into larger feature |
| **2-4 tasks** | ✅ Good balance | Keep as-is |
| **5+ tasks** | Story too big | Split into multiple stories |

### Story Sizing Guidelines

| Story Size | Tasks | Typical Scope |
|------------|-------|---------------|
| **S** | Should be combined | Single component/endpoint - too small for story |
| **M** | 2-3 tasks | Feature area (e.g., "List Page with Filters") |
| **L** | 3-4 tasks | Major feature (e.g., "Complete CRUD Module") |
| **XL** | Split story | Epic-level work |

### When to Combine Stories

Combine small stories if they:
- Are on the same page/module
- Share common components
- Would each only have 1 task
- Are naturally implemented together

**Example - Before (too granular):**
```
Story 1: Summary Cards (1 task)
Story 2: Data Grid with Sorting (1 task)
Story 3: Search Functionality (1 task)
Story 4: Grid Utilities (1 task)
```

**Example - After (balanced):**
```
Story: Orders List View
  Task 1: [Frontend] Summary cards + grid layout
  Task 2: [Frontend] Search and grid utilities (group, density, export)
  Task 3: [Testing] E2E tests for list interactions
```

### Task Granularity

**Too Big (hard to review, risky):**
```
Implement entire Orders module
```

**Too Small (too many PRs, fragmented):**
```
Create SummaryCard component
Create SummaryCardRow component
Add click handler
Add tests
Integrate with page
```

**Just Right (complete feature, single PR):**
```
Implement Order Status Summary Cards with filtering
- Create SummaryCard and SummaryCardRow components
- Implement click-to-filter behavior
- Integrate with page and filter state
- Include unit tests
```

### Anti-Patterns to Avoid

❌ **Separate task for tests** - Tests should be included with the feature
❌ **One component = one task** - Group related components together
❌ **Splitting by file** - Split by feature/functionality instead
❌ **Too many dependencies** - If task 5 depends on 1,2,3,4 → consolidate

## Standard Task Templates (Balanced Scope)

### Frontend Feature Task (Recommended)

A complete frontend feature in a single task:

```markdown
**SCENARIO:**
GIVEN [user context]
WHEN [user action]
THEN [expected outcome with full functionality]

**[Frontend] USER STORY:** As a [role], I want to [complete feature], so that [benefit].

**CRITERIA/DESCRIPTION:**

**Components to Create:**
• [Component1] - [brief description]
• [Component2] - [brief description]

**Behavior:**
• [Interaction 1]
• [Interaction 2]
• [State management approach]

**Integration:**
• [How it connects to page/app]
• [API hooks needed]
• [URL/state sync if applicable]

**Testing:**
• Unit tests for components
• [Specific test scenarios]

**Files:** [comma-separated list of files to create/modify]
```

### Backend Feature Task (Recommended)

A complete backend feature in a single task:

```markdown
**SCENARIO:**
GIVEN [API context]
WHEN [API is called with parameters]
THEN [complete response with all features]

**[Backend] USER STORY:** As a developer, I need [API capability], so that [frontend/system benefit].

**CRITERIA/DESCRIPTION:**

**Endpoint:** [HTTP method] [route]

**Features:**
• [Feature 1 - filtering/sorting/etc]
• [Feature 2]
• [Validation rules]

**Request/Response:**
• Input parameters and types
• Response structure

**Implementation:**
• Service layer changes
• Repository changes (if needed)
• Unit tests included

**Files:** [comma-separated list]
```

### Fullstack Feature Task

When FE and BE are tightly coupled and small enough for one PR:

```markdown
**SCENARIO:**
GIVEN [user context]
WHEN [user performs action]
THEN [end-to-end feature works]

**[Fullstack] USER STORY:** As a [role], I want to [feature], so that [benefit].

**CRITERIA/DESCRIPTION:**

**Backend:**
• API endpoint and logic
• Unit tests

**Frontend:**
• Components and integration
• Unit tests

**E2E:**
• Happy path test

**Files:** [BE files], [FE files], [test files]
```

## Task Dependencies (Keep Minimal)

### Ideal: No Dependencies
Most tasks should be independent. If you have many dependencies, consolidate tasks.

**Bad (too many deps):**
```
Task 5 depends on: Task 1, 2, 3, 4
```

**Good (minimal deps):**
```
Task 1: [Frontend] Complete feature (no deps)
Task 2: [Backend] API support (no deps, can parallel)
```

### When to Split (FE/BE boundary)

Only split when:
- Backend work is substantial (>1 day)
- Different developers will work on FE/BE
- API needs to be deployed before FE can test

### Dependency Notation

```
**Depends On:** PROJ-XXX (brief reason)
```

## Estimation Guidelines (Feature-Based)

### Feature Estimates (Recommended)

| Feature Scope | Time | Example |
|---------------|------|---------|
| Simple feature | 0.5-1d | Search input, single filter |
| Standard feature | 1-2d | Filter panel, data grid |
| Complex feature | 2-3d | Calendar view, complex form |
| Major feature | 3-5d | Consider splitting story |

### Don't Estimate by Component

❌ **Bad:** "SummaryCard = 3h, SummaryCardRow = 2h, tests = 2h"
✅ **Good:** "Order Status Summary Cards feature = 1 day"

## Task Naming Conventions

### Format
```
[{Type}] {Feature name} {brief scope}
```

### Good Examples (Feature-Focused)
```
[Frontend] Implement Order Status Summary Cards with filtering
[Frontend] Products Filter Panel with category/status/date filters
[Backend] Orders API with filtering, sorting, and pagination
[Fullstack] Export functionality with Excel/CSV support
```

### Bad Examples (Too Granular)
```
❌ [Frontend] Create SummaryCard component
❌ [Frontend] Add click handler to SummaryCard
❌ [Testing] Unit tests for SummaryCard
```

## Common Patterns by Feature Type (Balanced)

### Filter Feature (1-2 tasks)

**Option A: Single fullstack task (small filter)**
```
[Fullstack] Add category filter to Products list
- Backend: filter parameter + service logic
- Frontend: filter dropdown + grid integration
- Tests: unit + basic E2E
```

**Option B: Split FE/BE (complex filter)**
```
[Backend] Orders filtering API (status, date range, customer, amount)
[Frontend] Orders Filter Panel with all filter controls
```

### CRUD Feature (1-2 tasks)

```
[Backend] {Entity} CRUD API with validation
- All endpoints (GET, POST, PUT, DELETE)
- Service layer logic
- Unit tests

[Frontend] {Entity} management page
- List grid with actions
- Create/Edit form modal
- Delete confirmation
- E2E tests
```

### List Page Feature (1-3 tasks)

```
[Frontend] {Entity} List Page - grid, filters, search
[Frontend] {Entity} List Page - calendar view (if complex)
[Backend] {Entity} API with filtering and aggregations
```

## Related

- **Command**: `/flow:plan` - Create implementation plan
- **Command**: `/flow:implement` - Execute tasks
- **Skill**: `pm/story-writing` - Story patterns
