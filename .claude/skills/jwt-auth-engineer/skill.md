# JWT Auth Engineer Skill

## Purpose
Provides token handling and security capabilities for the Todo Evolution Hackathon application.

## Functions
- Implement Better Auth
- Handle JWT token verification
- Manage user authentication
- Enforce authorization
- Implement token expiry
- Enforce user isolation
- Secure API endpoints
- Implement JWT verification middleware
- Create proactive token refresh mechanism

## Usage
```
/sp.jwt-auth-engineer [auth-feature-request]
```

## Constraints
- Require JWT for all APIs
- Enforce user_id isolation
- Prevent cross-user data leaks
- Implement secure token handling
- Maintain 7-day token expiry
- Reject unauthenticated requests with 401
- Ensure user_id extracted from token only
- Implement proactive refresh 1 hour before expiry with fallback to reactive handling