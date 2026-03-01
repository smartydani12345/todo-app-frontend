from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
import os
from datetime import datetime

from auth.jwt import get_current_user
from models.user import UserResponse as User
from database.session import get_session
from models.chat import Conversation, Message
from models.chatbot import ConversationCreate, MessageCreate
from services.chatbot_service import (
    create_conversation, get_conversation_by_id, get_conversations_by_user,
    create_message, get_messages_by_conversation
)

# Initialize router
router = APIRouter(prefix="/chat", tags=["chat"])

# Import OpenAI compatible client for Cohere
try:
    from openai import OpenAI
    from dotenv import load_dotenv
    
    # Load environment variables from .env file
    load_dotenv()
    
    COHERE_API_KEY = os.getenv("COHERE_API_KEY")
    COHERE_BASE_URL = os.getenv("COHERE_BASE_URL", "https://api.cohere.ai/v1/")
    COHERE_MODEL = os.getenv("COHERE_MODEL", "command-r")

    if not COHERE_API_KEY:
        # For testing purposes, we'll log this but not raise an error immediately
        # The error will be raised when trying to use the client
        client = None
        print("WARNING: COHERE_API_KEY environment variable is not set. Chat functionality will be limited.")
    else:
        # Initialize client with Cohere API and OpenAI compatibility
        # Note: Using httpx client directly to avoid proxies parameter issue
        import httpx
        http_client = httpx.Client(base_url=COHERE_BASE_URL)
        client = OpenAI(
            api_key=COHERE_API_KEY,
            http_client=http_client,
        )
        print(f"Cohere client initialized successfully with model: {COHERE_MODEL}")
except ImportError:
    client = None
    print("WARNING: OpenAI package is not installed. Chat functionality will be limited. Install with: pip install openai")


@router.post("/conversations", response_model=Conversation)
async def create_new_conversation(
    conversation: ConversationCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Create a new conversation."""
    # Override user_id to be the authenticated user's ID
    # Create a new instance to avoid modifying the original
    conversation_dict = conversation.model_dump()
    conversation_dict["user_id"] = current_user["user_id"]
    
    # Set default title if not provided
    if not conversation_dict["title"]:
        conversation_dict["title"] = f"Conversation {datetime.utcnow().strftime('%Y-%m-%d %H:%M')}"
    
    # Create a new ConversationCreate instance with the updated user_id
    validated_conversation = ConversationCreate(**conversation_dict)
    db_conversation = create_conversation(session, validated_conversation)
    return db_conversation


@router.get("/conversations/{conversation_id}", response_model=Conversation)
async def get_conversation(
    conversation_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get a specific conversation by ID."""
    db_conversation = get_conversation_by_id(session, conversation_id)
    if not db_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    # Verify that the conversation belongs to the current user
    if db_conversation.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    return db_conversation


@router.get("/conversations", response_model=List[Conversation])
async def list_conversations(
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """List all conversations for the current user."""
    conversations = get_conversations_by_user(session, current_user["user_id"])
    return conversations


@router.post("/conversations/{conversation_id}/messages", response_model=Message)
async def send_message(
    conversation_id: int,
    message: MessageCreate,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Send a message in a conversation and get AI response."""
    # Verify that the conversation exists and belongs to the user
    db_conversation = get_conversation_by_id(session, conversation_id)
    if not db_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    if db_conversation.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    # Save user's message
    message_dict = message.model_dump()
    message_dict["role"] = "user"
    message_dict["language"] = db_conversation.language
    validated_message = MessageCreate(**message_dict)
    user_message = create_message(session, validated_message)
    
    # Get AI response using Cohere
    try:
        # Get recent conversation history for context
        recent_messages = get_messages_by_conversation(session, conversation_id, limit=10)
        
        # Format messages for the AI model
        formatted_messages = []
        for msg in recent_messages:
            role = "user" if msg.role == "user" else "assistant"
            formatted_messages.append({
                "role": role,
                "content": msg.content
            })
        
        # Add the current user message
        formatted_messages.append({
            "role": "user",
            "content": message.content
        })
        
        # Check if client is available
        if client is None:
            # Return a mock response for testing purposes
            ai_response = "This is a mock response. The AI model is not configured. Please set the COHERE_API_KEY environment variable."
        else:
            # Call the AI model
            response = client.chat.completions.create(
                model="command-r",  # Using Cohere's command-r model
                messages=formatted_messages,
                temperature=0.7,
                max_tokens=500,
            )
            
            # Extract the AI's response
            ai_response = response.choices[0].message.content
        
        # Create AI message
        ai_message_data = {
            "conversation_id": conversation_id,
            "role": "assistant",
            "content": ai_response,
            "language": db_conversation.language
        }
        ai_message = MessageCreate(**ai_message_data)
        ai_db_message = create_message(session, ai_message)

        return ai_db_message
    except Exception as e:
        # Log the error with full traceback for debugging
        import traceback
        error_detail = f"{str(e)}\n{traceback.format_exc()}"
        print(f"Error calling AI model: {error_detail}")
        
        # Return a user-friendly error message without technical details
        ai_response = "I apologize, but I'm having a bit of trouble processing that right now. Let me try again..."
        
        # Try to create a fallback AI message
        try:
            ai_message_data = {
                "conversation_id": conversation_id,
                "role": "assistant",
                "content": ai_response,
                "language": db_conversation.language
            }
            ai_message = MessageCreate(**ai_message_data)
            ai_db_message = create_message(session, ai_message)
            return ai_db_message
        except Exception:
            # If even the fallback fails, just return the error silently
            # The frontend will handle showing an appropriate message
            raise HTTPException(
                status_code=500,
                detail="Temporary service issue. Please try again."
            )


@router.get("/conversations/{conversation_id}/messages", response_model=List[Message])
async def get_conversation_messages(
    conversation_id: int,
    current_user: dict = Depends(get_current_user),
    session: Session = Depends(get_session)
):
    """Get all messages in a conversation."""
    # Verify that the conversation exists and belongs to the user
    db_conversation = get_conversation_by_id(session, conversation_id)
    if not db_conversation:
        raise HTTPException(status_code=404, detail="Conversation not found")
    
    if db_conversation.user_id != current_user["user_id"]:
        raise HTTPException(status_code=403, detail="Access denied")
    
    messages = get_messages_by_conversation(session, conversation_id)
    return messages