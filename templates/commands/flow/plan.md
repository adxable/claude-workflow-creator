# /flow:plan - Context-Aware Planning

Research the codebase and create an implementation plan for the given task.

## Arguments

- `$ARGUMENTS` - Feature/task description with optional context override

## Usage

```bash
/flow:plan "Add user authentication"
/flow:plan [frontend] "Add filter to the orders page"
/flow:plan [backend] "Add export endpoint for reports"
```

## Instructions

### 1. Show Start Banner

```
═══════════════════════════════════════════════════
📋 Starting Plan
   └─ Task: {$ARGUMENTS}
   └─ Detecting context...
═══════════════════════════════════════════════════
```

### 2. Detect Context

**Priority order:**
1. Manual override: `[frontend]` or `[backend]` in description
2. Auto-detect from description keywords
3. Ask user if ambiguous

| Indicators | Context |
|------------|---------|
| {YOUR_FRONTEND_KEYWORDS} | **Frontend** |
| {YOUR_BACKEND_KEYWORDS} | **Backend** |
| Unclear | **Ask user** |

If context cannot be determined:
```
Is this a frontend or backend task?
- Frontend ({YOUR_FRONTEND_TECH})
- Backend ({YOUR_BACKEND_TECH})
```

### 3. Invoke Planner Agent

**If Frontend:**
```
Use Task tool with subagent_type: "planner-fe", model: "opus"

Task: Research the codebase and create an implementation plan for: {description}

Search in {YOUR_FRONTEND_DIR}/:
- Similar components: {YOUR_COMPONENT_GLOB}
- API patterns: {YOUR_API_GLOB}
- Hooks: {YOUR_HOOKS_GLOB}

Create plan at: .claude/plans/fe/{type}-{name}.md
```

**If Backend:**
```
Use Task tool with subagent_type: "planner-be", model: "opus"

Task: Research the codebase and create an implementation plan for: {description}

Search in {YOUR_BACKEND_DIR}/:
- Similar services: {YOUR_SERVICE_GLOB}
- Controllers: {YOUR_CONTROLLER_GLOB}
- Models: {YOUR_MODEL_GLOB}

Create plan at: .claude/plans/be/{type}-{name}.md
```

### 4. Show Completion Banner

```
═══════════════════════════════════════════════════
        📋 PLAN COMPLETE
═══════════════════════════════════════════════════

Context:  {Frontend | Backend}
Plan:     .claude/plans/{context}/{name}.md
Research: Found {N} similar patterns

═══════════════════════════════════════════════════
              NEXT STEPS
═══════════════════════════════════════════════════

1. IMPLEMENT: /flow:implement {plan-path}
2. Or review plan first and modify if needed

═══════════════════════════════════════════════════
```

## Plan Template

```markdown
# Plan: {Title}

## Metadata

**Type:** {Feature | Bug | Patch | Refactor | Chore}
**Context:** {Frontend | Backend}
**Created:** {YYYY-MM-DD}
**Status:** Draft

## Goal

{What we're trying to achieve}

## Research Findings

- Similar patterns found at: {locations}
- Architecture observations
- Files to reference

## Approach

{High-level approach}

## Implementation Steps

### Step 1: {Action}
- {Detail}

### Step 2: {Action}
- {Detail}

## Relevant Files

| File | Action | Purpose |
|------|--------|---------|
| {path} | Create/Modify | {why} |

## Verification

- [ ] {YOUR_TYPECHECK_COMMAND}
- [ ] {YOUR_LINT_COMMAND}
- [ ] {YOUR_BUILD_COMMAND}

## Acceptance Criteria

- [ ] {criterion}
```

## Workflow Position

```
/flow:plan → /flow:implement → /flow:review → /flow:verify → /flow:commit → /flow:pr
    ↑
YOU ARE HERE
```
