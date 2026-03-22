# CLAUDE.md — RPG Task Manager

This file provides guidance for AI assistants (Claude and others) working on this repository.

---

## Project Overview

**RPG Task Manager** is a gamified task management application that applies RPG (role-playing game) mechanics to productivity. Users gain experience points (XP), level up, complete quests (tasks), and manage a character/party as they accomplish real-world goals.

This repository is in its **initial state** — no source code has been committed yet. This document should be updated as the codebase grows.

---

## Repository Status

- **Current state**: Empty repository, initial setup phase
- **Branch**: `claude/add-claude-documentation-wLgsM`
- **Remote**: `http://local_proxy@127.0.0.1:32885/git/ssto2222/Rpg_task_manager`

---

## Intended Architecture (To Be Confirmed)

The following is the anticipated structure based on the project name. Update this section once the technology stack is decided and scaffolded.

```
Rpg_task_manager/
├── CLAUDE.md              # This file
├── README.md              # Project overview for humans
├── .gitignore
├── src/                   # Main application source
│   ├── models/            # Data models (Task, Character, Quest, etc.)
│   ├── services/          # Business logic layer
│   ├── controllers/       # Request handlers / route controllers
│   ├── views/             # UI templates or frontend components
│   └── utils/             # Shared utilities and helpers
├── tests/                 # Test suite
│   ├── unit/
│   └── integration/
├── docs/                  # Additional documentation
└── config/                # Configuration files
```

---

## Development Workflow

### Branching Strategy

- `main` — stable, production-ready code; never commit directly
- `develop` — integration branch; merge feature branches here
- `feature/<description>` — new features
- `fix/<description>` — bug fixes
- `claude/<description>` — branches for AI-assisted work

### Commit Convention

Use [Conventional Commits](https://www.conventionalcommits.org/):

```
<type>(<scope>): <short description>

[optional body]
```

Types: `feat`, `fix`, `docs`, `style`, `refactor`, `test`, `chore`

Examples:
```
feat(quests): add XP reward calculation on task completion
fix(character): correct level-up threshold off-by-one error
docs: update CLAUDE.md with API conventions
test(tasks): add unit tests for task priority sorting
```

### Making Changes

1. Create a feature branch from `develop` (or `main` if no `develop` exists yet)
2. Make focused, small commits
3. Ensure tests pass before pushing
4. Open a pull request with a clear description

---

## Key Domain Concepts

Understanding these concepts is essential for working on this codebase:

| Concept | Description |
|---------|-------------|
| **Task** | A real-world to-do item the user needs to complete |
| **Quest** | A collection of related tasks forming a larger goal |
| **XP (Experience Points)** | Reward for completing tasks; drives leveling |
| **Level** | Character progression milestone based on accumulated XP |
| **Character** | The user's in-app avatar with stats, level, and inventory |
| **Party** | Group of characters (useful for team/collaborative features) |
| **Skill** | Special abilities unlocked through completing task categories |
| **Inventory** | Items earned as rewards for completing quests/tasks |

---

## Coding Conventions

These conventions should be followed once the stack is chosen. Update this section with language/framework-specific rules.

### General

- Keep functions small and single-purpose
- Prefer explicit over implicit behavior
- Write code that reads like prose where possible
- Avoid premature optimization; favor clarity

### Naming

- **Variables/Functions**: `camelCase` (JS/TS) or `snake_case` (Python)
- **Classes/Types**: `PascalCase`
- **Constants**: `UPPER_SNAKE_CASE`
- **Files**: `kebab-case` for components/modules, `PascalCase` for class files

### Domain Naming Examples

```
// Good — domain language is clear
calculateXpReward(task)
levelUpCharacter(character, xp)
completeQuest(questId)

// Avoid — too generic
processItem(item)
update(data)
handle(input)
```

---

## Testing

- Write tests for all business logic (XP calculation, leveling thresholds, quest completion)
- Test file should mirror source file location:
  - `src/services/xp-service.js` → `tests/unit/services/xp-service.test.js`
- Use descriptive test names following `should <behavior> when <condition>` pattern:
  ```
  "should award 50 XP when a high-priority task is completed"
  "should not level up when XP is below threshold"
  ```

---

## Environment Setup

> **Note**: Update this section once the stack is chosen.

Typical setup steps expected for this project:

```bash
# Clone the repository
git clone <repo-url>
cd Rpg_task_manager

# Install dependencies (Node.js example)
npm install
# or for Python:
pip install -r requirements.txt

# Copy environment config
cp .env.example .env

# Run development server
npm run dev

# Run tests
npm test
```

---

## For AI Assistants

When working on this repository:

1. **Read this file first** before making any changes
2. **Update this file** when you introduce new patterns, conventions, or significant structure
3. **Prefer editing existing files** over creating new ones unless structure demands it
4. **Keep changes focused** — implement only what is requested
5. **Check for existing patterns** before introducing new abstractions
6. **Domain vocabulary matters** — use the RPG terminology defined above consistently
7. **Never commit secrets** — `.env` files, API keys, credentials must never be committed
8. **Run tests before pushing** — do not push code with failing tests

### Common Tasks for AI

- Adding a new task type: check `src/models/` for existing model patterns
- Adding XP logic: business logic lives in `src/services/`
- Adding API endpoints: follow controller patterns in `src/controllers/`
- Adding UI components: check existing component structure in `src/views/`

---

## Questions / Unknowns

These should be resolved before significant development begins:

- [ ] What is the primary technology stack? (Node.js/React, Python/Django, etc.)
- [ ] Is this a web app, CLI tool, mobile app, or desktop app?
- [ ] Is there a database? If so, which one (PostgreSQL, SQLite, MongoDB)?
- [ ] Is there a REST API, GraphQL API, or is it a monolith?
- [ ] Are there multiplayer/social features planned?
- [ ] What is the deployment target (cloud, self-hosted, local-only)?

---

*Last updated: 2026-03-22 — Initial CLAUDE.md created for empty repository.*
