import requests
import json

# Test the backend API directly
BASE_URL = "http://localhost:8000/api"

# First, let's try to register a test user
print("Testing registration...")
try:
    reg_response = requests.post(f"{BASE_URL}/auth/register", data={
        'name': 'Test User',
        'email': 'test@example.com',
        'password': 'password123'
    })
    print(f"Registration: {reg_response.status_code}, Response: {reg_response.text}")
    
    if reg_response.status_code == 200:
        token_data = reg_response.json()
        token = token_data.get('access_token')
        
        if token:
            print("\nTesting task creation...")
            headers = {'Authorization': f'Bearer {token}'}
            
            # Try to create a task
            task_response = requests.post(f"{BASE_URL}/tasks/", data={
                'title': 'Test Task',
                'description': 'Test Description',
                'priority': 'medium',
                'tags': 'test,important'
            }, headers=headers)
            
            print(f"Task Creation: {task_response.status_code}, Response: {task_response.text}")
        else:
            print("No token received from registration")
    else:
        print(f"Registration failed with status: {reg_response.status_code}")
        
except Exception as e:
    print(f"Error during testing: {str(e)}")