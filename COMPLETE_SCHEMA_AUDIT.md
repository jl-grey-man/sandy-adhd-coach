# Complete Database Schema Audit
**Date**: February 3, 2026
**Issue**: Bot failing due to model/database mismatches

## Critical Mismatches Found

### 1. CONVERSATIONS Table ❌ CRITICAL
**Migration 001 creates:**
```sql
- role (String)
- content (Text)
- session_id (NOT NULL)
```

**Model expects:**
```python
- user_message (Text)
- ai_response (Text)
- input_type (String, default='text')
- context (JSONB, nullable)
- suggestions (JSONB, nullable)
- session_id (nullable)
```

**Impact**: telegram_service.py line 305 queries `Conversation` - will fail on every message
**SQL Error**: Column `conversations.user_message` does not exist

---

### 2. TASKS Table ❌ CRITICAL
**Migration 001 creates:**
```sql
- goal_id (ForeignKey to goals)
- updated_at (DateTime)
- status (default='pending')
```

**Model expects:**
```python
- project_id (ForeignKey to projects)  # NOT goal_id!
- NO updated_at column
- status (enum: TODO/IN_PROGRESS/DONE, default=TODO)
```

**Impact**: Context building fails, bot crashes on every message
**SQL Error**: Column `tasks.project_id` does not exist (fixed by migration 005)
**SQL Error**: Column `tasks.updated_at` may cause issues if code tries to access it

---

### 3. PROJECTS Table ❌ CRITICAL
**Context service (line 91) accesses:**
```python
project.title  # Does not exist!
```

**Model has:**
```python
project.name  # Actual column name
```

**Impact**: Context building fails when user has active projects
**Error**: AttributeError: 'Project' object has no attribute 'title'

---

### 4. CONVERSATION Indexes
**Migration 001 creates:**
- `ix_conversations_user_id`
- `ix_conversations_session_id`

**Model expects:**
- `idx_conversations_user_id`
- `idx_conversations_session_id`
- `idx_conversations_created_at`

**Impact**: Minor - slower queries but won't crash

---

## Migration Chain Analysis

### Migration 001 (Initial)
- Creates base tables with OLD schema
- Conversations has role/content (not user_message/ai_response)
- Tasks has goal_id (not project_id)
- Projects table missing entirely!

### Migration 002 (User columns)
- Adds telegram fields to users ✅

### Migration 003 (Table renames)
- Renames calendar → calendar_events ✅
- Renames backburner → backburner_items ✅
- Creates wheel_scores table ✅
- Does NOT fix conversations or tasks ❌

### Migration 004 (Project columns)
- Adds columns to projects table ✅
- Assumes projects table exists (may not!)

### Migration 005 (Task project_id)
- Adds project_id to tasks ✅
- But tasks still has goal_id too!
- Still missing: conversations schema fix

---

## Required Fixes

### FIX 1: Conversations Table Schema ❌ URGENT
Need migration to:
```sql
ALTER TABLE conversations
  DROP COLUMN role,
  DROP COLUMN content,
  ADD COLUMN user_message TEXT NOT NULL,
  ADD COLUMN ai_response TEXT NOT NULL,
  ADD COLUMN input_type VARCHAR(20) DEFAULT 'text',
  ADD COLUMN context JSONB,
  ADD COLUMN suggestions JSONB,
  ALTER COLUMN session_id DROP NOT NULL;
```

### FIX 2: Context Service Project Title ❌ URGENT
Change line 91 in `app/services/context.py`:
```python
"title": project.title,  # WRONG
```
To:
```python
"title": project.name,  # CORRECT
```

### FIX 3: Remove goal_id from Tasks (Optional)
Tasks table has BOTH goal_id and project_id now. Should remove goal_id:
```sql
ALTER TABLE tasks DROP COLUMN goal_id;
```

### FIX 4: Verify Projects Table Exists
Migration 004 assumes projects table exists. Check if migration 001 creates it.

---

## Why Bot Fails on Every Message

**Current Flow:**
1. User sends message via Telegram ✅
2. Bot receives via getUpdates ✅
3. handle_message() called ✅
4. build_context_for_ai() queries tasks → ❌ FAILS (no project_id until mig 005)
5. Query conversations history → ❌ FAILS (wrong schema)
6. Never reaches AI service
7. Transaction aborted
8. No response sent

**After Migration 005 deploys:**
1-3. Same ✅
4. build_context_for_ai() queries tasks → ✅ Works now (project_id added)
5. Query conversations → ❌ STILL FAILS (still wrong schema)
6. Transaction aborted
7. No response

**After Conversations Fix:**
All steps should work ✅

---

## Action Plan

**IMMEDIATE (Blocking bot):**
1. ✅ Migration 005 deployed (adds project_id to tasks)
2. ❌ Create migration 006: Fix conversations table schema
3. ❌ Fix context.py line 91: project.title → project.name

**NEXT:**
4. Verify projects table exists in database
5. Consider removing goal_id from tasks (cleanup)
6. Fix index names to match models

---

## Testing After Fixes

**Test 1**: Send message in Telegram
- Should not see "column tasks.project_id does not exist" ✅
- Should not see "column conversations.user_message does not exist" ❌

**Test 2**: Create project, add task
- Verify task.project_id works
- Verify project.name (not title) is used

**Test 3**: Check conversation history
- Verify user_message and ai_response are saved
- Verify old role/content columns gone
