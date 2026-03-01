from fastapi import Depends, HTTPException, status
from auth.jwt import get_current_user, get_current_user_id
from typing import Dict, Any

async def validate_chat_token(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Validate JWT token specifically for chatbot endpoints.
    This function ensures that the user is authenticated before
    allowing access to chat functionality.

    Returns:
        Dict containing user information from the token
    """
    # Additional validation specific to chatbot functionality
    # Check if user has chatbot enabled
    if not current_user.get("chatbot_enabled", True):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Chatbot functionality is disabled for this user"
        )

    return current_user
