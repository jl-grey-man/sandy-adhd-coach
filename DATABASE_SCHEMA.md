# DATABASE SCHEMA - Complete Reference

**Complete database structure for Sandy ADHD Coach**

---

## 📊 **DATABASE OVERVIEW**

**Database Type**: PostgreSQL  
**Hosted**: Railway  
**ORM**: SQLAlchemy  
**Migrations**: Alembic

---

## 📋 **ALL TABLES**

### Core Tables
1. **users** - User accounts
2. **tasks** - Work items to complete
3. **projects** - Multi-step work with deadlines
4. **reminders** - Time-based notifications

### Learning Tables
5. **pattern_categories** - 18 ADHD pattern types
6. **pattern_observations** - Individual observations extracted from conversations
7. **pattern_hypotheses** - Formed patterns with confidence scores

### Feedback Table
8. **user_feedback** - Feedback on AI responses

---

## 🗄️ **DETAILED TABLE SCHEMAS**

### 1. users

```sql
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    full_name VARCHAR(255),
    timezone VARCHAR(50) DEFAULT 'Europe/Stockholm',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP,
    telegram_chat_id BIGINT UNIQUE
);
```

**Purpose**: Store user accounts and authentication  
**Key Fields**:
- `email` - Login identifier (unique)
- `password_hash` - Bcrypt hashed password
- `telegram_chat_id` - Links to Telegram account (optional, unique)
- `timezone` - User's timezone for time-aware features

**Relationships**:
- One user → Many tasks
- One user → Many projects
- One user → Many reminders
- One user → Many observations
- One user → Many hypotheses

---

### 2. tasks

```sql
CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    project_id INTEGER REFERENCES projects(id) ON DELETE SET NULL,
    
    title VARCHAR(500) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'pending',
    priority VARCHAR(50),
    energy_level VARCHAR(50),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    stuck_since TIMESTAMP,
    
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_project FOREIGN KEY (project_id) REFERENCES projects(id)
);
```

**Purpose**: Store actionable work items  
**Key Fields**:
- `title` - Task description
- `status` - 'pending', 'in_progress', 'completed', 'stuck'
- `priority` - 'low', 'medium', 'high' (only if user specifies)
- `energy_level` - 'low', 'medium', 'high' (only if user specifies)
- `project_id` - Optional link to parent project
- `stuck_since` - Auto-set when task stuck >7 days

**Status Values**:
- `pending` - Not started
- `in_progress` - Currently working on
- `completed` - Done
- `stuck` - User avoiding / blocked

**Stuck Detection**: 
- Task automatically marked `stuck` if `status='in_progress'` and no update for 7+ days
- Used by context.py to surface problematic tasks

---

### 3. projects

```sql
CREATE TABLE projects (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    title VARCHAR(500) NOT NULL,
    description TEXT,
    status VARCHAR(50) DEFAULT 'active',
    
    deadline DATE,
    estimated_hours DECIMAL(10, 2),
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP,
    
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Purpose**: Multi-step work with deadlines and time estimates  
**Key Fields**:
- `title` - Project name
- `deadline` - Target completion date (used for capacity analysis)
- `estimated_hours` - Time required (used for overload detection)
- `status` - 'active', 'completed', 'on_hold'

**Relationships**:
- One project → Many tasks
- Used by time intelligence to calculate workload

---

### 4. reminders

```sql
CREATE TABLE reminders (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    message VARCHAR(500) NOT NULL,
    remind_at TIMESTAMP NOT NULL,
    sent BOOLEAN DEFAULT FALSE,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Purpose**: Time-based notifications (NOT work items)  
**Key Fields**:
- `message` - Reminder text
- `remind_at` - When to send notification
- `sent` - Has been delivered

**Note**: Reminders are for life maintenance ("drink water", "take break"), NOT actionable work

---

### 5. pattern_categories

```sql
CREATE TABLE pattern_categories (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) UNIQUE NOT NULL,
    description TEXT,
    priority_score INTEGER DEFAULT 50,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

**Purpose**: Define the 18 ADHD pattern types  
**Key Fields**:
- `name` - Category identifier (e.g., 'task_initiation', 'hyperfocus')
- `description` - Human-readable explanation shown to user
- `priority_score` - Determines exploration order (higher = more important)

**The 18 Categories**:
1. `task_initiation` - What gets you started on tasks
2. `hyperfocus` - What puts you in the zone
3. `time_perception` - How you experience time
4. `urgency_response` - How deadlines affect you
5. `avoidance` - Why you avoid certain tasks
6. `completion_triggers` - What helps you finish
7. `emotional_regulation` - How you handle emotions
8. `accountability` - What external accountability works
9. `novelty_seeking` - New vs. routine tasks
10. `transition_difficulty` - Switching between activities
11. `working_memory` - How you handle mental load
12. `sensory_sensitivity` - Environmental factors
13. `rejection_sensitivity` - Social feedback impact
14. `impulsivity` - Impulse control patterns
15. `overthinking` - Analysis paralysis triggers
16. `energy_patterns` - When you have energy
17. `social_patterns` - Social interaction preferences
18. `executive_dysfunction` - Planning/organizing challenges

**Seeded at Signup**: These 18 categories are automatically created when user signs up

---

### 6. pattern_observations

```sql
CREATE TABLE pattern_observations (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES pattern_categories(id),
    
    observation TEXT NOT NULL,
    sub_pattern VARCHAR(255),
    context TEXT,
    
    observed_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES pattern_categories(id)
);
```

**Purpose**: Store individual observations extracted from conversations  
**Key Fields**:
- `observation` - What was observed (e.g., "Created task when deadline mentioned")
- `sub_pattern` - Specific variant (e.g., 'external_deadline', 'body_doubling')
- `context` - Additional context from conversation
- `observed_at` - When observation made

**90 Subpatterns**: See PATTERN_LEARNING_SYSTEM.md for complete list

**Created By**: `learning_extraction.py` after each conversation

**Example Flow**:
```
User: "I need to finish this report. The deadline is tomorrow"
→ learning_extraction.py detects:
   - category: task_initiation
   - sub_pattern: external_deadline
   - observation: "Created task when external deadline mentioned"
→ Saved to pattern_observations
```

---

### 7. pattern_hypotheses

```sql
CREATE TABLE pattern_hypotheses (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    category_id INTEGER NOT NULL REFERENCES pattern_categories(id),
    
    hypothesis_text TEXT NOT NULL,
    sub_pattern VARCHAR(255),
    confidence_score INTEGER DEFAULT 0,
    observation_count INTEGER DEFAULT 0,
    
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id),
    CONSTRAINT fk_category FOREIGN KEY (category_id) REFERENCES pattern_categories(id),
    UNIQUE(user_id, category_id, sub_pattern)
);
```

**Purpose**: Store formed pattern hypotheses with confidence scores  
**Key Fields**:
- `hypothesis_text` - Human-readable pattern description
- `sub_pattern` - Specific variant this hypothesis covers
- `confidence_score` - 0-100% based on observation count
- `observation_count` - Number of supporting observations
- `last_updated` - Last time hypothesis updated

**Unique Constraint**: One hypothesis per (user, category, subpattern) combination

**Confidence Calculation**:
```python
# Simplified version
if observation_count >= 10:
    confidence = 95
elif observation_count >= 7:
    confidence = 85
elif observation_count >= 5:
    confidence = 70
elif observation_count >= 3:
    confidence = 50
else:
    confidence = observation_count * 10  # 1=10%, 2=20%
```

**Formation Trigger**: ≥3 observations for same (category, subpattern)

**Example**:
```sql
hypothesis_text: "External deadline pressure"
sub_pattern: "external_deadline"
confidence_score: 77
observation_count: 10
```

**Used By**: `context.py` loads hypotheses with confidence ≥50% and presents to Sandy

---

### 8. user_feedback

```sql
CREATE TABLE user_feedback (
    id SERIAL PRIMARY KEY,
    user_id INTEGER NOT NULL REFERENCES users(id) ON DELETE CASCADE,
    
    feedback_type VARCHAR(50) NOT NULL,
    feedback_text TEXT,
    rating INTEGER,
    
    context_data JSONB,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users(id)
);
```

**Purpose**: Store user feedback on AI responses and system behavior  
**Key Fields**:
- `feedback_type` - Type of feedback (e.g., 'response_quality', 'pattern_accuracy')
- `feedback_text` - Free-form feedback
- `rating` - Numerical rating if applicable
- `context_data` - JSON with additional context (conversation ID, pattern ID, etc.)

**Used For**: Improving Sandy's responses over time

---

## 🔗 **RELATIONSHIPS DIAGRAM**

```
users (1) ──────────┬───> (∞) tasks
                    ├───> (∞) projects
                    ├───> (∞) reminders
                    ├───> (∞) pattern_observations
                    ├───> (∞) pattern_hypotheses
                    └───> (∞) user_feedback

pattern_categories (1) ──┬───> (∞) pattern_observations
                         └───> (∞) pattern_hypotheses

projects (1) ────────> (∞) tasks
```

---

## 🔍 **KEY QUERIES**

### Get Stuck Tasks
```sql
SELECT * FROM tasks 
WHERE user_id = ? 
  AND status IN ('stuck', 'in_progress')
  AND created_at < NOW() - INTERVAL '7 days'
ORDER BY created_at ASC;
```

### Get Pattern Hypotheses (≥50% confidence)
```sql
SELECT 
    pc.name as category_name,
    ph.hypothesis_text,
    ph.sub_pattern,
    ph.confidence_score,
    ph.observation_count
FROM pattern_hypotheses ph
JOIN pattern_categories pc ON ph.category_id = pc.id
WHERE ph.user_id = ?
  AND ph.confidence_score >= 50
ORDER BY ph.confidence_score DESC;
```

### Get Time Intelligence Data
```sql
-- Get total estimated hours
SELECT SUM(estimated_hours) as total_hours
FROM projects
WHERE user_id = ?
  AND status = 'active'
  AND deadline BETWEEN NOW() AND NOW() + INTERVAL '30 days';

-- Get task count by status
SELECT status, COUNT(*) as count
FROM tasks
WHERE user_id = ?
GROUP BY status;
```

---

## 🔧 **MIGRATIONS**

**Migration Tool**: Alembic

**Location**: `/backend/alembic/versions/`

**Run Migration**:
```bash
cd backend
alembic upgrade head
```

**Create New Migration**:
```bash
alembic revision --autogenerate -m "Description"
```

---

## 🚨 **IMPORTANT NOTES**

### Pattern Learning Tables
- `pattern_observations` can grow large (one per conversation)
- `pattern_hypotheses` stays small (max 18 categories × ~5 subpatterns per user = ~90 rows)

### Cascade Deletes
- Deleting a user deletes ALL their data (CASCADE)
- Deleting a project sets task's `project_id` to NULL (SET NULL)
- Deleting a category does NOT cascade (categories shouldn't be deleted)

### Timezone Handling
- All timestamps stored in UTC
- User's timezone in `users.timezone` for display conversion

### Stuck Detection
- Tasks auto-marked stuck after 7 days in 'in_progress' without update
- Used by context.py to surface problems
- Trigger runs periodically (can be cron job)

---

**Next**: Read `PROMPT_SYSTEM.md` to understand how Sandy's personality works
