# Phase 3 MCP Tools Integration Skill

## Overview
This skill enables ChatAgent to interact with MCP (Model Context Protocol) tools for comprehensive task management through natural language commands.

## Available MCP Tools

### 1. add_task
**Purpose:** Create a new task

**Trigger Phrases:**
- "Add a task to..."
- "Create a task..."
- "Remind me to..."
- "I need to..."
- "Add to my list..."

**Example:**
```
User: "Add a task to buy groceries"
AI: "I've added the task 'Buy groceries' to your list."
```

**Implementation:**
```python
def _handle_create_request(self, user_input: str, user_id: str):
    title = self._extract_task_title(user_input)
    task = Task(title=title, user_id=user_id, priority='medium')
    db_session.add(task)
    db_session.commit()
    return {"success": True, "task": task}
```

### 2. list_tasks
**Purpose:** Retrieve user's tasks

**Trigger Phrases:**
- "Show my tasks"
- "List my tasks"
- "What are my tasks?"
- "Display tasks"

**Example:**
```
User: "Show my tasks"
AI: "You have 3 tasks: 1. Buy groceries (pending) 2. Call mom (pending) 3. Finish report (completed)"
```

### 3. complete_task
**Purpose:** Mark a task as completed

**Trigger Phrases:**
- "Mark task as done"
- "Complete the task..."
- "I finished..."
- "Task completed"

**Example:**
```
User: "Mark 'buy milk' as done"
AI: "I've marked the task 'Buy milk' as completed."
```

### 4. delete_task
**Purpose:** Remove a task

**Trigger Phrases:**
- "Delete the task..."
- "Remove task..."
- "Cancel task..."
- "Get rid of..."

**Example:**
```
User: "Delete the meeting task"
AI: "I've deleted the task 'Meeting' from your list."
```

### 5. update_task
**Purpose:** Modify an existing task

**Trigger Phrases:**
- "Edit task..."
- "Change task..."
- "Update task..."
- "Modify task..."

**Example:**
```
User: "Change meeting to 3pm"
AI: "I've updated the task 'Meeting' to 'Meeting at 3pm'."
```

### 6. recurring_task
**Purpose:** Set up recurring tasks

**Trigger Phrases:**
- "Set daily reminder..."
- "Recurring task..."
- "Every day/week/month..."

**Example:**
```
User: "Set daily reminder for exercise"
AI: "I've created a recurring task 'Exercise' that repeats daily."
```

### 7. set_due_date
**Purpose:** Set task due date

**Trigger Phrases:**
- "Due tomorrow"
- "Set deadline..."
- "Due date..."

**Example:**
```
User: "Set report due date to Friday"
AI: "I've set the due date for 'Report' to Friday."
```

### 8. send_reminder
**Purpose:** Send task reminder

**Trigger Phrases:**
- "Remind me at..."
- "Set reminder..."
- "Alert me..."

**Example:**
```
User: "Remind me at 5pm"
AI: "I've set a reminder for 5pm."
```

## Intent Detection

### Pattern Matching
```python
CREATE_PATTERNS = [
    r"add (a )?task",
    r"create (a )?task",
    r"remind me to",
    r"i need to",
    r"have to",
    r"should"
]

COMPLETE_PATTERNS = [
    r"complete",
    r"finish",
    r"done",
    r"marked? as done"
]

DELETE_PATTERNS = [
    r"delete",
    r"remove",
    r"cancel",
    r"get rid of"
]
```

### Task Title Extraction
```python
def _extract_task_title(self, user_input: str) -> str:
    phrases_to_remove = [
        "add a task to ",
        "create a task to ",
        "remind me to ",
        "need to ",
        "have to "
    ]
    
    cleaned = user_input.lower()
    for phrase in phrases_to_remove:
        if cleaned.startswith(phrase):
            cleaned = cleaned[len(phrase):]
    
    return cleaned.strip().capitalize()
```

## Response Templates

### Success Responses
```python
RESPONSES = {
    "create": {
        "en": "I've added the task '{title}' to your list.",
        "ur": "میں نے کام '{title}' آپ کی فہرست میں شامل کر دیا ہے۔",
        "roman_ur": "Maine task '{title}' aap ki list mein shamil kar diya hai."
    },
    "complete": {
        "en": "I've marked '{title}' as completed.",
        "ur": "میں نے '{title}' کو مکمل کے طور پر نشان زد کر دیا ہے۔",
        "roman_ur": "Maine '{title}' ko complete mark kar diya hai."
    },
    "delete": {
        "en": "I've deleted '{title}' from your list.",
        "ur": "میں نے '{title}' کو آپ کی فہرست سے حذف کر دیا ہے۔",
        "roman_ur": "Maine '{title}' ko aap ki list se delete kar diya hai."
    }
}
```

## Error Handling

### Task Not Found
```python
if not matched_task:
    return {
        "success": False,
        "message": f"I couldn't find a task matching '{identifier}' in your list.",
        "operation": "complete"
    }
```

### Operation Failed
```python
except Exception as e:
    logger.error(f"Error in task operation: {str(e)}")
    return {
        "success": False,
        "message": "Sorry, I couldn't complete that operation. Please try again.",
        "operation": operation_type
    }
```

## Integration Flow

```
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ User Input  │────▶│ Intent       │────▶│ MCP Tool    │
│ (Natural    │     │ Detection    │     │ Execution   │
│ Language)   │     │              │     │             │
└─────────────┘     └──────────────┘     └─────────────┘
                                              │
                                              ▼
┌─────────────┐     ┌──────────────┐     ┌─────────────┐
│ Response    │◀────│ Response     │◀────│ Result      │
│ Generation  │     │ Template     │     │ Processing  │
└─────────────┘     └──────────────┘     └─────────────┘
```

## Testing Examples

### Test Cases
```python
def test_add_task():
    result = process_natural_language_request(
        "Add a task to buy milk",
        "user123"
    )
    assert result["success"] == True
    assert result["operation"] == "create"

def test_complete_task():
    result = process_natural_language_request(
        "Mark buy milk as done",
        "user123"
    )
    assert result["success"] == True
    assert result["operation"] == "complete"

def test_delete_task():
    result = process_natural_language_request(
        "Delete the meeting task",
        "user123"
    )
    assert result["success"] == True
    assert result["operation"] == "delete"
```

## Best Practices

1. **Always confirm task operations** - Let user know what was done
2. **Handle ambiguous requests** - Ask for clarification when needed
3. **Preserve task context** - Remember previous tasks in conversation
4. **Provide helpful errors** - Guide users when operations fail
5. **Support partial matches** - Find tasks even with incomplete names

## Limitations

- Complex task descriptions may need manual entry
- Multiple tasks in one request not supported
- Task dependencies require explicit specification

## Future Enhancements

1. Batch task operations
2. Smart task suggestions
3. Natural language due dates
4. Task priority from context
5. Subtask support
