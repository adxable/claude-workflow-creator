# 02 — Context Detector: Auto-Detect Your Work Context

The context detector is a Python script that automatically determines whether you're working on frontend, backend, or another context based on file paths, extensions, and keywords in your prompt.

## How It Works

```
User prompt: "Add a filter to the orders table"
                 ↓
         detector.py runs
                 ↓
   Scores each context (frontend: 9, backend: 2)
                 ↓
   Returns: { context: "frontend", confidence: 85% }
                 ↓
   Commands dispatch to the right agent/tools
```

The scoring algorithm checks three signal types:
1. **Path signals** (strongest, +10 each): File paths like `src/components/` or `api/controllers/`
2. **Extension signals** (+5 each): `.tsx`, `.cs`, `.py`, `.go`
3. **Keyword signals** (+3 each): "React", "component", "service", "endpoint"

---

## Files

```
.claude/contexts/
├── detector.py          ← The scoring engine
├── frontend.yaml        ← Frontend indicators + tools + skills
└── backend.yaml         ← Backend indicators + tools + skills
```

The generic detector implementation is in `templates/contexts/detector.py` — copy it and it reads from any YAML config files you create.

---

## Setting Up for Your Stack

### Step 1: Copy the detector

```bash
mkdir -p .claude/contexts
cp .claude/claude-init/templates/contexts/detector.py .claude/contexts/detector.py
```

The detector is generic — it reads from YAML config files, so you don't need to modify the Python.

### Step 2: Create your context YAML files

Copy the template and customize:

```bash
cp .claude/claude-init/templates/contexts/context-template.yaml .claude/contexts/frontend.yaml
cp .claude/claude-init/templates/contexts/context-template.yaml .claude/contexts/backend.yaml
```

### Step 3: Customize the YAMLs

**Example: React/TypeScript frontend**

```yaml
# .claude/contexts/frontend.yaml
name: frontend
description: React/TypeScript frontend

indicators:
  paths:
    - "src/components"
    - "src/pages"
    - "src/features"
    - "src/app"
  extensions:
    - ".tsx"
    - ".ts"
    - ".css"
    - ".scss"
  keywords:
    - "React"
    - "component"
    - "hook"
    - "form"
    - "table"
    - "modal"
    - "page"

project_root: "frontend/"

tools:
  verify:
    - "npm run typecheck"
    - "npm run lint"
    - "npm run build"
  test: "npm test"
  start: "npm run dev"

skills:
  - frontend/react-patterns
  - workflow/code-quality-rules

agents:
  planner: planner-fe
  implementer: implementer-fe
  reviewer: code-reviewer-fe
```

**Example: Node.js/Express backend**

```yaml
# .claude/contexts/backend.yaml
name: backend
description: Node.js/Express API

indicators:
  paths:
    - "src/routes"
    - "src/controllers"
    - "src/services"
    - "src/models"
  extensions:
    - ".ts"
  keywords:
    - "endpoint"
    - "route"
    - "controller"
    - "service"
    - "middleware"
    - "database"

project_root: "backend/"

tools:
  verify:
    - "npm run build"
    - "npm test"
  test: "npm test"

skills:
  - backend/node-patterns

agents:
  planner: planner-be
  implementer: implementer-be
```

**Example: .NET/C# backend**

```yaml
# .claude/contexts/backend.yaml
name: backend
description: .NET/C# API

indicators:
  paths:
    - "src/services"
    - "src/controllers"
    - "src/models"
    - "src/repositories"
    - ".chp"              # CodeHelper entity definitions
  extensions:
    - ".cs"
    - ".csproj"
    - ".sln"
  keywords:
    - "service"
    - "controller"
    - "endpoint"
    - "entity"
    - "repository"
    - "migration"
    - "dotnet"
    - ".NET"

project_root: "src/"

tools:
  verify:
    - "dotnet build --property WarningLevel=0"
    - "dotnet test"
  test: "dotnet test"

skills:
  - backend/dotnet-patterns
  - workflow/code-quality-rules

agents:
  planner: planner-be
  implementer: implementer-be
  reviewer: code-reviewer-be
```

**Example: Python/FastAPI backend**

```yaml
# .claude/contexts/backend.yaml
name: backend
description: Python/FastAPI API

indicators:
  paths:
    - "app/routers"
    - "app/services"
    - "app/models"
    - "app/schemas"
  extensions:
    - ".py"
  keywords:
    - "endpoint"
    - "route"
    - "service"
    - "schema"
    - "pydantic"
    - "alembic"
    - "migration"

project_root: "backend/"

tools:
  verify:
    - "mypy app/"
    - "ruff check app/"
    - "pytest"
  test: "pytest"
  start: "uvicorn app.main:app --reload"

skills:
  - backend/python-patterns

agents:
  planner: planner-be
  implementer: implementer-be
  reviewer: code-reviewer-be
```

---

## Using the Detector in Commands

Commands call the detector to route to the right agent. The detection is embedded in each command's instructions. Here's the pattern:

```markdown
## Instructions

### 1. Detect Context

**Priority order:**
1. Manual override: `[frontend]` or `[backend]` in the prompt
2. Run context detection on the prompt text
3. Ask user if score is below 30 (ambiguous)

| Indicators | Context |
|------------|---------|
| .tsx, .ts in src/components | Frontend |
| .ts in src/routes, src/controllers | Backend |
| Both or unclear | Ask user |
```

---

## Testing the Detector

```bash
# Test from your project root
cd .claude
python contexts/detector.py "Add a new React component"
# → Detected: frontend (confidence: 75%)

python contexts/detector.py "Add a POST endpoint for orders"
# → Detected: backend (confidence: 65%)

python contexts/detector.py "Update the README"
# → Detected: unknown (confidence: 0%)
```

---

## Adding More Contexts

You can add as many contexts as needed — just create more YAML files:

```bash
.claude/contexts/
├── detector.py
├── frontend.yaml
├── backend.yaml
├── mobile.yaml        # React Native
└── infrastructure.yaml # Terraform/K8s
```

The detector scores all contexts and returns the highest.

---

## Disabling Context Detection

If you have a single-context project (e.g., frontend-only), you can skip context detection entirely. Just hardcode the context in your commands instead of dispatching dynamically.

---

**Next Step →** `guide/03-agents.md`
