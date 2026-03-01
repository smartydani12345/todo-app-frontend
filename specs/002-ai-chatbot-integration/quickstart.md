# Quickstart Guide: Advanced AI Chatbot with Complete User Query Resolution

## Overview
This guide provides instructions for setting up and running the Advanced AI Chatbot with Complete User Query Resolution feature. The chatbot integrates with the existing Phase 2 todo application while maintaining strict separation between the phases.

## Prerequisites
- Python 3.11+
- Node.js 18+ and npm/yarn
- Next.js 16.1.6
- FastAPI
- Access to Cohere API (command-r model)
- Neon Serverless PostgreSQL database
- Git

## Environment Setup

### 1. Clone the Repository
```bash
git clone <repository-url>
cd <repository-directory>
```

### 2. Backend Setup
```bash
# Navigate to backend directory
cd backend

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
```

### 3. Frontend Setup
```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install
# or
yarn install
```

## Configuration

### 1. Backend Configuration
Update the `.env` file in the backend directory with the following variables:

```env
# Database
DATABASE_URL="your_neon_postgres_connection_string"

# Cohere API
COHERE_API_KEY="your_cohere_api_key_here"

# JWT Secret (reuse from Phase 2)
JWT_SECRET_KEY="your_jwt_secret_from_phase2"

# Application
ENVIRONMENT="development"  # or "production"
DEBUG="True"  # Set to "False" in production
```

### 2. Database Migrations
Run the following command to create the new tables for the chatbot:

```bash
# From the backend directory
python -m alembic upgrade head
```

If alembic is not set up, you may need to initialize it first:

```bash
python -m alembic init alembic
# Then create a migration for the new tables
python -m alembic revision --autogenerate -m "Add Conversation and Message tables"
python -m alembic upgrade head
```

## Running the Application

### 1. Start the Backend
```bash
# From the backend directory
uvicorn main:app --reload --port 8000
```

The backend will be available at `http://localhost:8000`.

### 2. Start the Frontend
```bash
# From the frontend directory
npm run dev
# or
yarn dev
```

The frontend will be available at `http://localhost:3000`.

## API Endpoints

### Chat Endpoint
- **POST** `/api/chat`
- Headers: `Authorization: Bearer <jwt_token>`
- Request Body:
```json
{
  "message": "Your message here",
  "language": "en", // Optional: en, ur, roman_ur, roman_en
  "conversation_id": 123 // Optional: ID of existing conversation (creates new if not provided)
}
```
- Response:
```json
{
  "response": "AI response here",
  "conversation_id": 123,
  "message_id": 456,
  "timestamp": "2026-02-13T10:00:00Z",
  "language": "en",
  "tools_used": ["create_task_tool", "search_knowledge_base_tool"],
  "response_time": 1.25
}
```

## Frontend Integration

### 1. Chat Panel Component
The chatbot UI is integrated as a side panel on the existing dashboard. To use it:

1. Navigate to the dashboard page
2. Click the chatbot icon to open the chat panel
3. Type your message or use voice input
4. Select your preferred language if needed

### 2. Voice Commands
- Click the microphone icon to activate voice input
- Speak in any of the supported languages (English, Urdu, Roman Urdu, Roman English)
- The system will automatically detect the language or use your preference

### 3. Language Selection
- Use the language selector dropdown to switch between supported languages
- Your preference will be saved for future sessions

### 4. Proactive Assistance
- The system will detect confusion and offer help automatically
- Look for yellow notification banners offering assistance
- Use the "About Dev" button to learn about the developer

### 5. Conversation History
- View your conversation history in the chat panel
- Use the "Clear Chat" button to reset the conversation
- The system maintains context across messages

## Testing the Feature

### 1. Natural Language Task Management
Try commands like:
- "Add a task to buy groceries"
- "Mark the meeting task as complete"
- "Edit the workout task to say workout at 7pm"

### 2. Multi-Language Support
Switch between languages:
- English: "Add a task to buy groceries"
- Urdu: "کھانے کے لئے خریداری کا کام شامل کریں"
- Roman Urdu: "Khane ke liye groceries add karen"
- Roman English: "Add task to buy groceries"

### 3. Feature Explanations
Ask questions like:
- "How do I create a new task?"
- "Show me how to edit a task"
- "What features are available?"

### 4. Author Information
Ask questions like:
- "Who created this app?"
- "Tell me about the developer"
- "What is the project about?"

### 5. Context-Aware Conversations
Engage in multi-turn conversations:
- "I want to create a task to buy groceries"
- "Also add a task to pick up dry cleaning"
- Notice how the system understands the context

## Troubleshooting

### Common Issues

#### 1. API Key Not Set
**Problem**: Getting 401 or 500 errors from the chat endpoint
**Solution**: Verify that COHERE_API_KEY is set correctly in your .env file

#### 2. Database Connection Issues
**Problem**: Cannot connect to the database
**Solution**: Check that DATABASE_URL is set correctly in your .env file

#### 3. JWT Authentication Failing
**Problem**: Getting 401 errors when calling the chat endpoint
**Solution**: Ensure you're sending the correct JWT token in the Authorization header

#### 4. Voice Recognition Not Working
**Problem**: Voice input not being processed
**Solution**: Check that your browser supports Web Speech API and that microphone permissions are granted

#### 5. Multi-Language Not Working
**Problem**: System not responding in the selected language
**Solution**: Verify that the language parameter is being sent correctly in the API request

#### 6. Response Time Too Slow
**Problem**: Responses taking longer than 3 seconds
**Solution**: Check your Cohere API key permissions and internet connection speed

### Debugging Tips

1. Check backend logs for error messages
2. Verify that all environment variables are set correctly
3. Ensure the database migrations have been applied
4. Confirm that the Cohere API key has the necessary permissions
5. Check that response times are under 3 seconds for optimal performance

## Development

### Adding New Features
1. Update the specification in `/specs/002-ai-chatbot-integration/spec.md`
2. Run `/sp.plan` to update the implementation plan
3. Run `/sp.tasks` to generate development tasks
4. Implement the tasks following the generated guidelines

### Running Tests
```bash
# Backend tests
cd backend
python -m pytest

# Frontend tests
cd frontend
npm test
# or
yarn test
```

## Deployment

### Production Build
```bash
# Frontend
cd frontend
npm run build

# Backend
cd backend
# Ensure environment variables are set for production
```

### Environment Variables for Production
```env
# Database
DATABASE_URL="your_production_database_url"

# Cohere API
COHERE_API_KEY="your_production_cohere_api_key"

# JWT Secret
JWT_SECRET_KEY="your_production_jwt_secret"

# Application
ENVIRONMENT="production"
DEBUG="False"