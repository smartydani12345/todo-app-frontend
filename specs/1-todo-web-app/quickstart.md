# Quickstart Guide: Todo Evolution Hackathon – Phase 2

## Prerequisites

- **Node.js**: Version 18 or higher for frontend development
- **Python**: Version 3.11 or higher for backend development
- **Package Managers**: npm/yarn for frontend, pip for backend
- **Database**: Neon Serverless PostgreSQL account with API access
- **Authentication**: Better Auth account and configuration

## Project Structure

```
todo-evolution-hackathon-phase2/
├── frontend/                 # Next.js 16+ application
│   ├── app/                 # App Router pages
│   ├── components/          # Reusable UI components
│   ├── lib/                 # Utility functions and API client
│   ├── public/              # Static assets
│   ├── styles/              # Global styles and Tailwind config
│   └── package.json         # Frontend dependencies
├── backend/                 # FastAPI application
│   ├── api/                 # API routes
│   ├── models/              # SQLModel definitions
│   ├── services/            # Business logic
│   ├── auth/                # Authentication utilities
│   ├── database/            # Database connection and setup
│   └── requirements.txt     # Backend dependencies
├── specs/                   # Specifications and plans
│   └── 1-todo-web-app/     # Current feature specs
└── .env                     # Environment variables
```

## Setup Instructions

### 1. Clone and Initialize Repository

```bash
# Clone the repository
git clone <repository-url>
cd todo-evolution-hackathon-phase2

# Install frontend dependencies
cd frontend
npm install

# Install backend dependencies
cd ../backend
pip install -r requirements.txt
```

### 2. Configure Environment Variables

Create `.env` files for both frontend and backend:

**Backend** (`backend/.env`):
```env
# Database Configuration
DATABASE_URL=postgresql://neondb_owner:npg_Z5SrBTPLAF8J@ep-fragrant-union-a1szssc1-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require

# Authentication Configuration
BETTER_AUTH_SECRET=1J9sGzWBBciZ9w93jdsAI4jPvG1qkLpU
BETTER_AUTH_JWT_EXPIRES_IN=7d

# Server Configuration
SERVER_HOST=localhost
SERVER_PORT=8000
```

**Frontend** (`frontend/.env.local`):
```env
# Backend API URL
NEXT_PUBLIC_API_URL=http://localhost:8000

# Better Auth Configuration
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=1J9sGzWBBciZ9w93jdsAI4jPvG1qkLpU
```

### 3. Set Up Database

The application uses Neon Serverless PostgreSQL. Make sure your database is created and accessible:

1. Sign up for Neon (if not already done)
2. Create a new project
3. Copy the connection string to your backend `.env` file
4. The application will handle schema migrations automatically

### 4. Start Development Servers

**Backend** (in `backend/` directory):
```bash
# Activate virtual environment if using one
python -m backend.main
# or
uvicorn backend.main:app --reload --host 0.0.0.0 --port 8000
```

**Frontend** (in `frontend/` directory):
```bash
npm run dev
```

Both servers will start in development mode with hot reloading enabled.

## Development Workflow

### Running Tests

**Backend** (in `backend/` directory):
```bash
# Run all backend tests
pytest

# Run with coverage
pytest --cov=.

# Run specific test file
pytest tests/test_tasks.py
```

**Frontend** (in `frontend/` directory):
```bash
# Run all frontend tests
npm run test

# Run tests in watch mode
npm run test:watch

# Run linting
npm run lint

# Run formatting
npm run format
```

### Building for Production

**Backend**:
```bash
# Build backend (usually handled by deployment pipeline)
pip install -r requirements.txt --target ./dist
```

**Frontend**:
```bash
# Build frontend application
npm run build

# Preview production build locally
npm run start
```

## Key Features Configuration

### Authentication Setup

1. Better Auth is configured with JWT tokens
2. Tokens have a 7-day expiry
3. Frontend handles login/signup flows
4. Backend validates JWT on every API call

### Theme System

1. Dark/light mode toggle available in header
2. Default is light mode
3. System preference detection enabled
4. Preference saved in localStorage

### Task Management

1. Tasks are isolated by user_id
2. Priority levels: high (red), medium (yellow), low (green)
3. Tags can be added with comma-separated input
4. Search has 300ms debounce for performance

## Troubleshooting

### Common Issues

**Issue**: Database connection fails
**Solution**: Verify your Neon PostgreSQL connection string and ensure your account has the necessary permissions

**Issue**: Authentication not working
**Solution**: Check that BETTER_AUTH_SECRET is identical in both frontend and backend configurations

**Issue**: API calls return 401 Unauthorized
**Solution**: Ensure JWT is properly attached to all API requests and hasn't expired

### Useful Commands

```bash
# Check backend API status
curl http://localhost:8000/health

# Reset database (development only)
cd backend && python -c "from database.init_db import init_db; init_db()"

# Clear frontend cache
cd frontend && rm -rf .next && npm cache clean --force
```

## Deployment Notes

For production deployment:

1. Update environment variables with production values
2. Set up SSL certificates for secure connections
3. Configure load balancer and CDN if needed
4. Set up monitoring and logging
5. Plan for database backup and recovery procedures