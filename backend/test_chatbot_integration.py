import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from sqlmodel import Session
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

# Import our app
from main import app
from database.init_db import engine, create_db_and_tables
from models.user import User
from models.chat import Conversation, Message

# Initialize database tables before creating the test client
create_db_and_tables()

# Create test client
client = TestClient(app)

# Global variables to share state between tests
shared_token = None
shared_email = None
shared_user_id = None

def test_basic_auth():
    """Test basic auth functionality"""
    global shared_token, shared_email, shared_user_id
    print("Testing basic auth functionality...")
    
    import time
    shared_email = f"test_auth_{int(time.time())}@example.com"
    
    # Register a user
    register_response = client.post(
        "/api/auth/register",
        data={
            "name": "Test User",
            "email": shared_email,
            "password": "password123"
        }
    )
    
    print(f"Registration status: {register_response.status_code}")
    if register_response.status_code == 200:
        print(f"Registration response: {register_response.json()}")
    else:
        print(f"Registration failed: {register_response.text}")
    
    if register_response.status_code != 200:
        return False
    
    # Extract token and user info
    response_data = register_response.json()
    shared_token = response_data.get("access_token")
    user_info = response_data.get("user")
    if user_info:
        shared_user_id = user_info.get("id")
    
    print(f"Access token received: {'Yes' if shared_token else 'No'}")
    print(f"User ID: {shared_user_id}")
    
    if not shared_token:
        print("No access token in response")
        return False
    
    # Try to access protected endpoint
    headers = {"Authorization": f"Bearer {shared_token}"}
    profile_response = client.get("/api/auth/me", headers=headers)
    
    print(f"Profile access status: {profile_response.status_code}")
    if profile_response.status_code == 200:
        print(f"Profile response: {profile_response.json()}")
    else:
        print(f"Profile access failed: {profile_response.text}")
    
    return profile_response.status_code == 200

def test_chatbot_integration():
    """
    Test the complete chatbot integration workflow:
    1. Use the existing authenticated user
    2. Create a conversation
    3. Send a message
    4. Verify response
    """
    global shared_token, shared_email, shared_user_id
    print("\nStarting chatbot integration test...")
    
    # Step 1: Use the existing authenticated user
    if not shared_token:
        print("No shared token available. Did basic auth test run?")
        return False
    
    print(f"\n1. Using existing authenticated user with email: {shared_email}")
    
    # Step 2: Create a conversation
    print("\n2. Creating a conversation...")
    headers = {"Authorization": f"Bearer {shared_token}"}
    
    conversation_data = {
        "title": "Test Conversation",
        "language": "en"
    }
    
    conversation_response = client.post(
        "/api/chat/conversations",
        json=conversation_data,
        headers=headers
    )
    
    print(f"Conversation creation status: {conversation_response.status_code}")
    if conversation_response.status_code == 200:
        print(f"Conversation creation response: {conversation_response.json()}")
    else:
        print(f"Conversation creation failed: {conversation_response.text}")
    
    if conversation_response.status_code != 200:
        print(f"Conversation creation failed: {conversation_response.status_code}, {conversation_response.text}")
        return False
    
    conversation = conversation_response.json()
    conversation_id = conversation.get("id")
    
    if not conversation_id:
        print("No conversation ID received after creation")
        return False
    
    print(f"[SUCCESS] Conversation created successfully with ID: {conversation_id}")
    
    # Step 3: Send a message to the conversation
    print("\n3. Sending a message to the conversation...")
    
    message_data = {
        "conversation_id": conversation_id,
        "content": "Hello, can you help me manage my tasks?",
        "language": "en"
    }
    
    message_response = client.post(
        f"/api/chat/conversations/{conversation_id}/messages",
        json=message_data,
        headers=headers
    )
    
    print(f"Message send status: {message_response.status_code}")
    if message_response.status_code == 200:
        print(f"Message response preview: {message_response.json().get('content', '')[:100]}...")
    else:
        print(f"Message send failed: {message_response.text}")
    
    if message_response.status_code != 200:
        print(f"Sending message failed: {message_response.status_code}, {message_response.text}")
        return False
    
    message = message_response.json()
    print(f"[SUCCESS] Message sent successfully, AI response: {message.get('content', '')[:100]}...")
    
    # Step 4: Get all messages in the conversation
    print("\n4. Retrieving all messages in the conversation...")
    
    messages_response = client.get(
        f"/api/chat/conversations/{conversation_id}/messages",
        headers=headers
    )
    
    print(f"Messages retrieval status: {messages_response.status_code}")
    if messages_response.status_code == 200:
        messages = messages_response.json()
        print(f"Retrieved {len(messages)} messages")
    else:
        print(f"Messages retrieval failed: {messages_response.text}")
    
    if messages_response.status_code != 200:
        print(f"Retrieving messages failed: {messages_response.status_code}, {messages_response.text}")
        return False
    
    messages = messages_response.json()
    print(f"[SUCCESS] Retrieved {len(messages)} messages from the conversation")
    
    # Step 5: Get the conversation details
    print("\n5. Retrieving conversation details...")
    
    conv_details_response = client.get(
        f"/api/chat/conversations/{conversation_id}",
        headers=headers
    )
    
    print(f"Conversation details status: {conv_details_response.status_code}")
    if conv_details_response.status_code == 200:
        conv_details = conv_details_response.json()
        print(f"Conversation title: {conv_details.get('title')}")
    else:
        print(f"Conversation details retrieval failed: {conv_details_response.text}")
    
    if conv_details_response.status_code != 200:
        print(f"Retrieving conversation details failed: {conv_details_response.status_code}, {conv_details_response.text}")
        return False
    
    conv_details = conv_details_response.json()
    print(f"[SUCCESS] Conversation details retrieved: {conv_details.get('title')}")
    
    # Step 6: List all conversations for the user
    print("\n6. Listing all conversations for the user...")
    
    all_conv_response = client.get(
        "/api/chat/conversations",
        headers=headers
    )
    
    print(f"All conversations status: {all_conv_response.status_code}")
    if all_conv_response.status_code == 200:
        all_conversations = all_conv_response.json()
        print(f"Found {len(all_conversations)} conversations")
    else:
        print(f"Listing conversations failed: {all_conv_response.text}")
    
    if all_conv_response.status_code != 200:
        print(f"Listing conversations failed: {all_conv_response.status_code}, {all_conv_response.text}")
        return False
    
    all_conversations = all_conv_response.json()
    print(f"[SUCCESS] Found {len(all_conversations)} conversations for the user")
    
    print("\n[SUCCESS] All tests passed! Chatbot integration is working correctly.")
    return True

def run_complete_test():
    """Run the complete test suite"""
    print("Running complete test suite...")
    
    # First test basic auth
    auth_success = test_basic_auth()
    
    if not auth_success:
        print("\n[ERROR] Basic auth test failed.")
        return False
    
    # Check if COHERE_API_KEY is set
    if not os.getenv("COHERE_API_KEY"):
        print("Warning: COHERE_API_KEY is not set in environment. Using mock for testing.")
        
        # Mock the OpenAI client for testing without API key
        with patch.dict(os.environ, {"COHERE_API_KEY": "test-key"}):
            with patch('api.chatbot.client') as mock_client:
                # Mock the chat.completions.create method
                mock_response = MagicMock()
                mock_response.choices = [MagicMock()]
                mock_response.choices[0].message.content = "This is a mocked AI response for testing purposes."
                mock_client.chat.completions.create.return_value = mock_response
                
                success = test_chatbot_integration()
                
                if success:
                    print("\n[SUCCESS] All tests completed successfully with mocked API!")
                    return True
                else:
                    print("\n[ERROR] Some tests failed.")
                    return False
    else:
        success = test_chatbot_integration()
        if success:
            print("\n[SUCCESS] All tests completed successfully!")
            return True
        else:
            print("\n[ERROR] Some tests failed.")
            return False

if __name__ == "__main__":
    success = run_complete_test()
    if not success:
        sys.exit(1)