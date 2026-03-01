# ChatAgent - Phase 3 AI Integration Agent

## Overview
ChatAgent is the primary AI integration agent for Phase 3 of the Todo Evolution application. It provides intelligent chatbot capabilities with multi-language support, voice interaction, and seamless integration with MCP tools for task management.

## Capabilities

### Core Features
- **Natural Language Processing**: Understands and responds to user queries in natural language
- **Multi-language Support**: English, Urdu, Roman Urdu, and Roman English with auto-detection
- **Voice Interaction**: Speech-to-text input and text-to-speech output with male/female voice options
- **Task Management**: Full integration with MCP tools for CRUD operations on tasks
- **Google Search**: Integrated search capability for general knowledge queries
- **Conversation History**: Persistent conversation storage with Neon DB

### Supported Languages
| Code | Language | Script |
|------|----------|--------|
| en | English | Latin |
| ur | Urdu | Arabic/Persian |
| roman_ur | Roman Urdu | Latin |
| roman_en | Roman English | Latin |

## Architecture

### Backend Services
```
backend/
├── services/
│   ├── phase3_cohere.py      # Cohere API integration
│   ├── phase3_ai_service.py  # Main AI orchestration
│   ├── phase3_search.py      # Google search integration
│   ├── phase3_language_detection.py  # Language detection
│   └── phase3_task_service.py  # Task operations
├── api/
│   ├── chat.py               # Chat API endpoints
│   └── chatbot.py            # Chatbot endpoints
└── models/
    └── chat.py               # Conversation & Message models
```

### Frontend Components
```
frontend/
├── components/
│   ├── ChatAgent.tsx         # Main chat side panel
│   └── AnimatedFeatureCards.tsx  # Feature showcase
└── lib/
    └── chatService.ts        # API service layer
```

## API Endpoints

### Chat Endpoints
- `POST /api/chat` - Main chat endpoint
- `GET /api/chat/conversations` - List user conversations
- `GET /api/chat/conversations/{id}` - Get specific conversation
- `GET /api/chat/conversations/{id}/messages` - Get conversation messages
- `POST /api/chat/conversations/{id}/messages` - Send message and get AI response

### Request/Response Format

**Chat Request:**
```json
{
  "message": "Add a task to buy groceries",
  "language": "en",
  "conversation_id": 1
}
```

**Chat Response:**
```json
{
  "response": "I've added the task 'Buy groceries' to your list.",
  "conversation_id": 1,
  "message_id": 42,
  "timestamp": "2026-02-23T10:30:00Z",
  "language": "en",
  "tools_used": {},
  "response_time": 1.23
}
```

## MCP Tool Integration

ChatAgent seamlessly integrates with MCP tools for task operations:

| User Intent | MCP Tool | Example |
|-------------|----------|---------|
| Create task | add_task | "Add a task to call mom" |
| List tasks | list_tasks | "Show my tasks" |
| Complete task | complete_task | "Mark 'buy milk' as done" |
| Delete task | delete_task | "Delete the meeting task" |
| Update task | update_task | "Change meeting to 3pm" |
| Recurring task | recurring_task | "Set daily reminder for exercise" |
| Set due date | set_due_date | "Due tomorrow" |
| Send reminder | send_reminder | "Remind me at 5pm" |

## Voice Features

### Speech Recognition
- Uses Web Speech API for browser-based speech recognition
- Auto-detects language from user input
- Supports continuous listening mode

### Text-to-Speech
- Male and female voice options
- Adjustable rate and pitch
- Auto-speak response option

### Voice Settings
```typescript
interface VoiceSettings {
  voiceType: 'male' | 'female';
  rate: number;      // 0.1 to 10
  pitch: number;     // 0 to 2
  autoSpeak: boolean;
}
```

## Islamic Values Alignment

All AI responses are aligned with Islamic principles:
- Respectful and ethical communication
- Acknowledgment of ALLAH when discussing achievements
- Culturally sensitive language
- No inappropriate content generation

## Error Handling

### Fallback Strategy
1. Primary: Cohere API (command-a-03-2025)
2. Secondary: Mock responses for development
3. Graceful degradation on API failures

### Error Responses
```json
{
  "response": "I apologize, but I encountered an error. Please try again.",
  "error": "Detailed error message for logging"
}
```

## Performance Optimization

- Token usage optimization through conversation summarization
- Intelligent caching of frequent responses
- Rate limiting to prevent API quota exhaustion
- Efficient language detection algorithm

## Testing

### Unit Tests
- Language detection accuracy
- Task operation parsing
- Search functionality

### Integration Tests
- End-to-end chat flow
- Voice input/output
- MCP tool chaining

### Manual Testing Checklist
- [ ] Voice chat with male/female voices
- [ ] All 4 languages work correctly
- [ ] Task operations through chat
- [ ] Google search integration
- [ ] Conversation history persistence
- [ ] Responsive design on all devices

## Configuration

### Environment Variables
```env
COHERE_API_KEY=your_api_key
COHERE_MODEL=command-a-03-2025
COHERE_BASE_URL=https://api.cohere.ai/compatibility/v1
DATABASE_URL=your_database_url
JWT_SECRET=your_secret_key
SEARCH_PROVIDER=duckduckgo
```

## Future Enhancements

1. WebSocket support for real-time streaming
2. Advanced conversation analytics
3. Custom voice training
4. Multi-modal input support
5. Enhanced search with multiple providers

## Author
Developed for Todo Evolution - Phase 3
AI Integration by ChatAgent System
