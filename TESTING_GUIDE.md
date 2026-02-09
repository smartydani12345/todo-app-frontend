# Testing Guide for Todo Application

## Prerequisites

Before testing the application, ensure you have:

- Node.js (v16 or higher)
- Python (v3.8 or higher)
- pip (Python package manager)

## Setup Instructions

### 1. Backend Setup

```bash
cd backend
pip install -r requirements.txt
```

Start the backend server:

```bash
uvicorn main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`

### 2. Frontend Setup

```bash
cd frontend
npm install
```

Start the frontend development server:

```bash
npm run dev
```

The frontend will be available at `http://localhost:3000`

## Complete Flow Testing

### 1. Registration Flow

1. Navigate to `http://localhost:3000/register`
2. Fill in the registration form:
   - Full Name: Enter your name
   - Email: Enter a valid email address
   - Password: Enter a strong password
   - Confirm Password: Re-enter the same password
3. Click "Register"
4. Verify that you are automatically redirected to the dashboard
5. Check that a success toast notification appears

### 2. Login Flow

1. Navigate to `http://localhost:3000/login`
2. Enter the email and password you used during registration
3. Click "Sign in"
4. Verify that you are redirected to the dashboard
5. Check that a success toast notification appears

### 3. Todo CRUD Operations

#### Add Task
1. On the dashboard, fill in the "Add New Task" form
2. Enter a title (required)
3. Optionally add description, priority, and tags
4. Click "Add Task"
5. Verify that the task appears in the task list
6. Check that a success toast notification appears

#### Edit Task
1. Find a task in the list and click the "Edit" button
2. Modify the task details in the form
3. Click "Update Task"
4. Verify that the task updates in the list
5. Check that a success toast notification appears

#### Mark Complete/Incomplete
1. Click the checkbox next to any task
2. Verify that the task appearance changes (strikethrough for completed)
3. Check that a success toast notification appears

#### Delete Task
1. Click the "Delete" button for any task
2. Confirm the deletion in the confirmation dialog
3. Verify that the task is removed from the list
4. Check that a success toast notification appears

### 4. Advanced Features

#### Filtering
1. Use the filter dropdowns to filter tasks by:
   - Status (All, Completed, Incomplete)
   - Priority (All, High, Medium, Low)
   - Tag (enter a tag to filter by)

#### Sorting
1. Use the sort controls to sort tasks by:
   - Created Date
   - Due Date
   - Priority
   - Title
2. Toggle between Ascending and Descending order

#### Search
1. Use the search input to search tasks by title or description
2. Verify that the task list updates dynamically

### 5. Error Handling

#### Invalid Credentials
1. Try logging in with incorrect email/password
2. Verify that an error message appears

#### Network Errors
1. Temporarily disconnect from the internet
2. Try performing any action (add/update/delete task)
3. Verify that an appropriate error message appears

#### Form Validation
1. Try submitting forms with invalid data
2. Verify that appropriate error messages appear

### 6. Logout

1. Click the "Logout" button in the top right corner
2. Verify that you are redirected to the login page
3. Check that the authentication token is cleared

## Expected Behavior

- All API calls should be properly authenticated with JWT tokens
- Token should persist across page refreshes
- All CRUD operations should work seamlessly
- All filters, sorting, and search should work in real-time
- All error scenarios should be handled gracefully with user-friendly messages
- The UI should be responsive on all device sizes
- All toast notifications should appear and disappear appropriately

## Troubleshooting

If you encounter issues:

1. Check that both backend and frontend servers are running
2. Verify that the backend is accessible at `http://localhost:8000`
3. Check browser console for any error messages
4. Verify that the database is properly initialized
5. Ensure that CORS settings allow communication between frontend and backend