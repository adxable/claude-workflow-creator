# 05 — Memory System: Persistent Context Across Sessions

Claude loses context between sessions by default. The memory system solves this with three markdown files that persist knowledge across conversations.

## Architecture

```
.claude/memory/
├── decisions.md     <- Loaded into every prompt
├── lessons.md       <- Loaded into every prompt
├── conventions.md   <- Loaded into every prompt
└── README.md
```

---

## Memory Files

Three markdown files that are injected into **every** Claude prompt automatically (via the `context_loader.py` hook):

### `decisions.md` — Architectural decisions

```markdown
# Architectural Decisions

## 2026-01-15: Use TanStack Query for all API calls
- Decided: Use useSuspenseQuery + Suspense boundaries
- Reason: Consistent loading states, better error handling
- Applies to: All new components

## 2026-01-20: Use Zod for form validation
- Decided: All forms use Zod schemas + react-hook-form
- Reason: Type-safe forms with automatic TypeScript inference
```

### `lessons.md` — Lessons learned from mistakes

```markdown
# Lessons Learned

## React
- Always wrap data-fetching components in Suspense boundaries
- Don't use useEffect for data fetching (use TanStack Query instead)
- Memo() only for list items with >50 elements

## Git
- Always use HEREDOC for multi-line commit messages
- Never amend published commits
```

### `conventions.md` — Code conventions

```markdown
# Code Conventions

## TypeScript
- Use `interface` for object types, never `type`
- Use `import type` for type-only imports
- No `any` types

## Naming
- React components: PascalCase
- Hooks: camelCase, starts with `use`
- Files: kebab-case
```

---

## Setting Up the Memory System

### Step 1: Copy the templates

```bash
cp templates/memory/decisions.md .claude/memory/decisions.md
cp templates/memory/lessons.md .claude/memory/lessons.md
cp templates/memory/conventions.md .claude/memory/conventions.md
```

### Step 2: Configure the hook

In `settings.json`:

```json
{
  "hooks": {
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "uv run .claude/hooks/context_loader.py || true"
          }
        ]
      }
    ]
  }
}
```

### Step 3: Fill in your project knowledge

Edit the three files with your project's actual decisions, lessons, and conventions. Start with:
- Key architectural decisions already made
- Known gotchas or traps in your codebase
- Code style rules beyond what's in ESLint/Prettier

---

## Tips

- Keep each file under ~100 lines for best results
- Write short, actionable statements
- Remove outdated entries regularly
- Review quarterly — consolidate lessons, prune decisions

---

## Team Collaboration

Memory files are committed to git — team members share knowledge:

```bash
git add .claude/memory/
git commit -m "chore(memory): add learnings from auth implementation"
git push
```

---

**Next Step ->** `guide/06-hooks.md`
