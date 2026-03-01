# Phase 3 Multi-Language Skill

## Purpose
This skill enables the AI agent to handle multi-language support for the chatbot feature, including language detection, response generation in multiple languages, and language-specific processing.

## Capabilities
- Detect user input language (English, Urdu, Roman Urdu, Roman English)
- Generate responses in the appropriate language
- Handle language-specific formatting and conventions
- Manage language preferences and settings
- Auto-detect language from user message or use explicit selection

## Implementation Details
- Uses language detection algorithms to identify input language
- Maintains language-specific response templates
- Integrates with the LanguageDetectionService for accurate detection
- Supports automatic language switching based on user preferences
- Cohere prompts are language-aware for better response quality

## Language Support
- **en**: English (Latin script, formal)
- **ur**: Urdu (Arabic/Persian script, formal)
- **roman_ur**: Roman Urdu (Latin script, informal Urdu transliteration)
- **roman_en**: Roman English (Latin script, informal English)

## Detection Algorithm
- Urdu script detection: Unicode range \u0600-\u06FF
- Roman Urdu vocabulary matching: Common Urdu words in Roman script
- English: Default for Latin script with high confidence
- Confidence thresholds: ur >0.5, roman_ur >0.3 vocabulary match, en >0.7

## Usage
When processing user input, the agent should:
1. Detect the language of the incoming message (auto or explicit)
2. Generate the response in the same language
3. Apply language-specific formatting rules
4. Update user's language preference if needed
5. Pass language parameter to Cohere API for context-aware responses

## Constraints
- Must support all 4 specified languages (en, ur, roman_ur, roman_en)
- Responses must be culturally appropriate for each language
- Language detection must be accurate (>90% for supported languages)
- Must handle mixed-language inputs gracefully
- System prompts are pre-translated for each language