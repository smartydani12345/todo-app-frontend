import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from typing import List, Optional
from sqlmodel import Session, select, func
from database.models import Task
from models.task import TaskCreate, TaskUpdate, TaskPublic
from fastapi import HTTPException, status

class TaskService:
    """
    Service class to handle business logic for tasks.
    Implements user isolation and validation.
    """

    def create_task(self, session: Session, task_data: TaskCreate, user_id: str) -> TaskPublic:
        """
        Create a new task for the authenticated user.
        """
        # Validate input
        if len(task_data.title) < 1 or len(task_data.title) > 100:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Title must be between 1 and 100 characters"
            )

        if task_data.description and len(task_data.description) > 1000:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Description must be 1000 characters or less"
            )

        if task_data.priority not in ["high", "medium", "low"]:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Priority must be 'high', 'medium', or 'low'"
            )

        if task_data.tags and len(task_data.tags) > 10:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
                detail="Maximum 10 tags allowed"
            )

        # Create task
        import json
        db_task = Task(
            title=task_data.title,
            description=task_data.description,
            completed=task_data.completed,
            priority=task_data.priority,
            tags=json.dumps(task_data.tags) if isinstance(task_data.tags, list) else task_data.tags,
            due_date=task_data.due_date,
            user_id=user_id
        )

        session.add(db_task)
        session.commit()
        session.refresh(db_task)

        import json
        return TaskPublic(
            id=db_task.id,
            user_id=db_task.user_id,
            title=db_task.title,
            description=db_task.description,
            completed=db_task.completed,
            priority=db_task.priority,
            tags=db_task.tags,  # Already stored as JSON string
            due_date=db_task.due_date,
            created_at=db_task.created_at,
            updated_at=db_task.updated_at
        )

    def get_tasks(
        self,
        session: Session,
        user_id: str,
        skip: int = 0,
        limit: int = 50,
        filter_status: Optional[str] = None,
        filter_priority: Optional[str] = None,
        filter_tag: Optional[str] = None,
        search: Optional[str] = None,
        sort_field: Optional[str] = None,
        sort_order: Optional[str] = "asc"
    ) -> List[TaskPublic]:
        """
        Get tasks for the authenticated user with optional filtering, sorting, and pagination.
        """
        query = select(Task).where(Task.user_id == user_id)

        # Apply filters
        if filter_status:
            if filter_status == "completed":
                query = query.where(Task.completed == True)
            elif filter_status == "incomplete":
                query = query.where(Task.completed == False)

        if filter_priority:
            query = query.where(Task.priority == filter_priority)

        if filter_tag:
            # For tag filtering, we need to find tasks that contain the tag
            # Using a LIKE operation to check if the tag exists in the JSON array
            query = query.where(Task.tags.like(f'%{filter_tag}%'))

        if search:
            query = query.where(
                (Task.title.contains(search)) |
                (Task.description.contains(search))
            )

        # Apply sorting
        if sort_field == "due_date":
            if sort_order == "desc":
                query = query.order_by(Task.due_date.desc())
            else:
                query = query.order_by(Task.due_date.asc())
        elif sort_field == "priority":
            if sort_order == "desc":
                query = query.order_by(Task.priority.desc())
            else:
                query = query.order_by(Task.priority.asc())
        elif sort_field == "title":
            if sort_order == "desc":
                query = query.order_by(Task.title.desc())
            else:
                query = query.order_by(Task.title.asc())
        elif sort_field == "created_at":
            if sort_order == "desc":
                query = query.order_by(Task.created_at.desc())
            else:
                query = query.order_by(Task.created_at.asc())
        else:  # Default sort by created_at
            if sort_order == "desc":
                query = query.order_by(Task.created_at.desc())
            else:
                query = query.order_by(Task.created_at.asc())

        # Apply pagination
        query = query.offset(skip).limit(limit)

        import json
        # Use the correct method based on SQLModel version
        try:
            # Try the SQLModel 0.0.22+ way first
            result = session.exec(query)
            tasks = result.all()
        except AttributeError:
            # Fallback to older SQLModel/SQLAlchemy way
            result = session.execute(query)
            tasks = result.scalars().all()

        return [
            TaskPublic(
                id=task.id,
                user_id=task.user_id,
                title=task.title,
                description=task.description,
                completed=task.completed,
                priority=task.priority,
                tags=task.tags,  # Already stored as JSON string
                due_date=task.due_date,
                created_at=task.created_at,
                updated_at=task.updated_at
            )
            for task in tasks
        ]

    def get_task(self, session: Session, task_id: str, user_id: str) -> TaskPublic:
        """
        Get a specific task by ID for the authenticated user.
        """
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Check user isolation
        if task.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Cannot access tasks owned by other users"
            )

        import json
        return TaskPublic(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            priority=task.priority,
            tags=task.tags,  # Already stored as JSON string
            due_date=task.due_date,
            created_at=task.created_at,
            updated_at=task.updated_at
        )

    def update_task(self, session: Session, task_id: str, task_update: TaskUpdate, user_id: str) -> TaskPublic:
        """
        Update a task for the authenticated user.
        """
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Check user isolation
        if task.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Cannot modify tasks owned by other users"
            )

        # Apply updates
        update_data = task_update.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == 'tags' and value is not None and isinstance(value, list):
                # Convert tags list to JSON string for storage
                import json
                setattr(task, field, json.dumps(value))
            else:
                setattr(task, field, value)

        task.updated_at = func.now()
        session.add(task)
        session.commit()
        session.refresh(task)

        import json
        return TaskPublic(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            priority=task.priority,
            tags=task.tags,  # Already stored as JSON string
            due_date=task.due_date,
            created_at=task.created_at,
            updated_at=task.updated_at
        )

    def delete_task(self, session: Session, task_id: str, user_id: str) -> bool:
        """
        Delete a task for the authenticated user.
        """
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Check user isolation
        if task.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Cannot delete tasks owned by other users"
            )

        session.delete(task)
        session.commit()
        return True

    def toggle_complete_task(self, session: Session, task_id: str, user_id: str, completed: bool) -> TaskPublic:
        """
        Toggle the completion status of a task for the authenticated user.
        """
        task = session.get(Task, task_id)
        if not task:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Task not found"
            )

        # Check user isolation
        if task.user_id != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Access denied: Cannot modify tasks owned by other users"
            )

        task.completed = completed
        task.updated_at = func.now()
        session.add(task)
        session.commit()
        session.refresh(task)

        import json
        return TaskPublic(
            id=task.id,
            user_id=task.user_id,
            title=task.title,
            description=task.description,
            completed=task.completed,
            priority=task.priority,
            tags=task.tags,  # Already stored as JSON string
            due_date=task.due_date,
            created_at=task.created_at,
            updated_at=task.updated_at
        )

    def get_user_task_count(self, session: Session, user_id: str) -> int:
        """
        Get the count of tasks for a user.
        """
        query = select(func.count(Task.id)).where(Task.user_id == user_id)
        count = session.exec(query).one()
        return count