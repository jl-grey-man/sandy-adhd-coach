# API REFERENCE - Quick Reference

**For complete code, see: `backend/app/main.py` and `backend/app/routers/`**

---

## Base URL
```
Production: https://sandy-adhd-coach-production.up.railway.app
Local Dev:  http://localhost:8000
```

---

## Authentication

### POST /auth/signup
Create new user account
```json
{
  "email": "user@example.com",
  "password": "password123",
  "full_name": "Name"
}
```

### POST /auth/login
Get JWT token
```json
{
  "email": "user@example.com",
  "password": "password123"
}
```

Returns:
```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

---

## Chat

### POST /chat
Send message, get Sandy's response

**Headers:**
```
Authorization: Bearer {jwt_token}
```

**Body:**
```json
{
  "message": "your message here"
}
```

**Response:**
```json
{
  "response": "Sandy's reply",
  "actions": [
    {"type": "create_task", "title": "..."},
    {"type": "create_reminder", "message": "...", "minutes_from_now": 30}
  ]
}
```

---

## Tasks

### GET /tasks
List all tasks
```
GET /tasks?status=pending
```

### POST /tasks
Create task
```json
{
  "title": "Task title",
  "priority": "high",
  "project_id": 123
}
```

### PATCH /tasks/{id}
Update task
```json
{
  "status": "completed"
}
```

### DELETE /tasks/{id}
Delete task

---

## Projects

### GET /projects
List all projects

### POST /projects
Create project
```json
{
  "title": "Project name",
  "deadline": "2026-02-10",
  "estimated_hours": 20
}
```

---

## Patterns

### GET /patterns
View pattern hypotheses (≥50% confidence)

### POST /patterns/feedback
Give feedback on pattern accuracy
```json
{
  "pattern_id": 123,
  "feedback_type": "pattern_accuracy",
  "rating": 5
}
```

---

## Telegram

### POST /telegram/webhook
Telegram bot webhook (called by Telegram)

---

## Admin

### POST /admin/fix-descriptions
Fix category descriptions (change him/he to you)
Requires authentication

---

## Action Parsing

Sandy's responses can contain action blocks:

```
```action
{"type": "create_task", "title": "Email client"}
```
```

Backend parses these and executes them.

**Action Types:**
- `create_task` - Work items
- `create_reminder` - Time-based notifications
- `create_project` - Multi-step work with deadlines

---

**For complete implementation, see:**
- `backend/app/main.py` - FastAPI app
- `backend/app/routers/` - Route handlers
- `backend/app/models/` - Database models
