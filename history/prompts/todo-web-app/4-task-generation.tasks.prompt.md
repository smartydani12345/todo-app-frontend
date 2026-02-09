---
id: 4
title: task-generation
stage: tasks
date: 2026-02-05
surface: agent
model: Claude Sonnet 4.5
feature: todo-web-app
branch: 1-todo-web-app
user: user
command: /sp.tasks "Todo Evolution Hackathon – Phase 2"
labels: [tasks, implementation, todo-app]
links:
  spec: specs/1-todo-web-app/spec.md
  plan: specs/1-todo-web-app/plan.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-todo-web-app/tasks.md
tests:
  - none
---

## Prompt

```
─────────────────────────────────────
1. Create .claude/agents folder
   Acceptance: Folder exists at .claude/agents

2. Create Frontend Engineer agent
   - Path: .claude/agents/frontend-engineer/agent.md
   Acceptance: agent.md defines role, responsibilities, delegation rules

3. Create Backend Engineer agent
   - Path: .claude/agents/backend-engineer/agent.md
   Acceptance: agent.md defines FastAPI + service-layer focus

4. Create JWT/Auth Engineer agent
   - Path: .claude/agents/jwt-auth-engineer/agent.md
   Acceptance: agent.md defines JWT verification + security scope

5. Create Database Engineer agent
   - Path: .claude/agents/database-engineer/agent.md
   Acceptance: agent.md defines SQLModel + Neon responsibilities

6. Create Spec Writer Engineer agent
   - Path: .claude/agents/spec-writer-engineer/agent.md
   Acceptance: agent.md defines spec/plan/tasks lineage rules

7. Create Integration Engineer agent
   - Path: .claude/agents/integration-engineer/agent.md
   Acceptance: agent.md defines frontend-backend contract ownership

🔎 CHECKPOINT 1: Review all agent definitions before proceeding

────────────────────────────────────────
SECTION 2: REUSABLE SKILLS CREATION
────────────────────────────────────────
8. Create .claude/skills folder
   Acceptance: Folder exists at .claude/skills

9. Create Frontend Engineer Skill
   - Path: .claude/skills/frontend-engineer/skill.md
   Acceptance: skill.md documents UI/UX + animation patterns

10. Create Backend Engineer Skill
    - Path: .claude/skills/backend-engineer/skill.md
    Acceptance: skill.md documents route + service patterns

11. Create JWT/Auth Engineer Skill
    - Path: .claude/skills/jwt-auth-engineer/skill.md
    Acceptance: skill.md documents JWT validation logic

12. Create Database Engineer Skill
    - Path: .claude/skills/database-engineer/skill.md
    Acceptance: skill.md documents SQLModel + async queries

13. Create Spec Writer Engineer Skill
    - Path: .claude/skills/spec-writer-engineer/skill.md
    Acceptance: skill.md documents spec-driven workflow

14. Create Integration Engineer Skill
    - Path: .claude/skills/integration-engineer/skill.md
    Acceptance: skill.md documents API client integration

🔎 CHECKPOINT 2: Confirm all 6 agents + 6 skills exist and are reusable

────────────────────────────────────────
SECTION 3: ENVIRONMENT & CONFIGURATION
────────────────────────────────────────
15. Plan and create .env file
    Acceptance: .env contains BETTER_AUTH_SECRET, DATABASE_URL, NEXT_PUBLIC_API_URL

16. Configure backend to read DATABASE_URL from env
    Acceptance: Backend connects without hardcoded secrets

17. Configure frontend to read NEXT_PUBLI─────
21. Create JWT verification dependency
    Acceptance: Requests without JWT return 401

22. Implement Create Task endpoint
    Acceptance: Task saved for authenticated user only

23. Implement Get Tasks endpoint (search/filter/sort)
    Acceptance: Only user's tasks returned, filters applied

24. Implement Update Task endpoint
    Acceptance: Only owner can update task

25. Implement Delete Task endpoint
    Acceptance: Only owner can delete task

26. Implement Toggle Complete endpoint
    Acceptance: completed state toggles correctly

27. Add validation rules (title length, tags count, enums)
    Acceptance: Invalid input returns 422

🔎 CHECKPOINT 4: Backend APIs tested manually

────────────────────────────────────────
SECTION 6: FRONTEND DASHBOARD (NEXT.JS)
────────────────────────────────────────
28. Setup Next.js App Router structure
    Acceptance: /tasks page renders

29. Implement API client with JWT attachment
    Acceptance: All requests include Authorization header

30. Build single-page dashboard layout
    Acceptance: Sidebar + main task area visible

31. Implement task list with cards
    Acceptance: Cards show title, priority badge, tags

32. Implement add/edit task form
    Acceptance: User can create and edit tasks inline or via modal

33. Implement delete & complete actions
    Acceptance: UI updates immediately on action

34. Implement search with debounce
    Acceptance: Search triggers after defined delay

35. Implement filter & sort controls
    Acceptance: Only one active sort applied

36. Implement dark/light mode toggle
    Acceptance: Preference stored in localStorage

37. Implement language toggle (English / Urdu)
    Acceptance: UI text switches language

38. Implement voice commands (CRUD)
    Acceptance: Voice can add/update/delete tasks

39. Add animations (Framer Motion)
    Acceptance: Add = fade-in, de
```

## Response snapshot

Successfully generated comprehensive implementation tasks for the Todo Evolution Hackathon – Phase 2 project. The tasks.md file contains 85 detailed, sequential tasks organized by user story in priority order. The tasks cover all required components from foundational infrastructure through advanced UX features. Each task follows the required checklist format with proper IDs, story labels, and file paths. The implementation strategy follows MVP-first approach with clear dependencies and parallel execution opportunities identified.

## Outcome

- ✅ Impact: Complete task breakdown ready for implementation with clear execution order
- 🧪 Tests: none
- 📁 Files: 1 file created (tasks.md) with 85 detailed implementation tasks
- 🔁 Next prompts: /sp.implement to begin execution of tasks
- 🧠 Reflection: Successfully created actionable task list that follows specification requirements and implementation strategy.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin task execution with /sp.implement