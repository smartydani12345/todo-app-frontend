from typing import Dict, Any, Optional
from sqlmodel import Session, select
from database.models import Task
from models.task import TaskCreate, TaskUpdate, TaskBase, TaskPublic
from models.user import User
from database.session import get_session
import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TaskService:
    """
    Service to handle task operations based on natural language input.
    This service parses user requests to create, update, delete, or complete tasks.
    """
    
    def __init__(self, db_session: Session):
        self.db_session = db_session
    
    def process_natural_language_request(self, user_input: str, user_id: str) -> Dict[str, Any]:
        """
        Process a natural language request to perform task operations.
        
        Args:
            user_input: The natural language request from the user
            user_id: The ID of the user making the request
            
        Returns:
            Dictionary containing the result of the operation
        """
        # Convert to lowercase for easier processing
        user_input_lower = user_input.lower().strip()
        
        # Check for different types of requests
        if self._is_create_request(user_input_lower):
            return self._handle_create_request(user_input, user_id)
        elif self._is_complete_request(user_input_lower):
            return self._handle_complete_request(user_input, user_id)
        elif self._is_edit_request(user_input_lower):
            return self._handle_edit_request(user_input, user_id)
        elif self._is_delete_request(user_input_lower):
            return self._handle_delete_request(user_input, user_id)
        else:
            # If we can't determine the intent, return a message
            return {
                "success": False,
                "message": "I couldn't understand your request. Please try rephrasing.",
                "operation": "unknown"
            }
    
    def _is_create_request(self, user_input: str) -> bool:
        """Check if the user wants to create a task."""
        create_indicators = [
            "add a task", "create a task", "add task", "create task", 
            "new task", "add to my list", "put on my list", "remind me to",
            "need to", "have to", "should", "must", "want to"
        ]
        return any(indicator in user_input for indicator in create_indicators)
    
    def _is_complete_request(self, user_input: str) -> bool:
        """Check if the user wants to complete a task."""
        complete_indicators = [
            "complete", "finish", "done", "finished", "mark as done", 
            "check off", "tick off", "accomplish", "achieve", "did",
            "already did", "already completed", "already finished"
        ]
        return any(indicator in user_input for indicator in complete_indicators)
    
    def _is_edit_request(self, user_input: str) -> bool:
        """Check if the user wants to edit a task."""
        edit_indicators = [
            "edit", "change", "update", "modify", "alter", "fix", 
            "correct", "adjust", "revise", "improve"
        ]
        return any(indicator in user_input for indicator in edit_indicators)
    
    def _is_delete_request(self, user_input: str) -> bool:
        """Check if the user wants to delete a task."""
        delete_indicators = [
            "delete", "remove", "get rid of", "eliminate", "cancel",
            "trash", "dispose", "erase", "destroy", "scratch"
        ]
        return any(indicator in user_input for indicator in delete_indicators)
    
    def _extract_task_title(self, user_input: str) -> str:
        """Extract the task title from the user input."""
        # Remove common phrases that indicate task creation
        phrases_to_remove = [
            "add a task to ", "create a task to ", "add task to ",
            "create task to ", "add to my list ", "put on my list ",
            "remind me to ", "need to ", "have to ", "should ",
            "must ", "want to ", "please ", "can you ", "could you "
        ]
        
        cleaned_input = user_input.lower().strip()
        for phrase in phrases_to_remove:
            if cleaned_input.startswith(phrase):
                cleaned_input = cleaned_input[len(phrase):]
                break
        
        # If the cleaned input still has common verbs, try to extract the meaningful part
        if any(cleaned_input.startswith(verb) for verb in ["to ", "for ", "that "]):
            # Look for the next meaningful word
            parts = cleaned_input.split(" ")
            if len(parts) > 1:
                cleaned_input = " ".join(parts[1:])
        
        # Capitalize the first letter
        if cleaned_input:
            cleaned_input = cleaned_input[0].upper() + cleaned_input[1:]
        
        return cleaned_input.strip()
    
    def _extract_task_identifier(self, user_input: str) -> str:
        """Extract the identifier (title or number) of the task to be operated on."""
        # Look for common patterns like "the meeting task", "task about groceries", etc.
        patterns = [
            r"the (.+?) task",
            r"task (.+?) ",
            r"task about (.+?) ",
            r"task to (.+?) ",
            r"task that (.+?) ",
            r"(\w+) task",
            r"task (.+)$"
        ]
        
        for pattern in patterns:
            match = re.search(pattern, user_input.lower())
            if match:
                identifier = match.group(1).strip()
                # Remove common words that don't help identify the task
                identifier = re.sub(r"(is|was|will be|should be|needs to be)", "", identifier).strip()
                return identifier
        
        # If no pattern matches, return the original input
        return user_input.strip()
    
    def _handle_create_request(self, user_input: str, user_id: str) -> Dict[str, Any]:
        """Handle requests to create a new task."""
        try:
            title = self._extract_task_title(user_input)
            
            if not title:
                return {
                    "success": False,
                    "message": "I couldn't identify what task you want to create.",
                    "operation": "create"
                }
            
            # Create the task
            task = Task(
                title=title,
                description="",  # Could be enhanced to extract description
                completed=False,
                priority="medium",
                user_id=user_id
            )
            
            self.db_session.add(task)
            self.db_session.commit()
            self.db_session.refresh(task)
            
            logger.info(f"Created task '{title}' for user {user_id}")
            
            return {
                "success": True,
                "message": f"I've added the task '{title}' to your list.",
                "operation": "create",
                "task": {
                    "id": task.id,
                    "title": task.title,
                    "completed": task.completed
                }
            }
        except Exception as e:
            logger.error(f"Error creating task: {str(e)}")
            return {
                "success": False,
                "message": "Sorry, I couldn't create that task. Please try again.",
                "operation": "create"
            }
    
    def _handle_complete_request(self, user_input: str, user_id: str) -> Dict[str, Any]:
        """Handle requests to complete a task."""
        try:
            identifier = self._extract_task_identifier(user_input)
            
            # Find the task by title or partial match
            statement = select(Task).where(
                Task.user_id == user_id,
                Task.completed == False  # Only look for incomplete tasks
            )
            tasks = self.db_session.exec(statement).all()
            
            # Find the best match
            matched_task = None
            for task in tasks:
                if identifier.lower() in task.title.lower() or task.title.lower() in identifier.lower():
                    matched_task = task
                    break
            
            if not matched_task:
                return {
                    "success": False,
                    "message": f"I couldn't find a task matching '{identifier}' in your list.",
                    "operation": "complete"
                }
            
            # Mark the task as completed
            matched_task.completed = True
            self.db_session.add(matched_task)
            self.db_session.commit()
            
            logger.info(f"Completed task '{matched_task.title}' for user {user_id}")
            
            return {
                "success": True,
                "message": f"I've marked the task '{matched_task.title}' as completed.",
                "operation": "complete",
                "task": {
                    "id": matched_task.id,
                    "title": matched_task.title,
                    "completed": matched_task.completed
                }
            }
        except Exception as e:
            logger.error(f"Error completing task: {str(e)}")
            return {
                "success": False,
                "message": "Sorry, I couldn't complete that task. Please try again.",
                "operation": "complete"
            }
    
    def _handle_edit_request(self, user_input: str, user_id: str) -> Dict[str, Any]:
        """Handle requests to edit a task."""
        # Extract both the identifier and the new content
        # Pattern: edit "task title" to "new content" or change "task title" to "new content"
        edit_pattern = r'(?:edit|change|update)\s+(?:the\s+)?(.+?)\s+(?:to|with|as)\s+(.+)$'
        match = re.search(edit_pattern, user_input.lower())
        
        try:
            if not match:
                # If the pattern doesn't match, try to extract info differently
                identifier = self._extract_task_identifier(user_input)
                
                # Find the task by title or partial match
                statement = select(Task).where(
                    Task.user_id == user_id
                )
                tasks = self.db_session.exec(statement).all()
                
                # Find the best match
                matched_task = None
                for task in tasks:
                    if identifier.lower() in task.title.lower() or task.title.lower() in identifier.lower():
                        matched_task = task
                        break
                
                if not matched_task:
                    return {
                        "success": False,
                        "message": f"I couldn't find a task matching '{identifier}' in your list.",
                        "operation": "edit"
                    }
                
                # For now, return a message indicating we need more specific instructions
                return {
                    "success": False,
                    "message": f"I found the task '{matched_task.title}', but I need more specific instructions on how to edit it. Please specify what you'd like to change.",
                    "operation": "edit"
                }
            else:
                identifier = match.group(1).strip()
                new_content = match.group(2).strip()
                
                # Find the task by title or partial match
                statement = select(Task).where(
                    Task.user_id == user_id
                )
                tasks = self.db_session.exec(statement).all()
                
                # Find the best match
                matched_task = None
                for task in tasks:
                    if identifier.lower() in task.title.lower() or task.title.lower() in identifier.lower():
                        matched_task = task
                        break
                
                if not matched_task:
                    return {
                        "success": False,
                        "message": f"I couldn't find a task matching '{identifier}' in your list.",
                        "operation": "edit"
                    }
                
                # Update the task title
                old_title = matched_task.title
                matched_task.title = new_content[0].upper() + new_content[1:] if new_content else matched_task.title
                self.db_session.add(matched_task)
                self.db_session.commit()
                
                logger.info(f"Updated task '{old_title}' to '{matched_task.title}' for user {user_id}")
                
                return {
                    "success": True,
                    "message": f"I've updated the task '{old_title}' to '{matched_task.title}'.",
                    "operation": "edit",
                    "task": {
                        "id": matched_task.id,
                        "title": matched_task.title,
                        "completed": matched_task.completed
                    }
                }
        except Exception as e:
            logger.error(f"Error editing task: {str(e)}")
            return {
                "success": False,
                "message": "Sorry, I couldn't edit that task. Please try again.",
                "operation": "edit"
            }
    
    def _handle_delete_request(self, user_input: str, user_id: str) -> Dict[str, Any]:
        """Handle requests to delete a task."""
        try:
            identifier = self._extract_task_identifier(user_input)
            
            # Find the task by title or partial match
            statement = select(Task).where(
                Task.user_id == user_id
            )
            tasks = self.db_session.exec(statement).all()
            
            # Find the best match
            matched_task = None
            for task in tasks:
                if identifier.lower() in task.title.lower() or task.title.lower() in identifier.lower():
                    matched_task = task
                    break
            
            if not matched_task:
                return {
                    "success": False,
                    "message": f"I couldn't find a task matching '{identifier}' in your list.",
                    "operation": "delete"
                }
            
            # Delete the task
            self.db_session.delete(matched_task)
            self.db_session.commit()
            
            logger.info(f"Deleted task '{matched_task.title}' for user {user_id}")
            
            return {
                "success": True,
                "message": f"I've deleted the task '{matched_task.title}' from your list.",
                "operation": "delete",
                "task": {
                    "id": matched_task.id,
                    "title": matched_task.title
                }
            }
        except Exception as e:
            logger.error(f"Error deleting task: {str(e)}")
            return {
                "success": False,
                "message": "Sorry, I couldn't delete that task. Please try again.",
                "operation": "delete"
            }

def get_task_service(db_session: Session) -> TaskService:
    """
    Get an instance of TaskService.

    Args:
        db_session: The database session to use

    Returns:
        TaskService instance
    """
    return TaskService(db_session)