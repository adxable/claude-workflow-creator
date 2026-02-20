# Memory System

> This directory contains Claude's persistent memory for the project. Knowledge stored here survives across sessions and is automatically loaded when relevant.

## How It Works

```
.claude/memory/
├── README.md            ← You are here
├── decisions.md         ← L1: Loaded into every prompt
├── lessons.md           ← L1: Loaded into every prompt
├── conventions.md       ← L1: Loaded into every prompt
├── knowledge/           ← L2: Semantic search (shared via git)
│   ├── index.json
│   └── fragments/
│       └── {id}.json
└── local/               ← L3: Personal knowledge (gitignored)
    ├── index.json
    └── fragments/
```

## Three Layers

### Layer 1 — Always-Loaded Core (Markdown)

Three files injected into **every** Claude prompt via the `context_loader.py` hook:

| File | Purpose | What to put here |
|------|---------|-----------------|
| `decisions.md` | Architectural decisions | Tech choices, patterns adopted, trade-offs made |
| `lessons.md` | Lessons from mistakes | Gotchas, debugging insights, things to avoid |
| `conventions.md` | Code conventions | Naming rules, file organization, style beyond linting |

**Tips:**
- Keep each file under ~100 lines for best results
- Write short, actionable statements
- Remove outdated entries regularly
- These files are the most impactful — Claude reads them every time

### Layer 2 — Semantic Knowledge Store (JSON fragments)

Indexed knowledge fragments in `knowledge/fragments/`. When you submit a prompt, `knowledge_loader.py`:
1. Tokenizes your prompt
2. Searches the TF-IDF index for relevant fragments
3. Injects the top matches as additional context

**Fragment example:**
```json
{
  "id": "a1b2c3d4",
  "content": "When building tables, always define columnDefs with useMemo to prevent re-renders",
  "tags": ["react", "tables", "performance"],
  "source": "manual",
  "scope": "shared",
  "created": "2026-01-29T10:30:00"
}
```

**This layer is committed to git** — team members get your learnings automatically.

### Layer 3 — Personal Knowledge (gitignored)

Same as L2 but stored in `local/fragments/`. Personal preferences, workflow shortcuts, and session-specific learnings that don't belong in the shared repo.

**Automatically populated** by the `knowledge_ingestor.py` hook at the end of each session.

## Adding Knowledge

### Editing L1 files directly

Open `decisions.md`, `lessons.md`, or `conventions.md` and add entries:

```markdown
## 2026-02-20: Use React.lazy for route-level code splitting
- Decided: All route components use React.lazy + Suspense
- Reason: Reduces initial bundle by ~40%
- Applies to: All top-level route components
```

### Automatic ingestion

The `knowledge_ingestor.py` hook (configured in `Stop` event) extracts learnings from each session transcript and stores them as L2/L3 fragments automatically.

### Via the memory command

```bash
/utils:memory add "Always validate API responses with Zod" --tags api,validation
```

## Hooks That Power Memory

| Hook | Event | Role |
|------|-------|------|
| `context_loader.py` | UserPromptSubmit | Loads L1 files into prompt |
| `knowledge_loader.py` | UserPromptSubmit | Searches L2/L3 for relevant fragments |
| `memory_updater.py` | Stop | Updates L1 files based on session |
| `knowledge_ingestor.py` | Stop | Extracts learnings into L2/L3 fragments |
| `memory_extractor.py` | PreCompact | Saves context before compaction |

## Team Collaboration

L2 fragments in `knowledge/fragments/` are shared via git:

```bash
git add .claude/memory/knowledge/
git commit -m "chore(memory): add learnings from auth implementation"
git push
```

Team members get the knowledge auto-loaded on their next relevant prompt.

## Maintenance

- **Review L1 quarterly** — remove outdated decisions, consolidate lessons
- **Prune L2 fragments** — delete fragments that are no longer relevant
- **Keep L1 concise** — aim for signal, not volume
