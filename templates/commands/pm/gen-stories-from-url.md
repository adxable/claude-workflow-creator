# /pm:gen-stories-from-url - Generate Stories from URL

Generate user stories by investigating a URL and analyzing requirements.

## Arguments

- `$ARGUMENTS`:
  - **url** - URL to investigate (staging app, Figma, existing feature)
  - **description** - Description of what features/stories to generate
  - **image_path** (optional) - Screenshot or mockup for additional context

## Usage

```bash
/pm:gen-stories-from-url https://staging.yourapp.com/feature/123 "Implement filters and export"
/pm:gen-stories-from-url https://figma.com/file/xxx "Dashboard redesign" /path/to/mockup.png
```

## Output

Creates: `.claude/jira/{feature-slug}-stories.md`

## Instructions

### 1. Show Start Banner

```
═══════════════════════════════════════════════════
🔍 PM: Generate Stories from URL
   └─ URL: {url}
   └─ Description: {description}
   └─ Image: {image_path or "None"}
═══════════════════════════════════════════════════
```

### 2. Create Directories

```bash
mkdir -p .claude/screenshots/{feature-slug}/before
mkdir -p .claude/jira
```

### 3. Investigate the URL

If the Chrome extension is available, use the browser-tester agent:

```
Use Task tool with subagent_type: "browser-tester", model: "sonnet"

Task: Investigate the URL and capture screenshots for story generation.

URL: {url}
Description: {description}

Steps:
1. Navigate to the URL
2. Take full page screenshot (JPEG format)
3. Identify key UI areas — tabs, sections, forms, tables
4. Take targeted screenshots of each important area
5. Save all screenshots to: .claude/screenshots/{feature-slug}/before/
6. Return a summary: UI elements found, current state, improvement opportunities
```

If browser tools are not available, ask the user to describe the UI or provide screenshots.

### 4. Load Story Writing Skill (if configured)

If you have a story templates skill, load it:

```
Read .claude/skills/pm/{YOUR_TEMPLATES_SKILL}/SKILL.md
```

Otherwise use the default template in Step 6.

### 5. Analyze Requirements

Based on the investigation and description:
- Identify distinct user capabilities (each = one story)
- Group related functionality together
- Consider happy paths and edge cases (empty states, errors, permissions)
- Map UI elements to user needs
- Note critical business rules

### 6. Generate Stories

For each identified story use this template:

```markdown
## Story {n}: {Area} - {Title}

**LINK TO DESIGN:**
{url_investigated}

---

**USER STORY:**
As a {role}, I need {feature/functionality} so that I can {benefit}.

**DESCRIPTION:**
The {view/feature name} provides {purpose}. It consists of {high-level structure}.

**IMPORTANT:**
This {view/feature} is responsible for {key responsibility}.
{!! Critical business rules or constraints, if any}

**ACCEPTANCE CRITERIA:**
- {Criterion — specific, testable}
- {Criterion}
- {Empty/error state criterion}

---

**Metadata:**
- Complexity: {S|M|L|XL}
- Labels: {frontend, backend, database, ...}
- Notes: {additional context}
```

### 7. Save Output

Write to `.claude/jira/{feature-slug}-stories.md`:

```markdown
# Stories: {Feature Name}

**Source:** {url}
**Generated:** {YYYY-MM-DD HH:MM}
**Description:** {user description}
**Screenshots:** .claude/screenshots/{feature-slug}/before/

---

{generated stories}
```

### 8. Show Completion Banner

```
═══════════════════════════════════════════════════
✅ Stories Generated
   └─ File: .claude/jira/{feature-slug}-stories.md
   └─ Stories: {N} stories created
   └─ Screenshots: .claude/screenshots/{feature-slug}/before/
═══════════════════════════════════════════════════

Next Steps:
1. Review: .claude/jira/{feature-slug}-stories.md
2. Configure: /pm:prepare .claude/jira/{feature-slug}-stories.md
3. Or generate tasks: /pm:gen-tasks-for-stories .claude/jira/{feature-slug}-stories.md

═══════════════════════════════════════════════════
```

## Story Writing Guidelines

### DESCRIPTION
Explain: what the feature provides, how it is structured, main functionality areas.

### IMPORTANT section
Use for: critical business rules (prefix with `!!`), scope constraints, key dependencies.

### Acceptance Criteria
- Use dash `-` bullets
- Be specific about UI behavior
- Always include empty state and error cases

## Workflow Position

```
/pm:gen-stories-from-url  →  /pm:prepare  →  /pm:push
        ↑
    YOU ARE HERE
```

## Related

- **Agent**: `browser-tester` - URL investigation (requires Chrome extension)
- **Command**: `/pm:gen-stories-from-img` - Generate from screenshot instead of URL
- **Command**: `/pm:prepare` - Configure tracker fields before pushing
