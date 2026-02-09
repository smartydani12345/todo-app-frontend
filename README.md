<<<<<<< HEAD
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
