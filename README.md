# Todo Evolution Hackathon – Phase 2

**Author:** Daniyal Azhar

## 1️⃣ MVP Overview

Objective: Build a modern, full-stack Todo app with per-user data isolation, task management, and responsive UI.

**MVP Features (Phase 2):**

- **User Authentication:** Register/Login, JWT-based, per-user data isolation  
- **Task Management:** CRUD for tasks (title, description, due_date, status, priority)  
- **Tagging & Priority Management:** Assign tags to tasks, manage priority levels  
- **Search/Filter & Sorting:** Client-side real-time filtering by title, tag, status, date, priority  
- **Responsive UI:** Dark/Light mode, accessibility-ready components  

---

## 2️⃣ Recommended Tech Stack

| Layer           | Technology                    | Notes / Constraints |
|-----------------|-------------------------------|-------------------|
| Frontend        | Next.js (App Router preferred)| TypeScript, Tailwind CSS, Axios/fetch API client |
| Backend         | FastAPI + SQLModel            | PostgreSQL (Neon Serverless), JWT auth, bcrypt password hashing |
| Authentication  | JWT + Refresh Tokens          | Access token ~15min, refresh token rotation |
| State / UX      | React context / Zustand       | Minimal global state for user/session |
| Testing         | Pytest (backend), Jest + React Testing Library (frontend) | Unit + integration tests |
| Deployment      | Vercel (frontend), Docker + cloud DB (backend) | Environment variables, migrations, logging |

---

## 3️⃣ Data Models (SQLModel / FastAPI)

```python
from sqlmodel import SQLModel, Field, Relationship
from typing import List, Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    email: str
    password_hash: str
    tasks: List["Task"] = Relationship(back_populates="user")
    tags: List["Tag"] = Relationship(back_populates="user")

class Task(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="user.id")
    title: str
    description: Optional[str] = ""
    due_date: Optional[datetime] = None
    status: str = "pending"
    priority: str = "medium"
    tags: List["Tag"] = Relationship(back_populates="tasks", link_model="TaskTag")
    user: "User" = Relationship(back_populates="tasks")

class Tag(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    user_id: int = Field(foreign_key="user.id")
    tasks: List[Task] = Relationship(back_populates="tags", link_model="TaskTag")
    user: "User" = Relationship(back_populates="tags")

class TaskTag(SQLModel, table=True):
    task_id: int = Field(foreign_key="task.id", primary_key=True)
    tag_id: int = Field(foreign_key="tag.id", primary_key=True)
4️⃣ API Contract (REST-like)
Endpoint	Method	Request	Response	Notes
/auth/register	POST	{email, password}	{user_id, token}	Register user
/auth/login	POST	{email, password}	{access_token, refresh_token}	Login, JWT auth
/auth/refresh	POST	{refresh_token}	{access_token, refresh_token}	Rotate refresh tokens
/tasks	GET	?search=&tag=&status=&priority=	[Task]	List/filter tasks
/tasks	POST	{title, description, due_date, priority, tags[]}	Task	Create task
/tasks/{id}	PUT	{title, description, due_date, priority, tags[]}	Task	Update task
/tasks/{id}	DELETE	None	{success: true}	Delete task
/tasks/{id}/complete	PATCH	None	Task	Toggle status
/tags	GET	None	[Tag]	List user tags
/tags	POST	{name}	Tag	Create tag
/tags/{id}	DELETE	None	{success: true}	Delete tag
5️⃣ Frontend Pages & Components

Pages:

/login → Auth form

/register → Auth form

/dashboard → Task list with filters

/task/[id] → Task editor/detail page

Components:

TaskList → Display filtered tasks

TaskEditor → Add/edit task modal/page

TagFilter → Multi-tag filter UI

PriorityBadge → Color-coded priority

Header → Dark/light mode switch

ResponsiveNav → Mobile/desktop navigation

SearchInput → Debounced search input

6️⃣ Step-by-Step Implementation Plan (Phase 2)

Initialize repo (frontend + backend mono repo)

Scaffold backend: FastAPI + SQLModel, JWT auth, PostgreSQL setup

Scaffold frontend: Next.js App Router + Tailwind CSS

Implement auth pages + JWT flow

Implement task CRUD endpoints + database models

Build frontend TaskList + TaskEditor + TagFilter

Implement search, filtering, sorting

Ensure responsive UI + dark/light mode

Real-time UX: debounce search, optimistic updates

Advanced filtering: multi-tag, status, priority

Add unit & integration tests

CI/CD: GitHub Actions

Logging & error reporting

Accessibility improvements

7️⃣ Example Code Snippets

Backend – Password Hashing

from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password, hashed):
    return pwd_context.verify(password, hashed)

Frontend – Fetch Tasks

import axios from "axios";

export const fetchTasks = async (token: string, filters = {}) => {
  const res = await axios.get("/api/tasks", {
    headers: { Authorization: `Bearer ${token}` },
    params: filters,
  });
  return res.data;
};
8️⃣ Repo & Project Layout
todo-app/
├── backend/
│   ├── api/
│   ├── auth/
│   ├── database/
│   ├── models/
│   ├── services/
│   └── main.py
├── frontend/
│   ├── app/
│   ├── components/
│   ├── lib/
│   ├── public/
│   └── styles/
├── docker-compose.yml
├── .env.example
└── README.md
9️⃣ Non-Functional Considerations

Auth & Security: JWT, bcrypt, refresh token rotation, per-user data isolation

Testing: Unit + integration coverage, CI on GitHub Actions

Accessibility: Keyboard navigation, ARIA labels, contrast ratios

Logging & Monitoring: FastAPI logging, optional Sentry integration<<<<<<< HEAD
# MERN Stack Todo App (Frontend)

![Todo App](https://user-images.githubusercontent.com/your-username/placeholder-image.png)

A modern **Todo Application Frontend** built with **React.js** (part of MERN stack), fully responsive and integrated with a backend API for task management.

---

## Features

- Add, update, delete, and view tasks
- Responsive design (desktop + mobile friendly)
- Connects to a backend API for persistent data
- Filter tasks by status (completed / pending)
- Drag & drop reordering of tasks (if implemented in backend)

---

## Tech Stack

- **Frontend:** React.js, CSS/SCSS, Axios for API requests  
- **Backend:** FastAPI / Node.js (separate repo)  
- **Version Control:** Git & GitHub  
- **Deployment:** Vercel / Netlify (Frontend)

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/smartydani12345/todo-app-frontend.git
cd todo-app-frontend

2. Install dependencies
npm install

3. Configure environment variables

Create a .env file at the root:

REACT_APP_API_URL=http://localhost:8000  # Change to your backend URL

4. Run the app locally
npm start


Open http://localhost:3000
 to view in the browser.
git clone https://github.com/smartydani12345/todo-app-frontend.git
cd todo-app-frontend
=======
# Todo Evolution Hackathon – Phase 2

A modern full-stack todo application with advanced features including priorities, tags, search, filtering, and sorting.

## Features

- **User Authentication**: Secure JWT-based authentication with Better Auth
- **Task Management**: Create, read, update, delete tasks with full CRUD operations
- **Priorities**: High, medium, low priority levels with color-coded badges
- **Tags**: Organize tasks with customizable tags
- **Search & Filter**: Powerful search with debounced input and multiple filter options
- **Sorting**: Sort tasks by various criteria
- **Responsive Design**: Works seamlessly on mobile and desktop
- **Dark/Light Mode**: Theme switching with system preference detection
- **Animations**: Smooth animations using Framer Motion
- **Voice Commands**: (Optional) Voice-controlled task management

## Tech Stack

- **Frontend**: Next.js 16+, TypeScript, Tailwind CSS, Framer Motion
- **Backend**: FastAPI, SQLModel, PostgreSQL (Neon Serverless)
- **Authentication**: Better Auth with JWT
- **Database**: Neon Serverless PostgreSQL
- **Styling**: Tailwind CSS for responsive design
- **Animations**: Framer Motion for smooth transitions

## Setup

### Prerequisites

- Node.js 18+ for frontend
- Python 3.11+ for backend
- PostgreSQL-compatible database (Neon recommended)

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-name>
   ```

2. Install frontend dependencies:
   ```bash
   cd frontend
   npm install
   ```

3. Install backend dependencies:
   ```bash
   cd ../backend
   pip install -r requirements.txt
   ```

4. Configure environment variables:
   ```bash
   # In the root directory
   cp .env.example .env
   # Update the values in .env file
   ```

## Environment Variables

- `BETTER_AUTH_SECRET`: Secret key for JWT signing
- `DATABASE_URL`: Neon PostgreSQL connection string
- `NEXT_PUBLIC_API_URL`: Backend API endpoint
- `BETTER_AUTH_JWT_EXPIRES_IN`: JWT expiration time (default: 7d)
- `NEXT_PUBLIC_BASE_URL`: Frontend base URL

## Development

### Backend

1. Navigate to the backend directory:
   ```bash
   cd backend
   ```

2. Run the development server:
   ```bash
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```

### Frontend

1. Navigate to the frontend directory:
   ```bash
   cd frontend
   ```

2. Run the development server:
   ```bash
   npm run dev
   ```

## Deployment

### Backend

1. Build the backend application:
   ```bash
   cd backend
   pip install -r requirements.txt
   ```

2. Deploy to your preferred Python hosting service (e.g., Heroku, AWS, Google Cloud)

### Frontend

1. Build the frontend application:
   ```bash
   cd frontend
   npm run build
   ```

2. Deploy to your preferred hosting service (e.g., Vercel, Netlify, AWS)

## API Endpoints

- `GET /api/tasks` - Get tasks with filtering, sorting, and pagination
- `POST /api/tasks` - Create a new task
- `GET /api/tasks/{id}` - Get a specific task
- `PUT /api/tasks/{id}` - Update a task
- `DELETE /api/tasks/{id}` - Delete a task
- `PATCH /api/tasks/{id}/complete` - Toggle task completion status

## Architecture

### Backend Structure

```
backend/
├── api/           # API routes
├── models/        # SQLModel definitions
├── services/      # Business logic
├── auth/          # Authentication utilities
├── database/      # Database connection and setup
└── main.py        # Application entry point
```

### Frontend Structure

```
frontend/
├── app/           # Next.js App Router pages
├── components/    # Reusable UI components
├── lib/           # Utility functions and API client
├── public/        # Static assets
└── styles/        # Global styles
```

## Security

- JWT-based authentication with 7-day token expiry
- User isolation: Users can only access their own tasks
- Input validation on both frontend and backend
- Proactive token refresh 1 hour before expiry

## License

This project is part of the Todo Evolution Hackathon – Phase 2.
>>>>>>> 9570323 (Phase 2: frontend + backend integration, landing page, fixes, docs)
