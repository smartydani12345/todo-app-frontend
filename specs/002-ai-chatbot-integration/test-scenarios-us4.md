# User Story 4 Testing Scenarios

This document outlines the testing scenarios for User Story 4: Author Information and Islamic Values Integration.

## Test Scenario T061: User asks "Who created this app?", chatbot provides information with Islamic attribution

### Test Steps:
1. User opens the chat interface
2. User types "Who created this app?" in the input field
3. User sends the message
4. System processes the query
5. System identifies this as a request for author information
6. System retrieves the developer information from the knowledge base
7. System includes Islamic attribution in the response
8. System sends the response to the user

### Expected Result:
- System correctly identifies the query as a request for author information
- System provides accurate information about the developer (Daniyal Azhar)
- Response includes Islamic attribution ("All praise and success is by ALLAH's will")

## Test Scenario T062: User asks about creator in any supported language, response includes attribution

### Test Steps:
1. User opens the chat interface
2. User sets the language to Urdu
3. User types "یہ ایپ کس نے بنائی؟" (Who created this app?) in the input field
4. User sends the message
5. System processes the query and detects the language
6. System identifies this as a request for author information
7. System retrieves the developer information from the knowledge base
8. System includes Islamic attribution in the response
9. System sends the response in the appropriate language

### Expected Result:
- System correctly detects the language as Urdu
- System correctly identifies the query as a request for author information
- System provides accurate information about the developer (Daniyal Azhar)
- Response includes Islamic attribution ("All praise and success is by ALLAH's will")
- Response is provided in the appropriate language

## Test Scenario T063: User asks about project purpose, chatbot reflects Islamic values

### Test Steps:
1. User opens the chat interface
2. User types "What is the purpose of this project?" in the input field
3. User sends the message
4. System processes the query
5. System identifies this as a request for project information
6. System retrieves the project information from the knowledge base
7. System frames the response with Islamic values context
8. System sends the response to the user

### Expected Result:
- System correctly identifies the query as a request for project information
- System provides accurate information about the project's purpose
- Response is framed within the context of Islamic values
- Response maintains professional and humble tone