import traceback
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

try:
    response = client.post('/api/auth/register', json={
        'name': 'Test Script User',
        'email': 'testscript@example.com',
        'password': 'Test123!'
    })

    print(f'Status: {response.status_code}')
    print(f'Response: {response.json()}')
except Exception as e:
    print(f'Error: {e}')
    traceback.print_exc()
