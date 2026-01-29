# RECENT UPDATES - Current System State

**Last Updated**: January 29, 2026  
**Status**: Production - All systems operational

---

## 📊 **CURRENT STATE SUMMARY**

### ✅ **What's Working**
- Web and Telegram chat interfaces
- Task/project/reminder management
- Pattern learning (18 categories, 90 subpatterns)
- Hypothesis formation with confidence scoring
- Context-aware AI responses
- Time intelligence (capacity analysis)
- Memory system (Pinecone)
- Spirit-over-script prompt system
- Hypothesis challenge behavior

### 🚀 **Recent Deployments**

#### January 29, 2026 - Spirit Over Script Rewrite (Commit: 4d6aa2f)
**What Changed**: Complete rewrite of all 27+ prompt examples
- Changed from prescriptive quotes to adaptive principles
- All examples now show APPROACH/SPIRIT instead of exact phrases
- Emphasizes natural variation, not memorization
- Sandy now embodies character vs. reciting script

**Impact**: Sandy should sound more natural, never repeat same phrases

#### January 29, 2026 - Pronoun Fix (Commit: 915b0fc)
**What Changed**: Fixed all category descriptions from "him/he" to "you"
- Updated ADVANCED_LEARNING_CATEGORIES.py
- Updated seed_pattern_categories.py
- Created admin endpoint to fix existing user data

**Impact**: /explore command now says "what gets YOU started" not "what gets HIM started"

#### January 29, 2026 - 90 Subpatterns Connected (Commit: cff14db)
**What Changed**: Connected all 90 subpatterns to learning system
- Created subpatterns.py with keyword-based detection
- Updated learning_extraction.py to detect specific subpatterns
- Updated pattern_learning.py to group by subpattern
- Now forms multiple hypotheses per category (one per subpattern)

**Impact**: More granular pattern detection (e.g., "external_deadline" vs. just "task_initiation")

#### January 29, 2026 - Hypothesis Challenge Behavior (Commit: cff14db)
**What Changed**: Sandy now presents patterns as theories, not facts
- Added "WORKING WITH HYPOTHESES" section to prompt
- Context.py presents patterns as "working hypotheses"
- Confidence-based language (50-70%: "might be", 95%+: "consistently")
- When challenged, Sandy gets curious, never defensive

**Impact**: Sandy invites correction, stays humble about patterns

---

## 🏗️ **SYSTEM ARCHITECTURE QUICK REF**

### Technology Stack
```
Frontend: React + TypeScript + Vite (Vercel)
Backend: FastAPI + Python (Railway)
Database: PostgreSQL (Railway)
AI: OpenAI GPT-4
Memory: Pinecone vector DB
Bot: Telegram integration
```

### Core Flow
```
User Message
  ↓
Backend API (FastAPI)
  ↓
Load Prompts (FULL.md + PART2.md)
  ↓
Build Context (tasks, patterns, time intelligence)
  ↓
Call OpenAI GPT-4
  ↓
Parse Response (text + actions)
  ↓
Execute Actions (create tasks/reminders)
  ↓
Extract Learnings (observations → hypotheses)
  ↓
Return Response to User
```

---

## 📋 **KEY FILES & LOCATIONS**

### Essential Documentation (Read These)
```
/README_ARCHITECTURE.md          ← START HERE
/DATABASE_SCHEMA.md              Complete DB structure
/backend/SANDY_SYSTEM_PROMPT_FULL.md    Sandy's personality (Part 1)
/backend/SANDY_SYSTEM_PROMPT_PART2.md   Actions & learning (Part 2)
```

### Core Backend Files
```
backend/app/main.py                     FastAPI app entry
backend/app/services/context.py         Context building for AI
backend/app/services/pattern_learning.py   Pattern hypothesis system
backend/app/services/learning_extraction.py   Extract observations
backend/app/services/subpatterns.py     90 subpattern definitions
```

### Recent Change Documentation
```
/PHASE_2_COMPLETE_SPIRIT_OVER_SCRIPT.md   Spirit-over-script details
/BUG_FIXES_HIM_TO_YOU.md                  Pronoun fix details
/DEPLOYMENT_COMPLETE.md                   Latest deployment summary
```

---

## 🗄️ **DATABASE QUICK REF**

### 8 Tables
1. **users** - User accounts, auth
2. **tasks** - Work items (pending/in_progress/completed/stuck)
3. **projects** - Multi-step work with deadlines
4. **reminders** - Time-based notifications
5. **pattern_categories** - 18 ADHD pattern types
6. **pattern_observations** - Individual observations from conversations
7. **pattern_hypotheses** - Formed patterns with confidence scores
8. **user_feedback** - User feedback on responses

### Key Relationships
- Users → Tasks/Projects/Reminders/Observations/Hypotheses
- Categories → Observations/Hypotheses
- Projects → Tasks

Full schema: See DATABASE_SCHEMA.md

---

## 🎭 **PROMPT SYSTEM QUICK REF**

### Two-Part System
**Part 1** (SANDY_SYSTEM_PROMPT_FULL.md):
- Personality, voice, rules
- Situation handling approaches
- Never hallucinate, acknowledge first, ground in reality
- Working with hypotheses (stay curious)

**Part 2** (SANDY_SYSTEM_PROMPT_PART2.md):
- Actions (tasks/reminders/projects)
- Exploration mode
- Memory & learning integration
- Conversational patterns

### Spirit Over Script Philosophy
- Examples show PRINCIPLES, not scripts to copy
- Sandy embodies character, doesn't recite lines
- Each response should be unique and natural
- Same personality, different words every time

---

## 🧠 **PATTERN LEARNING QUICK REF**

### The Flow
```
Conversation
  ↓
Extract observations (learning_extraction.py)
  ↓
Detect category + subpattern (subpatterns.py)
  ↓
Save to pattern_observations table
  ↓
If ≥3 observations for same subpattern
  ↓
Form hypothesis (pattern_learning.py)
  ↓
Calculate confidence score (0-100%)
  ↓
Save to pattern_hypotheses table
  ↓
Next conversation: Load hypotheses ≥50% confidence
  ↓
Present to Sandy as "working hypotheses"
```

### 18 Categories
task_initiation, hyperfocus, time_perception, urgency_response, avoidance, completion_triggers, emotional_regulation, accountability, novelty_seeking, transition_difficulty, working_memory, sensory_sensitivity, rejection_sensitivity, impulsivity, overthinking, energy_patterns, social_patterns, executive_dysfunction

### 90 Subpatterns
Examples:
- task_initiation: body_doubling, external_deadline, accountability, momentum, trigger, curiosity, spite
- avoidance: perfectionism, complexity, emotional_difficulty, uncertainty, low_reward, social_anxiety, past_failure

Full list: backend/app/services/subpatterns.py

---

## 🔌 **API QUICK REF**

### Base URL
```
Production: https://sandy-adhd-coach-production.up.railway.app
```

### Key Endpoints
```
POST /auth/signup        Create account
POST /auth/login         Get JWT token
POST /chat               Send message, get response
GET  /tasks              List tasks
POST /tasks              Create task
GET  /patterns           View pattern hypotheses
POST /telegram/webhook   Telegram bot webhook
POST /admin/fix-descriptions   Fix category descriptions (admin)
```

### Authentication
```
Headers: Authorization: Bearer {jwt_token}
```

---

## 🚀 **DEPLOYMENT QUICK REF**

### Deploy Process
```bash
git add .
git commit -m "Description"
git push origin main
# Railway and Vercel auto-deploy
```

### Environment Variables

**Backend (Railway)**:
```
DATABASE_URL=postgresql://...
OPENAI_API_KEY=sk-...
PINECONE_API_KEY=...
JWT_SECRET=...
TELEGRAM_BOT_TOKEN=...
```

**Frontend (Vercel)**:
```
VITE_API_URL=https://sandy-adhd-coach-production.up.railway.app
```

---

## 🎯 **WHAT'S NEXT / KNOWN ISSUES**

### Potential Improvements
- [ ] Time-aware greetings (Sandy doesn't know time of day yet)
- [ ] Vary /explore responses (currently static database text)
- [ ] Enhanced pattern visualization for user
- [ ] Export task/pattern data

### No Known Blocking Issues
All systems operational as of Jan 29, 2026

---

## 📚 **COMPLETE DOCUMENTATION INDEX**

**Start Here**:
1. README_ARCHITECTURE.md - Complete overview (you are here's parent)
2. DATABASE_SCHEMA.md - Database structure
3. This file (RECENT_UPDATES.md) - Current state

**Dive Deeper**:
- PHASE_2_COMPLETE_SPIRIT_OVER_SCRIPT.md - Spirit-over-script transformation
- BUG_FIXES_HIM_TO_YOU.md - Pronoun fix details
- DEPLOYMENT_COMPLETE.md - Latest deployment

**Code**:
- backend/SANDY_SYSTEM_PROMPT_FULL.md - Sandy's personality
- backend/SANDY_SYSTEM_PROMPT_PART2.md - Actions & features
- backend/app/services/context.py - Context building
- backend/app/services/pattern_learning.py - Learning system
- backend/app/services/subpatterns.py - 90 subpatterns

---

## ✅ **VERIFICATION**

After reading documentation, you should know:
- [x] What Sandy is and how it works
- [x] The dual-prompt system (FULL.md + PART2.md)
- [x] Pattern learning flow (observations → hypotheses)
- [x] 18 categories + 90 subpatterns
- [x] Spirit-over-script philosophy
- [x] Recent changes (hypothesis challenge, subpatterns, pronoun fix)
- [x] How to deploy changes
- [x] Database schema and relationships

**If yes to all** → You understand the system completely! 🎉

---

**Status**: ✅ Production Ready  
**Version**: Jan 29, 2026 (Spirit-over-script + 90 subpatterns + hypothesis challenge)  
**Deployment**: Railway + Vercel  
**Repository**: https://github.com/jl-grey-man/sandy-adhd-coach
