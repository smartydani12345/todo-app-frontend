# Data Model: Todo Evolution Hackathon – Phase 2

## Task Entity

### Fields

| Field | Type | Constraints | Default | Description |
|-------|------|-------------|---------|-------------|
| id | UUID | Primary Key, Not Null | Auto-generated | Unique identifier for each task |
| user_id | UUID | Foreign Key, Not Null | - | Reference to the user who owns the task |
| title | VARCHAR(100) | Not Null, Length: 1-100 | - | Task title or description |
| description | TEXT | Length: 0-1000 | NULL | Extended description of the task |
| completed | BOOLEAN | Not Null | FALSE | Whether the task is completed |
| priority | VARCHAR(10) | Not Null, Enum: high/medium/low | 'medium' | Priority level of the task |
| tags | JSON | Max 10 items, String length: 1-50 each | [] | Array of tag strings associated with the task |
| due_date | TIMESTAMP | Nullable | NULL | Optional deadline for the task |
| created_at | TIMESTAMP | Not Null | Current timestamp | When the task was created |
| updated_at | TIMESTAMP | Not Null | Current timestamp | When the task was last updated |

### Validation Rules

1. **Title**: Must be between 1-100 characters, not null
2. **Description**: May be null, maximum 1000 characters if provided
3. **Priority**: Must be one of 'high', 'medium', or 'low'
4. **Tags**: Array of strings, maximum 10 tags, each tag 1-50 characters
5. **Due Date**: If provided, must be a valid future date
6. **User Isolation**: Each task must belong to the authenticated user (enforced by user_id)

### Relationships

```
Better Auth User (via user_id) ── One-to-Many ── Task
```

- One user can have many tasks
- Tasks are strictly isolated by user_id (no cross-user access)

### Indexes

| Name | Fields | Purpose |
|------|--------|---------|
| idx_task_user_id | user_id | Efficient querying by user |
| idx_task_completed | completed | Fast filtering by completion status |
| idx_task_priority | priority | Fast filtering by priority |
| idx_task_due_date | due_date | Fast sorting by due date |
| idx_task_created_at | created_at | Chronological ordering |
| idx_task_user_status | user_id, completed | Combined user and status filtering |

### State Transitions

**Task Lifecycle States**:
1. **Created**: New task added to user's list
2. **Updated**: Task details modified by user
3. **Completed**: Task marked as done by user
4. **Deleted**: Task removed from user's list (soft delete with flag)

**Transition Rules**:
- Created → Updated/Completed/Deleted: User initiated actions
- Updated → Updated/Completed/Deleted: Continuous modifications
- Completed ↔ Updated: Tasks can be unmarked as complete
- Any state → Deleted: User can delete at any point

### Sample JSON Representation

```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "user_id": "123e4567-e89b-12d3-a456-426614174000",
  "title": "Implement user authentication",
  "description": "Set up JWT-based authentication with Better Auth",
  "completed": false,
  "priority": "high",
  "tags": ["frontend", "security", "authentication"],
  "due_date": "2024-01-15T10:00:00Z",
  "created_at": "2024-01-10T09:00:00Z",
  "updated_at": "2024-01-10T09:00:00Z"
}
```

### Access Control Rules

1. **Ownership**: Users can only access tasks where user_id matches their authenticated user
2. **Isolation**: No cross-user task visibility
3. **Authorization**: All operations require valid JWT with matching user_id claim
4. **Operations**: Users can CRUD their own tasks but not others'

### Performance Considerations

1. **Query Optimization**: Use indexes for common filtering/sorting operations
2. **Pagination**: Limit results to 50 per page to maintain performance
3. **Caching**: Cache authenticated user's tasks temporarily for dashboard display
4. **Connection Pooling**: Use async database connections for concurrency

### Constraints Enforcement

- **Database Level**: Foreign key constraints to ensure user_id validity
- **Application Level**: JWT validation to ensure user_id matches authenticated user
- **Business Logic**: Prevent operations on tasks belonging to other users
- **Validation**: Input validation to ensure data integrity