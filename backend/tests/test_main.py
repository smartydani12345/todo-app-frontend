import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from main import app
from database.models import Task

# Create a test client
client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Todo Evolution Hackathon - Phase 2 Backend API"}

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "healthy", "service": "backend"}

def test_create_task_unauthorized():
    """Test creating a task without authentication"""
    task_data = {
        "title": "Test Task",
        "description": "Test Description",
        "priority": "medium"
    }
    response = client.post("/api/tasks/", json=task_data)
    assert response.status_code == 401  # Unauthorized

def test_get_tasks_unauthorized():
    """Test getting tasks without authentication"""
    response = client.get("/api/tasks/")
    assert response.status_code == 401  # Unauthorized

def test_get_specific_task_unauthorized():
    """Test getting a specific task without authentication"""
    response = client.get("/api/tasks/123")
    assert response.status_code == 401  # Unauthorized

def test_update_task_unauthorized():
    """Test updating a task without authentication"""
    task_data = {"title": "Updated Title"}
    response = client.put("/api/tasks/123", json=task_data)
    assert response.status_code == 401  # Unauthorized

def test_delete_task_unauthorized():
    """Test deleting a task without authentication"""
    response = client.delete("/api/tasks/123")
    assert response.status_code == 401  # Unauthorized

def test_toggle_complete_task_unauthorized():
    """Test toggling task completion without authentication"""
    response = client.patch("/api/tasks/123/complete", params={"completed": True})
    assert response.status_code == 401  # Unauthorized