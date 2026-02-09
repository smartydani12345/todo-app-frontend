📝 Todo App – Phase 2


Optional: add screenshot of landing page or dashboard

🚀 Tech Stack
Frontend

Next.js / React.js – Modern React framework

Tailwind CSS – Styling and responsive layout

TypeScript – Type safety (optional)

Components: Task List, Task Form, Landing Page, Theme Toggle, Search & Sort

Backend

FastAPI (Python) – High-performance backend framework

PostgreSQL – Persistent relational database

SQLModel / SQLAlchemy – Database ORM

JWT Authentication – Secure login and user sessions

Modular structure: Routes, Models, Services

⚙️ Features

Full CRUD operations for tasks

User authentication with JWT

Landing page and dashboard integration

Persistent PostgreSQL database

API-based frontend-backend integration

Responsive UI using Tailwind CSS

📂 Folder Structure
backend/
│
├── app/
│   ├── models/
│   ├── routes/
│   ├── schemas/
│   ├── services/
│   └── main.py
│
├── requirements.txt
└── .env

frontend/
│
├── app/
├── components/
├── tests/
├── package.json
└── tailwind.config.js

⚡ Run Locally
Backend
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload

Frontend
cd frontend
npm install
npm run dev

🗄 Database

PostgreSQL

SQLModel / SQLAlchemy ORM

Ready for deployment (Neon, Supabase, Railway, or local)

🔖 Notes

Phase 2 focuses on full frontend + backend integration

Phase 1 (console-based) has been superseded

Ensure .env has correct database credentials before running backend

🏷 Badges (Optional)
![Python](https://img.shields.io/badge/python-3.11-blue)
![FastAPI](https://img.shields.io/badge/FastAPI-0.99-green)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)
