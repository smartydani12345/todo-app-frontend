import json
from datetime import datetime
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Form
from sqlmodel import Session, select

from database.models import Task
from models.task import TaskCreate, TaskUpdate  # Import validation models only
from database.session import get_session
from api.dependencies import get_current_user_id

router = APIRouter()

@router.get("/tasks/")
def get_tasks(
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session),
    search: str = None,
    status: str = None,  # 'completed', 'incomplete', or None for all
    priority: str = None,  # 'high', 'medium', 'low', or None for all
    tag: str = None,  # filter by tag
    sort_by: str = "created_at",  # 'created_at', 'due_date', 'priority', 'title'
    sort_order: str = "asc"  # 'asc' or 'desc'
) -> List[Task]:
    """Get all tasks for the authenticated user with filtering, sorting, and search"""
    # Start with base query
    query = select(Task).where(Task.user_id == current_user_id)

    # Apply search filter (search in title and description)
    if search:
        query = query.where(
            (Task.title.contains(search)) |
            (Task.description.contains(search))
        )

    # Apply status filter
    if status == "completed":
        query = query.where(Task.completed == True)
    elif status == "incomplete":
        query = query.where(Task.completed == False)

    # Apply priority filter
    if priority:
        query = query.where(Task.priority == priority)

    # Apply tag filter - tags are stored as comma-separated strings
    if tag:
        # For comma-separated tags, we need to check if the tag exists in the comma-separated list
        # Using SQL LIKE with commas to match exact tags (e.g., match "search" but not "searching")
        from sqlalchemy import or_
        query = query.where(
            or_(
                Task.tags.like(f'%{tag},%'),  # Tag at the beginning/middle of the list
                Task.tags.like(f'%{tag}'),    # Tag at the end of the list
                Task.tags == tag             # Tag is the only one in the list
            )
        )

    # Apply sorting
    if sort_by == "due_date":
        if sort_order == "desc":
            query = query.order_by(Task.due_date.desc())
        else:
            query = query.order_by(Task.due_date.asc())
    elif sort_by == "priority":
        if sort_order == "desc":
            query = query.order_by(Task.priority.desc())
        else:
            query = query.order_by(Task.priority.asc())
    elif sort_by == "title":
        if sort_order == "desc":
            query = query.order_by(Task.title.desc())
        else:
            query = query.order_by(Task.title.asc())
    else:  # default to created_at
        if sort_order == "desc":
            query = query.order_by(Task.created_at.desc())
        else:
            query = query.order_by(Task.created_at.asc())

    # Execute query using SQLAlchemy's execute method
    result = session.execute(query)
    tasks = result.scalars().all()

    return tasks

@router.post("/tasks/")
def create_task(
    title: str = Form(...),
    description: str = Form(None),
    priority: str = Form("medium"),
    tags: str = Form(""),  # Accept tags as comma-separated string
    due_date: str = Form(None),  # Optional due date
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Create a new task for the authenticated user"""
    if not title or title.strip() == "":
        raise HTTPException(status_code=400, detail="Title is required")

    # Process tags properly - convert comma-separated string to JSON array string
    if tags and tags.strip():
        # Split by comma and clean up tags
        tags_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
        processed_tags = json.dumps(tags_list)
    else:
        processed_tags = '[]'

    # Process due_date if provided
    due_date_obj = None
    if due_date:
        try:
            due_date_obj = datetime.fromisoformat(due_date.replace('Z', '+00:00'))
        except ValueError:
            # If it's not in ISO format, try other common formats
            for fmt in ("%Y-%m-%d", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M"):
                try:
                    due_date_obj = datetime.strptime(due_date, fmt)
                    break
                except ValueError:
                    continue
            else:
                # If none of the formats work, ignore the due date
                due_date_obj = None

    from datetime import datetime
    current_time = datetime.utcnow()
    
    new_task = Task(
        title=title.strip(),
        description=description,
        priority=priority,
        tags=processed_tags,
        due_date=due_date_obj,
        user_id=current_user_id,
        created_at=current_time,
        updated_at=current_time
    )

    session.add(new_task)
    try:
        session.commit()
        session.refresh(new_task)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error creating task: {str(e)}")

    return new_task

@router.put("/tasks/{task_id}")
def update_task(
    task_id: int,
    title: str = Form(None),
    description: str = Form(None),
    completed: bool = Form(None),
    priority: str = Form(None),
    tags: str = Form(None),
    current_user_id: str = Depends(get_current_user_id),
    session: Session = Depends(get_session)
):
    """Update a task for the authenticated user"""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify that the task belongs to the user
    if task.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to update this task")

    # Update fields that were provided
    if title is not None:
        task.title = title.strip() if title.strip() else task.title
    if description is not None:
        task.description = description
    if completed is not None:
        task.completed = completed
    if priority is not None:
        task.priority = priority
    if tags is not None:
        # Process tags properly - convert comma-separated string to JSON array string
        if tags and tags.strip():
            # Split by comma and clean up tags
            tags_list = [tag.strip() for tag in tags.split(',') if tag.strip()]
            task.tags = json.dumps(tags_list)
        else:
            task.tags = '[]'

    task.updated_at = datetime.utcnow()  # Update timestamp
    session.add(task)
    try:
        session.commit()
        session.refresh(task)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating task: {str(e)}")

    return task

@router.delete("/tasks/{task_id}")
def delete_task(task_id: int, current_user_id: str = Depends(get_current_user_id), session: Session = Depends(get_session)):
    """Delete a task for the authenticated user"""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify that the task belongs to the user
    if task.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this task")

    session.delete(task)
    session.commit()

    return {"message": "Task deleted successfully"}

@router.patch("/tasks/{task_id}/complete")
def toggle_complete_task(task_id: int, completed: bool = Form(...), current_user_id: str = Depends(get_current_user_id), session: Session = Depends(get_session)):
    """Toggle the completion status of a task for the authenticated user"""
    task = session.get(Task, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    # Verify that the task belongs to the user
    if task.user_id != current_user_id:
        raise HTTPException(status_code=403, detail="Not authorized to modify this task")

    task.completed = completed
    task.updated_at = datetime.utcnow()  # Update timestamp
    session.add(task)
    try:
        session.commit()
        session.refresh(task)
    except Exception as e:
        session.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating task: {str(e)}")

    return task