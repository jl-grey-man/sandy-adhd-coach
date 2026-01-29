# SANDY ADHD COACH - ARCHITECTURE & DOCUMENTATION
**Master Documentation Entry Point**

---

## 📋 **HOW TO USE THIS DOCUMENTATION**

**For a new AI to understand this entire project**:

```
1. Read this file completely (README_ARCHITECTURE.md)
2. Read the files listed in "ESSENTIAL READING ORDER" below
3. Reference the other docs as needed for specific subsystems
```

After completing the essential reading, you should understand:
- ✅ What Sandy is and how it works
- ✅ The complete system architecture
- ✅ Database schema and data flow
- ✅ Prompt system and learning mechanisms
- ✅ APIs and deployment process
- ✅ Recent changes and current state

---

## 🏗️ **HIGH-LEVEL SYSTEM OVERVIEW**

### What is Sandy?

**Sandy** is an AI-powered ADHD accountability coach designed specifically for one user: Jens.

**Core Concept**: A personal assistant with personality who:
- Learns Jens's ADHD patterns through conversation
- Provides accountability without being a therapist
- Manages tasks, projects, and reminders
- Calls out procrastination with playful directness
- Uses pattern recognition to improve over time

**Personality**: Rachel Zane (Suits) + Joan Holloway (Mad Men)
- Direct but respectful
- Playful but professional
- No BS, no cheerleading
- "I've got your back" energy

### Technology Stack

```
Frontend:
├─ React (TypeScript)
├─ Vite build system
├─ Tailwind CSS
└─ Deployed: Vercel

Backend:
├─ FastAPI (Python)
├─ PostgreSQL database
├─ OpenAI GPT-4
├─ Pinecone vector DB (memory)
└─ Deployed: Railway

Integrations:
├─ Telegram bot
├─ Web interface
└─ Shared authentication & data
```

### System Architecture

```
User Input (Telegram/Web)
    ↓
Backend API (FastAPI)
    ↓
┌───────────────────────────────────────┐
│  Core Processing Pipeline             │
│  ├─ Load system prompts               │
│  ├─ Build context (tasks, patterns)   │
│  ├─ Call OpenAI GPT-4                 │
│  ├─ Parse actions (tasks, reminders)  │
│  ├─ Extract learning observations     │
│  └─ Update pattern hypotheses         │
└───────────────────────────────────────┘
    ↓
Database Storage (PostgreSQL)
    ├─ Tasks, projects, reminders
    ├─ Pattern observations
    ├─ Pattern hypotheses
    └─ User feedback
    ↓
Memory System (Pinecone)
    └─ Long-term conversation embeddings
```

---

## 📚 **ESSENTIAL READING ORDER**

Read these files in this order to understand the complete system:

### 1. **DATABASE_SCHEMA.md** (Read First)
**Why**: Understand the data model before anything else
**Contains**:
- Complete database schema
- Table relationships
- Key fields and their purposes
- Pattern learning tables

### 2. **PROMPT_SYSTEM.md** (Read Second)
**Why**: The prompts ARE Sandy's personality and behavior
**Contains**:
- How the dual-prompt system works
- Sandy's complete personality definition
- Response principles and examples
- Recent prompt updates (spirit-over-script)

### 3. **API_REFERENCE.md** (Read Third)
**Why**: Understand how the system processes requests
**Contains**:
- Core API endpoints
- Authentication flow
- Request/response formats
- Action parsing system

### 4. **PATTERN_LEARNING_SYSTEM.md** (Read Fourth)
**Why**: This is what makes Sandy learn and improve
**Contains**:
- 18 ADHD pattern categories
- 90 subpatterns and detection
- Observation → Hypothesis flow
- Confidence scoring system

### 5. **RECENT_UPDATES.md** (Read Last)
**Why**: Know what changed recently and current state
**Contains**:
- Latest deployments
- Recent bug fixes
- Current system state
- Known issues

---

## 🗂️ **COMPLETE FILE STRUCTURE**

### Repository Structure
```
sandy-adhd-coach/
├── backend/                          # Python FastAPI backend
│   ├── app/
│   │   ├── main.py                  # FastAPI app entry point
│   │   ├── models/                  # SQLAlchemy models
│   │   ├── routers/                 # API route handlers
│   │   ├── services/                # Business logic
│   │   │   ├── context.py          # Context building for AI
│   │   │   ├── pattern_learning.py # Pattern hypothesis system
│   │   │   ├── learning_extraction.py # Extract observations from convos
│   │   │   ├── subpatterns.py      # 90 subpattern definitions
│   │   │   └── feedback.py         # User feedback processing
│   │   └── config.py               # Configuration
│   ├── SANDY_SYSTEM_PROMPT_FULL.md # Main system prompt (Part 1)
│   ├── SANDY_SYSTEM_PROMPT_PART2.md # Actions & learning (Part 2)
│   └── requirements.txt            # Python dependencies
│
├── frontend/                        # React TypeScript frontend
│   ├── src/
│   │   ├── components/             # React components
│   │   ├── pages/                  # Page components
│   │   ├── services/               # API client
│   │   └── App.tsx                # Main app component
│   └── package.json               # Node dependencies
│
├── docs/                           # THIS DOCUMENTATION
│   ├── README_ARCHITECTURE.md     # ← YOU ARE HERE
│   ├── DATABASE_SCHEMA.md         # Database structure
│   ├── PROMPT_SYSTEM.md          # How prompts work
│   ├── API_REFERENCE.md          # API documentation
│   ├── PATTERN_LEARNING_SYSTEM.md # Learning mechanism
│   ├── DEPLOYMENT_GUIDE.md       # How to deploy
│   ├── DEVELOPMENT_GUIDE.md      # How to develop
│   └── RECENT_UPDATES.md         # Latest changes
│
└── migrations/                    # Database migrations
```

### Important Backend Files

**Core Application**:
- `app/main.py` - FastAPI app, routes, middleware
- `app/config.py` - Environment variables, settings
- `app/dependencies.py` - Dependency injection

**Models** (SQLAlchemy ORM):
- `app/models/user.py` - User model
- `app/models/task.py` - Task, Project, Reminder models
- `app/models/pattern.py` - PatternCategory, PatternObservation, PatternHypothesis

**Services** (Business Logic):
- `app/services/context.py` - Build context for AI (tasks, patterns, time intelligence)
- `app/services/pattern_learning.py` - Pattern hypothesis formation & storage
- `app/services/learning_extraction.py` - Extract observations after each conversation
- `app/services/subpatterns.py` - 90 subpattern definitions for granular detection
- `app/services/feedback.py` - Process user feedback on AI responses

**Routers** (API Endpoints):
- `app/routers/auth.py` - Authentication (login, signup)
- `app/routers/telegram.py` - Telegram webhook handler
- `app/routers/chat.py` - Web chat endpoint
- `app/routers/tasks.py` - Task CRUD operations
- `app/routers/patterns.py` - Pattern viewing endpoints
- `app/routers/admin.py` - Admin operations (fix DB, etc.)

**Prompts**:
- `SANDY_SYSTEM_PROMPT_FULL.md` - Sandy's personality, rules, examples (Part 1)
- `SANDY_SYSTEM_PROMPT_PART2.md` - Actions, learning, advanced behavior (Part 2)

---

## 🔑 **KEY CONCEPTS TO UNDERSTAND**

### 1. The Dual-Prompt System

Sandy uses TWO prompt files that are concatenated:

**SANDY_SYSTEM_PROMPT_FULL.md** (Part 1):
- Sandy's core personality and identity
- Communication style and voice
- Critical rules (never hallucinate, acknowledge first, ground in reality)
- Situation handling (procrastination, overwhelm, energy issues)
- Working with hypotheses (stay curious, not defensive)

**SANDY_SYSTEM_PROMPT_PART2.md** (Part 2):
- Action system (tasks, reminders, projects)
- Exploration mode
- Memory & learning integration
- Context awareness
- Tone calibration

**Why two files?**
- Part 1 is personality/behavior (changes less often)
- Part 2 is actions/features (changes more often)
- Easier to maintain and update separately

### 2. Pattern Learning System

**Flow**: Conversation → Observation → Hypothesis → Confidence

```
1. User has conversation with Sandy
2. After conversation ends:
   → learning_extraction.py extracts observations
   → Detects ADHD pattern categories (18 types)
   → Detects subpatterns (90 specific variants)
   → Saves to pattern_observations table
3. Pattern Learning Service checks observations:
   → Groups by category and subpattern
   → If ≥3 observations for a subpattern: form hypothesis
   → Calculate confidence score (0-100%)
   → Store in pattern_hypotheses table
4. Next conversation:
   → context.py loads confirmed patterns (≥50% confidence)
   → Presents as "working hypotheses" to Sandy
   → Sandy uses them naturally (not as facts)
```

**18 Pattern Categories**:
task_initiation, hyperfocus, time_perception, urgency_response, avoidance, completion_triggers, emotional_regulation, accountability, novelty_seeking, transition_difficulty, working_memory, sensory_sensitivity, rejection_sensitivity, impulsivity, overthinking, energy_patterns, social_patterns, executive_dysfunction

**90 Subpatterns**: Specific variants within each category
- Example: task_initiation has 7 subpatterns (body_doubling, external_deadline, accountability, momentum, trigger, curiosity, spite)

### 3. Context Building

Every AI request includes context built by `context.py`:

```python
Context includes:
- Current tasks (in-progress, stuck, completed)
- Projects (with deadlines and estimated hours)
- Time intelligence (capacity analysis, overload detection)
- Pattern hypotheses (confirmed patterns ≥50% confidence)
- Recent conversation history (from memory)
```

This context is invisible to the user but crucial for Sandy's awareness.

### 4. Action System

Sandy can create tasks/reminders/projects using JSON actions:

```python
# User says: "Remind me to call John in 30 minutes"
Sandy outputs:
```action
{"type": "create_reminder", "message": "Call John", "minutes_from_now": 30}
```

Backend parses these actions and creates database records.

**Action Types**:
- `create_task` - Work items with optional priority, energy_level, project
- `create_reminder` - Time-based notifications (not work items)
- `create_project` - Multi-step work with deadlines and hour estimates

### 5. Memory System (Pinecone)

**Two-tier memory**:

**Short-term** (context window):
- Last 10-20 messages in current session
- Managed by FastAPI in-memory

**Long-term** (Pinecone vector DB):
- All past conversations as embeddings
- Retrieved via semantic search when relevant
- Adds continuity across sessions

### 6. Spirit Over Script Philosophy

**Recent critical change** (Jan 29, 2026):

All prompt examples reformatted from SCRIPTS to PRINCIPLES:

**OLD**:
```
✅ RIGHT: "What's stopping you?"
✅ RIGHT: "When specifically?"
```

**NEW**:
```
RIGHT APPROACH: Pin down timing
SPIRIT: Don't let vague "later" slide
EXPRESS NATURALLY: Ask when specifically (in your own words)
```

**Goal**: Sandy embodies character and responds naturally, never repeating memorized phrases.

---

## 🗄️ **DATABASE SCHEMA OVERVIEW**

**Core Tables**:

```sql
users
├─ id, email, password_hash, created_at

tasks
├─ id, user_id, title, status, priority, energy_level
├─ project_id (FK), created_at, completed_at, stuck_since

projects  
├─ id, user_id, title, deadline, estimated_hours, status

reminders
├─ id, user_id, message, remind_at, sent

pattern_categories
├─ id, name, description, priority_score

pattern_observations
├─ id, user_id, category_id, observation, sub_pattern
├─ observed_at, context

pattern_hypotheses
├─ id, user_id, category_id, hypothesis_text
├─ confidence_score, observation_count, sub_pattern
├─ last_updated
```

**Key Relationships**:
- Tasks → Projects (many-to-one)
- Observations → Categories (many-to-one)
- Hypotheses → Categories (many-to-one)

Full details in `DATABASE_SCHEMA.md`

---

## 🔌 **API OVERVIEW**

**Base URL**: `https://sandy-adhd-coach-production.up.railway.app`

**Key Endpoints**:

```
Authentication:
POST /auth/signup - Create user account
POST /auth/login  - Get JWT token

Chat:
POST /chat - Send message, get Sandy response
  Headers: Authorization: Bearer {token}
  Body: {"message": "your message"}
  Returns: {"response": "...", "actions": [...]}

Tasks:
GET    /tasks        - List all tasks
POST   /tasks        - Create task
PATCH  /tasks/{id}   - Update task
DELETE /tasks/{id}   - Delete task

Patterns:
GET /patterns        - View pattern hypotheses
POST /patterns/feedback - Give feedback on pattern

Telegram:
POST /telegram/webhook - Telegram bot webhook
```

Full details in `API_REFERENCE.md`

---

## 🚀 **DEPLOYMENT OVERVIEW**

**Frontend** (Vercel):
- Auto-deploys from main branch
- Environment: VITE_API_URL

**Backend** (Railway):
- Auto-deploys from main branch
- Environment: DATABASE_URL, OPENAI_API_KEY, PINECONE_API_KEY, JWT_SECRET

**Database** (Railway PostgreSQL):
- Managed by Railway
- Migrations via Alembic

**To deploy a change**:
```bash
git add .
git commit -m "Description"
git push origin main
# Railway and Vercel auto-deploy
```

Full details in `DEPLOYMENT_GUIDE.md`

---

## 🛠️ **DEVELOPMENT WORKFLOW**

**Local Development**:

```bash
# Backend
cd backend
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload

# Frontend
cd frontend
npm install
npm run dev
```

**Environment Variables**:
```
# Backend (.env)
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
JWT_SECRET=...
TELEGRAM_BOT_TOKEN=...

# Frontend (.env)
VITE_API_URL=http://localhost:8000
```

Full details in `DEVELOPMENT_GUIDE.md`

---

## 📊 **CURRENT SYSTEM STATE**

**Version**: Production (as of Jan 29, 2026)

**Key Features Working**:
- ✅ Web and Telegram chat
- ✅ Task/project/reminder management
- ✅ Pattern learning (18 categories, 90 subpatterns)
- ✅ Hypothesis formation with confidence scoring
- ✅ Context-aware responses
- ✅ Time intelligence (capacity analysis)
- ✅ Memory system (Pinecone)
- ✅ Spirit-over-script prompt system

**Recent Major Changes**:
1. **Hypothesis challenge behavior** (Jan 29)
   - Sandy presents patterns as theories, not facts
   - Invites correction, stays curious
   
2. **90 subpatterns connected** (Jan 29)
   - Granular pattern detection (e.g., "external_deadline" vs. just "task_initiation")
   
3. **Spirit-over-script rewrite** (Jan 29)
   - All prompt examples reformatted from scripts to principles
   - Emphasizes natural variation, not memorization

4. **Pronoun fix** (Jan 29)
   - Changed all "him/he" to "you" in category descriptions

**Known Issues**: None currently

Full details in `RECENT_UPDATES.md`

---

## 🎯 **CRITICAL FILES FOR AI UNDERSTANDING**

If you only read a few files, read these:

1. **README_ARCHITECTURE.md** (this file)
   - Complete system overview

2. **DATABASE_SCHEMA.md**
   - Data model and relationships

3. **PROMPT_SYSTEM.md**
   - How Sandy's personality works

4. **PATTERN_LEARNING_SYSTEM.md**
   - How Sandy learns and improves

5. **backend/app/services/context.py**
   - How context is built for each AI request

6. **backend/SANDY_SYSTEM_PROMPT_FULL.md**
   - Sandy's actual personality prompt (Part 1)

7. **backend/SANDY_SYSTEM_PROMPT_PART2.md**
   - Sandy's actions and learning prompt (Part 2)

---

## 📖 **ADDITIONAL DOCUMENTATION**

### Detailed Subsystem Docs

**`DEPLOYMENT_GUIDE.md`**:
- Railway deployment
- Vercel deployment
- Environment setup
- Database migrations

**`DEVELOPMENT_GUIDE.md`**:
- Local setup
- Testing procedures
- Code organization
- Contributing guidelines

**`API_REFERENCE.md`**:
- Complete endpoint documentation
- Request/response examples
- Authentication flow
- Error handling

### Historical Documentation

**`IMPLEMENTATION_COMPLETE.md`**:
- Original implementation notes
- Feature additions over time

**`PHASE_2_COMPLETE_SPIRIT_OVER_SCRIPT.md`**:
- Spirit-over-script rewrite details
- Before/after comparisons

**`BUG_FIXES_HIM_TO_YOU.md`**:
- Pronoun fix documentation

---

## 🧠 **HOW SANDY WORKS - COMPLETE FLOW**

**User sends message** (Telegram or Web)
    ↓
**Backend receives request** (`/chat` or `/telegram/webhook`)
    ↓
**Load system prompts** (FULL.md + PART2.md)
    ↓
**Build context** (`context.py`):
    ├─ Load tasks, projects (in-progress, stuck)
    ├─ Load pattern hypotheses (≥50% confidence)
    ├─ Load recent conversation from memory (Pinecone)
    ├─ Calculate time intelligence (capacity, overload)
    └─ Format as structured prompt
    ↓
**Call OpenAI GPT-4**:
    ├─ System prompt (personality + actions)
    ├─ Context (tasks + patterns + history)
    └─ User message
    ↓
**Parse response**:
    ├─ Extract text response for user
    ├─ Parse ```action blocks (tasks/reminders/projects)
    └─ Extract learning observations (`learning_extraction.py`)
    ↓
**Execute actions**:
    ├─ Create tasks/reminders in database
    └─ Return confirmation to user
    ↓
**Process learning** (after conversation):
    ├─ Detect pattern categories (18 types)
    ├─ Detect subpatterns (90 variants)
    ├─ Save observations to database
    ├─ Update hypotheses if ≥3 observations
    └─ Calculate confidence scores
    ↓
**Store conversation** (Pinecone):
    ├─ Create embedding of conversation
    └─ Store for future retrieval
    ↓
**Return response to user**

---

## 🔧 **COMMON OPERATIONS**

### Update Sandy's Personality
1. Edit `backend/SANDY_SYSTEM_PROMPT_FULL.md`
2. Commit and push to main
3. Railway auto-deploys

### Add New Feature
1. Update relevant service in `backend/app/services/`
2. Update prompt if needed
3. Test locally
4. Deploy via git push

### View Pattern Hypotheses
```bash
curl -X GET https://sandy-adhd-coach-production.up.railway.app/patterns \
  -H "Authorization: Bearer {token}"
```

### Run Database Migration
```bash
cd backend
alembic revision --autogenerate -m "Description"
alembic upgrade head
git add alembic/
git commit -m "Migration: Description"
git push
```

---

## 🎓 **UNDERSTANDING SANDY'S LEARNING**

**Example Learning Flow**:

```
Day 1:
User: "I need to call the accountant but the deadline is tomorrow"
→ Observation: task_initiation + external_deadline subpattern
→ Saved to database

Day 2:
User: "I should start the proposal. Client needs it by Friday"
→ Observation: task_initiation + external_deadline subpattern
→ Saved to database

Day 3:
User: "Got to finish the report, boss wants it today"
→ Observation: task_initiation + external_deadline subpattern
→ Saved to database
→ Pattern Learning Service detects ≥3 observations
→ Forms hypothesis: "External deadline pressure (3 observations, 30% confidence)"

Day 7: (10 total observations)
→ Hypothesis updated: "External deadline pressure (10 observations, 77% confidence)"

Next conversation:
→ context.py loads hypothesis (≥50% confidence)
→ Sandy sees: "Pattern: task_initiation / external_deadline / 77% confidence"
→ Sandy naturally applies: "Deadline's tomorrow? Want to knock it out now while pressure's on?"
```

---

## 🚨 **CRITICAL SAFETY RULES**

**Sandy NEVER**:
- Hallucinates information (only references actual data)
- Ignores what user just said (always acknowledges first)
- Makes assumptions (asks when uncertain)
- Repeats exact phrases (varies naturally)
- Acts as therapist (stays practical)

**Sandy ALWAYS**:
- Grounds responses in data
- Presents patterns as theories (not facts)
- Invites user correction
- Treats user as capable
- Keeps responses brief (1-3 sentences)

---

## 📞 **GETTING HELP**

### For Code Questions:
- Read relevant service file in `backend/app/services/`
- Check `API_REFERENCE.md` for endpoint details
- Review `DATABASE_SCHEMA.md` for data structure

### For Behavior Questions:
- Read `PROMPT_SYSTEM.md`
- Check actual prompts in `backend/SANDY_SYSTEM_PROMPT_*.md`
- Review `PATTERN_LEARNING_SYSTEM.md`

### For Deployment Questions:
- Read `DEPLOYMENT_GUIDE.md`
- Check Railway dashboard for logs
- Review `RECENT_UPDATES.md` for latest changes

---

## ✅ **VERIFICATION CHECKLIST**

After reading this documentation, you should be able to answer:

- [ ] What is Sandy and what does it do?
- [ ] What are the 18 pattern categories?
- [ ] How does the observation → hypothesis flow work?
- [ ] What's the difference between FULL.md and PART2.md?
- [ ] How does context get built for each AI request?
- [ ] What's the "spirit over script" philosophy?
- [ ] Where is the database hosted?
- [ ] How do you deploy a change?
- [ ] What's the action system and how does it work?
- [ ] Where are pattern hypotheses stored?

If yes to all → You understand the system! 🎉

---

## 🎯 **FINAL NOTES**

This is a **living system** that learns and improves over time.

**The core philosophy**:
- Sandy is not a generic AI chatbot
- She's a specific character built for one person
- She learns through interaction
- She embodies principles, not scripts
- She respects the user and calls out BS

**Key success metrics**:
- User actually uses it daily
- Conversations feel natural
- Sandy's suggestions improve over time
- User completes more tasks
- ADHD patterns become visible

**Remember**: The goal isn't perfect AI. The goal is a useful, personality-filled accountability partner who genuinely helps Jens get shit done.

---

## 🛠️ **KEEPING IT CURRENT**

**This documentation should stay current as the system evolves.**

### When You Make Major Changes

Update these files in this order:

1. **Update RECENT_UPDATES.md** (most important - current state)
   - Add what changed, when, and why
   - Update "Current State Summary"
   - Note new deployments

2. **Update README_ARCHITECTURE.md** only if architecture changes
   - Database changes (new tables, relationships)
   - Technology stack changes (new services, APIs)
   - Major architectural shifts

3. **Update DATABASE_SCHEMA.md** only if database schema changes
   - New tables or columns
   - Changed relationships
   - New indexes or constraints

### Quick Update Checklist

After deploying a major change, ask yourself:
- [ ] What changed? → Add to RECENT_UPDATES.md
- [ ] Did the architecture change? → Update README_ARCHITECTURE.md if needed
- [ ] Did the database schema change? → Update DATABASE_SCHEMA.md if needed

**That's it!** The system stays current.

Most updates only require updating RECENT_UPDATES.md.

---

**Documentation Version**: 1.0 (January 29, 2026)
**Last Updated**: After spirit-over-script rewrite and 90-subpattern implementation
**Maintainer**: Jens Lennartsson
**Repository**: https://github.com/jl-grey-man/sandy-adhd-coach

---

## 📚 **NEXT: READ THESE FILES IN ORDER**

1. ✅ You just finished: `README_ARCHITECTURE.md` (this file)
2. ➡️  Read next: `DATABASE_SCHEMA.md`
3. Then: `PROMPT_SYSTEM.md`
4. Then: `API_REFERENCE.md`
5. Then: `PATTERN_LEARNING_SYSTEM.md`
6. Finally: `RECENT_UPDATES.md`

**After completing all essential reading**, you'll have complete understanding of the Sandy ADHD Coach system.

Good luck! 🚀
