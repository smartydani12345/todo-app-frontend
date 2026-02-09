import pytest
from unittest.mock import Mock, AsyncMock
from services.task_service import TaskService
from database.models import Task
from models.task import TaskCreate, TaskUpdate, TaskPublic
from fastapi import HTTPException
import uuid
from datetime import datetime

@pytest.fixture
def task_service():
    """Create a TaskService instance for testing"""
    return TaskService()

@pytest.fixture
def mock_session():
    """Create a mock database session for testing"""
    session = Mock()
    session.get = Mock()
    session.add = Mock()
    session.commit = Mock()
    session.refresh = Mock()
    session.exec = Mock()
    return session

def test_create_task_success(task_service, mock_session):
    """Test successful task creation"""
    user_id = "test_user_id"
    task_data = TaskCreate(
        title="Test Task",
        description="Test Description",
        priority="medium",
        tags=["test", "important"]
    )

    # Mock the database operations
    created_task = Task(
        id=str(uuid.uuid4()),
        user_id=user_id,
        title=task_data.title,
        description=task_data.description,
        priority=task_data.priority,
        tags=task_data.tags,
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    result = task_service.create_task(mock_session, task_data, user_id)

    # Verify the result is a TaskPublic object
    assert isinstance(result, TaskPublic)
    assert result.title == "Test Task"
    assert result.user_id == user_id

def test_create_task_invalid_title_length(task_service, mock_session):
    """Test creating a task with invalid title length"""
    user_id = "test_user_id"
    task_data = TaskCreate(
        title="",  # Invalid: empty title
        priority="medium"
    )

    with pytest.raises(HTTPException) as exc_info:
        task_service.create_task(mock_session, task_data, user_id)

    assert exc_info.value.status_code == 422

def test_create_task_long_title(task_service, mock_session):
    """Test creating a task with a too-long title"""
    user_id = "test_user_id"
    task_data = TaskCreate(
        title="a" * 101,  # Invalid: title too long
        priority="medium"
    )

    with pytest.raises(HTTPException) as exc_info:
        task_service.create_task(mock_session, task_data, user_id)

    assert exc_info.value.status_code == 422

def test_create_task_invalid_priority(task_service, mock_session):
    """Test creating a task with invalid priority"""
    user_id = "test_user_id"
    task_data = TaskCreate(
        title="Test Task",
        priority="invalid"  # Invalid priority
    )

    with pytest.raises(HTTPException) as exc_info:
        task_service.create_task(mock_session, task_data, user_id)

    assert exc_info.value.status_code == 422

def test_create_task_too_many_tags(task_service, mock_session):
    """Test creating a task with too many tags"""
    user_id = "test_user_id"
    task_data = TaskCreate(
        title="Test Task",
        priority="medium",
        tags=[f"tag{i}" for i in range(11)]  # Too many tags (>10)
    )

    with pytest.raises(HTTPException) as exc_info:
        task_service.create_task(mock_session, task_data, user_id)

    assert exc_info.value.status_code == 422

def test_get_task_success(task_service, mock_session):
    """Test successfully retrieving a task"""
    task_id = str(uuid.uuid4())
    user_id = "test_user_id"

    # Create a mock task
    mock_task = Task(
        id=task_id,
        user_id=user_id,
        title="Test Task",
        completed=False,
        priority="medium",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    # Configure the mock to return the task
    mock_session.get.return_value = mock_task

    result = task_service.get_task(mock_session, task_id, user_id)

    assert isinstance(result, TaskPublic)
    assert result.id == task_id
    assert result.title == "Test Task"

def test_get_task_not_found(task_service, mock_session):
    """Test retrieving a non-existent task"""
    task_id = str(uuid.uuid4())
    user_id = "test_user_id"

    # Configure the mock to return None (task not found)
    mock_session.get.return_value = None

    with pytest.raises(HTTPException) as exc_info:
        task_service.get_task(mock_session, task_id, user_id)

    assert exc_info.value.status_code == 404

def test_get_task_wrong_user(task_service, mock_session):
    """Test retrieving a task owned by another user"""
    task_id = str(uuid.uuid4())
    task_user_id = "other_user_id"
    requesting_user_id = "requesting_user_id"

    # Create a mock task owned by another user
    mock_task = Task(
        id=task_id,
        user_id=task_user_id,
        title="Test Task",
        completed=False,
        priority="medium",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    # Configure the mock to return the task
    mock_session.get.return_value = mock_task

    with pytest.raises(HTTPException) as exc_info:
        task_service.get_task(mock_session, task_id, requesting_user_id)

    assert exc_info.value.status_code == 403

def test_update_task_success(task_service, mock_session):
    """Test successfully updating a task"""
    task_id = str(uuid.uuid4())
    user_id = "test_user_id"

    # Create a mock task
    mock_task = Task(
        id=task_id,
        user_id=user_id,
        title="Original Task",
        completed=False,
        priority="medium",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    # Configure the mock to return the task
    mock_session.get.return_value = mock_task

    # Update data
    update_data = TaskUpdate(title="Updated Task", completed=True)

    result = task_service.update_task(mock_session, task_id, update_data, user_id)

    assert isinstance(result, TaskPublic)
    assert result.title == "Updated Task"
    assert result.completed is True

def test_delete_task_success(task_service, mock_session):
    """Test successfully deleting a task"""
    task_id = str(uuid.uuid4())
    user_id = "test_user_id"

    # Create a mock task
    mock_task = Task(
        id=task_id,
        user_id=user_id,
        title="Test Task",
        completed=False,
        priority="medium",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    # Configure the mock to return the task
    mock_session.get.return_value = mock_task
    mock_session.delete = Mock()
    mock_session.commit = Mock()

    result = task_service.delete_task(mock_session, task_id, user_id)

    assert result is True
    mock_session.delete.assert_called_once()
    mock_session.commit.assert_called_once()

def test_toggle_complete_task_success(task_service, mock_session):
    """Test successfully toggling task completion status"""
    task_id = str(uuid.uuid4())
    user_id = "test_user_id"

    # Create a mock task
    mock_task = Task(
        id=task_id,
        user_id=user_id,
        title="Test Task",
        completed=False,
        priority="medium",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    # Configure the mock to return the task
    mock_session.get.return_value = mock_task
    mock_session.add.return_value = None
    mock_session.commit.return_value = None
    mock_session.refresh.return_value = None

    result = task_service.toggle_complete_task(mock_session, task_id, user_id, True)

    assert isinstance(result, TaskPublic)
    assert result.completed is True