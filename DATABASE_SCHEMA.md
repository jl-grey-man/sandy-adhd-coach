# DATABASE SCHEMA - Complete Reference

**Last Updated:** February 2, 2026
**Status:** Telegram-only interface, no web UI, no reminders

---

## 📊 **DATABASE OVERVIEW**

**Database Type:** PostgreSQL
**Hosted:** Railway
**ORM:** SQLAlchemy
**Migrations:** Alembic

**IMPORTANT:** See `MIGRATIONS_GUIDE.md` before making any database changes!

---

## 📋 **ALL TABLES**

### Core User & Chat Tables
1. **users** - User accounts with Telegram integration
2. **conversations** - Chat message history
3. **conversation_embeddings** - Pinecone vector storage references

### Task Management Tables
4. **tasks** - Work items to complete
5. **projects** - Multi-step work with deadlines
6. **milestones** - Project check-in points
7. **goals** - User goals with progress tracking
8. **backburner_items** - Ideas saved for later

### Tracking & Reflection Tables
9. **checkins** - Daily/weekly/monthly check-ins with ratings
10. **metrics** - General metrics tracking
11. **work_sessions** - Time tracking and focus analysis
12. **calendar_events** - Synced calendar events
13. **wheel_categories** - Wheel of Life categories (customizable)
14. **wheel_scores** - Wheel of Life scores over time

### Pattern Learning Tables
15. **pattern_categories** - 18 ADHD pattern types (system-defined)
16. **pattern_observations** - Individual observations from conversations
17. **pattern_tracking** - Pattern analysis and confidence scores

---

## 🗄️ **DETAILED TABLE SCHEMAS**

### 1. users

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100),
    timezone VARCHAR(50) DEFAULT 'UTC',
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,

    -- User preferences (JSONB)
    preferences JSONB NOT NULL DEFAULT '{"voice_enabled": true, "notification_enabled": true, "checkin_times": {"morning": "09:00", "evening": "20:00"}}',
    adhd_profile JSONB NOT NULL DEFAULT '{}',

    -- Telegram integration
    telegram_chat_id BIGINT UNIQUE,
    telegram_username VARCHAR(100),
    morning_briefing_time VARCHAR(5) DEFAULT '09:00'
);
```

**Purpose:** Store user accounts with Telegram integration
**Key Fields:**
- `preferences` - User settings as JSONB
- `adhd_profile` - ADHD type and patterns as JSONB
- `telegram_chat_id` - Links to Telegram account (primary interface)
- `morning_briefing_time` - When to send daily briefing

**Relationships:**
- One user → Many tasks, projects, goals, observations, etc.

---

### 2. conversations

```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    session_id VARCHAR(100),
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    input_type VARCHAR(20) DEFAULT 'text',
    context JSONB,
    suggestions JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_conversations_user_id ON conversations(user_id);
CREATE INDEX idx_conversations_session_id ON conversations(session_id);
CREATE INDEX idx_conversations_created_at ON conversations(created_at);
```

**Purpose:** Store complete chat history
**Key Fields:**
- `user_message` - What the user said
- `ai_response` - Sandy's response
- `session_id` - Groups related messages
- `context` - Context data used for response (JSONB)

---

### 3. conversation_embeddings

```sql
CREATE TABLE conversation_embeddings (
    id SERIAL PRIMARY KEY,
    conversation_id INTEGER NOT NULL REFERENCES conversations(id) ON DELETE CASCADE,
    pinecone_id VARCHAR(100) NOT NULL UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_conversation FOREIGN KEY (conversation_id) REFERENCES conversations(id)
);
```

**Purpose:** Link conversations to Pinecone vector embeddings
**Key Fields:**
- `pinecone_id` - ID in Pinecone vector database
- Used for semantic memory search

---

### 4. tasks

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    project_id INTEGER REFERENCES projects(id) ON DELETE SET NULL,
    goal_id INTEGER REFERENCES goals(id) ON DELETE SET NULL,

    title VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'pending',
    priority INTEGER,
    energy_level VARCHAR(20),
    estimated_minutes INTEGER,

    due_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,

    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_project FOREIGN KEY (project_id) REFERENCES projects(id),
    CONSTRAINT fk_goal FOREIGN KEY (goal_id) REFERENCES goals(id)
);
```

**Purpose:** Store actionable work items
**Status Values:** `pending`, `in_progress`, `completed`, `stuck`

---

### 5. projects

```sql
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    name VARCHAR(200) NOT NULL,
    description TEXT,
    status VARCHAR(20) DEFAULT 'active',
    priority INTEGER,
    color VARCHAR(7),

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,

    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Purpose:** Multi-task projects with organization
**Status Values:** `active`, `completed`, `on_hold`

---

### 6. milestones

```sql
CREATE TABLE milestones (
    id SERIAL PRIMARY KEY,
    project_id INTEGER NOT NULL REFERENCES projects(id) ON DELETE CASCADE,

    check_in_date TIMESTAMP NOT NULL,
    message TEXT NOT NULL,
    completed BOOLEAN DEFAULT FALSE,

    user_response TEXT,
    responded_at TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_project FOREIGN KEY (project_id) REFERENCES projects(id)
);

CREATE INDEX idx_milestones_project ON milestones(project_id);
CREATE INDEX idx_milestones_check_in_date ON milestones(check_in_date);
```

**Purpose:** Automated project check-in points

---

### 7. goals

```sql
CREATE TABLE goals (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    category VARCHAR(50) NOT NULL CHECK (category IN ('personal', 'work')),
    title VARCHAR(200) NOT NULL,
    description TEXT,

    target_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,

    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'completed', 'paused', 'abandoned')),
    progress INTEGER DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),

    extra_data JSONB DEFAULT '{}',

    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Purpose:** Long-term goals with progress tracking
**Key Fields:**
- `category` - 'personal' or 'work'
- `progress` - 0-100% completion
- `extra_data` - Flexible storage for goal-specific data

---

### 8. backburner_items

```sql
CREATE TABLE backburner_items (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    title VARCHAR(200) NOT NULL,
    description TEXT,
    context_tags VARCHAR[] DEFAULT '{}',
    reason TEXT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    resurfaced_at TIMESTAMP,
    activated_at TIMESTAMP,

    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE INDEX idx_backburner_user ON backburner_items(user_id);
```

**Purpose:** Ideas and projects saved for later
**Key Fields:**
- `context_tags` - Tags for smart resurfacing
- `resurfaced_at` - When Sandy reminded user
- `activated_at` - When moved to active tasks/projects

---

### 9. checkins

```sql
CREATE TABLE checkins (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    type VARCHAR(20) NOT NULL CHECK (type IN ('daily', 'weekly', 'monthly')),

    -- Ratings (1-10 scale)
    overall_rating INTEGER CHECK (overall_rating >= 1 AND overall_rating <= 10),
    energy_rating INTEGER CHECK (energy_rating >= 1 AND energy_rating <= 10),
    focus_rating INTEGER CHECK (focus_rating >= 1 AND focus_rating <= 10),
    mood_rating INTEGER CHECK (mood_rating >= 1 AND mood_rating <= 10),
    stress_rating INTEGER CHECK (stress_rating >= 1 AND stress_rating <= 10),

    responses JSONB DEFAULT '[]',
    ai_analysis TEXT,
    insights JSONB DEFAULT '{}',

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Purpose:** Regular check-ins for tracking patterns
**Check-in Types:** daily, weekly, monthly

---

### 10. metrics

```sql
CREATE TABLE metrics (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    metric_type VARCHAR(50) NOT NULL,
    value JSONB NOT NULL,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Purpose:** Flexible metrics storage with JSONB values

---

### 11. work_sessions

```sql
CREATE TABLE work_sessions (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    task_id INTEGER REFERENCES tasks(id) ON DELETE SET NULL,

    started_at TIMESTAMP NOT NULL,
    ended_at TIMESTAMP,
    duration_minutes INTEGER,

    energy_at_start INTEGER CHECK (energy_at_start >= 1 AND energy_at_start <= 10),
    focus_at_start INTEGER CHECK (focus_at_start >= 1 AND focus_at_start <= 10),
    strategy_used VARCHAR(100),

    completed BOOLEAN DEFAULT FALSE,
    switched_task BOOLEAN DEFAULT FALSE,
    reason_for_switching TEXT,
    effectiveness_rating INTEGER CHECK (effectiveness_rating >= 1 AND effectiveness_rating <= 10),

    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_task FOREIGN KEY (task_id) REFERENCES tasks(id)
);
```

**Purpose:** Track work sessions for pattern learning

---

### 12. calendar_events

```sql
CREATE TABLE calendar_events (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    external_id VARCHAR(255),
    title VARCHAR(200),
    description TEXT,
    location VARCHAR(200),

    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    all_day BOOLEAN DEFAULT FALSE,

    calendar_source VARCHAR(50) DEFAULT 'google',
    synced_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, external_id, calendar_source)
);
```

**Purpose:** Synced calendar events from Google Calendar

---

### 13. wheel_categories

```sql
CREATE TABLE wheel_categories (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    name VARCHAR(100) NOT NULL,
    description TEXT,
    definition_of_10 TEXT,
    display_order INTEGER,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id),
    UNIQUE(user_id, name)
);
```

**Purpose:** User-customizable Wheel of Life categories

---

### 14. wheel_scores

```sql
CREATE TABLE wheel_scores (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES wheel_categories(id) ON DELETE CASCADE,

    score INTEGER NOT NULL,
    notes TEXT,
    recorded_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES wheel_categories(id)
);
```

**Purpose:** Track Wheel of Life scores over time

---

### 15. pattern_categories

```sql
CREATE TABLE pattern_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    icon VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Purpose:** System-defined 18 ADHD pattern types
**See:** `docs/PATTERN_LEARNING_SYSTEM.md` for complete list

---

### 16. pattern_observations

```sql
CREATE TABLE pattern_observations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES pattern_categories(id),

    observation TEXT NOT NULL,
    context TEXT,
    observed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES pattern_categories(id)
);
```

**Purpose:** Individual observations extracted from conversations

---

### 17. pattern_tracking

```sql
CREATE TABLE pattern_tracking (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,

    pattern_type VARCHAR(50) NOT NULL,
    pattern_data JSONB NOT NULL,
    confidence_score FLOAT,

    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Purpose:** Pattern analysis with confidence scores

---

## 🔗 **RELATIONSHIPS DIAGRAM**

```
users (1) ──────────┬───> (∞) conversations
                    ├───> (∞) tasks
                    ├───> (∞) projects
                    ├───> (∞) goals
                    ├───> (∞) backburner_items
                    ├───> (∞) checkins
                    ├───> (∞) metrics
                    ├───> (∞) work_sessions
                    ├───> (∞) calendar_events
                    ├───> (∞) wheel_categories
                    ├───> (∞) wheel_scores
                    ├───> (∞) pattern_observations
                    └───> (∞) pattern_tracking

pattern_categories (1) ───> (∞) pattern_observations

projects (1) ───> (∞) tasks
projects (1) ───> (∞) milestones

goals (1) ───> (∞) tasks

tasks (1) ───> (∞) work_sessions

conversations (1) ───> (∞) conversation_embeddings

wheel_categories (1) ───> (∞) wheel_scores
```

---

## ❌ **REMOVED FEATURES**

### Reminders Table - REMOVED February 2, 2026

The reminders feature was removed. All reminder-related code, models, and migrations have been deleted.

**Reason:** Feature wasn't working properly and will be re-implemented later.

**See:** `REMOVAL_SUMMARY.md` for complete details of what was removed.

---

## 🔧 **MIGRATIONS**

**Migration Tool:** Alembic
**Location:** `/backend/migrations/versions/`

**Current Migrations:**
- `001_initial_schema.py` - Base tables
- `002_add_missing_user_columns.py` - User JSONB columns
- `003_add_all_missing_tables.py` - All remaining tables

**CRITICAL:** Always read `MIGRATIONS_GUIDE.md` before creating new migrations!

**Run Migrations:**
```bash
cd backend
alembic upgrade head
```

**Create New Migration:**
```bash
alembic revision --autogenerate -m "Description"
```

**NEVER manually create migrations!** Always use `--autogenerate`.

---

## 🚨 **IMPORTANT NOTES**

### Cascade Deletes
- Deleting a user deletes ALL their data (CASCADE)
- Deleting a project sets task's `project_id` to NULL (SET NULL)
- Deleting a task sets work_session's `task_id` to NULL (SET NULL)

### Timezone Handling
- All timestamps stored with timezone awareness
- User's timezone in `users.timezone` for display conversion

### JSONB Columns
- `users.preferences` - User settings
- `users.adhd_profile` - ADHD type and profile data
- `conversations.context` - Context used for AI response
- `conversations.suggestions` - Suggested follow-up actions
- `checkins.responses` - Check-in question responses
- `checkins.insights` - AI-generated insights
- `goals.extra_data` - Flexible goal data
- `metrics.value` - Flexible metric values
- `pattern_tracking.pattern_data` - Pattern details

### Check Constraints
- All rating fields: 1-10 scale
- Goal progress: 0-100%
- Category and status fields have explicit allowed values

---

**Next:** Read `MIGRATIONS_GUIDE.md` before making database changes
**See Also:** `docs/PATTERN_LEARNING_SYSTEM.md` for pattern details
