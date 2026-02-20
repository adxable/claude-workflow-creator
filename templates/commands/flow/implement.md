# /flow:implement - Context-Aware Implementation

Execute a plan file step by step with context-aware tooling and validation.

## Arguments

- `$ARGUMENTS` - Path to plan file OR task description with context override

## Usage

```bash
/flow:implement .claude/plans/fe/feature-auth.md
/flow:implement .claude/plans/be/feature-api.md
/flow:implement [frontend] "Quick fix for button style"
/flow:implement [backend] "Add validation to service"
```

## Instructions

### 1. Show Start Banner

```
═══════════════════════════════════════════════════
🚀 Starting Implementation
   └─ Plan: {$ARGUMENTS}
   └─ Detecting context...
═══════════════════════════════════════════════════
```

### 2. Detect Context

**Priority order:**
1. From plan file: Read `**Context:**` field in plan metadata
2. Manual override: `[frontend]` or `[backend]` in arguments
3. From file path: `plans/fe/` or `plans/be/`
4. Ask user if unclear

### 3. Invoke Implementer Agent

**If Frontend:**
```
Use Task tool with subagent_type: "implementer-fe", model: "sonnet"

Task: Execute the implementation plan step by step.
Plan: {plan file path}

Working directory: {YOUR_FRONTEND_DIR}/

Key patterns to follow:
- {YOUR_COMPONENT_PATTERN}
- {YOUR_NAMING_CONVENTIONS}
- {YOUR_CODE_STYLE_RULES}

After each file change, verify:
  {YOUR_TYPECHECK_COMMAND} 2>&1 | head -20
```

**If Backend:**
```
Use Task tool with subagent_type: "implementer-be", model: "sonnet"

Task: Execute the implementation plan step by step.
Plan: {plan file path}

Working directory: {YOUR_BACKEND_DIR}/

Key patterns to follow:
- {YOUR_SERVICE_PATTERN}
- {YOUR_NAMING_CONVENTIONS}
- {YOUR_CODE_STYLE_RULES}

After each file change, verify:
  {YOUR_BUILD_COMMAND} 2>&1 | head -30
```

### 4. Run Final Verification

**Frontend:**
```bash
{YOUR_TYPECHECK_COMMAND}
{YOUR_LINT_COMMAND}
{YOUR_BUILD_COMMAND}
```

**Backend:**
```bash
{YOUR_BUILD_COMMAND}
{YOUR_TEST_COMMAND}
```

### 5. Show Completion Banner

```
═══════════════════════════════════════════════════
        🎉 IMPLEMENTATION COMPLETE
═══════════════════════════════════════════════════

Context: {Frontend | Backend}
Files:   {N} created, {N} modified

Validation:
✅ Type check: Passed
✅ Lint:       Passed
✅ Build:      Passed

═══════════════════════════════════════════════════
              NEXT STEPS
═══════════════════════════════════════════════════

1. REVIEW:  /flow:review
2. VERIFY:  /flow:verify
3. COMMIT:  /flow:commit

═══════════════════════════════════════════════════
```

## Error Handling

| Error Type | Action |
|------------|--------|
| Type error | Show error, suggest fix |
| Lint error | Run lint --fix, retry |
| Build error | Show full error, stop |
| Missing file | Create from pattern |

## Workflow Position

```
/flow:plan → /flow:implement → /flow:review → /flow:verify → /flow:commit → /flow:pr
                  ↑
              YOU ARE HERE
```
