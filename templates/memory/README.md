# Memory System

> This directory contains Claude's persistent memory for the project. Knowledge stored here survives across sessions and is automatically loaded when relevant.

## How It Works

```
.claude/memory/
├── README.md            <- You are here
├── decisions.md         <- Loaded into every prompt
├── lessons.md           <- Loaded into every prompt
└── conventions.md       <- Loaded into every prompt
```

## Memory Files

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

## Adding Knowledge

Open `decisions.md`, `lessons.md`, or `conventions.md` and add entries:

```markdown
## 2026-02-20: Use React.lazy for route-level code splitting
- Decided: All route components use React.lazy + Suspense
- Reason: Reduces initial bundle by ~40%
- Applies to: All top-level route components
```

## Team Collaboration

Memory files are committed to git — team members share knowledge automatically:

```bash
git add .claude/memory/
git commit -m "chore(memory): add learnings from auth implementation"
git push
```

## Maintenance

- **Review quarterly** — remove outdated decisions, consolidate lessons
- **Keep concise** — aim for signal, not volume
