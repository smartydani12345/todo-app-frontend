from fastapi import HTTPException, status, Request
from typing import Union

def get_current_user_id(request: Request) -> Union[int, str]:
    """
    Extract user ID from the Authorization header in format 'UserId <id>'
    """
    authorization = request.headers.get("authorization")

    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated"
        )

    try:
        # Expected format: "UserId <user_id>"
        parts = authorization.split(" ")
        if len(parts) != 2 or parts[0].lower() != "userid":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization header format"
            )

        user_id = parts[1]  # Keep as string since it's a UUID
        return user_id

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authorization header"
        )