# Database Schema

**Last Updated:** 2025-01-26  
**Database:** PostgreSQL (Supabase for production, local for development)

---

## Overview

The database is designed to support:
- User management and authentication
- Conversational AI interactions
- Work and task management
- Check-in tracking (daily, weekly, monthly)
- Personalized Wheel of Life
- Calendar integration
- Pattern detection and metrics

---

## Schema Diagram

```
users
  ├── conversations (1:many)
  ├── goals (1:many)
  ├── projects (1:many)
  │     └── tasks (1:many)
  ├── work_sessions (1:many)
  ├── checkins (1:many)
  ├── wheel_categories (1:many)
  │     └── wheel_scores (1:many)
  ├── calendar_events (1:many)
  └── metrics (1:many)
```

---

## Tables

### **users**

Core user account information.

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100),
    timezone VARCHAR(50) DEFAULT 'UTC',
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    -- Preferences (stored as JSONB for flexibility)
    preferences JSONB DEFAULT '{
        "voice_enabled": true,
        "notification_enabled": true,
        "checkin_times": {
            "morning": "09:00",
            "evening": "20:00"
        }
    }'::jsonb
);

CREATE INDEX idx_users_email ON users(email);
```

---

### **conversations**

Stores all chat interactions between user and AI.

```sql
CREATE TABLE conversations (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    
    -- Message content
    user_message TEXT NOT NULL,
    ai_response TEXT NOT NULL,
    
    -- Input method
    input_type VARCHAR(20) CHECK (input_type IN ('text', 'voice')),
    audio_url VARCHAR(500),  -- If voice, link to stored audio file
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    
    -- Metadata for context and analysis
    metadata JSONB DEFAULT '{}'::jsonb
    -- Example metadata:
    -- {
    --   "mood": "positive",
    --   "energy_level": 7,
    --   "topics": ["work", "focus"],
    --   "intervention_type": "reminder",
    --   "user_feedback": "helpful"
    -- }
);

CREATE INDEX idx_conversations_user ON conversations(user_id);
CREATE INDEX idx_conversations_created ON conversations(created_at DESC);
CREATE INDEX idx_conversations_metadata ON conversations USING gin(metadata);
```

---

### **goals**

User's personal and work goals.

```sql
CREATE TABLE goals (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    
    -- Goal details
    category VARCHAR(50) CHECK (category IN ('personal', 'work')),
    title VARCHAR(200) NOT NULL,
    description TEXT,
    
    -- Timeline
    target_date DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    
    -- Status
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'completed', 'paused', 'abandoned')),
    progress INT DEFAULT 0 CHECK (progress >= 0 AND progress <= 100),
    
    -- Metadata
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_goals_user ON goals(user_id);
CREATE INDEX idx_goals_status ON goals(status);
```

---

### **projects**

Work projects container.

```sql
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    
    -- Project details
    name VARCHAR(200) NOT NULL,
    description TEXT,
    
    -- Status and priority
    status VARCHAR(20) DEFAULT 'active' CHECK (status IN ('active', 'on_hold', 'completed', 'someday')),
    priority VARCHAR(20) CHECK (priority IN ('urgent', 'high', 'medium', 'low', 'someday')),
    
    -- Timeline
    deadline DATE,
    created_at TIMESTAMP DEFAULT NOW(),
    completed_at TIMESTAMP,
    
    -- ADHD-specific metadata
    energy_level VARCHAR(20) CHECK (energy_level IN ('mixed', 'high_energy', 'low_energy')),
    
    -- Additional metadata
    metadata JSONB DEFAULT '{}'::jsonb
);

CREATE INDEX idx_projects_user ON projects(user_id);
CREATE INDEX idx_projects_status ON projects(status);
```

---

### **tasks**

Individual tasks with ADHD-specific metadata.

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    project_id INT REFERENCES projects(id) ON DELETE CASCADE,
    parent_task_id INT REFERENCES tasks(id) ON DELETE CASCADE,  -- For subtasks
    
    -- Task details
    title VARCHAR(200) NOT NULL,
    description TEXT,
    
    -- ADHD-specific categorization
    difficulty VARCHAR(20) CHECK (difficulty IN ('easy', 'medium', 'hard', 'very_hard')),
    energy_needed VARCHAR(20) CHECK (energy_needed IN ('low', 'medium', 'high')),
    focus_needed VARCHAR(20) CHECK (focus_needed IN ('low', 'medium', 'high')),
    task_type VARCHAR(50) CHECK (task_type IN ('creative', 'mechanical', 'admin', 'communication', 'planning')),
    
    -- Time estimation
    estimated_time_minutes INT,
    actual_time_minutes INT,
    
    -- Context for when to do it
    best_time_of_day VARCHAR(20) CHECK (best_time_of_day IN ('morning', 'midday', 'afternoon', 'evening', 'anytime')),
    best_energy_state VARCHAR(20) CHECK (best_energy_state IN ('high', 'medium', 'low', 'any')),
    requires_strategy VARCHAR(100),  -- e.g., 'body_doubling', 'timer', 'breaks'
    
    -- Status
    status VARCHAR(20) DEFAULT 'next' CHECK (status IN ('next', 'active', 'waiting', 'someday', 'completed', 'cancelled')),
    
    -- Timeline
    deadline DATE,
    completed_at TIMESTAMP,
    
    -- Breakdown support
    can_break_down BOOLEAN DEFAULT true,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_tasks_user ON tasks(user_id);
CREATE INDEX idx_tasks_project ON tasks(project_id);
CREATE INDEX idx_tasks_status ON tasks(status);
CREATE INDEX idx_tasks_difficulty ON tasks(difficulty);
CREATE INDEX idx_tasks_energy ON tasks(energy_needed);
```

---

### **work_sessions**

Tracks actual work time (when user uses timer or reports).

```sql
CREATE TABLE work_sessions (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    task_id INT REFERENCES tasks(id) ON DELETE SET NULL,
    
    -- Session timing
    started_at TIMESTAMP NOT NULL,
    ended_at TIMESTAMP,
    duration_minutes INT,
    
    -- Context at start
    energy_at_start INT CHECK (energy_at_start >= 1 AND energy_at_start <= 10),
    focus_at_start INT CHECK (focus_at_start >= 1 AND focus_at_start <= 10),
    strategy_used VARCHAR(100),  -- What strategy helped
    
    -- Outcome
    completed BOOLEAN DEFAULT false,
    switched_task BOOLEAN DEFAULT false,
    reason_for_switching TEXT,
    effectiveness_rating INT CHECK (effectiveness_rating >= 1 AND effectiveness_rating <= 10)
);

CREATE INDEX idx_work_sessions_user ON work_sessions(user_id);
CREATE INDEX idx_work_sessions_task ON work_sessions(task_id);
CREATE INDEX idx_work_sessions_started ON work_sessions(started_at DESC);
```

---

### **checkins**

Daily, weekly, and monthly check-in data.

```sql
CREATE TABLE checkins (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    
    -- Check-in type
    type VARCHAR(20) CHECK (type IN ('daily', 'weekly', 'monthly')),
    
    -- Ratings (1-10 scale, nullable for daily if not applicable)
    overall_rating INT CHECK (overall_rating >= 1 AND overall_rating <= 10),
    energy_rating INT CHECK (energy_rating >= 1 AND energy_rating <= 10),
    focus_rating INT CHECK (focus_rating >= 1 AND focus_rating <= 10),
    mood_rating INT CHECK (mood_rating >= 1 AND mood_rating <= 10),
    stress_rating INT CHECK (stress_rating >= 1 AND stress_rating <= 10),
    
    -- Conversational responses (JSONB array of Q&A)
    responses JSONB DEFAULT '[]'::jsonb,
    -- Example:
    -- [
    --   {"question": "What were your wins?", "answer": "...", "audio_url": "..."},
    --   {"question": "What challenges?", "answer": "...", "audio_url": "..."}
    -- ]
    
    -- AI analysis and insights
    ai_analysis TEXT,
    insights JSONB DEFAULT '{}'::jsonb,
    -- Example:
    -- {
    --   "patterns": ["sleep affects energy", "body doubling works"],
    --   "wins": ["finished proposal", "exercised 3x"],
    --   "challenges": ["Monday struggles", "late scrolling"],
    --   "recommendations": ["phone bedtime mode", "meds by coffee"]
    -- }
    
    -- Timestamp
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_checkins_user ON checkins(user_id);
CREATE INDEX idx_checkins_type ON checkins(type);
CREATE INDEX idx_checkins_created ON checkins(created_at DESC);
```

---

### **wheel_categories**

User's custom Wheel of Life categories.

```sql
CREATE TABLE wheel_categories (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    
    -- Category details
    name VARCHAR(100) NOT NULL,
    description TEXT,
    definition_of_10 TEXT,  -- What does 10/10 look like for this category
    
    -- Display order
    display_order INT,
    
    -- Timestamps
    created_at TIMESTAMP DEFAULT NOW(),
    updated_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id, name)
);

CREATE INDEX idx_wheel_categories_user ON wheel_categories(user_id);
```

---

### **wheel_scores**

Historical Wheel of Life ratings.

```sql
CREATE TABLE wheel_scores (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    category_id INT REFERENCES wheel_categories(id) ON DELETE CASCADE,
    
    -- Score
    score INT NOT NULL CHECK (score >= 0 AND score <= 10),
    
    -- Optional notes
    notes TEXT,
    
    -- Timestamp
    recorded_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_wheel_scores_user ON wheel_scores(user_id);
CREATE INDEX idx_wheel_scores_category ON wheel_scores(category_id);
CREATE INDEX idx_wheel_scores_recorded ON wheel_scores(recorded_at DESC);
```

---

### **calendar_events**

Synced calendar data (from Google Calendar, etc.).

```sql
CREATE TABLE calendar_events (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    
    -- Event details
    external_id VARCHAR(255),  -- ID from calendar provider
    title VARCHAR(200),
    description TEXT,
    location VARCHAR(200),
    
    -- Timing
    start_time TIMESTAMP NOT NULL,
    end_time TIMESTAMP NOT NULL,
    all_day BOOLEAN DEFAULT false,
    
    -- Source
    calendar_source VARCHAR(50) DEFAULT 'google',  -- 'google', 'outlook', etc.
    
    -- Sync metadata
    synced_at TIMESTAMP DEFAULT NOW(),
    
    UNIQUE(user_id, external_id, calendar_source)
);

CREATE INDEX idx_calendar_events_user ON calendar_events(user_id);
CREATE INDEX idx_calendar_events_time ON calendar_events(start_time, end_time);
```

---

### **metrics**

Time-series data for pattern detection and analytics.

```sql
CREATE TABLE metrics (
    id SERIAL PRIMARY KEY,
    user_id INT REFERENCES users(id) ON DELETE CASCADE,
    
    -- Metric type
    metric_type VARCHAR(50) NOT NULL,
    -- Examples: 'mood', 'focus', 'energy', 'medication_taken', 'exercise', 'sleep_quality'
    
    -- Value (flexible structure)
    value JSONB NOT NULL,
    -- Examples:
    -- {"rating": 7}
    -- {"taken": true, "time": "08:30"}
    -- {"duration": 45, "type": "cardio"}
    
    -- Timestamp
    recorded_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_metrics_user ON metrics(user_id);
CREATE INDEX idx_metrics_type ON metrics(metric_type);
CREATE INDEX idx_metrics_recorded ON metrics(recorded_at DESC);
CREATE INDEX idx_metrics_value ON metrics USING gin(value);
```

---

### **conversation_embeddings**

Reference to vector embeddings stored in Pinecone.

```sql
CREATE TABLE conversation_embeddings (
    id SERIAL PRIMARY KEY,
    conversation_id INT REFERENCES conversations(id) ON DELETE CASCADE,
    
    -- Pinecone reference
    pinecone_id VARCHAR(100) NOT NULL UNIQUE,
    
    -- Timestamp
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_embeddings_conversation ON conversation_embeddings(conversation_id);
CREATE INDEX idx_embeddings_pinecone ON conversation_embeddings(pinecone_id);
```

---

## Views (Optional Helper Queries)

### **active_tasks_view**

Quick view of tasks ready to work on.

```sql
CREATE VIEW active_tasks_view AS
SELECT 
    t.*,
    p.name as project_name,
    p.priority as project_priority
FROM tasks t
LEFT JOIN projects p ON t.project_id = p.id
WHERE t.status IN ('next', 'active')
ORDER BY 
    CASE t.status 
        WHEN 'active' THEN 1
        WHEN 'next' THEN 2
    END,
    p.priority DESC;
```

---

### **recent_checkins_view**

Latest check-in data for quick access.

```sql
CREATE VIEW recent_checkins_view AS
SELECT 
    user_id,
    type,
    overall_rating,
    energy_rating,
    focus_rating,
    mood_rating,
    stress_rating,
    created_at,
    ROW_NUMBER() OVER (PARTITION BY user_id, type ORDER BY created_at DESC) as recency
FROM checkins;
```

---

## Migrations Strategy

Using Alembic for database migrations:

```bash
# Create migration
alembic revision --autogenerate -m "description"

# Apply migration
alembic upgrade head

# Rollback
alembic downgrade -1
```

---

## Seed Data (Development)

For testing, seed with:
- 1 test user
- Sample goals
- Sample projects with tasks
- Sample check-ins
- Sample Wheel of Life categories

---

## Performance Considerations

**Indexes:**
- All foreign keys are indexed
- Timestamp fields for filtering are indexed
- JSONB fields use GIN indexes for querying

**Partitioning (Future):**
- Consider partitioning `conversations` by month if grows large
- Consider partitioning `metrics` by month

**Archiving (Future):**
- Archive conversations older than 2 years
- Keep aggregated metrics indefinitely

---

## Backup Strategy

- Daily automated backups via Supabase
- Keep 30 days of point-in-time recovery
- Monthly full backups stored separately
