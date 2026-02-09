# Implementation Plan: Todo Evolution Hackathon – Phase 2

## Technical Context

**Feature**: Todo Evolution Hackathon – Phase 2: Intermediate Full-Stack Todo Web Application
**Architecture**: Monorepo with /frontend (Next.js 16+) and /backend (FastAPI)
**Database**: Neon Serverless PostgreSQL
**Authentication**: Better Auth with JWT
**Environment**: Node.js 18+/Python 3.11+

**Unknowns**:
- Specific deployment strategy details
- Exact CORS configuration requirements
- Production build optimization settings

## Constitution Check

### Spec-Driven Development (NON-NEGOTIABLE)
- All code must be generated via /sp.implement after constitution, specify, plan, and tasks are defined and refined
- No manual code writing allowed without proper task breakdown
- **Post-Design Verification**: Plan includes comprehensive task breakdown via API contracts and data models

### Enhanced Technology Stack
- Frontend – Next.js 16+ (App Router, TypeScript, Tailwind CSS for responsive design, Framer Motion for animations)
- Backend – FastAPI, SQLModel for ORM, Neon Serverless PostgreSQL
- **Post-Design Verification**: Both frontend and backend technologies implemented as specified in contracts and data models

### Authentication with Better Auth (SECURITY-CRITICAL)
- Better Auth with JWT (BETTER_AUTH_SECRET=1J9sGzWBBciZ9w93jdsAI4jPvG1qkLpU)
- All APIs JWT-required with 401/403 errors
- User_id isolation enforced across all operations
- **Post-Design Verification**: API contracts specify JWT security scheme and user_id isolation in data model

### Data Persistence with User Isolation
- Persist tasks in Neon DB using SQLModel
- Always filter by authenticated user_id
- No cross-user data leaks allowed
- **Post-Design Verification**: Data model includes user_id foreign key with access control rules, indexes for performance

### Modular and Reusable Design with Extensibility
- Create and maintain exactly 6 agents and 6 skills as specified
- Reuse core logic in backend routes
- Make code extensible for Phase 3 chatbot
- **Post-Design Verification**: Plan includes service layer architecture for reusability and agent-specific guidelines

### Intermediate Features Implementation
- Implement priorities (high/medium/low with color badges)
- Tags/Categories (work/home as editable chips)
- Search (keyword in title/description)
- Filter (by status/priority/tag/date)
- Sort (by due_date/priority/alphabetical ascending/descending)
- **Post-Design Verification**: API contracts and data models include all required features with proper validation rules

## Gates

### Gate 1: Architecture Alignment ✅
The planned architecture aligns with constitution requirements:
- Monorepo structure with separate frontend/backend
- Specified technology stack (Next.js 16+, FastAPI, SQLModel, Neon)
- Proper authentication and data isolation

### Gate 2: Security Compliance ✅
The planned security measures meet constitutional requirements:
- JWT-based authentication on all routes
- User_id isolation across all operations
- Secure token handling

### Gate 3: Agent/Skill Requirements ✅
Plan addresses all 12 required components:
- 6 Agents in .claude/agents/ with agent.md files
- 6 Skills in .claude/skills/ with skill.md files

### Gate 4: Feature Completeness ✅
All intermediate features planned:
- Priorities with visual badges
- Tag management
- Search, filter, and sort capabilities
- Single dashboard interface

## Phase 0: Outline & Research

### Research Task 1: Next.js 16+ Best Practices
- Decision: Use App Router with server components for performance
- Rationale: Leverages latest Next.js features, better performance
- Alternatives considered: Pages router (legacy approach)

### Research Task 2: Better Auth Integration Patterns
- Decision: Frontend JWT issuance with backend verification
- Rationale: Follows security best practices, maintains session state
- Alternatives considered: Custom JWT management (higher complexity)

### Research Task 3: SQLModel Async Operations
- Decision: Use async SQLAlchemy operations with proper connection pooling
- Rationale: Ensures scalability and prevents blocking operations
- Alternatives considered: Synchronous operations (performance concerns)

### Research Task 4: Framer Motion Animation Patterns
- Decision: Page transitions and micro-interactions for task operations
- Rationale: Enhances UX with smooth animations
- Alternatives considered: CSS-only animations (less flexible)

### Research Task 5: Task Filtering and Sorting Architecture
- Decision: Client-side filtering with debounced search and backend pagination
- Rationale: Balances performance and user experience
- Alternatives considered: Full backend filtering (higher latency)

## Phase 1: Design & Contracts

### Data Model: Task Entity

**Fields**:
- id: UUID (Primary Key)
- user_id: UUID (Foreign Key to Better Auth user)
- title: String(1-100) - Required
- description: String(0-1000) - Optional
- completed: Boolean - Default: False
- priority: Enum('high', 'medium', 'low') - Default: 'medium'
- tags: JSON Array[String] - Optional, Max 10 tags
- due_date: DateTime - Optional
- created_at: DateTime - Auto-generated
- updated_at: DateTime - Auto-generated

**Validation**:
- Title: 1-100 characters
- Description: 0-1000 characters
- Priority: Must be 'high', 'medium', or 'low'
- Tags: Array of 1-50 character strings, max 10 items
- Due date: Must be future date if provided

**Relationships**:
- One User (via Better Auth) to Many Tasks
- Indexes on: user_id, completed, priority, due_date

### API Contracts

#### Authentication Routes
- POST /api/auth/login - User login (handled by Better Auth)
- POST /api/auth/register - User registration (handled by Better Auth)
- GET /api/auth/me - Get current user (handled by Better Auth)

#### Task Management Routes
- GET /api/tasks - Retrieve user's tasks with filtering/sorting/search
- POST /api/tasks - Create new task
- GET /api/tasks/{task_id} - Get specific task
- PUT /api/tasks/{task_id} - Update task
- DELETE /api/tasks/{task_id} - Delete task
- PATCH /api/tasks/{task_id}/complete - Mark task as complete/incomplete

#### Query Parameters
- filter: {status, priority, tag, date}
- sort: {due_date, priority, title, created_at}
- search: {keyword}
- page: {number}
- limit: {number}

### Frontend Components Architecture

#### Dashboard Layout
- Header: Navigation, user profile, theme toggle
- Sidebar: Search, filters, sort options, language toggle
- Main Content: Task grid/list view with priority badges and tag chips
- Footer: Status information, additional controls

#### Task Card Component
- Priority badge (colored according to specification: high=red, medium=yellow, low=green)
- Title and description preview
- Tag chips (editable)
- Due date display
- Action buttons (edit, delete, toggle complete)

#### Form Components
- Task creation/editing form
- Inline editing capability
- Validation and error handling
- Keyboard navigation support

## Quickstart Guide

### Prerequisites
- Node.js 18+ for frontend
- Python 3.11+ for backend
- PostgreSQL-compatible database (Neon recommended)
- Better Auth account configuration

### Setup Instructions

1. **Clone Repository**
   ```bash
   git clone <repo-url>
   cd <repo-name>
   ```

2. **Backend Setup**
   ```bash
   cd backend
   pip install -r requirements.txt
   cp .env.example .env
   # Update environment variables in .env
   python -m backend.main
   ```

3. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   cp .env.example .env.local
   # Update environment variables in .env.local
   npm run dev
   ```

4. **Environment Variables**
   - BETTER_AUTH_SECRET: Secret key for JWT signing
   - DATABASE_URL: Neon PostgreSQL connection string
   - NEXT_PUBLIC_API_URL: Backend API endpoint

### Development Commands
- Backend: `python -m backend.main` (development server)
- Frontend: `npm run dev` (development server)
- Tests: `npm run test` (frontend), `pytest` (backend)

## Agent Context Updates

### Frontend Engineer Agent
- Focus on Next.js 16+ App Router implementation
- Implement Tailwind CSS responsive design
- Integrate Framer Motion animations for UX
- Handle voice commands via Web Speech API
- Implement i18n support for EN/UR

### Backend Engineer Agent
- Develop FastAPI REST endpoints
- Implement async SQLModel database operations
- Ensure proper validation and error handling
- Create reusable service layer for Phase 3

### JWT/Auth Engineer Agent
- Implement JWT verification middleware
- Enforce user_id isolation
- Handle token refresh strategies
- Manage secure authentication flow

### Database Engineer Agent
- Design SQLModel schemas
- Implement async query patterns
- Create proper indexes for performance
- Handle data migration strategies

### Spec Writer Engineer Agent
- Maintain spec/plan/task lineage
- Ensure constitution compliance
- Document decisions and rationale

### Integration Engineer Agent
- Create frontend-backend API client
- Manage contract definitions
- Handle error states and loading states

## Next Steps

1. **Complete Task Generation**: Run `/sp.tasks` to generate implementation tasks
2. **Review Architecture**: Validate with stakeholders
3. **Begin Implementation**: Use `/sp.implement` to execute tasks
4. **Continuous Validation**: Ensure all implementations meet constitutional requirements