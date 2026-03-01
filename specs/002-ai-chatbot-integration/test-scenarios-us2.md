# User Story 2 Testing Scenarios

This document outlines the testing scenarios for User Story 2: Multi-Language Support and Voice Commands.

## Test Scenario T041: User speaks in Urdu, system processes and responds in Urdu

### Test Steps:
1. User opens the chat interface
2. User selects Urdu language from the language selector
3. User clicks the voice input button and speaks in Urdu
4. System processes the speech and converts it to text
5. System detects the language as Urdu
6. System processes the request using the appropriate language models
7. System responds in Urdu

### Expected Result:
- Speech is accurately converted to Urdu text
- System correctly identifies the language as Urdu
- Response is generated in Urdu
- User receives response in Urdu

## Test Scenario T042: User types in Roman Urdu, system understands and responds appropriately

### Test Steps:
1. User opens the chat interface
2. User types a message in Roman Urdu (e.g., "kal main market jana chahta hun")
3. System detects the language as Roman Urdu
4. System processes the request
5. System responds appropriately

### Expected Result:
- System correctly identifies the input as Roman Urdu
- System processes the request correctly
- System responds appropriately in the same language or as requested

## Test Scenario T043: User toggles from English to Urdu, subsequent interactions happen in Urdu

### Test Steps:
1. User starts a conversation in English
2. User uses the language selector to switch to Urdu
3. User sends a message in Urdu
4. System responds in Urdu
5. User continues conversation in Urdu

### Expected Result:
- Language preference is saved
- Subsequent interactions happen in Urdu
- System maintains language consistency