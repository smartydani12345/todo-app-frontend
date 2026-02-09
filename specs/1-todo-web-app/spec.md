# Phase 2: Full-Stack Todo Web Application Specification

## Overview
Transforming Phase 1 console app into a modern multi-user web application with persistent storage and intermediate organization features. Implements a strong, beautiful (khoobsoorat), responsive single-page dashboard where all features are accessible in an easy, aligned manner (sub kaam align wise ho, no missing elements) for handling complex tasks simply.

## User Scenarios & Testing
- **Scenario 1**: New user signs up for the application, creates tasks with priorities and tags, and manages them through the dashboard interface
- **Scenario 2**: Existing user logs in, searches for specific tasks, filters by priority/date, sorts by various criteria, and marks tasks as complete
- **Scenario 3**: User manages tasks on mobile device, benefits from responsive design and smooth animations
- **Scenario 4**: User experiences dark/light mode toggle and benefits from intuitive navigation

## Functional Requirements
- FR-001: User registration and authentication with Better Auth/JWT
- FR-002: User login/logout functionality with secure token handling
- FR-003: Create new tasks with title (1-100 characters), description (up to 1000 characters), priority (high/medium/low) with visual badges (high: bg-red-100 text-red-800, medium: bg-yellow-100 text-yellow-800, low: bg-green-100 text-green-800), tags (comma-separated input with validation and auto-suggestions), and optional due date
- FR-004: View list of user's tasks with priority badges and tag chips
- FR-005: Update existing tasks including title, description, priority, tags, and completion status
- FR-006: Delete tasks with confirmation
- FR-007: Mark tasks as complete/incomplete
- FR-008: Search tasks by keyword in title/description with 300ms debounce time to balance responsiveness with performance
- FR-009: Filter tasks by status (complete/incomplete), priority, tag, or date
- FR-010: Sort tasks by due date, priority, or alphabetically
- FR-011: Real-time dashboard updates reflecting all task operations
- FR-012: Responsive design supporting mobile and desktop views
- FR-013: Dark/light mode toggle with localStorage persistence, defaulting to light mode but detecting system preference with option to sync with system settings
- FR-014: Loading indicators during API operations
- FR-015: Error notifications/toasts for failed operations
- FR-016: Data isolation ensuring users only see their own tasks
- FR-017: Handle edge cases like empty task list, invalid tokens, no search results
- FR-018: When JWT tokens expire, show login modal/prompt while preserving user context; implement proactive refresh 1 hour before expiry with fallback to reactive handling
- FR-019: Filter and sort operations must complete within 2 seconds for up to 1000 tasks

## Non-Functional Requirements
- NFR-001: Application must be responsive and work seamlessly on mobile and desktop devices
- NFR-002: All API calls must be secured with JWT token verification
- NFR-003: Smooth animations must be implemented for task add/delete operations
- NFR-004: Dashboard must load within 3 seconds on standard internet connection
- NFR-005: Application must handle concurrent users without data leakage between accounts
- NFR-006: UI must be accessible with proper ARIA labels and keyboard navigation
- NFR-007: All data must be persisted in Neon Serverless PostgreSQL database
- NFR-008: All operations must be user-isolated to prevent unauthorized access to others' tasks

## Success Criteria
- 95% of users can complete basic task operations (add, edit, delete, mark complete) within 2 minutes of first use
- Users can successfully authenticate and access their personal task dashboard
- Task CRUD operations complete successfully 99% of the time
- Mobile responsiveness verified across different screen sizes (tested on 320px, 768px, 1024px widths)
- Dashboard displays with smooth animations and no jank (60fps target)
- Authentication system prevents unauthorized access and ensures data isolation between users
- Token expiration handled gracefully with login prompt while preserving user context
- Large task lists (up to 1000 tasks) maintain responsive filter/sort operations (under 2 seconds)
- All intermediate features (priorities, tags, search, filter, sort) function correctly on single dashboard page
- System handles edge cases gracefully (empty lists, invalid tokens, search with no results)

## Key Entities
- **User**: Identity managed by Better Auth with JWT tokens, includes user_id for data isolation
- **Task**: Core entity with properties - id, title, description, status (complete/incomplete), priority (high/medium/low), tags (list of strings), due_date (optional), created_at, updated_at, user_id
- **Authentication Token**: JWT token for secure API access with 7-day expiry
- **Filter/Sort Parameters**: Search queries, priority filters, tag filters, date ranges, sort criteria
- **Theme Settings**: Dark/light mode preference stored in localStorage

## Scope
### In Scope
- Complete web-based todo application with all basic and intermediate features
- User authentication and data isolation
- Responsive dashboard with all functionality on single page
- Priority levels (high/medium/low) and tag assignment (work/home)
- Search, filter, and sort capabilities
- Animated UI interactions and dark/light mode
- Neon DB integration with user isolation
- All required agents and skills maintenance

### Out of Scope
- AI/chatbot functionality (reserved for Phase 3)
- Cloud deployment/Kubernetes (reserved for Phases 4/5)
- Recurring tasks or notifications (reserved for Phase 5)
- Voice commands or advanced multilingual support
- Separate pages - all functionality on single dashboard

## Assumptions
- Better Auth provides reliable JWT-based authentication with proper token management
- Neon Serverless PostgreSQL supports the required concurrent connections and performance
- Next.js 16+ with App Router provides sufficient performance for the dashboard
- Users have basic familiarity with web applications
- Internet connection is stable during normal usage
- The development team follows the established code standards (PEP 8, ESLint/Prettier)

## Dependencies
- Next.js 16+ for frontend framework
- FastAPI for backend API framework
- Better Auth for authentication system
- SQLModel for ORM
- Neon Serverless PostgreSQL for database (with provided connection URL)
- Tailwind CSS for responsive styling
- Framer Motion for animations
- react-hot-toast for notification system
- Spec-Driven Development tools for project management

## Agent and Skill Infrastructure
- Frontend Engineer Agent: Next.js UI development and animations (located at .claude/agents/frontend-engineer/agent.md)
- Backend Engineer Agent: FastAPI routes and business logic (located at .claude/agents/backend-engineer/agent.md)
- JWT/Auth Engineer Agent: Security and token verification (located at .claude/agents/jwt-auth-engineer/agent.md)
- Database Engineer Agent: SQLModel/Neon models and queries (located at .claude/agents/database-engineer/agent.md)
- Spec Writer Engineer Agent: Constitution/spec/plan/tasks/clarify (located at .claude/agents/spec-writer-engineer/agent.md)
- Integration Engineer Agent: Frontend-backend API client connectivity (located at .claude/agents/integration-engineer/agent.md)
- Corresponding skills located in .claude/skills/ directory

## Clarifications

### Session 2026-02-05
- Q: What specific colors should be used for priority badges and how should the "behtreen UI/UX" be interpreted in practical terms? → A: Use specific Tailwind classes: high (bg-red-100 text-red-800), medium (bg-yellow-100 text-yellow-800), low (bg-green-100 text-green-800)
- Q: How should users input and manage tags - comma-separated input, predefined dropdown, or free-form with validation? → A: Comma-separated input with validation and auto-suggestions for common tags
- Q: What should be the default theme state and how should the system handle theme persistence and system preference detection? → A: Default to light mode but detect system preference and offer option to sync with system settings
- Q: Should the system implement proactive token refresh before expiry or only handle it reactively when it expires? → A: Proactive refresh 1 hour before expiry with fallback to reactive handling when token is expired
- Q: What debounce time should be used for search input to balance responsiveness with performance? → A: 300ms debounce time to balance responsiveness with performance

## Open Questions
None