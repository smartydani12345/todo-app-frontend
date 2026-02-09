import pytest
from fastapi import HTTPException
from auth.jwt import verify_token, get_current_user, get_current_user_id
from unittest.mock import Mock
import os
import jwt

def test_verify_token_valid():
    """Test verifying a valid JWT token"""
    # Create a mock token
    secret = os.getenv("BETTER_AUTH_SECRET", "fallback_secret_for_dev")
    payload = {"sub": "test_user_id", "email": "test@example.com", "name": "Test User"}
    token = jwt.encode(payload, secret, algorithm="HS256")

    result = verify_token(token)
    assert result["sub"] == "test_user_id"
    assert result["email"] == "test@example.com"
    assert result["name"] == "Test User"

def test_verify_token_invalid():
    """Test verifying an invalid JWT token"""
    # Use an invalid token
    invalid_token = "invalid.token.here"

    with pytest.raises(HTTPException) as exc_info:
        verify_token(invalid_token)

    assert exc_info.value.status_code == 401

def test_verify_token_missing_sub():
    """Test verifying a token without sub field"""
    # Create a token without sub field
    secret = os.getenv("BETTER_AUTH_SECRET", "fallback_secret_for_dev")
    payload = {"email": "test@example.com"}  # Missing 'sub'
    token = jwt.encode(payload, secret, algorithm="HS256")

    with pytest.raises(HTTPException) as exc_info:
        verify_token(token)

    assert exc_info.value.status_code == 401

def test_verify_token_expired():
    """Test verifying an expired JWT token"""
    # Create an expired token
    import time
    secret = os.getenv("BETTER_AUTH_SECRET", "fallback_secret_for_dev")
    payload = {"sub": "test_user_id", "exp": time.time() - 100}  # Expired 100 seconds ago
    token = jwt.encode(payload, secret, algorithm="HS256")

    with pytest.raises(HTTPException) as exc_info:
        verify_token(token)

    assert exc_info.value.status_code == 401