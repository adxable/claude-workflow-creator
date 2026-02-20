# /flow:review - Context-Aware Code Review

Comprehensive code review using context-appropriate agents and checklists.

## Arguments

- `$ARGUMENTS` - Optional: file paths, context override, or flags

## Usage

```bash
/flow:review                              # Auto-detect from changed files
/flow:review [frontend]                   # Force frontend review
/flow:review [backend]                    # Force backend review
/flow:review src/components/Button.tsx    # Review specific file
/flow:review [frontend] --browser         # Code review + browser verification
```

## Flags

| Flag | Context | Description |
|------|---------|-------------|
| `--browser` | Frontend only | Add visual verification after code review |
| `--browser-only` | Frontend only | Skip code review, only browser verification |

## Instructions

### 1. Show Start Banner

```
═══════════════════════════════════════════════════
🔍 Starting Code Review
   └─ Detecting context...
═══════════════════════════════════════════════════
```

### 2. Detect Context & Identify Files

**Priority order:**
1. **Manual override**: `[frontend]` or `[backend]` in arguments
2. **From file paths**: Analyze provided file extensions
3. **From git diff**: Check changed files on branch

```bash
git diff main...HEAD --name-only
```

| File Extensions | Context |
|-----------------|---------|
| `.tsx`, `.ts`, `.jsx`, `.js`, `.css` | **Frontend** |
| `.cs`, `.py`, `.go`, `.java`, `.rb` | **Backend** |
| Mixed | Review both separately |

### 3. Run Context-Specific Review

#### FRONTEND Review

**Invoke `code-reviewer-fe` agent:**
```
Use Task tool with subagent_type: "code-reviewer-fe", model: "opus"

Task: Review frontend code changes.
Files: {list of frontend files}

Review checklist:

TypeScript Quality:
- [ ] No any types (use unknown or proper types)
- [ ] interface for object types, not type
- [ ] import type for type-only imports
- [ ] No unused imports or variables

React Patterns:
- [ ] Hooks follow rules (no conditional hooks)
- [ ] useCallback only when passed to memoized children
- [ ] useMemo only for expensive computations (>1ms)
- [ ] memo() only for frequently re-rendering list items

Code Quality:
- [ ] Files under ~150 lines
- [ ] Single responsibility per component
- [ ] No dead code
- [ ] Proper error handling (no silent catches)
- [ ] No console.log statements

Conventions (from CLAUDE.md):
- [ ] {YOUR_STYLE_RULES}
```

#### BACKEND Review

**Invoke `code-reviewer-be` agent:**
```
Use Task tool with subagent_type: "code-reviewer-be", model: "opus"

Task: Review backend code changes.
Files: {list of backend files}

Review checklist:

{YOUR_LANGUAGE} Quality:
- [ ] Interfaces/abstractions defined for services
- [ ] Async/await used correctly
- [ ] Proper null/error handling
- [ ] No magic strings or numbers

Architecture:
- [ ] Business logic in services, not controllers
- [ ] Proper separation of concerns
- [ ] Repository/service patterns followed

Code Quality:
- [ ] Methods reasonably sized (<50 lines)
- [ ] Classes reasonably sized
- [ ] No commented-out code
- [ ] Proper logging (not console.log in production)
```

### 4. Browser Verification (if `--browser` flag, Frontend only)

**Invoke `browser-tester` agent:**
```
Use Task tool with subagent_type: "browser-tester", model: "sonnet"

Task: Visual verification after code review.
URL: {YOUR_DEV_URL}

Steps:
1. Ensure dev server running
2. Navigate to the changed feature
3. Take screenshots
4. Verify UI renders correctly
5. Test interactions (buttons, forms, links)
6. Check console for errors
7. If issues found → fix → re-verify (max 5 iterations)
```

### 5. Generate Review Report

Create report at `.claude/reviews/review-{date}-{context}.md`:

```markdown
# Code Review Report

**Branch:** {branch}
**Context:** {Frontend | Backend}
**Date:** {date}
**Files Reviewed:** {count}

## Summary

{2-3 sentence overview}

## Issues Found

### Critical (Must Fix)

| File | Line | Issue | Suggestion |
|------|------|-------|------------|

### Important (Should Fix)

| File | Line | Issue | Suggestion |
|------|------|-------|------------|

### Minor (Nice to Have)

- {file}:{line} - {suggestion}

## Checklist Results

| Category | Passed | Failed |
|----------|--------|--------|
| Type Quality | {n} | {n} |
| Patterns | {n} | {n} |
| Code Quality | {n} | {n} |
```

### 6. Show Completion Banner

```
═══════════════════════════════════════════════════
        🔍 REVIEW COMPLETE
═══════════════════════════════════════════════════

Context: {Frontend | Backend}
Files:   {N} reviewed

Issues Found:
  Critical:  {N}
  Important: {N}
  Minor:     {N}

Report: .claude/reviews/review-{date}.md

═══════════════════════════════════════════════════
              SUGGESTED NEXT STEPS
═══════════════════════════════════════════════════

{If critical issues > 0}
1. Fix critical issues first
2. Then: /flow:verify

{If no critical issues}
1. VERIFY: /flow:verify
2. COMMIT: /flow:commit

═══════════════════════════════════════════════════
```

## Workflow Position

```
/flow:plan → /flow:implement → /flow:review → /flow:verify → /flow:commit → /flow:pr
                                    ↑
                                YOU ARE HERE
```

## Related

- **Agent**: `code-reviewer-fe` - Frontend code review
- **Agent**: `code-reviewer-be` - Backend code review
- **Command**: `/flow:verify` - Run validation suite after review
