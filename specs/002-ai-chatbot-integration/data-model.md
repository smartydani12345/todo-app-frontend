# Data Model: Advanced AI Chatbot with Complete User Query Resolution

## Overview
This document defines the data model for the Advanced AI Chatbot with Complete User Query Resolution feature. It extends the existing Phase 2 data model while maintaining strict separation between the phases.

## Entity Definitions

### 1. Conversation
Represents a single conversation thread between user and chatbot.

**Fields:**
- `id`: Integer (Primary Key, Auto-increment)
- `user_id`: String (Foreign Key to User.id, indexed)
- `created_at`: DateTime (Timestamp when conversation started)
- `updated_at`: DateTime (Timestamp when conversation was last updated)
- `title`: String (Generated from first message or user-edited title, nullable)
- `status`: String (active, archived, deleted - default: active)

**Relationships:**
- One-to-Many: Conversation → Messages (conversation.messages)
- Many-to-One: Conversation ← User (conversation.user)

**Validation Rules:**
- `user_id` must reference an existing user
- `created_at` must be in the past
- `updated_at` must be >= `created_at`
- `status` must be one of ['active', 'archived', 'deleted']

### 2. Message
Represents individual messages within a conversation.

**Fields:**
- `id`: Integer (Primary Key, Auto-increment)
- `conversation_id`: Integer (Foreign Key to Conversation.id, indexed)
- `role`: String (sender type: 'user' or 'assistant')
- `content`: String (The actual message content)
- `language`: String (Language code: 'en', 'ur', 'roman_ur', 'roman_en')
- `timestamp`: DateTime (When the message was sent/received)
- `tools_used`: JSON (Array of tools used by AI to generate response, nullable)
- `parent_message_id`: Integer (For threaded conversations, nullable, self-referencing)

**Relationships:**
- Many-to-One: Message ← Conversation (message.conversation)
- Self-referencing: Message → Message (for threading, nullable)

**Validation Rules:**
- `conversation_id` must reference an existing conversation
- `role` must be one of ['user', 'assistant']
- `language` must be one of ['en', 'ur', 'roman_ur', 'roman_en']
- `timestamp` must be in the past
- `content` length must be > 0 and < 10000 characters
- `parent_message_id` must reference a message in the same conversation

### 3. User (Existing from Phase 2 - Extended)
Represents authenticated users with additional preferences for chatbot functionality.

**Additional Fields (for chatbot functionality):**
- `preferred_language`: String (Default language: 'en', 'ur', 'roman_ur', 'roman_en')
- `voice_preference`: String (Voice type: 'male', 'female', 'none' - default: 'none')
- `chatbot_enabled`: Boolean (Whether user has enabled chatbot features - default: true)

**Extended Validation Rules:**
- `preferred_language` must be one of ['en', 'ur', 'roman_ur', 'roman_en']
- `voice_preference` must be one of ['male', 'female', 'none']

## State Transitions

### Conversation State Transitions
- `active` → `archived`: When user archives conversation
- `active` → `deleted`: When user deletes conversation
- `archived` → `active`: When user unarchives conversation
- `deleted` → `active`: When user restores conversation (within retention period)

### Message State Transitions
- Messages are immutable after creation (no state transitions)
- Deleted messages are soft-deleted with a deletion flag

## Indexes

### Required Indexes
1. `conversations.user_id_idx` ON conversations(user_id)
2. `messages.conversation_id_idx` ON messages(conversation_id)
3. `messages.timestamp_idx` ON messages(timestamp)
4. `conversations.updated_at_idx` ON conversations(updated_at)

### Composite Indexes
1. `conversations.user_status_idx` ON conversations(user_id, status)

## Relationships Diagram

```
User (1) ←→ (Many) Conversation (1) ←→ (Many) Message
```

## Constraints

### Referential Integrity
- Foreign key constraints ensure data consistency between related tables
- Cascade delete for conversations removes associated messages
- Orphaned messages are prevented

### Data Integrity
- All timestamps are stored in UTC
- Content is validated for appropriate length and format
- Language codes follow ISO standards where applicable

## API Considerations

### Query Patterns
1. Retrieve all conversations for a user (with pagination)
2. Retrieve messages for a specific conversation (with pagination)
3. Search messages by content within a user's conversations
4. Update conversation metadata (title, status)

### Performance Considerations
- Pagination implemented for conversation and message lists
- Indexes optimized for common query patterns
- Large conversation histories handled with summarization