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


## Run Locally

### Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
Frontend
cd frontend
npm install
npm run dev
Database
PostgreSQL

SQLModel / SQLAlchemy ORM

Ready for deployment (Neon, Supabase, Railway, or local)

Notes
Open http://localhost:3000 to view in the browser

Make sure your .env has correct database credentials before running backend

Phase 1 (console-based) has been superseded by this full-stack Phase 2

