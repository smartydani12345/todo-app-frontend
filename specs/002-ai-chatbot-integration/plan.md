# Implementation Plan: Advanced AI Chatbot with Complete User Query Resolution

**Branch**: `002-ai-chatbot-integration` | **Date**: 2026-02-13 | **Spec**: [link to spec.md]
**Input**: Feature specification from `/specs/002-ai-chatbot-integration/spec.md`

**Note**: This template is filled in by the `/sp.plan` command. See `.specify/templates/commands/plan.md` for the execution workflow.

## Summary

This plan outlines the implementation of an Advanced AI Chatbot with Complete User Query Resolution for the existing todo application. The chatbot will provide natural language task management, multi-language support (English, Urdu, Roman Urdu, Roman English), voice commands, feature explanations, troubleshooting assistance, and author information with Islamic values integration. The implementation will maintain strict separation from Phase 2 functionality while reusing existing authentication and database infrastructure.

## Technical Context

**Language/Version**: Python 3.11 (Backend), TypeScript/JavaScript (Frontend Next.js 16.1.6)
**Primary Dependencies**: FastAPI (Backend), Next.js 16.1.6 (Frontend), Cohere API (AI), SQLModel (ORM), Web Speech API (Voice)
**Storage**: Neon Serverless PostgreSQL (existing Phase 2 DB extended with Conversation/Message tables)
**Testing**: pytest (Backend), Jest/React Testing Library (Frontend)
**Target Platform**: Web application (Browser-based with mobile responsiveness)
**Project Type**: Web (frontend + backend with shared database)
**Performance Goals**: <3 second response time for 90% of interactions, 100 concurrent chatbot sessions
**Constraints**: <200ms p95 for API responses, JWT authentication reuse from Phase 2, no modifications to existing Phase 2 functionality
**Scale/Scope**: 100 concurrent users, 4 supported languages, 90% voice recognition accuracy in quiet environments

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

- ✅ SPEC-DRIVEN DEVELOPMENT: All code will be generated via /sp.implement after constitution → specify → clarify → plan → tasks
- ✅ PHASE SEPARATION: Phase 2 files will remain untouched; Phase 3 features will be in phase3-prefixed locations
- ✅ TECHNOLOGY STACK: Will use Next.js 16.1.6, FastAPI, Neon PostgreSQL, SQLModel, Cohere API, Web Speech API
- ✅ CHATBOT CAPABILITIES: Will implement task management, feature guidance, troubleshooting, author knowledge, Islamic values
- ✅ INTEGRATION REQUIREMENTS: Will create chatbot overlay, new /api/chat endpoint, extend DB with Conversation/Message tables
- ✅ REUSABLE INTELLIGENCE: Will create exactly 9 agents + 9 skills in .claude/agents/phase3-* and .claude/skills/phase3-* folders
- ✅ STANDARDS: Will maintain stateless server design, clean modular code, 100% agent-generated code
- ✅ SUCCESS CRITERIA: Will handle all user queries, support 4 languages, maintain Phase 2 functionality, embed Islamic values

## Project Structure

### Documentation (this feature)

```text
specs/002-ai-chatbot-integration/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (/sp.plan command)
├── data-model.md        # Phase 1 output (/sp.plan command)
├── quickstart.md        # Phase 1 output (/sp.plan command)
├── contracts/           # Phase 1 output (/sp.plan command)
│   └── chat-api.yaml    # OpenAPI specification for chat endpoint
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Web application (frontend + backend)
backend/
├── api/
│   └── chat.py          # New chat endpoint (Phase 3)
├── services/
│   ├── phase3-agents.py    # Cohere SDK integration (Phase 3)
│   ├── phase3-language.py  # Language detection service (Phase 3)
│   ├── phase3-guidance.py  # Guidance system service (Phase 3)
│   └── phase3-voice.py     # Voice service (Phase 3)
├── models.py            # Extended with Conversation/Message (Phase 3)
└── main.py              # Existing (Phase 2)

frontend/
├── components/
│   └── ChatBot/         # New chatbot components (Phase 3)
│       ├── ChatPanel.tsx
│       ├── VoiceInput.tsx
│       ├── LanguageSelector.tsx
│       ├── VoiceSelector.tsx
│       └── GuidanceSystem.tsx
├── pages/
│   └── dashboard/       # Existing (Phase 2 - unchanged)
└── services/
    └── api-client.ts    # Existing (Phase 2 - unchanged)

.specify/phase3/         # New Phase 3 specific configs (Phase 3)

.claude/
├── agents/
│   ├── phase3-chatbot-engineer/
│   ├── phase3-agent-sdk-engineer/
│   ├── phase3-mcp-server-engineer/
│   ├── phase3-frontend-engineer/
│   ├── phase3-backend-engineer/
│   ├── phase3-database-engineer/
│   ├── phase3-jwt-auth-engineer/
│   ├── phase3-integration-engineer/
│   └── phase3-spec-writer-engineer/
└── skills/
    ├── phase3-frontend/
    ├── phase3-backend/
    ├── phase3-database/
    ├── phase3-auth/
    ├── phase3-ai-integration/
    ├── phase3-voice/
    ├── phase3-multilang/
    ├── phase3-guidance/
    └── phase3-islamic-values/
```

**Structure Decision**: Selected web application structure with separate frontend and backend. Phase 2 components remain unchanged while Phase 3 features are added in new directories with phase3 prefixes to maintain clear separation. Database models are extended rather than modified to preserve Phase 2 functionality.

## Phase 1 Deliverables

### Completed Artifacts
- **research.md**: Comprehensive research on technology choices, multi-language strategy, data model considerations, security measures, and risk mitigation strategies
- **data-model.md**: Detailed data model for Conversation and Message entities with validation rules, relationships, and constraints
- **quickstart.md**: Complete setup and configuration guide for the chatbot feature
- **contracts/chat-api.yaml**: OpenAPI specification for the chat endpoint with request/response schemas and security definitions
- **Agent Context Update**: Successfully updated Qwen Code context with new technology stack information

### Agent Context Update
- Updated Qwen Code context file (QWEN.md) with new technology stack information
- Added language details: Python 3.11 (Backend), TypeScript/JavaScript (Frontend Next.js 16.1.6)
- Added framework details: FastAPI (Backend), Next.js 16.1.6 (Frontend), Cohere API (AI), SQLModel (ORM), Web Speech API (Voice)
- Added database details: Neon Serverless PostgreSQL (extended with Conversation/Message tables)

## Complexity Tracking

> **Fill ONLY if Constitution Check has violations that must be justified**

| Violation | Why Needed | Simpler Alternative Rejected Because |
|-----------|------------|-------------------------------------|
| [e.g., 4th project] | [current need] | [why 3 projects insufficient] |
| [e.g., Repository pattern] | [specific problem] | [why direct DB access insufficient] |
