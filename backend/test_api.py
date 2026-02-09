import requests
import json

# Test the backend API endpoints
BASE_URL = "http://localhost:8000/api"

def test_endpoints():
    print("Testing FastAPI backend endpoints...")
    
    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL.replace('/api', '')}/health")
        print(f"Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")
    
    # Test login to get token
    try:
        login_data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        print(f"Login: {response.status_code}")
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            print("Successfully got access token")
            
            # Test getting tasks
            headers = {"Authorization": f"Bearer {access_token}"}
            response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
            print(f"Get tasks: {response.status_code}")
            
            # Test creating a task
            task_data = {
                "title": "Test Task from Script",
                "description": "This is a test task created via script",
                "priority": "medium",
                "tags": "test,script"
            }
            response = requests.post(f"{BASE_URL}/tasks/", data=task_data, headers=headers)
            print(f"Create task: {response.status_code}")
            if response.status_code != 200:
                print(f"Error response: {response.text}")
                
        else:
            print(f"Login failed: {response.text}")
    except Exception as e:
        print(f"Test failed: {e}")

if __name__ == "__main__":
    test_endpoints()