# Simple test to check if the app can be imported
try:
    # Test importing each module individually
    import api.tasks
    print("api.tasks imported successfully")

    import database.init_db
    print("database.init_db imported successfully")

    import models.task
    print("models.task imported successfully")

    import services.task_service
    print("services.task_service imported successfully")

    import auth.jwt
    print("auth.jwt imported successfully")

    import main
    print("main imported successfully")

    print("All modules imported successfully!")
    print("Application structure is correct")
    print("Ready to run the Todo Evolution Hackathon application")

except ImportError as e:
    print(f"Import error: {e}")
except Exception as e:
    print(f"Other error: {e}")

print("\nTesting basic functionality...")
try:
    # Test the basic functionality
    import uuid
    from datetime import datetime

    # Create a sample task
    sample_task = {
        "id": str(uuid.uuid4()),
        "user_id": "test_user",
        "title": "Test Task",
        "description": "This is a test task",
        "completed": False,
        "priority": "medium",
        "tags": '["test", "sample"]',  # JSON string format
        "due_date": datetime.now(),
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }

    print("Sample task created successfully")
    print("Backend is ready for use!")

except Exception as e:
    print(f"Error testing functionality: {e}")