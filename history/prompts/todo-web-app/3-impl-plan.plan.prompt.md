---
id: 3
title: impl-plan
stage: plan
date: 2026-02-05
surface: agent
model: Claude Sonnet 4.5
feature: todo-web-app
branch: 1-todo-web-app
user: user
command: /sp.plan "Todo Evolution Hackathon – Phase 2"
labels: [plan, architecture, design, todo-app]
links:
  spec: specs/1-todo-web-app/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/1-todo-web-app/plan.md
  - specs/1-todo-web-app/research.md
  - specs/1-todo-web-app/data-model.md
  - specs/1-todo-web-app/contracts/api-contract.yaml
  - specs/1-todo-web-app/quickstart.md
tests:
  - none
---

## Prompt

```
/sp.plan

Create a complete execution plan for:
Todo Evolution Hackathon – Phase 2: Intermediate Full-Stack Todo Web Application

This plan must strictly follow the approved /sp.constitution and /sp.specify.
The constitution has highest priority.

────────────────────────────────────────
1. Architecture Sketch (High-Level)
────────────────────────────────────────
Define a clear, spec-driven architecture covering:

- Monorepo layout:
  - /frontend → Next.js 16+ (App Router, TypeScript, Tailwind CSS, Framer Motion)
  - /backend → FastAPI (async), SQLModel, Neon PostgreSQL
  - /specs → Spec-Kit managed specs
  - /.claude/agents → reusable agents (exactly 6)
  - /.claude/skills → reusable skills (exactly 6)

- Frontend architecture:
  - Single dashboard page (/tasks)
  - Sidebar: search, filter, sort, language toggle (EN/UR), dark/light mode
  - Main area: task cards with priority badges, tag chips, due date
  - Inline add/edit (form or modal allowed, still single-page)
  - Voice commands via Web Speech API
  - API client layer attaching JWT automatically

- Backend architecture:
  - REST API under /api
  - JWT verification dependency on every route
  - Service layer reusable for Phase 3 chatbot / MCP tools
  - SQLModel models with async DB access
  - Strict user_id isolation from JWT

- Authentication flow:
  - Better Auth on frontend issues JWT
  - JWT sent via Authorization: Bearer <token>
  - Backend verifies using BETTER_AUTH_SECRET
  - Token expiry: 7 days

- Database architecture:
  - Neon Serverless PostgreSQL
  - tasks table only (users managed externally by Better Auth)
  - Indexes on user_id, completed, priority, due_date

────────────────────────────────────────
2. Agents & Skills Plan (Mandatory)
────────────────────────────────────────
Create and maintain EXACTLY these reusable agents:

Agents (in .claude/agents/, each with agent.md):
1. Frontend Engineer – UI, animations, accessibility, voice, i18n
2. Backend Engineer – FastAPI routes, services, validation
3. JWT/Auth Engineer – JWT verification, security, auth middleware
4. Database Engineer – SQLModel schema, queries, migrations
5. Spec Writer Engineer – constitution/spec/plan/tasks lineage
6. Integration Engineer – frontend-backend API client & contracts

Skills (in .claude/skills/, each with skill.md):
1. Frontend Engineer Skill
2. Backend Engineer Skill
3. JWT/Auth Engineer Skill
4. Database Engineer Skill
5. Spec Writer Engineer Skill
6. Integration Engineer Skill

Rules:
- Agents and skills must be reusable intelligence
- Agents may delegate to other agents
- All agents/skills must be added to main PHR history
- Creation/update rules must be documented in plan

────────────────────────────────────────
3. Feature Breakdown by Layer
────────────────────────────────────────
Frontend:
- Single-page dashboard
- CRUD tasks
- Priority badges (high/medium/low with fixed colors)
- Tags as editable chips
- Search (debounced)
- Filter (status, priority, tag, date)
- Sort (single active sort at a time)
- Dark/light mode (localStorage)
- Language toggle (English / Urdu)
- Voice commands (CRUD required, filter/sort optional)
- Loading states + error toasts

Backend:
- REST endpoints for tasks
- JWT-protected routes
- Validation rules (title length, tag count, enums)
- Graceful HTTPException handling
- Async SQLModel queries
- MCP-compatible service layer (no MCP server yet)

Database:
- Task model fields:
  id, user_id, title, completed, priority,
  tags, due_date, created_at, updated_at

────────────────────────
```

## Response snapshot

Successfully created a comprehensive implementation plan for the Todo Evolution Hackathon – Phase 2 project. The plan includes all required architectural components, data models, API contracts, and quickstart instructions. The architecture aligns with the constitution requirements including the monorepo structure with Next.js frontend and FastAPI backend, Better Auth integration, Neon PostgreSQL database, and the required 6 agents and 6 skills infrastructure. All specifications are properly linked and documented.

## Outcome

- ✅ Impact: Complete implementation architecture defined with all constitutional requirements met
- 🧪 Tests: none
- 📁 Files: 5 files created (plan.md, research.md, data-model.md, api-contract.yaml, quickstart.md)
- 🔁 Next prompts: /sp.tasks to generate implementation tasks
- 🧠 Reflection: Successfully created a comprehensive plan that satisfies all constitutional and specification requirements.

## Evaluation notes (flywheel)

- Failure modes observed: none
- Graders run and results (PASS/FAIL): PASS
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Begin task generation with /sp.tasks