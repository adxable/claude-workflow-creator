# /setup:audit - Audit Workflow Installation

Verify that the Claude workflow is fully and correctly installed. Checks for missing files, unreplaced placeholders, broken agent references, hook configuration, and memory setup.

## Instructions

### 1. Show Start Banner

```
══════════════════════════════════════════════════════
  WORKFLOW AUDIT
  Checking .claude/ installation...
══════════════════════════════════════════════════════
```

### 2. Run All Checks

Execute the following checks. For each check, record status as PASS, WARN, or FAIL.

#### Check 1: Core Files

Verify these files exist and are non-empty:

```
.claude/CLAUDE.md
.claude/settings.json
```

FAIL if missing.

#### Check 2: Commands

Verify all flow commands exist:

```
.claude/commands/flow/plan.md
.claude/commands/flow/implement.md
.claude/commands/flow/verify.md
.claude/commands/flow/review.md
.claude/commands/flow/commit.md
.claude/commands/flow/pr.md
```

Verify utility commands:
```
.claude/commands/utils/refactor.md
.claude/commands/setup/init.md
.claude/commands/setup/resume.md
.claude/commands/setup/audit.md
```

FAIL if any flow command is missing. WARN if utility commands are missing.

#### Check 3: Agents

Verify generic agents exist:

```
.claude/agents/explorer.md
.claude/agents/git-automator.md
.claude/agents/refactorer.md
.claude/agents/code-reviewer.md
.claude/agents/planner.md
.claude/agents/implementer.md
```

Check for specialized agents (based on project type in CLAUDE.md):

If frontend detected:
```
.claude/agents/planner-fe.md
.claude/agents/implementer-fe.md
.claude/agents/code-reviewer-fe.md
```

If backend detected:
```
.claude/agents/planner-be.md
.claude/agents/implementer-be.md
.claude/agents/code-reviewer-be.md
```

FAIL if generic agents missing. WARN if specialized agents missing for detected stack.

**Agent frontmatter validation:**
For each agent file, verify:
- Has valid YAML frontmatter between `---` markers
- Has `name`, `description`, `tools`, `model` fields
- `name` matches the filename (without `.md`)

WARN if frontmatter is invalid.

#### Check 4: Unreplaced Placeholders

Search all files in `.claude/` for unreplaced placeholder patterns:

```
{YOUR_*}
{PLACEHOLDER}
{TODO}
```

Exclude skill reference files (`.claude/skills/`) since they may contain example code with curly braces.

FAIL if any `{YOUR_*}` placeholders found in commands or agents.

#### Check 5: Command-Agent Wiring

For each flow command, verify the referenced `subagent_type` has a matching agent file:

Read each command in `.claude/commands/flow/` and extract all `subagent_type: "..."` values. For each value, verify `.claude/agents/{value}.md` exists.

FAIL if any referenced agent is missing.

#### Check 6: Settings & Hooks

Read `.claude/settings.json` and verify:
- Valid JSON
- Has `hooks` section
- Has entries for: `UserPromptSubmit`, `PreToolUse`, `PostToolUse`, `Stop`
- Each hook command references a file that exists in `.claude/hooks/`

FAIL if settings.json is invalid. WARN if hook files are missing.

#### Check 7: Context Detection

Verify context detection files exist:

```
.claude/contexts/detector.py
.claude/contexts/frontend.yaml  (if frontend)
.claude/contexts/backend.yaml   (if backend)
```

Read YAML configs and verify:
- `project_root` matches the project structure
- `validation.commands` are set (not placeholder)

WARN if missing or misconfigured.

#### Check 8: Memory System

Verify memory structure:

```
.claude/memory/README.md
.claude/memory/decisions.md
.claude/memory/lessons.md
.claude/memory/conventions.md
.claude/memory/knowledge/index.json
.claude/memory/local/index.json
```

Verify knowledge store utilities:
```
.claude/hooks/utils/knowledge_store.py
.claude/hooks/utils/knowledge_retriever.py
.claude/hooks/utils/constants.py
```

WARN if any missing.

#### Check 9: Skills

Verify skill activation rules exist:
```
.claude/skills/skill-rules.json
```

Verify it contains valid JSON.

WARN if missing or invalid.

#### Check 10: Optional Integrations

Check for optional but configured integrations:

**Jira** (if commands exist):
```
.claude/commands/jira/start.md
.claude/commands/jira/pr-desc.md
.claude/agents/jira.md
```

**Browser Testing** (if agent exists):
```
.claude/agents/browser-tester.md
.claude/skills/frontend/browser-testing/SKILL.md
```

**PM Commands** (if directory exists):
```
.claude/commands/pm/gen-stories-from-url.md
.claude/commands/pm/gen-tasks-for-story.md
.claude/commands/pm/prepare.md
.claude/commands/pm/push.md
```

WARN if partially installed (some files but not all).

### 3. Show Results

```
══════════════════════════════════════════════════════
  AUDIT RESULTS
══════════════════════════════════════════════════════

  {PASS|WARN|FAIL} Core Files          {details}
  {PASS|WARN|FAIL} Commands            {N}/{total} found
  {PASS|WARN|FAIL} Agents              {N}/{total} found
  {PASS|WARN|FAIL} Placeholders        {N} unreplaced
  {PASS|WARN|FAIL} Agent Wiring        {N}/{total} verified
  {PASS|WARN|FAIL} Settings & Hooks    {N}/{total} hooks valid
  {PASS|WARN|FAIL} Context Detection   {details}
  {PASS|WARN|FAIL} Memory System       {N}/{total} files
  {PASS|WARN|FAIL} Skills              {details}
  {PASS|WARN|FAIL} Integrations        {details}

──────────────────────────────────────────────────────
  Total: {pass_count} passed, {warn_count} warnings, {fail_count} failures
══════════════════════════════════════════════════════
```

### 4. Show Issues (if any)

If there are FAIL or WARN results, list each issue with:
- **Category** (which check)
- **Severity** (FAIL or WARN)
- **File** (affected file path)
- **Issue** (what's wrong)
- **Fix** (how to resolve)

Example:
```
ISSUES FOUND:

  FAIL  Placeholders    .claude/commands/jira/pr-desc.md:70
        Issue: Unreplaced placeholder {YOUR_TYPE_CHECK_COMMAND}
        Fix: Replace with actual typecheck command (e.g., pnpm tsc --noEmit)

  WARN  Memory          .claude/memory/README.md
        Issue: File missing
        Fix: Run /setup:init to reinstall, or create manually
```

### 5. Show Summary

If all checks pass:
```
══════════════════════════════════════════════════════
  ALL CHECKS PASSED
  Your Claude workflow is fully configured.

  Quick start:
    /flow:plan "your feature description"
══════════════════════════════════════════════════════
```

If issues found:
```
══════════════════════════════════════════════════════
  {fail_count} issues need attention

  To fix automatically: /setup:init (safe — only fills gaps)
  To fix manually: see issue list above
══════════════════════════════════════════════════════
```

## Workflow Position

```
/setup:init → (complete) → /setup:audit
                               ↓
                    ALL PASS → /flow:plan
                    ISSUES  → fix manually or /setup:init
```
