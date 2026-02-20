# Architectural Decisions

Record significant decisions here. This file is loaded into every Claude prompt automatically.

**Format:**

```
## {YYYY-MM-DD}: {Short title}
- Decided: {What was decided}
- Reason: {Why this was chosen over alternatives}
- Applies to: {What code/features this affects}
- Alternatives considered: {What else was evaluated}
```

---

## {YYYY-MM-DD}: {Your first decision}

- Decided: {What you decided to do}
- Reason: {Why}
- Applies to: {Scope}

---

<!--
EXAMPLES TO INSPIRE YOU:

## 2026-01-15: Use TanStack Query for all API calls
- Decided: Use useSuspenseQuery + Suspense boundaries for all data fetching
- Reason: Consistent loading states, better error handling, automatic caching
- Applies to: All new React components that fetch data

## 2026-01-20: Service layer pattern for backend
- Decided: All business logic goes in services, controllers are thin wrappers
- Reason: Testability, separation of concerns
- Applies to: All new API endpoints

## 2026-02-01: Zod for form validation
- Decided: All forms use Zod schemas with react-hook-form
- Reason: Type-safe validation with automatic TypeScript inference
- Applies to: All new forms
-->
