# Database Schema Fix Plan

**Generated:** February 2, 2026
**Issue:** Migrations and documentation don't match actual models

---

## 🚨 CRITICAL ISSUES FOUND

### Migration 001 is INCOMPLETE

The `001_initial_schema.py` migration is missing **10+ tables** that exist in the models:

**Missing from Migration:**
1. ✅ `goals` - Has model, NOT in migration
2. ✅ `checkins` - Has model, NOT in migration
3. ✅ `metrics` - Has model, NOT in migration
4. ✅ `conversation_embeddings` - Has model, NOT in migration
5. ✅ `wheel_categories` - Has model, NOT in migration
6. ✅ `wheel_scores` - Has model, NOT in migration
7. ✅ `work_sessions` - Has model, NOT in migration
8. ✅ `calendar_events` - Has model, NOT in migration
9. ✅ `backburner_items` - Has model, NOT in migration
10. ✅ `milestones` - Has model, already in migration ✓
11. ✅ `conversations` - Has model, already in migration ✓

**In Migration but Incorrectly:**
- `users` table - Missing columns that were added in migration 002
- `calendar` table - Should be `calendar_events`
- `backburner` table - Should be `backburner_items`
- `wheel` table - Should be `wheel_categories` + `wheel_scores` (two tables!)

---

## 📋 DETAILED TABLE DISCREPANCIES

### 1. Goals Table - **MISSING FROM MIGRATION**

**Model:** `app/models/goal.py`
**Table Name:** `goals`

```python
id (PK)
user_id (FK → users.id)
category (String(50)) - CHECK: 'personal', 'work'
title (String(200))
description (Text)
target_date (Date)
created_at (DateTime with TZ)
completed_at (DateTime with TZ)
status (String(20)) - CHECK: 'active', 'completed', 'paused', 'abandoned'
progress (Integer) - CHECK: 0-100
extra_data (JSONB)
```

### 2. Checkins Table - **MISSING FROM MIGRATION**

**Model:** `app/models/checkin.py`
**Table Name:** `checkins`

```python
id (PK)
user_id (FK → users.id)
type (String(20)) - CHECK: 'daily', 'weekly', 'monthly'
overall_rating (Integer) - CHECK: 1-10
energy_rating (Integer) - CHECK: 1-10
focus_rating (Integer) - CHECK: 1-10
mood_rating (Integer) - CHECK: 1-10
stress_rating (Integer) - CHECK: 1-10
responses (JSONB)
ai_analysis (Text)
insights (JSONB)
created_at (DateTime with TZ)
```

### 3. Metrics Table - **MISSING FROM MIGRATION**

**Model:** `app/models/metric.py`
**Table Name:** `metrics`

```python
id (PK)
user_id (FK → users.id)
metric_type (String(50))
value (JSONB)
recorded_at (DateTime with TZ)
```

### 4. Conversation Embeddings - **MISSING FROM MIGRATION**

**Model:** `app/models/metric.py` (same file as Metric)
**Table Name:** `conversation_embeddings`

```python
id (PK)
conversation_id (FK → conversations.id)
pinecone_id (String(100)) UNIQUE
created_at (DateTime with TZ)
```

### 5. Wheel Categories - **WRONG TABLE NAME IN MIGRATION**

**Model:** `app/models/wheel.py`
**Table Name:** `wheel_categories` (NOT `wheel`)

```python
id (PK)
user_id (FK → users.id)
name (String(100))
description (Text)
definition_of_10 (Text)
display_order (Integer)
created_at (DateTime with TZ)
updated_at (DateTime with TZ)
UNIQUE(user_id, name)
```

### 6. Wheel Scores - **COMPLETELY MISSING**

**Model:** `app/models/wheel.py` (same file)
**Table Name:** `wheel_scores`

```python
id (PK)
user_id (FK → users.id)
category_id (FK → wheel_categories.id)
score (Integer)
notes (Text)
recorded_at (DateTime with TZ)
```

**Note:** Migration 001 has `wheel` table with wrong structure!

### 7. Work Sessions - **MISSING FROM MIGRATION**

**Model:** `app/models/work_session.py`
**Table Name:** `work_sessions`

```python
id (PK)
user_id (FK → users.id)
task_id (FK → tasks.id) SET NULL
started_at (DateTime with TZ)
ended_at (DateTime with TZ)
duration_minutes (Integer)
energy_at_start (Integer) - CHECK: 1-10
focus_at_start (Integer) - CHECK: 1-10
strategy_used (String(100))
completed (Boolean)
switched_task (Boolean)
reason_for_switching (Text)
effectiveness_rating (Integer) - CHECK: 1-10
```

**Note:** Migration 001 has `work_sessions` but with WRONG columns!

### 8. Calendar Events - **WRONG TABLE NAME**

**Model:** `app/models/calendar.py`
**Table Name:** `calendar_events` (NOT `calendar`)

```python
id (PK)
user_id (FK → users.id)
external_id (String(255))
title (String(200))
description (Text)
location (String(200))
start_time (DateTime with TZ)
end_time (DateTime with TZ)
all_day (Boolean)
calendar_source (String(50)) default='google'
synced_at (DateTime with TZ)
UNIQUE(user_id, external_id, calendar_source)
```

**Note:** Migration 001 has `calendar` with wrong columns!

### 9. Backburner Items - **WRONG TABLE NAME**

**Model:** `app/models/backburner.py`
**Table Name:** `backburner_items` (NOT `backburner`)

```python
id (PK)
user_id (FK → users.id)
title (String(200))
description (Text)
context_tags (ARRAY of String)
reason (Text)
created_at (DateTime)
resurfaced_at (DateTime)
activated_at (DateTime)
INDEX(user_id)
```

**Note:** Migration 001 has `backburner` with wrong columns!

---

## ⚠️ DOCUMENTATION ISSUES

`DATABASE_SCHEMA.md` lists these tables that DON'T EXIST:

1. **`reminders`** - Feature was REMOVED (Feb 2, 2026)
2. **`pattern_hypotheses`** - No model exists (might be `pattern_tracking`?)
3. **`user_feedback`** - No model exists

---

## ✅ ACTION PLAN

### Step 1: Create Migration 003 - Fix All Table Issues

Create `003_fix_all_missing_tables.py` that:

1. **Drop incorrectly named tables:**
   - DROP TABLE `calendar` → recreate as `calendar_events`
   - DROP TABLE `backburner` → recreate as `backburner_items`
   - DROP TABLE `wheel` → recreate as `wheel_categories` + `wheel_scores`
   - DROP TABLE `work_sessions` → recreate with correct columns

2. **Add completely missing tables:**
   - CREATE TABLE `goals`
   - CREATE TABLE `checkins`
   - CREATE TABLE `metrics`
   - CREATE TABLE `conversation_embeddings`

3. **Verify pattern_tracking:**
   - Check if this is the real table or if it's a duplicate class name issue

### Step 2: Update DATABASE_SCHEMA.md

Remove:
- `reminders` table (feature removed)
- `pattern_hypotheses` (verify replacement)
- `user_feedback` (doesn't exist)

Add full documentation for:
- `goals`
- `checkins`
- `metrics`
- `conversation_embeddings`
- `wheel_categories`
- `wheel_scores`
- `work_sessions`
- `calendar_events`
- `backburner_items`
- `conversations` (expand existing)

### Step 3: Test Deployment

1. Create migration 003
2. Push to Railway
3. Verify all tables created correctly
4. Test that app can access all tables

---

## 🎯 IMMEDIATE NEXT STEPS

1. **DO NOW:** Create comprehensive migration 003
2. **THEN:** Update DATABASE_SCHEMA.md
3. **FINALLY:** Test full deployment

---

**Priority:** 🔥 CRITICAL - App will fail when trying to access missing tables
