# /flow:pr - Create Pull Request

Create a pull request with context-aware description and formatting.

## Arguments

- `$ARGUMENTS` - Optional: base branch, context override

## Usage

```bash
/flow:pr                    # Auto-detect, PR to main
/flow:pr [frontend]         # Force frontend context
/flow:pr [backend]          # Force backend context
/flow:pr develop            # PR to develop branch
```

## Instructions

### 1. Show Start Banner

```
═══════════════════════════════════════════════════
🚀 Creating Pull Request
   └─ Detecting context...
═══════════════════════════════════════════════════
```

### 2. Detect Context & Gather Info

```bash
# Current branch
git branch --show-current

# Commits on branch
git log main...HEAD --oneline

# Changed files
git diff main...HEAD --stat
```

### 3. Invoke Git-Automator Agent

```
Use Task tool with subagent_type: "git-automator", model: "haiku"

Context: {Frontend | Backend | Fullstack}

Gather information and create a pull request.

1. Analyze all commits on branch:
   git log main...HEAD --oneline
   git diff main...HEAD --stat

2. Generate PR title:
   {type}({scope}): {description}
   - Keep under 70 characters

3. Generate PR description:

## Summary
{1-2 sentence overview of what this PR does}

## Changes
### Added
- {New feature/component}

### Changed
- {Modified behavior}

### Fixed
- {Bug fix}

## Testing
- [ ] {YOUR_TYPE_CHECK_COMMAND} passes
- [ ] {YOUR_LINT_COMMAND} passes
- [ ] {YOUR_BUILD_COMMAND} succeeds
- [ ] Tested locally

## Checklist
- [ ] Follows project conventions (see CLAUDE.md)
- [ ] No debug code left in
- [ ] Self-reviewed the diff

---
Generated with Claude Code

4. Push branch and create PR:
   git push -u origin HEAD
   gh pr create --title "{title}" --body "{body}" --base {base}
```

### 4. Push and Create PR

```bash
git push -u origin HEAD

gh pr create \
  --title "{type}({scope}): {description}" \
  --body "$(cat <<'EOF'
{generated PR description}
EOF
)" \
  --base {base_branch}
```

### 5. Show Completion Banner

```
═══════════════════════════════════════════════════
        ✅ PULL REQUEST CREATED
═══════════════════════════════════════════════════

#{number}: {title}
URL: {pr_url}

Base: {base} ← {branch}
Commits: {N}
Files changed: {N}

═══════════════════════════════════════════════════
        ✓ WORKFLOW COMPLETE
═══════════════════════════════════════════════════
```

## Error Handling

| Error | Action |
|-------|--------|
| No commits on branch | Show message, suggest committing first |
| Branch already has PR | Show existing PR URL, ask to update |
| Push fails | Check remote, show error |
| gh not authenticated | Show `gh auth login` command |

## Customization

Update the PR description template to match your team's conventions:
- Add your required checklist items
- Include your testing checklist (`{YOUR_TEST_COMMAND}`)
- Add any required review steps

## Workflow Position

```
/flow:plan → /flow:implement → /flow:review → /flow:verify → /flow:commit → /flow:pr
                                                                               ↑
                                                                           YOU ARE HERE
                                                                               ✓ DONE
```

## Related

- **Agent**: `git-automator` - Handles git operations
- **Command**: `/flow:commit` - Create commit before PR
