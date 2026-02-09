# Todo Evolution Hackathon – Phase 2

A modern full-stack todo application with advanced features including priorities, tags, search, filtering, and sorting.

## Tech Stack

### Frontend
- Next.js 16+, TypeScript
- Tailwind CSS – Responsive styling
- Framer Motion – Smooth animations
- Components: Task List, Task Form, Landing Page, Theme Toggle, Search & Sort

### Backend
- FastAPI (Python) – High-performance backend framework
- PostgreSQL – Persistent relational database
- SQLModel / SQLAlchemy – Database ORM
- JWT Authentication – Secure login and user sessions
- Modular structure: Routes, Models, Services

## Features
- Full CRUD operations for tasks
- User authentication with JWT
- Landing page and dashboard integration
- Persistent PostgreSQL database
- API-based frontend-backend integration
- Responsive UI using Tailwind CSS
- Optional: Voice command support

## Folder Structure
backend/
├── app/
│ ├── models/
│ ├── routes/
│ ├── schemas/
│ ├── services/
│ └── main.py
├── requirements.txt
└── .env

frontend/
├── app/
├── components/
├── tests/
├── package.json
└── tailwind.config.js


## Setup

### Prerequisites
- Node.js 18+ for frontend
- Python 3.11+ for backend
- PostgreSQL-compatible database (Neon recommended)

### Installation
```bash
# Clone repo
git clone https://github.com/smartydani12345/todo-app-frontend.git
cd todo-app-frontend

# Frontend
cd frontend
npm install
npm run dev

# Backend
cd ../backend
pip install -r requirements.txt
uvicorn app.main:app --reload
Environment Variables
DATABASE_URL: PostgreSQL connection string

BETTER_AUTH_SECRET: Secret key for JWT

NEXT_PUBLIC_API_URL: Backend API endpoint

BETTER_AUTH_JWT_EXPIRES_IN: JWT expiration (default: 7d)

NEXT_PUBLIC_BASE_URL: Frontend base URL

Deployment
Backend: Deploy to Heroku, Railway, or any Python hosting

Frontend: Deploy to Vercel, Netlify, or any Node.js hosting

API Endpoints
GET /api/tasks – List tasks

POST /api/tasks – Create task

GET /api/tasks/{id} – Get task

PUT /api/tasks/{id} – Update task

DELETE /api/tasks/{id} – Delete task

PATCH /api/tasks/{id}/complete – Toggle completion

Notes
Phase 1 (console-based) has been superseded

Ensure .env has correct database credentials before running backend

Open http://localhost:3000 to view frontend