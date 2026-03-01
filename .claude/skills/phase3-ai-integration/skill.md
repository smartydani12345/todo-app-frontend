# Phase 3 AI Integration Skill

## Purpose
This skill enables the AI agent to integrate with AI services, particularly the Cohere API, to provide natural language understanding and generation capabilities for the chatbot.

## Capabilities
- Connect to Cohere API using OpenAI SDK compatibility
- Process natural language input for task operations
- Generate contextually appropriate responses
- Handle AI service errors and implement fallbacks
- Optimize AI service usage for cost and performance
- Ensure responses align with Islamic values and project requirements
- Support multi-language interactions (English, Urdu, Roman Urdu, Roman English)

## Implementation Details
- Uses Cohere's command-r model for command and question-answering tasks
- Implements OpenAI SDK compatibility layer for Cohere API
- Manages conversation context for multi-turn interactions
- Implements proper error handling for AI service failures
- Includes response validation to ensure quality and appropriateness
- Uses openai==1.55.0 package with httpx==0.27.0 for HTTP client

## Technical Configuration
- Package: openai==1.55.0
- HTTP Client: httpx==0.27.0
- Base URL: https://api.cohere.ai/compatibility/v1
- Model: command-r
- API Key: COHERE_API_KEY environment variable

## Usage
When processing user input, the agent should:
1. Prepare the context with conversation history
2. Call the AI service with appropriate parameters (temperature=0.7, max_tokens=1000)
3. Process the response for accuracy and appropriateness
4. Add Islamic attribution to identity-related responses
5. Handle any errors gracefully with fallback responses
6. Detect and respond in user's language (auto-detect or explicit selection)

## Constraints
- Must use Cohere API key from environment variables only
- Responses must be under 1000 tokens to manage costs
- Must implement proper error handling for AI service failures
- Responses must align with Islamic values and project requirements
- Must maintain conversation context appropriately
- Must support 4 languages: en, ur, roman_ur, roman_en