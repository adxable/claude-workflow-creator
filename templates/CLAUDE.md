# CLAUDE.md — {YOUR_PROJECT} Workflow

This file defines the Claude Code workflow for {YOUR_PROJECT}.

## Project Overview

| Context | Location | Tech Stack |
|---------|----------|------------|
| **Frontend** | `{FRONTEND_DIR}/` | {React/Vue/Angular/etc} |
| **Backend** | `{BACKEND_DIR}/` | {Node/Python/.NET/etc} |

## Context Detection

The workflow automatically detects whether you're working on frontend or backend based on:
- File paths mentioned in your prompt
- File extensions
- Keywords in the prompt

**Manual override:** Start your prompt with `[frontend]` or `[backend]` to force a context.

## Commands

### Core Pipeline

| Command | Description |
|---------|-------------|
| `/flow:plan {desc}` | Research codebase and create implementation plan |
| `/flow:implement {plan}` | Execute plan step by step |
| `/flow:review` | Code review with checklists |
| `/flow:verify` | Run type checks, lint, build, tests |
| `/flow:commit` | Conventional commit |
| `/flow:pr` | Create pull request |

### Full Pipeline

```bash
/flow:plan "Add feature X"
→ /flow:implement .claude/plans/{name}.md
→ /flow:verify
→ /flow:review
→ /flow:commit
→ /flow:pr
```

## Code Standards

### {Frontend Tech} Standards

```
{Add your ESLint/TypeScript/style rules here}
```

Examples for React/TypeScript:
- Use `interface` for object types (not `type`)
- Use `import type` for type-only imports
- No `any` types
- Single quotes, semicolons, 120 char limit
- No `console.log` (use warn/error)

### {Backend Tech} Standards

```
{Add your backend code standards here}
```

## Project Structure

```
{YOUR_FRONTEND_DIR}/
├── src/
│   ├── components/     ← Shared UI components
│   ├── features/       ← Feature modules
│   ├── hooks/          ← Custom hooks
│   └── api/            ← API layer

{YOUR_BACKEND_DIR}/
├── src/
│   ├── controllers/    ← API endpoints
│   ├── services/       ← Business logic
│   └── models/         ← Data models
```

## Validation Commands

### Frontend
```bash
{YOUR_TYPECHECK_COMMAND}   # e.g., pnpm tsc --noEmit
{YOUR_LINT_COMMAND}        # e.g., pnpm eslint src/
{YOUR_BUILD_COMMAND}       # e.g., pnpm build
{YOUR_TEST_COMMAND}        # e.g., pnpm test
```

### Backend
```bash
{YOUR_BUILD_COMMAND}       # e.g., dotnet build / npm run build
{YOUR_TEST_COMMAND}        # e.g., dotnet test / npm test
```

## Memory

Core knowledge lives in `.claude/memory/`:
- `decisions.md` — Architectural decisions
- `lessons.md` — Lessons learned
- `conventions.md` — Code conventions

These are loaded automatically on every prompt via hooks.
