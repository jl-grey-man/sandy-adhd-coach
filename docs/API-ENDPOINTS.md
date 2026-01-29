# API Endpoints Specification

**Last Updated:** 2025-01-26  
**Base URL (Development):** `http://localhost:8000`  
**Base URL (Production):** `https://api.adhd-coach.com` (TBD)

---

## Overview

RESTful API built with FastAPI. All endpoints return JSON.

**Authentication:** JWT tokens via Bearer authentication  
**Rate Limiting:** 100 requests/minute per user  
**Error Format:** Standard JSON error responses

---

## Authentication

### **POST /auth/register**

Register a new user.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword",
  "name": "John Doe",
  "timezone": "Europe/Stockholm"
}
```

**Response (201):**
```json
{
  "user_id": 1,
  "email": "user@example.com",
  "name": "John Doe",
  "token": "eyJhbGciOiJIUzI1NiIs..."
}
```

---

### **POST /auth/login**

Login existing user.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "securepassword"
}
```

**Response (200):**
```json
{
  "user_id": 1,
  "token": "eyJhbGciOiJIUzI1NiIs...",
  "expires_at": "2025-02-26T10:00:00Z"
}
```

---

### **POST /auth/logout**

Logout (invalidate token).

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "message": "Logged out successfully"
}
```

---

## Chat / Conversations

### **POST /chat/message**

Send a text message to the AI coach.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "message": "I'm struggling with focus today",
  "context": {
    "energy": 5,
    "current_task": "client_proposal"
  }
}
```

**Response (200):**
```json
{
  "conversation_id": 123,
  "ai_response": "I notice you forgot your meds today...",
  "suggestions": [
    "Take a 5 minute break",
    "Try body doubling"
  ],
  "created_at": "2025-01-26T10:30:00Z"
}
```

---

### **POST /chat/voice**

Send voice message to AI coach.

**Headers:** `Authorization: Bearer <token>`

**Request:** `multipart/form-data`
```
audio: [audio file, .webm or .mp3]
context: {"energy": 5}
```

**Response (200):**
```json
{
  "conversation_id": 124,
  "transcription": "I'm struggling with focus today",
  "ai_response": "I notice you forgot your meds today...",
  "audio_url": "https://storage/audio_124.webm",
  "created_at": "2025-01-26T10:31:00Z"
}
```

---

### **GET /chat/history**

Get conversation history.

**Headers:** `Authorization: Bearer <token>`

**Query Params:**
- `limit` (default: 50)
- `offset` (default: 0)
- `since` (ISO date, optional)

**Response (200):**
```json
{
  "conversations": [
    {
      "id": 124,
      "user_message": "I'm struggling with focus today",
      "ai_response": "I notice...",
      "input_type": "voice",
      "created_at": "2025-01-26T10:31:00Z"
    }
  ],
  "total": 157,
  "limit": 50,
  "offset": 0
}
```

---

## Check-ins

### **POST /checkin/morning**

Submit morning check-in.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "energy": 6,
  "focus": 7,
  "mood": 7,
  "priority_task": "Finish client proposal"
}
```

**Response (200):**
```json
{
  "checkin_id": 45,
  "ai_response": "Energy is 6/10 and focus is good at 7/10. Since your priority is the client proposal, let's plan your day...",
  "suggested_plan": {
    "morning_window": "9:00-10:00",
    "priority_block": "11:00-13:00",
    "tasks": ["client_proposal"]
  }
}
```

---

### **POST /checkin/weekly/start**

Start weekly conversational check-in.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "ratings": {
    "overall": 7,
    "energy": 5,
    "focus": 8,
    "mood": 6,
    "stress": 4
  }
}
```

**Response (200):**
```json
{
  "checkin_id": 12,
  "session_id": "weekly_12",
  "first_question": "I see you rated your week 7/10 - that's pretty solid! But your energy was only 5/10. Let's dig into that. What were your wins this week?"
}
```

---

### **POST /checkin/weekly/continue**

Continue weekly check-in conversation.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "session_id": "weekly_12",
  "response": "I finished the big project proposal and worked out 3 times",
  "response_audio_url": "https://storage/audio_125.webm"  // optional
}
```

**Response (200):**
```json
{
  "next_question": "Nice! Finishing that proposal is huge. What helped you get it done? What made the difference this time?",
  "question_count": 2,
  "estimated_remaining": "3-5 questions"
}
```

---

### **POST /checkin/weekly/complete**

Finalize weekly check-in and get review.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "session_id": "weekly_12"
}
```

**Response (200):**
```json
{
  "checkin_id": 12,
  "summary": {
    "wins": ["Finished proposal", "Exercised 3x"],
    "challenges": ["Sleep issues", "Monday struggles"],
    "patterns": ["Body doubling works", "Sleep affects energy"],
    "next_week_focus": "Fix sleep quality",
    "recommendations": [
      "Phone charged in other room",
      "Meds by coffee maker"
    ]
  },
  "full_analysis": "Strong week overall with notable wins...",
  "created_at": "2025-01-26T18:00:00Z"
}
```

---

### **GET /checkin/history**

Get check-in history.

**Headers:** `Authorization: Bearer <token>`

**Query Params:**
- `type` (daily, weekly, monthly)
- `limit` (default: 20)

**Response (200):**
```json
{
  "checkins": [
    {
      "id": 12,
      "type": "weekly",
      "ratings": {...},
      "summary": {...},
      "created_at": "2025-01-26T18:00:00Z"
    }
  ]
}
```

---

## Tasks

### **POST /tasks**

Create a new task.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "title": "Design homepage mockup",
  "description": "Create initial design for client website",
  "project_id": 5,
  "difficulty": "hard",
  "energy_needed": "high",
  "focus_needed": "high",
  "task_type": "creative",
  "estimated_time_minutes": 120,
  "deadline": "2025-02-10"
}
```

**Response (201):**
```json
{
  "task_id": 67,
  "title": "Design homepage mockup",
  "status": "next",
  "best_time_of_day": "morning",  // AI suggested
  "best_energy_state": "high",
  "created_at": "2025-01-26T10:00:00Z"
}
```

---

### **GET /tasks**

Get tasks list.

**Headers:** `Authorization: Bearer <token>`

**Query Params:**
- `status` (next, active, waiting, someday, completed)
- `project_id`
- `difficulty`
- `limit` (default: 50)

**Response (200):**
```json
{
  "tasks": [
    {
      "id": 67,
      "title": "Design homepage mockup",
      "difficulty": "hard",
      "energy_needed": "high",
      "status": "next",
      "project": {
        "id": 5,
        "name": "Client Website"
      }
    }
  ]
}
```

---

### **GET /tasks/suggestions**

Get AI-suggested tasks based on current state.

**Headers:** `Authorization: Bearer <token>`

**Query Params:**
- `energy` (1-10)
- `focus` (1-10)
- `available_time_minutes`

**Response (200):**
```json
{
  "suggestions": [
    {
      "task_id": 45,
      "title": "Review client document",
      "reason": "Low energy task, perfect for your current state (5/10)",
      "estimated_time": 30
    },
    {
      "task_id": 52,
      "title": "Organize design files",
      "reason": "Mindless task, good for low focus",
      "estimated_time": 20
    }
  ],
  "avoid_now": [
    {
      "task_id": 67,
      "title": "Design homepage mockup",
      "reason": "Needs high energy (yours is 5/10). Save for tomorrow morning."
    }
  ]
}
```

---

### **PATCH /tasks/{task_id}**

Update a task.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "status": "completed",
  "actual_time_minutes": 135
}
```

**Response (200):**
```json
{
  "task_id": 67,
  "status": "completed",
  "completed_at": "2025-01-26T14:30:00Z"
}
```

---

### **DELETE /tasks/{task_id}**

Delete a task.

**Headers:** `Authorization: Bearer <token>`

**Response (204):** No content

---

## Projects

### **POST /projects**

Create a new project.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "name": "Client Website Redesign",
  "description": "Complete redesign for ABC Corp",
  "priority": "high",
  "deadline": "2025-03-15"
}
```

**Response (201):**
```json
{
  "project_id": 8,
  "name": "Client Website Redesign",
  "status": "active",
  "created_at": "2025-01-26T10:00:00Z"
}
```

---

### **GET /projects**

Get all projects.

**Headers:** `Authorization: Bearer <token>`

**Query Params:**
- `status` (active, on_hold, completed, someday)

**Response (200):**
```json
{
  "projects": [
    {
      "id": 8,
      "name": "Client Website Redesign",
      "status": "active",
      "task_count": 12,
      "completed_tasks": 3
    }
  ]
}
```

---

### **GET /projects/{project_id}**

Get project details with tasks.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "id": 8,
  "name": "Client Website Redesign",
  "description": "Complete redesign for ABC Corp",
  "status": "active",
  "tasks": [
    {
      "id": 67,
      "title": "Design homepage mockup",
      "status": "next"
    }
  ]
}
```

---

## Work Sessions

### **POST /work/start**

Start a work session (timer).

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "task_id": 67,
  "energy": 6,
  "focus": 7,
  "strategy": "body_doubling"
}
```

**Response (200):**
```json
{
  "session_id": 234,
  "task": {
    "id": 67,
    "title": "Design homepage mockup"
  },
  "started_at": "2025-01-26T11:00:00Z"
}
```

---

### **POST /work/end**

End a work session.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "session_id": 234,
  "completed": true,
  "effectiveness_rating": 8
}
```

**Response (200):**
```json
{
  "session_id": 234,
  "duration_minutes": 87,
  "ended_at": "2025-01-26T12:27:00Z",
  "ai_feedback": "Great session! Body doubling worked well for you again."
}
```

---

## Wheel of Life

### **POST /wheel/categories**

Create/update Wheel of Life categories.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "categories": [
    {
      "name": "Personal Growth",
      "description": "Learning and self-development",
      "definition_of_10": "Learning new things, reading 2 books/month, meditating daily"
    },
    {
      "name": "Health & Fitness",
      "description": "Physical health",
      "definition_of_10": "Exercising 4x/week, eating healthy, sleeping 7-8 hours"
    }
  ]
}
```

**Response (200):**
```json
{
  "categories": [
    {"id": 1, "name": "Personal Growth", "display_order": 1},
    {"id": 2, "name": "Health & Fitness", "display_order": 2}
  ]
}
```

---

### **POST /wheel/scores**

Submit Wheel of Life scores.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "scores": [
    {"category_id": 1, "score": 7, "notes": "Reading more this month"},
    {"category_id": 2, "score": 6, "notes": "Exercise good, sleep poor"}
  ]
}
```

**Response (200):**
```json
{
  "recorded_at": "2025-01-26T18:00:00Z",
  "average_score": 6.5,
  "changes": [
    {"category": "Personal Growth", "change": "+1", "previous": 6}
  ]
}
```

---

### **GET /wheel/current**

Get current Wheel of Life state.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "categories": [
    {
      "id": 1,
      "name": "Personal Growth",
      "current_score": 7,
      "previous_score": 6,
      "trend": "improving",
      "definition_of_10": "Learning new things..."
    }
  ],
  "average": 6.8,
  "last_updated": "2025-01-26T18:00:00Z"
}
```

---

## Calendar

### **GET /calendar/sync**

Sync calendar with external provider.

**Headers:** `Authorization: Bearer <token>`

**Query Params:**
- `provider` (google, outlook)
- `start_date` (ISO date)
- `end_date` (ISO date)

**Response (200):**
```json
{
  "synced_count": 15,
  "events": [
    {
      "id": 1,
      "title": "Team Meeting",
      "start_time": "2025-01-27T10:00:00Z",
      "end_time": "2025-01-27T11:00:00Z"
    }
  ]
}
```

---

### **GET /calendar/events**

Get calendar events.

**Headers:** `Authorization: Bearer <token>`

**Query Params:**
- `start_date` (ISO date)
- `end_date` (ISO date)

**Response (200):**
```json
{
  "events": [...]
}
```

---

### **GET /calendar/free-time**

Get available work windows based on calendar.

**Headers:** `Authorization: Bearer <token>`

**Query Params:**
- `date` (ISO date, default: today)

**Response (200):**
```json
{
  "date": "2025-01-27",
  "work_windows": [
    {
      "start": "09:00",
      "end": "10:00",
      "duration_minutes": 60
    },
    {
      "start": "11:00",
      "end": "14:00",
      "duration_minutes": 180
    }
  ],
  "total_available_minutes": 360
}
```

---

## Goals

### **POST /goals**

Create a goal.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "category": "personal",
  "title": "Read 24 books this year",
  "description": "2 books per month",
  "target_date": "2025-12-31"
}
```

**Response (201):**
```json
{
  "goal_id": 15,
  "title": "Read 24 books this year",
  "status": "active",
  "progress": 0
}
```

---

### **GET /goals**

Get all goals.

**Headers:** `Authorization: Bearer <token>`

**Response (200):**
```json
{
  "goals": [...]
}
```

---

### **PATCH /goals/{goal_id}**

Update goal progress.

**Headers:** `Authorization: Bearer <token>`

**Request:**
```json
{
  "progress": 25,
  "notes": "Finished 6 books so far"
}
```

**Response (200):**
```json
{
  "goal_id": 15,
  "progress": 25,
  "updated_at": "2025-01-26T20:00:00Z"
}
```

---

## Error Responses

All errors follow this format:

```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Invalid request data",
    "details": {
      "field": "email",
      "issue": "Email format is invalid"
    }
  }
}
```

**Common Error Codes:**
- `VALIDATION_ERROR` (400)
- `UNAUTHORIZED` (401)
- `FORBIDDEN` (403)
- `NOT_FOUND` (404)
- `RATE_LIMIT_EXCEEDED` (429)
- `INTERNAL_ERROR` (500)

---

## Rate Limiting

- **Default:** 100 requests/minute per user
- **Burst:** Up to 200 requests in 10 seconds
- **Headers:** 
  - `X-RateLimit-Limit: 100`
  - `X-RateLimit-Remaining: 87`
  - `X-RateLimit-Reset: 1706270400`

---

## Webhook Events (Future)

For real-time updates:

```json
{
  "event": "checkin.completed",
  "data": {...},
  "timestamp": "2025-01-26T18:00:00Z"
}
```

Events:
- `checkin.completed`
- `task.completed`
- `goal.achieved`
- `insight.detected`
