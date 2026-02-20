# 05 — Memory System: 3-Layer Context Persistence

Claude loses context between sessions by default. The memory system solves this with three complementary layers that persist knowledge across conversations.

## Architecture

```
.claude/memory/
├── decisions.md     ← L1: Always loaded into every prompt
├── lessons.md       ← L1: Always loaded into every prompt
├── conventions.md   ← L1: Always loaded into every prompt
├── knowledge/       ← L2: Semantic search (shared with team)
│   ├── index.json
│   └── fragments/
│       └── {id}.json
├── local/           ← L3: Personal knowledge (gitignored)
│   ├── index.json
│   └── fragments/
└── README.md
```

---

## Layer 1: Always-Loaded Core Knowledge

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

## Layer 2: Semantic Knowledge Store

A TF-IDF indexed store of knowledge fragments. When you submit a prompt, the `knowledge_loader.py` hook:
1. Tokenizes your prompt
2. Searches the index for relevant fragments
3. Injects the top 5 matches as context

**Fragment structure:**

```json
{
  "id": "a1b2c3d4",
  "content": "When building AG Grid tables, always define columnDefs with useMemo...",
  "tags": ["react", "ag-grid", "tables"],
  "source": "manual",
  "scope": "shared",
  "created": "2026-01-29T10:30:00"
}
```

**See implementation:** `starter-hooks/utils/knowledge_store.py` and `starter-hooks/utils/knowledge_retriever.py`

---

## Layer 3: Personal Knowledge Store

The `memory/local/` directory is gitignored. This is where personal workflow preferences and session-specific learnings are stored automatically.

---

## Setting Up the Memory System

### Step 1: Copy the templates

```bash
cp .claude/claude-init/templates/memory/decisions.md .claude/memory/decisions.md
cp .claude/claude-init/templates/memory/lessons.md .claude/memory/lessons.md
cp .claude/claude-init/templates/memory/conventions.md .claude/memory/conventions.md
```

### Step 2: Copy the knowledge store infrastructure

```bash
mkdir -p .claude/memory/knowledge/fragments
mkdir -p .claude/memory/local/fragments

cp .claude/claude-init/starter-hooks/utils/knowledge_store.py .claude/hooks/utils/knowledge_store.py
cp .claude/claude-init/starter-hooks/utils/knowledge_retriever.py .claude/hooks/utils/knowledge_retriever.py
```

### Step 3: Configure hooks to load L1 memory

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
          },
          {
            "type": "command",
            "command": "uv run .claude/hooks/knowledge_loader.py || true"
          }
        ]
      }
    ]
  }
}
```

### Step 4: Fill in your project knowledge

Edit the three L1 files with your project's actual decisions, lessons, and conventions. Start with:
- Key architectural decisions already made
- Known gotchas or traps in your codebase
- Code style rules beyond what's in ESLint/Prettier

---

## Using the Memory System

### Adding knowledge manually

```bash
/utils:memory add "Always use React.lazy for route-level code splitting" --tags react,performance
```

Or directly create a fragment JSON:

```bash
echo '{
  "id": "abc12345",
  "content": "Always use React.lazy for route-level code splitting",
  "tags": ["react", "performance", "lazy-loading"],
  "source": "manual",
  "scope": "shared",
  "created": "2026-02-19T10:00:00"
}' > .claude/memory/knowledge/fragments/abc12345.json
```

### Automatic ingestion

At the end of each session, `knowledge_ingestor.py` (configured in `Stop` hook) extracts learnings from the transcript and stores them as fragments.

**See implementation:** `starter-hooks/knowledge_ingestor.py`

---

## Team Collaboration

L2 knowledge in `memory/knowledge/fragments/` is committed to git. To share a learning with your team:

```bash
git add .claude/memory/knowledge/fragments/
git commit -m "chore(memory): add learnings from auth implementation"
git push
```

Team members will have the knowledge auto-loaded in their next relevant prompt.

---

## Minimal Memory Setup

If you want just the basics without semantic search, only implement L1:

1. Create the three markdown files
2. Set up `context_loader.py` in `UserPromptSubmit` hooks
3. Manually maintain the files

This is the simplest useful setup and requires no additional infrastructure.

---

**Next Step →** `guide/06-hooks.md`
