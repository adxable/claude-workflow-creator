# 08 — Chrome Extension: Browser Automation

The Claude in Chrome extension enables visual verification of your UI directly from Claude Code. It integrates a fix-verify loop: screenshot → analyze → fix → re-screenshot.

## Prerequisites

Install the Claude Chrome extension from the Chrome Web Store, or from source:
- Extension name: "Claude in Chrome" (by Anthropic)

Once installed, Claude Code gets access to `mcp__claude-in-chrome__*` tools.

---

## What It Enables

### 1. Visual Verification After Implementation

```bash
/flow:verify [frontend] --browser /dashboard
```

Claude will:
1. Start your dev server if not running
2. Navigate to the specified URL
3. Take a screenshot
4. Analyze for visual issues
5. Fix any problems found
6. Re-verify (up to 5 iterations)

### 2. Browser Investigation for Requirements

```bash
/frontend:investigate http://your-staging.com/new-feature
```

Claude will:
1. Navigate to the URL
2. Screenshot multiple viewport sizes
3. Read the DOM for component structure
4. Read network requests to understand API calls
5. Report findings as requirements

### 3. E2E Feature Testing

```bash
/frontend:e2e "User can add a new product"
```

Claude will navigate, click, fill forms, and verify the result visually.

---

## Available Tools

| Tool | What It Does |
|------|-------------|
| `mcp__claude-in-chrome__navigate` | Navigate to URL |
| `mcp__claude-in-chrome__computer` | Take screenshots |
| `mcp__claude-in-chrome__read_page` | Read page DOM |
| `mcp__claude-in-chrome__find` | Find element |
| `mcp__claude-in-chrome__form_input` | Fill form inputs |
| `mcp__claude-in-chrome__read_network_requests` | Read network activity |
| `mcp__claude-in-chrome__read_console_messages` | Read console output |
| `mcp__claude-in-chrome__tabs_context_mcp` | Get open tabs info |
| `mcp__claude-in-chrome__tabs_create_mcp` | Open new tab |
| `mcp__claude-in-chrome__gif_creator` | Record interaction as GIF |
| `mcp__claude-in-chrome__javascript_tool` | Execute JavaScript |

---

## Fix-Verify Loop

The core pattern for browser verification:

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ Screenshot  │ ──▶ │   Analyze   │ ──▶ │    Fix      │
│             │     │   Issues    │     │    Code     │
└─────────────┘     └──────┬──────┘     └──────┬──────┘
       ▲                    │                    │
       │                    │ No Issues          │
       │                    ▼                    │
       │             ┌─────────────┐             │
       └─────────────│  Re-verify  │◀────────────┘
                     └─────────────┘
                           │
                           │ All Pass
                           ▼
                       ┌─────────┐
                       │  Done   │
                       └─────────┘
Max iterations: 5 per issue
```

### Implementing in the `browser-tester` Agent

```markdown
# Browser Tester Agent

## Process

1. Load mcp__claude-in-chrome__tabs_context_mcp
2. Create new tab: mcp__claude-in-chrome__tabs_create_mcp
3. Navigate: mcp__claude-in-chrome__navigate with URL
4. Wait for load: mcp__claude-in-chrome__read_page
5. Screenshot: mcp__claude-in-chrome__computer

## Analysis Checklist
- [ ] Page loads without errors
- [ ] Components render correctly
- [ ] No console errors (check with read_console_messages)
- [ ] Buttons/forms are interactive
- [ ] Layout looks correct on multiple viewports

## Fix Loop (max 5 iterations)
If issues found:
- Fix the code
- Re-navigate and re-screenshot
- Re-check until passing
```

---

## Integration with `/flow:verify`

Add browser verification as an optional step in your verify command:

```markdown
## Step 3d: Browser Verification (if --browser flag)

Only run when `--browser` flag is present.

1. Ensure dev server is running:
   ```bash
   pnpm dev &
   sleep 3
   ```

2. Invoke browser-tester agent:
   Use Task tool with subagent_type: "browser-tester"
   URL: http://localhost:3000{url_path}
   Task: Visual verification — screenshot, analyze, fix loop
```

---

## PM Workflow: URL Investigation

When generating stories from a URL, the browser is used for discovery:

```bash
/pm:gen-stories-from-url http://staging.yourapp.com/orders "Add bulk export"
```

Claude will:
1. Navigate to the URL
2. Screenshot the current state
3. Read the DOM to understand components
4. Read network requests to understand API shape
5. Use findings to write accurate user stories

Screenshots are saved to `.claude/screenshots/{feature}/before/`.

---

## GIF Recording

For documenting interactions to share with the team:

```markdown
# Record a GIF of the feature

Use mcp__claude-in-chrome__gif_creator to record the interaction.

## Instructions
1. Start recording: gif_creator with name "feature-demo.gif"
2. Take extra frames before and after each action
3. Navigate, click, and interact as needed
4. Save to .claude/screenshots/demos/feature-demo.gif
```

---

## Session Startup Pattern

Always call `tabs_context_mcp` at the start of browser sessions — never reuse tab IDs from previous sessions:

```markdown
## Browser Session Rules
1. Call mcp__claude-in-chrome__tabs_context_mcp to see current tabs
2. Create a new tab with tabs_create_mcp for fresh state
3. Never reuse tab IDs from previous operations
4. If a tab operation fails, call tabs_context_mcp again for fresh IDs
```

---

## Troubleshooting

**Extension not connecting:** Ensure Claude Code is running and the extension is enabled in Chrome.

**Tab not responding:** Dismiss any JavaScript alert dialogs in the browser manually — they block all browser events.

**Screenshots blank:** Add a wait step after navigation before taking screenshots.

---

**Setup Complete** — Return to `guide/00-brainstorm.md` to generate your custom setup plan.
