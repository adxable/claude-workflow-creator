# Code Conventions

Define your team's coding standards here. This file is loaded into every Claude prompt automatically.

Keep this file focused on **non-obvious conventions** — things that can't be enforced by ESLint/Prettier alone.

---

## Naming Conventions

| Thing | Convention | Example |
|-------|-----------|---------|
| {Files} | {kebab-case/PascalCase/etc} | `{example}` |
| {Functions} | {camelCase/etc} | `{example}` |
| {Classes} | {PascalCase/etc} | `{example}` |
| {Constants} | {UPPER_SNAKE/etc} | `{example}` |

---

## File Organization

```
{YOUR_PROJECT_STRUCTURE}

{Example:}
src/
├── components/     ← Shared UI only (no business logic)
├── features/       ← Feature-specific code
│   └── {feature}/
│       ├── {Feature}.tsx   ← Main component
│       ├── hooks/          ← Feature hooks
│       └── api/            ← API calls
└── hooks/          ← Shared hooks only
```

---

## {Frontend} Conventions

```
{List your style/pattern rules:}

- {Rule 1: e.g., Use interface for object types, never type}
- {Rule 2: e.g., Use import type for type-only imports}
- {Rule 3: e.g., No console.log in production code}
- {Rule 4: e.g., Single quotes, semicolons, 120 char limit}
```

---

## {Backend} Conventions

```
{List your backend standards:}

- {Rule 1: e.g., Services handle business logic, controllers are thin}
- {Rule 2: e.g., Always validate input at API boundary}
- {Rule 3: e.g., Use async/await, never callbacks}
- {Rule 4: e.g., Return consistent error shapes}
```

---

## Git Conventions

```
Commit format: {type}({scope}): {description}

Types: feat, fix, refactor, chore, docs, test
Scopes: {your scopes, e.g., fe/pms, be/api, shared/auth}

Examples:
- feat(fe/orders): add status filter
- fix(be/api): handle null user in auth middleware
- chore: update dependencies
```

---

<!--
EXAMPLES TO INSPIRE YOU:

## TypeScript Conventions
- Use `interface` for object types (not `type`)
- Use `import type` for type-only imports
- Never use `any` — use `unknown` and narrow it
- Generic type parameters: T, TItem, TKey (descriptive names)

## React Conventions
- Components: PascalCase files matching the export name
- Hooks: camelCase, always starts with `use`
- Event handlers: `handle{Event}` (handleClick, handleSubmit)
- Boolean props: `is`, `has`, `can`, `should` prefixes

## API Conventions
- All routes: /api/v1/{resource}
- Response shape: { data: T, error?: string, meta?: {...} }
- Error codes: use HTTP status codes + descriptive messages
- Pagination: { page, pageSize, total } in meta
-->
