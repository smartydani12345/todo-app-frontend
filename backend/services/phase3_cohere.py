import os
from openai import OpenAI
from typing import Dict, Any, List, Optional, Callable
import logging
import httpx
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Define tool schemas for MCP-style tool calling
TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "add_task",
            "description": "Add a new task to the user's todo list. Use this when the user wants to create, add, or remember a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "title": {
                        "type": "string",
                        "description": "The title/description of the task to add"
                    },
                    "priority": {
                        "type": "string",
                        "enum": ["high", "medium", "low"],
                        "description": "Priority level of the task"
                    },
                    "tags": {
                        "type": "string",
                        "description": "Comma-separated tags for the task"
                    }
                },
                "required": ["title"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "complete_task",
            "description": "Mark a task as completed. Use when user says they finished or completed a task.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_identifier": {
                        "type": "string",
                        "description": "The task title or identifier to mark as complete"
                    }
                },
                "required": ["task_identifier"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "delete_task",
            "description": "Delete a task from the user's todo list.",
            "parameters": {
                "type": "object",
                "properties": {
                    "task_identifier": {
                        "type": "string",
                        "description": "The task title or identifier to delete"
                    }
                },
                "required": ["task_identifier"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "search_web",
            "description": "Search the web for information. Use when user asks 'what is', 'who is', 'search for', or asks about current events.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The search query"
                    }
                },
                "required": ["query"]
            }
        }
    },
    {
        "type": "function",
        "function": {
            "name": "list_tasks",
            "description": "List all tasks for the user. Use when user asks to show, list, or view their tasks.",
            "parameters": {
                "type": "object",
                "properties": {
                    "status": {
                        "type": "string",
                        "enum": ["all", "completed", "incomplete"],
                        "description": "Filter by task status"
                    }
                },
                "required": []
            }
        }
    }
]


class CohereService:
    """
    Service to interact with Cohere's command-a-03-2025 model via OpenAI SDK compatibility.
    This service provides a unified interface for AI interactions in the chatbot.
    """

    def __init__(self):
        # Initialize the OpenAI client with Cohere's API endpoint
        api_key = os.getenv("COHERE_API_KEY")
        base_url = os.getenv("COHERE_BASE_URL", "https://api.cohere.ai/compatibility/v1")
        self.model = os.getenv("COHERE_MODEL", "command-a-03-2025")
        
        if not api_key:
            # For development/testing purposes, we'll set up a mock client
            # that returns predefined responses instead of calling the real API
            self.client = None
            logger.warning("COHERE_API_KEY environment variable is not set. Using mock responses.")
        else:
            try:
                # Initialize httpx client to avoid proxies parameter issue
                http_client = httpx.Client(
                    base_url=base_url,
                    timeout=60.0
                )
                self.client = OpenAI(
                    api_key=api_key,
                    http_client=http_client,
                    base_url=base_url
                )
                logger.info(f"Cohere client initialized successfully with model: {self.model}")
            except Exception as e:
                logger.error(f"Error initializing Cohere client: {str(e)}")
                self.client = None

    def chat_completion(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict]] = None,
        tool_executor: Optional[Callable] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Generate a chat completion using Cohere's command-a-03-2025 model.
        Supports tool calling for MCP-style integrations.

        Args:
            messages: List of message dictionaries with 'role' and 'content' keys
            tools: Optional list of tool definitions for function calling
            tool_executor: Optional callable to execute tools (receives tool_name and arguments)
            **kwargs: Additional parameters to pass to the model

        Returns:
            Dictionary containing the AI response
        """
        if self.client is None:
            # Return a mock response when API key is not set
            logger.warning("Using mock response due to missing API key")
            return self._get_mock_response(messages, tools)

        try:
            # Prepare parameters for the API call
            params = {
                "model": self.model,
                "messages": messages,
                "temperature": kwargs.get("temperature", 0.7),
                "max_tokens": kwargs.get("max_tokens", 1000),
            }

            # Add tools if provided
            if tools:
                params["tools"] = tools

            response = self.client.chat.completions.create(**params)

            logger.info(f"Successfully generated completion with model: {self.model}")

            # Check if the model wants to call a tool
            choice = response.choices[0]
            message = choice.message

            # Handle tool calls
            if hasattr(message, 'tool_calls') and message.tool_calls:
                tool_results = []
                for tool_call in message.tool_calls:
                    function_name = tool_call.function.name
                    function_args = json.loads(tool_call.function.arguments)

                    logger.info(f"Tool call: {function_name} with args: {function_args}")

                    # Execute the tool if executor is provided
                    if tool_executor:
                        result = tool_executor(function_name, function_args)
                        tool_results.append({
                            "tool_call_id": tool_call.id,
                            "name": function_name,
                            "content": json.dumps(result) if isinstance(result, dict) else str(result)
                        })

                # If we have tool results, make another call to get the final response
                if tool_results and tool_executor:
                    # Add the assistant's tool call message
                    messages.append({
                        "role": "assistant",
                        "content": message.content,
                        "tool_calls": [{
                            "id": tc.id,
                            "type": "function",
                            "function": {
                                "name": tc.function.name,
                                "arguments": tc.function.arguments
                            }
                        } for tc in message.tool_calls]
                    })

                    # Add tool results
                    for result in tool_results:
                        messages.append({
                            "role": "tool",
                            "tool_call_id": result["tool_call_id"],
                            "content": result["content"]
                        })

                    # Get final response after tool execution
                    final_response = self.client.chat.completions.create(
                        model=self.model,
                        messages=messages,
                        temperature=kwargs.get("temperature", 0.7),
                        max_tokens=kwargs.get("max_tokens", 1000)
                    )

                    return {
                        "content": final_response.choices[0].message.content,
                        "role": "assistant",
                        "finish_reason": final_response.choices[0].finish_reason or "stop",
                        "usage": {
                            "prompt_tokens": final_response.usage.prompt_tokens if final_response.usage else 0,
                            "completion_tokens": final_response.usage.completion_tokens if final_response.usage else 0,
                            "total_tokens": final_response.usage.total_tokens if final_response.usage else 0
                        },
                        "tools_called": [tc.function.name for tc in message.tool_calls],
                        "tool_results": tool_results
                    }

                # Return tool call info if no executor
                return {
                    "content": message.content,
                    "role": "assistant",
                    "finish_reason": "tool_calls",
                    "usage": {
                        "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                        "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                        "total_tokens": response.usage.total_tokens if response.usage else 0
                    },
                    "tools_called": [tc.function.name for tc in message.tool_calls],
                    "tool_calls": [{
                        "name": tc.function.name,
                        "arguments": json.loads(tc.function.arguments)
                    } for tc in message.tool_calls]
                }

            # No tool calls, return normal response
            return {
                "content": message.content or "",
                "role": "assistant",
                "finish_reason": choice.finish_reason or "stop",
                "usage": {
                    "prompt_tokens": response.usage.prompt_tokens if response.usage else 0,
                    "completion_tokens": response.usage.completion_tokens if response.usage else 0,
                    "total_tokens": response.usage.total_tokens if response.usage else 0
                }
            }
        except Exception as e:
            logger.error(f"Error generating completion: {str(e)}")
            # Return a fallback response on error
            return {
                "content": f"I apologize, but I encountered an error processing your request. Please try again. Error: {str(e)}",
                "role": "assistant",
                "finish_reason": "error",
                "usage": {
                    "prompt_tokens": 0,
                    "completion_tokens": 0,
                    "total_tokens": 0
                }
            }

    def _get_mock_response(
        self,
        messages: List[Dict[str, str]],
        tools: Optional[List[Dict]] = None
    ) -> Dict[str, Any]:
        """
        Generate a mock response for testing purposes.

        Args:
            messages: List of message dictionaries
            tools: Optional list of available tools

        Returns:
            Dictionary containing a mock AI response
        """
        last_message = messages[-1]["content"] if messages else ""
        input_lower = last_message.lower()

        # Check if we should simulate tool calls
        if tools:
            # Simulate add_task tool call
            if any(phrase in input_lower for phrase in [
                "add task", "create task", "add a task", "create a task",
                "yaad karao", "kaam jodo", "reminder", "remind me"
            ]):
                # Extract task title from message
                title = last_message
                for phrase in ["add task", "create task", "add a task", "create a task",
                              "yaad karao", "kaam jodo", "reminder", "remind me to"]:
                    title = title.replace(phrase, "").strip()
                title = title.strip(" '\"-")

                return {
                    "content": f"I've added the task '{title}' to your list.",
                    "role": "assistant",
                    "finish_reason": "stop",
                    "tools_called": ["add_task"],
                    "tool_calls": [{"name": "add_task", "arguments": {"title": title, "priority": "medium"}}],
                    "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                }

            # Simulate search tool call
            if any(phrase in input_lower for phrase in [
                "search", "what is", "who is", "google", "look up"
            ]):
                query = last_message
                for phrase in ["search for", "what is", "who is", "google", "look up"]:
                    query = query.replace(phrase, "").strip()

                return {
                    "content": f"Here's what I found about '{query}': [Search results would appear here]",
                    "role": "assistant",
                    "finish_reason": "stop",
                    "tools_called": ["search_web"],
                    "tool_calls": [{"name": "search_web", "arguments": {"query": query}}],
                    "usage": {"prompt_tokens": 0, "completion_tokens": 0, "total_tokens": 0}
                }

        # Simple keyword-based mock responses
        if "task" in input_lower or "todo" in input_lower:
            content = "I can help you manage your tasks! You can create, update, complete, or delete tasks. Try saying 'Add a task to buy groceries' or 'Show my tasks'."
        elif "hello" in input_lower or "hi" in input_lower:
            content = "Hello! I'm your AI assistant for the Todo Evolution app. How can I help you today?"
        elif "help" in input_lower:
            content = "I can help you with:\n1. Creating tasks: 'Add a task to...'\n2. Listing tasks: 'Show my tasks'\n3. Completing tasks: 'Mark task as done'\n4. Deleting tasks: 'Delete task...'\n5. Answering questions about the app\n\nWhat would you like to do?"
        else:
            content = "This is a mock response. The AI model is not fully configured. Please ensure the COHERE_API_KEY environment variable is set correctly."

        return {
            "content": content,
            "role": "assistant",
            "finish_reason": "stop",
            "usage": {
                "prompt_tokens": 0,
                "completion_tokens": 0,
                "total_tokens": 0
            }
        }

    def execute_tool(
        self,
        tool_name: str,
        arguments: Dict[str, Any],
        user_id: str,
        db_session: Optional[Any] = None,
        search_service: Optional[Any] = None
    ) -> Dict[str, Any]:
        """
        Execute a tool with the given arguments.

        Args:
            tool_name: Name of the tool to execute
            arguments: Arguments for the tool
            user_id: ID of the user making the request
            db_session: Database session for task operations
            search_service: Search service for web searches

        Returns:
            Result of the tool execution
        """
        try:
            if tool_name == "add_task":
                if db_session is None:
                    return {"success": False, "error": "Database session not available"}

                from database.models import Task
                from datetime import datetime

                title = arguments.get("title", "Untitled Task")
                priority = arguments.get("priority", "medium")
                tags = arguments.get("tags", "")

                # Create task data with all required fields including timestamps
                task_data = {
                    "title": title,
                    "description": arguments.get("description", ""),
                    "completed": False,
                    "priority": priority,
                    "tags": tags if isinstance(tags, str) else ",".join(tags) if isinstance(tags, list) else "",
                    "user_id": user_id,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow()
                }
                
                # Use model_validate to handle default factories properly
                task = Task.model_validate(task_data)

                db_session.add(task)
                db_session.commit()
                db_session.refresh(task)

                logger.info(f"Tool add_task: Created task '{title}' (ID: {task.id}) for user {user_id}")

                return {
                    "success": True,
                    "task_id": task.id,
                    "title": task.title,
                    "priority": task.priority,
                    "tags": task.tags,
                    "message": f"Task '{title}' added successfully"
                }

            elif tool_name == "complete_task":
                if db_session is None:
                    return {"success": False, "error": "Database session not available"}

                from database.models import Task
                from sqlmodel import select

                identifier = arguments.get("task_identifier", "")

                statement = select(Task).where(
                    Task.user_id == user_id,
                    Task.completed == False
                )
                tasks = db_session.exec(statement).all()

                matched_task = None
                for task in tasks:
                    if identifier.lower() in task.title.lower() or task.title.lower() in identifier.lower():
                        matched_task = task
                        break

                if matched_task:
                    matched_task.completed = True
                    matched_task.updated_at = datetime.utcnow()
                    db_session.add(matched_task)
                    db_session.commit()

                    logger.info(f"Tool complete_task: Completed task '{matched_task.title}' for user {user_id}")

                    return {
                        "success": True,
                        "task_id": matched_task.id,
                        "title": matched_task.title,
                        "message": f"Task '{matched_task.title}' marked as complete"
                    }
                else:
                    return {"success": False, "error": f"Task '{identifier}' not found"}

            elif tool_name == "delete_task":
                if db_session is None:
                    return {"success": False, "error": "Database session not available"}

                from database.models import Task
                from sqlmodel import select

                identifier = arguments.get("task_identifier", "")

                statement = select(Task).where(Task.user_id == user_id)
                tasks = db_session.exec(statement).all()

                matched_task = None
                for task in tasks:
                    if identifier.lower() in task.title.lower() or task.title.lower() in identifier.lower():
                        matched_task = task
                        break

                if matched_task:
                    task_id = matched_task.id
                    task_title = matched_task.title
                    db_session.delete(matched_task)
                    db_session.commit()

                    logger.info(f"Tool delete_task: Deleted task '{task_title}' (ID: {task_id}) for user {user_id}")

                    return {
                        "success": True,
                        "task_id": task_id,
                        "title": task_title,
                        "message": f"Task '{task_title}' deleted successfully"
                    }
                else:
                    return {"success": False, "error": f"Task '{identifier}' not found"}

            elif tool_name == "search_web":
                if search_service is None:
                    return {"success": False, "error": "Search service not available"}

                query = arguments.get("query", "")
                logger.info(f"Tool search_web: Searching for '{query}'")
                
                search_result = search_service.search(query)

                if search_result.get("success"):
                    results = search_result.get("results", [])
                    formatted = search_service.format_results_for_chat(search_result)
                    
                    logger.info(f"Tool search_web: Found {len(results)} results for '{query}'")
                    
                    return {
                        "success": True,
                        "query": query,
                        "results": results,
                        "formatted": formatted
                    }
                else:
                    return {"success": False, "error": search_result.get("error", "Search failed")}

            elif tool_name == "list_tasks":
                if db_session is None:
                    return {"success": False, "error": "Database session not available"}

                from database.models import Task
                from sqlmodel import select

                status = arguments.get("status", "all")

                statement = select(Task).where(Task.user_id == user_id)
                if status == "completed":
                    statement = statement.where(Task.completed == True)
                elif status == "incomplete":
                    statement = statement.where(Task.completed == False)

                tasks = db_session.exec(statement).all()

                task_list = [
                    {
                        "id": task.id,
                        "title": task.title,
                        "completed": task.completed,
                        "priority": task.priority,
                        "tags": task.tags
                    }
                    for task in tasks
                ]

                logger.info(f"Tool list_tasks: Found {len(task_list)} tasks for user {user_id}")

                return {
                    "success": True,
                    "count": len(task_list),
                    "tasks": task_list
                }

            else:
                return {"success": False, "error": f"Unknown tool: {tool_name}"}

        except Exception as e:
            logger.error(f"Error executing tool {tool_name}: {str(e)}")
            import traceback
            logger.error(traceback.format_exc())
            return {"success": False, "error": str(e)}

    def embed_text(self, texts: List[str]) -> List[List[float]]:
        """
        Generate embeddings for the given texts using Cohere's embedding model.

        Args:
            texts: List of texts to embed

        Returns:
            List of embeddings (each embedding is a list of floats)
        """
        if self.client is None:
            logger.warning("Cannot generate embeddings - client not initialized")
            return [[] for _ in texts]
            
        try:
            response = self.client.embeddings.create(
                model="embed-english-v3.0",
                input=texts
            )

            return [item.embedding for item in response.data]
        except Exception as e:
            logger.error(f"Error generating embeddings: {str(e)}")
            raise


# Global instance of the service
cohere_service = CohereService()


def get_cohere_service() -> CohereService:
    """
    Get the global instance of CohereService.

    Returns:
        CohereService instance
    """
    return cohere_service
