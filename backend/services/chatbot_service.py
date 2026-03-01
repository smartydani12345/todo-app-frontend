from sqlmodel import Session, select
from models.chat import Conversation, Message
from models.chatbot import ConversationCreate, MessageCreate
from typing import List
import uuid
from datetime import datetime


def create_conversation(session: Session, conversation: ConversationCreate) -> Conversation:
    """Create a new conversation."""
    db_conversation = Conversation.model_validate(conversation)
    session.add(db_conversation)
    session.commit()
    session.refresh(db_conversation)
    return db_conversation


def get_conversation_by_id(session: Session, conversation_id: int) -> Conversation:
    """Retrieve a conversation by its ID."""
    return session.get(Conversation, conversation_id)


def get_conversations_by_user(session: Session, user_id: str) -> List[Conversation]:
    """Retrieve all conversations for a specific user."""
    statement = select(Conversation).where(Conversation.user_id == user_id)
    result = session.execute(statement)
    return result.scalars().all()


def update_conversation(session: Session, conversation_id: int, title: str) -> Conversation:
    """Update a conversation's title."""
    db_conversation = session.get(Conversation, conversation_id)
    if db_conversation:
        db_conversation.title = title
        db_conversation.updated_at = datetime.utcnow()
        session.add(db_conversation)
        session.commit()
        session.refresh(db_conversation)
    return db_conversation


def delete_conversation(session: Session, conversation_id: int) -> bool:
    """Delete a conversation and all its messages."""
    # First delete all messages associated with the conversation
    statement = select(Message).where(Message.conversation_id == conversation_id)
    result = session.execute(statement)
    messages = result.scalars().all()
    for message in messages:
        session.delete(message)
    
    # Then delete the conversation itself
    conversation = session.get(Conversation, conversation_id)
    if conversation:
        session.delete(conversation)
        session.commit()
        return True
    return False


def create_message(session: Session, message: MessageCreate) -> Message:
    """Create a new message in a conversation."""
    db_message = Message.model_validate(message)
    session.add(db_message)
    session.commit()
    session.refresh(db_message)
    return db_message


def get_messages_by_conversation(session: Session, conversation_id: int, limit: int = 50) -> List[Message]:
    """Retrieve messages for a specific conversation, ordered by timestamp."""
    statement = select(Message).where(
        Message.conversation_id == conversation_id
    ).order_by(Message.timestamp.asc()).limit(limit)
    result = session.execute(statement)
    return result.scalars().all()


def update_message(session: Session, message_id: int, content: str) -> Message:
    """Update a message's content."""
    db_message = session.get(Message, message_id)
    if db_message:
        db_message.content = content
        session.add(db_message)
        session.commit()
        session.refresh(db_message)
    return db_message


def delete_message(session: Session, message_id: int) -> bool:
    """Delete a message."""
    message = session.get(Message, message_id)
    if message:
        session.delete(message)
        session.commit()
        return True
    return False