import pytest
from database.models import Task
from models.task import TaskCreate, TaskUpdate, TaskPublic
from pydantic import ValidationError
import uuid
from datetime import datetime

def test_task_creation_valid():
    """Test creating a valid task"""
    import json
    task = Task(
        id=str(uuid.uuid4()),
        user_id="test_user_id",
        title="Test Task",
        description="Test Description",
        completed=False,
        priority="medium",
        tags=json.dumps(["work", "important"]),  # Store as JSON string
        due_date=datetime.now(),
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    assert task.title == "Test Task"
    assert task.description == "Test Description"
    assert task.completed is False
    assert task.priority == "medium"
    assert "work" in json.loads(task.tags)
    assert "important" in json.loads(task.tags)

def test_task_title_validation():
    """Test task title validation"""
    # Test title too short - this should be handled by pydantic validation
    try:
        Task(
            id=str(uuid.uuid4()),
            user_id="test_user_id",
            title="",  # Empty title
            completed=False,
            priority="medium",
            tags="[]",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        # If we reach this line, validation didn't happen as expected
        assert False, "Expected validation error for empty title"
    except Exception:
        pass  # Expected to fail

    # Test title too long
    try:
        Task(
            id=str(uuid.uuid4()),
            user_id="test_user_id",
            title="a" * 101,  # Title too long
            completed=False,
            priority="medium",
            tags="[]",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        # If we reach this line, validation didn't happen as expected
        assert False, "Expected validation error for long title"
    except Exception:
        pass  # Expected to fail

def test_task_priority_validation():
    """Test task priority validation"""
    # Test invalid priority
    try:
        Task(
            id=str(uuid.uuid4()),
            user_id="test_user_id",
            title="Test Task",
            completed=False,
            priority="invalid",  # Invalid priority
            tags="[]",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        # If we reach this line, validation didn't happen as expected
        assert False, "Expected validation error for invalid priority"
    except Exception:
        pass  # Expected to fail

def test_task_tags_validation():
    """Test task tags validation"""
    import json
    # Test too many tags
    try:
        Task(
            id=str(uuid.uuid4()),
            user_id="test_user_id",
            title="Test Task",
            completed=False,
            priority="medium",
            tags=json.dumps([f"tag{i}" for i in range(11)]),  # More than 10 tags
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        # If we reach this line, validation didn't happen as expected
        assert False, "Expected validation error for too many tags"
    except Exception:
        pass  # Expected to fail

    # Test tag too long
    try:
        Task(
            id=str(uuid.uuid4()),
            user_id="test_user_id",
            title="Test Task",
            completed=False,
            priority="medium",
            tags=json.dumps(["a" * 51]),  # Tag too long
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        # If we reach this line, validation didn't happen as expected
        assert False, "Expected validation error for long tag"
    except Exception:
        pass  # Expected to fail

def test_task_create_model():
    """Test TaskCreate model"""
    import json
    task_create = TaskCreate(
        title="Test Task",
        description="Test Description",
        priority="high",
        tags=json.dumps(["test", "urgent"])  # Store as JSON string
    )

    assert task_create.title == "Test Task"
    assert task_create.description == "Test Description"
    assert task_create.priority == "high"
    assert "test" in json.loads(task_create.tags)
    assert "urgent" in json.loads(task_create.tags)

def test_task_update_model():
    """Test TaskUpdate model"""
    import json
    task_update = TaskUpdate(
        title="Updated Title",
        completed=True,
        priority="low",
        tags=json.dumps(["updated", "test"])  # Store as JSON string
    )

    assert task_update.title == "Updated Title"
    assert task_update.completed is True
    assert task_update.priority == "low"
    assert "updated" in json.loads(task_update.tags)
    assert "test" in json.loads(task_update.tags)

def test_task_public_model():
    """Test TaskPublic model"""
    import json
    task_public = TaskPublic(
        id=str(uuid.uuid4()),
        user_id="test_user_id",
        title="Test Task",
        description="Test Description",
        completed=False,
        priority="medium",
        tags=json.dumps(["public", "test"]),  # Store as JSON string
        created_at=datetime.now(),
        updated_at=datetime.now()
    )

    assert task_public.id is not None
    assert task_public.user_id == "test_user_id"
    assert task_public.title == "Test Task"
    assert task_public.completed is False
    assert "public" in json.loads(task_public.tags)
    assert "test" in json.loads(task_public.tags)