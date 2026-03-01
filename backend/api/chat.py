from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Dict, Any
from auth.jwt import get_current_user
from services.phase3_ai_service import get_ai_service
from services.phase3_auth_validation import validate_chat_token
from database.session import get_session
from models.chat import Conversation, Message
from models.user import User
from datetime import datetime
from sqlalchemy import desc
import logging

router = APIRouter(tags=["chat"])

@router.post("/chat")
async def chat_endpoint(
    message: str,
    language: str = "en",
    conversation_id: int = None,
    current_user: Dict[str, Any] = Depends(validate_chat_token),
    db_session: Session = Depends(get_session)
):
    """
    Main chat endpoint that processes user messages and returns AI responses.
    Supports MCP-style tool calling for task operations and web search.

    Args:
        message: The user's message to the chatbot
        language: The language of the message (defaults to 'en')
        conversation_id: ID of existing conversation (optional)
        current_user: The authenticated user making the request
        db_session: Database session for database operations

    Returns:
        JSON response containing the AI's response and conversation metadata
    """
    try:
        start_time = datetime.now()

        # Get the AI service
        ai_service = get_ai_service()

        # Validate language parameter
        supported_languages = ["en", "ur", "roman_ur", "roman_en"]
        if language not in supported_languages:
            language = "en"  # Default to English if unsupported language provided

        # Get or create conversation
        if conversation_id:
            # Retrieve existing conversation
            conversation = db_session.get(Conversation, conversation_id)
            if not conversation:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Conversation not found"
                )

            # Verify that the conversation belongs to the current user
            if conversation.user_id != current_user["user_id"]:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Access denied: Cannot access conversations belonging to other users"
                )
        else:
            # Create new conversation
            conversation = Conversation(
                user_id=current_user["user_id"],
                title=message[:50] + "..." if len(message) > 50 else message,
                status="active"
            )
            db_session.add(conversation)
            db_session.commit()
            db_session.refresh(conversation)

        # Create user message record
        user_message = Message(
            conversation_id=conversation.id,
            role="user",
            content=message,
            language=language,
            timestamp=datetime.utcnow()
        )
        db_session.add(user_message)
        db_session.commit()

        # Get conversation history for context
        # Get last 10 messages for context (adjust as needed)
        conversation_messages = db_session.exec(
            select(Message).where(Message.conversation_id == conversation.id).order_by(desc(Message.timestamp)).limit(10)
        ).all()

        # Reverse to get chronological order
        conversation_history = []
        for msg in reversed(conversation_messages):
            conversation_history.append({
                "role": msg.role,
                "content": msg.content
            })

        # Process the request with AI service (includes tool calling)
        ai_response = ai_service.process_chat_request(
            user_input=message,
            user_id=current_user["user_id"],
            db_session=db_session,
            conversation_history=conversation_history[:-1] if conversation_history else [],
            language=language
        )

        # Create AI response message record
        ai_message = Message(
            conversation_id=conversation.id,
            role="assistant",
            content=ai_response["response"],
            language=language,
            timestamp=datetime.utcnow(),
            tools_used=str(ai_response.get("tools_used", {}))
        )
        db_session.add(ai_message)
        db_session.commit()

        # Update conversation timestamp
        conversation.updated_at = datetime.utcnow()
        db_session.add(conversation)
        db_session.commit()

        # Calculate response time
        response_time = (datetime.now() - start_time).total_seconds()
        logging.info(f"Chat response time: {response_time:.2f}s for user {current_user['user_id']}")

        # Build response with tool information
        response_data = {
            "response": ai_response["response"],
            "conversation_id": conversation.id,
            "message_id": ai_message.id,
            "timestamp": datetime.utcnow().isoformat(),
            "language": language,
            "response_time": round(response_time, 2)
        }

        # Add tool information if tools were used
        if ai_response.get("tools_used"):
            response_data["tools_used"] = ai_response["tools_used"]

        # Add task data if a task was created
        if ai_response.get("task_data"):
            response_data["task_data"] = ai_response["task_data"]

        # Add search results if search was performed
        if ai_response.get("search_performed"):
            response_data["search_performed"] = True
            response_data["search_results"] = ai_response.get("search_results", [])
            response_data["search_query"] = ai_response.get("search_query", "")

        # Return response
        return response_data

    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error in chat endpoint: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while processing your request"
        )


@router.get("/chat/conversations")
async def get_conversations(
    current_user: Dict[str, Any] = Depends(validate_chat_token),
    db_session: Session = Depends(get_session)
):
    """Get all conversations for the current user"""
    conversations = db_session.exec(
        select(Conversation)
        .where(Conversation.user_id == current_user["user_id"])
        .where(Conversation.status == "active")
        .order_by(desc(Conversation.updated_at))
    ).all()
    return conversations


@router.get("/chat/conversations/{conversation_id}/messages")
async def get_messages(
    conversation_id: int,
    current_user: Dict[str, Any] = Depends(validate_chat_token),
    db_session: Session = Depends(get_session)
):
    """Get all messages for a specific conversation"""
    # Verify conversation belongs to user
    conversation = db_session.get(Conversation, conversation_id)
    if not conversation or conversation.user_id != current_user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Conversation not found"
        )

    messages = db_session.exec(
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.timestamp)
    ).all()
    return messages


@router.post("/chat/conversations")
async def create_conversation(
    title: str,
    language: str = "en",
    current_user: Dict[str, Any] = Depends(validate_chat_token),
    db_session: Session = Depends(get_session)
):
    """Create a new conversation"""
    from datetime import datetime
    
    # Create conversation using model_validate to handle default factories
    conversation_data = {
        "user_id": current_user["user_id"],
        "title": title,
        "language": language,
        "status": "active",
        "created_at": datetime.utcnow(),
        "updated_at": datetime.utcnow()
    }
    conversation = Conversation.model_validate(conversation_data)
    
    db_session.add(conversation)
    db_session.commit()
    db_session.refresh(conversation)
    return conversation
