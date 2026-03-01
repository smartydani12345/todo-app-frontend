# User Story 5 Testing Scenarios

This document outlines the testing scenarios for User Story 5: Context-Aware Conversations and Proactive Assistance.

## Test Scenario T074: User discusses task management, follow-up question understood in context

### Test Steps:
1. User opens the chat interface
2. User types "I want to create a task to buy groceries" in the input field
3. User sends the message
4. System processes the request and creates the task
5. User types "Also add a task to pick up dry cleaning" in the input field
6. User sends the message
7. System processes the request in the context of task creation
8. System responds appropriately to the follow-up request

### Expected Result:
- System correctly understands the follow-up request in the context of task management
- System creates the second task without needing to repeat the full instruction
- Both tasks are created successfully

## Test Scenario T075: User seems confused, chatbot proactively offers assistance

### Test Steps:
1. User opens the chat interface
2. User types "I don't understand how to set priorities" in the input field
3. User sends the message
4. System processes the query and detects confusion indicators
5. System identifies this as a request for feature explanation about priorities
6. System retrieves appropriate information from the knowledge base
7. System includes proactive assistance in the response
8. System sends the response to the user

### Expected Result:
- System correctly identifies confusion indicators in the user's query
- System provides a clear explanation of how to set priorities
- System includes additional proactive assistance in the response
- Response invites the user to ask for more help if needed

## Test Scenario T076: User returns after inactivity, chatbot recalls previous context

### Test Steps:
1. User opens the chat interface
2. User has a conversation about creating tasks
3. User leaves the application idle for 10 minutes
4. User returns to the application
5. User sends a follow-up question related to the previous conversation
6. System retrieves the conversation history
7. System processes the request in the context of the previous conversation
8. System responds appropriately considering the context

### Expected Result:
- System correctly retrieves the conversation history
- System understands the follow-up question in the context of the previous conversation
- System provides a relevant response that takes the context into account