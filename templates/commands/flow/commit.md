# /flow:commit - Context-Aware Commit

Stage changes and create a conventional git commit with smart message generation.

## Arguments

- `$ARGUMENTS` - Optional: commit type override, custom message, or context override

## Usage

```bash
/flow:commit                        # Auto-detect everything
/flow:commit [frontend] feat        # Frontend feature commit
/flow:commit [backend] fix          # Backend bug fix commit
/flow:commit "feat(auth): add login" # Custom message
```

## Instructions

### 1. Show Start Banner

```
═══════════════════════════════════════════════════
📝 Starting Commit
   └─ Detecting context...
═══════════════════════════════════════════════════
```

### 2. Check for Changes

```bash
git status --porcelain
```

If no changes: Report "Nothing to commit" and exit.

### 3. Detect Context

**Priority order:**
1. **Manual override**: `[frontend]` or `[backend]` in arguments
2. **From staged/changed files**: Analyze file extensions and paths

```bash
git diff --name-only HEAD
git diff --staged --name-only
```

| File Pattern | Context |
|--------------|---------|
| `{YOUR_FRONTEND_DIR}/` files | **Frontend** |
| `{YOUR_BACKEND_DIR}/` files | **Backend** |
| `.ts`, `.tsx`, `.css` | **Frontend** |
| `.cs`, `.py`, `.go`, `.java` | **Backend** |
| Mixed | **Fullstack** |

### 4. Stage All Changes

```bash
git add -A
```

### 5. Analyze Staged Changes

```bash
git diff --staged --stat
git diff --staged
git log --oneline -5
```

### 6. Invoke Git-Automator Agent

```
Use Task tool with subagent_type: "git-automator", model: "haiku"

Context: {Frontend | Backend | Fullstack}

Analyze the staged changes and create a conventional commit.

1. Determine commit type:
   - feat: New functionality
   - fix: Bug fixes
   - refactor: Code restructuring (no behavior change)
   - chore: Maintenance, dependencies, config
   - docs: Documentation only
   - test: Test additions/changes

2. Detect scope from file paths:
   - Group by feature area or module
   - Keep scope short and descriptive

3. Generate commit message:
   - First line: {type}({scope}): {description} (max 72 chars)
   - Blank line
   - Body: What changed and why (if non-trivial)
   - Always end with Co-Authored-By

4. Create commit using HEREDOC format
```

### 7. Create Commit

**Always use HEREDOC format:**

```bash
git commit -m "$(cat <<'EOF'
{type}({scope}): {description}

{Optional body}

Co-Authored-By: Claude <noreply@anthropic.com>
EOF
)"
```

### 8. Verify Commit

```bash
git log -1 --stat
```

### 9. Show Completion Banner

```
═══════════════════════════════════════════════════
        ✅ COMMIT CREATED
═══════════════════════════════════════════════════

{hash} {type}({scope}): {description}

Files changed: {N}
Insertions:    +{N}
Deletions:     -{N}

═══════════════════════════════════════════════════
              SUGGESTED NEXT STEPS
═══════════════════════════════════════════════════

1. PR:   /flow:pr
2. Push: git push

═══════════════════════════════════════════════════
```

## Commit Types

| Type | When to Use | Example |
|------|-------------|---------|
| `feat` | New feature | `feat(auth): add login flow` |
| `fix` | Bug fix | `fix(api): resolve null pointer` |
| `refactor` | Code restructuring | `refactor(ui): extract form components` |
| `chore` | Maintenance | `chore: update dependencies` |
| `docs` | Documentation | `docs: update API guide` |
| `test` | Test changes | `test(auth): add login unit tests` |

## Important Rules

- **Always stage all changes** with `git add -A`
- **Never skip hooks** (no `--no-verify`)
- **Always include Co-Authored-By** for Claude commits
- **Use HEREDOC** for commit messages
- **Keep first line under 72 characters**
- **Don't amend** unless explicitly requested

## Workflow Position

```
/flow:plan → /flow:implement → /flow:review → /flow:verify → /flow:commit → /flow:pr
                                                                  ↑
                                                              YOU ARE HERE
```

## Related

- **Agent**: `git-automator` - Handles git operations
- **Command**: `/flow:pr` - Create pull request after commit
