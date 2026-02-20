# /utils:refactor - Code Cleanup

Clean up code using the refactorer agent. Targets changed files on the current branch by default.

## Arguments

- `$ARGUMENTS` - Optional: specific file paths, or empty for all changed files

## Usage

```bash
/utils:refactor                        # All changed files on branch
/utils:refactor src/features/auth/     # Specific directory
/utils:refactor src/components/Button.tsx  # Specific file
```

## Instructions

### 1. Show Start Banner

```
═══════════════════════════════════════════════════
🔧 Starting Refactor
   └─ Target: {files or "changed files on branch"}
═══════════════════════════════════════════════════
```

### 2. Identify Target Files

**If file paths provided:** use them directly.

**If no arguments:**
```bash
git diff main...HEAD --name-only
```

### 3. Invoke Refactorer Agent

```
Use Task tool with subagent_type: "refactorer", model: "sonnet"

Target files: {files}

Refactoring focus:

TypeScript/JavaScript:
- Eliminate `any` types (use `unknown` or proper types)
- Convert type aliases to interfaces for object definitions
- Add `import type` for type-only imports
- Remove unused imports and variables
- Fix implicit `any` function parameters

React (if applicable):
- Remove unnecessary `memo()` on simple components
- Remove `useCallback` for handlers passed to DOM elements
- Remove `useMemo` for cheap operations (<1ms)
- Split components over 150 lines

Code Quality:
- Remove dead code and commented-out code
- Inline single-use abstractions
- Fix silent error handling (empty catch blocks)
- Remove debug statements (console.log)
- Rename unclear variable names

Style (match project conventions in CLAUDE.md):
- {YOUR_STYLE_RULES}
```

### 4. Verify After Changes

Run verification after refactoring:

```bash
{YOUR_TYPECHECK_COMMAND}
{YOUR_LINT_COMMAND}
```

If verification fails:
- Revert the breaking change
- Try alternative approach
- Continue with remaining refactoring

### 5. Show Completion Banner

```
═══════════════════════════════════════════════════
        🔧 REFACTORING COMPLETE
═══════════════════════════════════════════════════

Changes:
  - {file}: {description of changes}

Stats:
  Files modified: {N}
  Lines removed:  {N}

═══════════════════════════════════════════════════
              SUGGESTED NEXT STEPS
═══════════════════════════════════════════════════

1. VERIFY: /flow:verify
2. REVIEW: /flow:review
3. COMMIT: /flow:commit

═══════════════════════════════════════════════════
```

## Refactoring Checklist

| Category | Check | Action |
|----------|-------|--------|
| Types | `any` types | Replace with proper type or `unknown` |
| Types | Aliases for objects | Convert to `interface` |
| Imports | Type-only imports | Add `import type` |
| Imports | Unused imports | Remove |
| React | Unnecessary `memo()` | Remove from simple components |
| React | `useCallback` to DOM | Remove |
| React | `useMemo` for cheap ops | Remove |
| Quality | Dead code | Remove |
| Quality | Empty catches | Add error handling |
| Quality | `console.log` | Remove or use `console.warn` |

## Workflow Position

```
/flow:plan → /flow:implement → /utils:refactor → /flow:verify → /flow:commit
                                      ↑
                                  YOU ARE HERE
```

## Related

- **Agent**: `refactorer` - Does the actual refactoring
- **Skill**: `code-quality-rules` - Quality guidelines
- **Command**: `/flow:verify` - Verify after refactoring
