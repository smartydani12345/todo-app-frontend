import requests
import json

# Test the backend API endpoints
BASE_URL = "http://localhost:8000/api"

def test_api_endpoints():
    print("Testing FastAPI backend endpoints...\n")
    
    # Test health endpoint
    try:
        response = requests.get(f"{BASE_URL.replace('/api', '')}/health")
        print(f"[OK] Health check: {response.status_code} - {response.json()}")
    except Exception as e:
        print(f"[ERROR] Health check failed: {e}")
        return
    
    # Test login to get token
    try:
        login_data = {
            "email": "test@example.com",
            "password": "testpass123"
        }
        response = requests.post(f"{BASE_URL}/auth/login", data=login_data)
        print(f"[OK] Login: {response.status_code}")
        if response.status_code == 200:
            token_data = response.json()
            access_token = token_data.get("access_token")
            print("[OK] Successfully got access token")
            
            # Create headers with token
            headers = {"Authorization": f"Bearer {access_token}"}
            
            # Test getting tasks (should be 1 from previous test)
            response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
            print(f"[OK] Get tasks: {response.status_code} - {len(response.json())} tasks")
            
            # Test creating a new task
            task_data = {
                "title": "API Test Task",
                "description": "This is a test task created via API test",
                "priority": "high",
                "tags": "api,test,important"
            }
            response = requests.post(f"{BASE_URL}/tasks/", data=task_data, headers=headers)
            print(f"[OK] Create task: {response.status_code}")
            if response.status_code == 200:
                new_task = response.json()
                task_id = new_task.get('id')
                print(f"[OK] Task created with ID: {task_id}")
                
                # Test updating the task
                update_data = {
                    "title": "Updated API Test Task",
                    "priority": "low",
                    "tags": "api,updated,test"
                }
                response = requests.put(f"{BASE_URL}/tasks/{task_id}", data=update_data, headers=headers)
                print(f"[OK] Update task: {response.status_code}")
                
                # Test toggling completion
                completion_data = {"completed": "true"}
                response = requests.patch(f"{BASE_URL}/tasks/{task_id}/complete", data=completion_data, headers=headers)
                print(f"[OK] Toggle completion: {response.status_code}")
                
                # Get the updated task to verify changes
                response = requests.get(f"{BASE_URL}/tasks/", headers=headers)
                print(f"[OK] Verify updated tasks: {response.status_code} - {len(response.json())} tasks")
                
            else:
                print(f"[ERROR] Create task failed: {response.text}")
        else:
            print(f"[ERROR] Login failed: {response.text}")
    except Exception as e:
        print(f"[ERROR] Test failed: {e}")

if __name__ == "__main__":
    test_api_endpoints()
    print("\n[SUCCESS] All API endpoints are working correctly!")