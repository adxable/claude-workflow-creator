# /flow:verify - Context-Aware Verification

Run type checking, linting, build, and tests. Auto-detects frontend vs backend context.

## Arguments

- `$ARGUMENTS` - Optional: context override, module name, or flags

## Usage

```bash
/flow:verify                    # Auto-detect from changed files
/flow:verify [frontend]         # Force frontend verification
/flow:verify [backend]          # Force backend verification
/flow:verify --fix              # Auto-fix lint errors (frontend)
/flow:verify [frontend] --browser  # Include browser verification
```

## Flags

| Flag | Context | Description |
|------|---------|-------------|
| `--fix` | Frontend | Auto-fix lint errors |
| `--browser` | Frontend | Visual verification with Chrome extension |

## Instructions

### 1. Show Start Banner

```
═══════════════════════════════════════════════════
✓ Starting Verification
   └─ Detecting context...
═══════════════════════════════════════════════════
```

### 2. Detect Context

**Priority order:**
1. Manual override in arguments
2. From git diff: Check changed file extensions
3. From working directory

```bash
git diff --name-only HEAD 2>/dev/null | head -20
```

| File Pattern | Context |
|--------------|---------|
| {YOUR_FRONTEND_EXTENSIONS} | **Frontend** |
| {YOUR_BACKEND_EXTENSIONS} | **Backend** |
| Mixed | Run both |

### 3. Run Frontend Verification

```
═══════════════════════════════════════════════════
✓ VERIFY: Frontend
═══════════════════════════════════════════════════
```

**Step 3a: Type Checking**
```bash
{YOUR_TYPECHECK_COMMAND}
```

**Step 3b: Linting**
```bash
{YOUR_LINT_COMMAND}
```

On failure with `--fix`:
```bash
{YOUR_LINT_FIX_COMMAND}
{YOUR_LINT_COMMAND}  # Re-check
```

**Step 3c: Build**
```bash
{YOUR_BUILD_COMMAND}
```

**Step 3d: Browser Verification (if --browser flag)**
```
Use Task tool with subagent_type: "browser-tester", model: "sonnet"

URL: http://localhost:{YOUR_DEV_PORT}{url_path}

Verify:
- Page loads without errors
- Components render correctly
- No console errors
- Interactions work
```

### 4. Run Backend Verification

```
═══════════════════════════════════════════════════
✓ VERIFY: Backend
═══════════════════════════════════════════════════
```

**Step 4a: Build**
```bash
{YOUR_BACKEND_BUILD_COMMAND}
```

**Step 4b: Tests**
```bash
{YOUR_TEST_COMMAND}
```

### 5. Show Results

**Success:**
```
═══════════════════════════════════════════════════
        ✅ VERIFICATION PASSED
═══════════════════════════════════════════════════

✓ Type check    (0 errors)
✓ Lint          (0 errors)
✓ Build         (success)
✓ Tests         (N passed)

NEXT STEPS:
1. COMMIT: /flow:commit
2. PR:     /flow:pr
═══════════════════════════════════════════════════
```

**Failure:**
```
═══════════════════════════════════════════════════
        ❌ VERIFICATION FAILED
═══════════════════════════════════════════════════

✗ Lint   (3 errors)

┌─────────────────────────────────────────────────┐
│ {file}:{line}                                   │
│ {error message}                                 │
└─────────────────────────────────────────────────┘

TRY: /flow:verify --fix
═══════════════════════════════════════════════════
```

## Verification Commands Summary

Replace these with your actual commands:

| Context | Command | Purpose |
|---------|---------|---------|
| Frontend | `{YOUR_TYPECHECK_COMMAND}` | Type checking |
| Frontend | `{YOUR_LINT_COMMAND}` | Lint checking |
| Frontend | `{YOUR_BUILD_COMMAND}` | Production build |
| Backend | `{YOUR_BACKEND_BUILD_COMMAND}` | Build solution |
| Backend | `{YOUR_TEST_COMMAND}` | Run tests |

## Workflow Position

```
/flow:plan → /flow:implement → /flow:review → /flow:verify → /flow:commit → /flow:pr
                                                   ↑
                                               YOU ARE HERE
```
