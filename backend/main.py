from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from auth import router as auth_router  # Import from auth package __init__.py
from api.tasks import router as tasks_router
from database.init_db import create_db_and_tables

# Create FastAPI app with lifespan to initialize database
from contextlib import asynccontextmanager
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Create database tables on startup
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

# Configure CORS for frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:3001", os.getenv("NEXT_PUBLIC_BASE_URL", "http://localhost:3000")],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include authentication and tasks routers
app.include_router(auth_router, prefix="/api")
app.include_router(tasks_router, prefix="/api")

@app.get("/")
def read_root():
    return {"message": "Todo Evolution Hackathon - Phase 2 Backend API"}

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "backend"}