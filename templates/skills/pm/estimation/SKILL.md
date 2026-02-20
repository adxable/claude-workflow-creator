---
name: pm-estimation
description: Estimation guidelines for Claude Code-assisted development including T-shirt sizing, productivity multipliers by task type, and risk buffers.
---

# EXPERIMENTAL SKILL - needs more accurate data

# Estimation Skill - Claude Code Assisted Development

Guidelines for estimating tickets when development is assisted by Claude Code.

## T-Shirt Size to Time Mapping

| Size | Calendar Days | Work Hours | Description |
|------|---------------|------------|-------------|
| **S** | 0-3 days | 4-24h | Single component, simple logic |
| **M** | 4-6 days | 32-48h | Multiple components, moderate logic |
| **L** | 7-13 days | 56-104h | Feature + API, complex logic |
| **XL** | 2+ weeks | 80-160h | Major feature, architectural changes |

## Claude Code Productivity Factors

When estimating with Claude Code assistance, apply these multipliers:

| Task Type | Traditional | With Claude | Speedup |
|-----------|-------------|-------------|---------|
| Boilerplate code | 1x | 0.2x | 5x faster |
| CRUD operations | 1x | 0.3x | 3x faster |
| UI components | 1x | 0.4x | 2.5x faster |
| API integration | 1x | 0.4x | 2.5x faster |
| Complex business logic | 1x | 0.6x | 1.7x faster |
| Bug investigation | 1x | 0.5x | 2x faster |
| Testing | 1x | 0.3x | 3x faster |
| Documentation | 1x | 0.2x | 5x faster |

## Estimation Formula

```
Estimated Time = Base Time × Task Complexity × Claude Factor × Risk Buffer
```

### Base Time by Size

| Size | Base Hours |
|------|------------|
| S | 16h (2 days) |
| M | 40h (5 days) |
| L | 80h (10 days) |
| XL | 120h (15 days) |

### Task Complexity Multipliers

| Complexity | Multiplier | Indicators |
|------------|------------|------------|
| Simple | 0.5x | Clear requirements, existing patterns |
| Standard | 1.0x | Some unknowns, standard patterns |
| Complex | 1.5x | Many unknowns, new patterns needed |
| Very Complex | 2.0x | Architectural changes, research needed |

### Claude Factor (Average)

For mixed task types, use **0.4x** as default Claude Code factor.

### Risk Buffer

| Risk Level | Buffer | When to Apply |
|------------|--------|---------------|
| Low | 1.0x | Well-understood domain, clear requirements |
| Medium | 1.2x | Some unknowns, standard complexity |
| High | 1.5x | New technology, unclear requirements |
| Very High | 2.0x | POC, research, external dependencies |

## Estimation Examples

### Example 1: Add Filter to List Page (S)

**Traditional estimate:** 3 days (24h)

| Component | Traditional | Claude Factor | With Claude |
|-----------|-------------|---------------|-------------|
| Backend criteria | 4h | 0.3x | 1.2h |
| Backend service | 4h | 0.3x | 1.2h |
| Frontend component | 8h | 0.4x | 3.2h |
| Integration | 4h | 0.4x | 1.6h |
| Testing | 4h | 0.3x | 1.2h |
| **Total** | **24h** | | **8.4h** |

**With Claude:** ~1 day (Size: S, lower range)

### Example 2: New CRUD Module (M)

**Traditional estimate:** 5 days (40h)

| Component | Traditional | Claude Factor | With Claude |
|-----------|-------------|---------------|-------------|
| Entity models | 4h | 0.2x | 0.8h |
| Repository | 4h | 0.2x | 0.8h |
| Service layer | 8h | 0.3x | 2.4h |
| API controller | 4h | 0.3x | 1.2h |
| Frontend list | 8h | 0.4x | 3.2h |
| Frontend form | 8h | 0.4x | 3.2h |
| Testing | 4h | 0.3x | 1.2h |
| **Total** | **40h** | | **12.8h** |

**With Claude:** ~2 days (Size: S, upper range)

### Example 3: Complex Feature with Business Logic (L)

**Traditional estimate:** 10 days (80h)

| Component | Traditional | Claude Factor | With Claude |
|-----------|-------------|---------------|-------------|
| Requirements analysis | 8h | 0.8x | 6.4h |
| Backend models | 8h | 0.2x | 1.6h |
| Business logic | 24h | 0.6x | 14.4h |
| API layer | 8h | 0.3x | 2.4h |
| Frontend UI | 16h | 0.4x | 6.4h |
| Integration | 8h | 0.4x | 3.2h |
| Testing | 8h | 0.3x | 2.4h |
| **Total** | **80h** | | **36.8h** |

**With Claude:** ~5 days (Size: M)

## Quick Estimation Table

For quick estimates with Claude Code assistance:

| Traditional Size | Traditional Time | With Claude | New Size |
|------------------|------------------|-------------|----------|
| S (0-3 days) | 1-3 days | 0.5-1 day | XS |
| M (4-6 days) | 4-6 days | 1.5-2.5 days | S |
| L (7-13 days) | 7-13 days | 3-5 days | M |
| XL (2+ weeks) | 14+ days | 5-8 days | L |

## Estimation Checklist

When estimating a ticket:

1. **Identify task types** - What components need work?
2. **Assess complexity** - Clear requirements? Existing patterns?
3. **Apply Claude factors** - Which tasks benefit most?
4. **Add risk buffer** - Unknowns? Dependencies?
5. **Round up** - Always round to next half-day

## Things Claude Code Does NOT Speed Up

Some tasks have minimal Claude speedup:

| Task | Why | Estimate at 1x |
|------|-----|----------------|
| Requirements gathering | Human collaboration | Full time |
| Design decisions | Human judgment | Full time |
| Code review | Human oversight | 0.8x |
| Deployment | Infrastructure | Full time |
| Meetings | Human communication | Full time |
| User acceptance testing | Human validation | Full time |

## Estimation Output Format

When providing estimates, use this format:

```
## Ticket: {JIRA-KEY} - {Title}

**Size:** {S/M/L/XL}
**Traditional Estimate:** {X} days
**With Claude Code:** {Y} days

### Breakdown
| Task | Hours | Notes |
|------|-------|-------|
| {task1} | {h} | {factor applied} |
| {task2} | {h} | {factor applied} |

### Risk Factors
- {risk1}: {impact}
- {risk2}: {impact}

### Confidence Level
{Low/Medium/High} - {reason}
```

## Integration with PM Workflow

Use estimation during:

1. **`/pm:stories`** - Initial sizing during story generation
2. **`/pm:review`** - Refine estimates during review
3. **`/pm:plan-tasks`** - Detailed task-level estimates
4. **`/jira:start`** - Validate estimate before starting work
