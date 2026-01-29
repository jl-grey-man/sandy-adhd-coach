# ADHD Coach Project - Complete Context

**Last Updated:** 2025-01-26  
**Status:** Phase 1 - Initial Setup  
**Current Sprint:** Week 1 - Project Foundation

---

## QUICK START FOR AI ASSISTANTS

This is a comprehensive ADHD coaching system that learns and adapts to the user's specific patterns.

**Key Features:**
- Conversational AI coach (fine-tuned Llama 3.3 70B via Together.ai)
- Adaptive work management system (discovers what works through experimentation)
- Daily/weekly conversational check-ins
- ADHD-native project/task management
- Calendar integration (Google Calendar)
- Personalized Wheel of Life tracking
- Voice input (push-to-talk and toggle modes)
- Vector memory system (RAG via Pinecone)
- Monthly automated fine-tuning

**Tech Stack:**
- Frontend: React/Next.js (TypeScript, Tailwind CSS)
- Backend: Python FastAPI
- Databases: PostgreSQL (Supabase), Pinecone (vector DB)
- LLM: Together.ai API (fine-tuned Llama 3.3 70B)
- Hosting: Vercel (frontend), Railway (backend)
- Calendar: Google Calendar API

**Development Stage:** Setting up project structure and core architecture

---

## PROJECT VISION

An ADHD-native work and life management system that:

1. **Learns what works for YOU specifically** - No assumptions about rigid schedules or "productivity hacks"
2. **Provides proactive coaching** - Checks in, reminds, catches you before you struggle
3. **Adapts continuously** - Gets smarter every month through fine-tuning on your conversations
4. **Respects your brain** - Built around ADHD patterns, not against them

### Core Principles

- **No rigid time blocks** - Flexible windows, not "9:00 AM sharp"
- **Discovery over prescription** - Test approaches to find what works
- **Explicit tracking only (V1)** - No surveillance, user controls all data
- **Voice-first option** - Speak naturally, don't force typing
- **Context-aware** - AI remembers your patterns and references them

---

## SYSTEM ARCHITECTURE

### High-Level Flow

```
USER ←→ FRONTEND (React) ←→ BACKEND (FastAPI) ←→ LLM (Together.ai)
                                    ↓
                            DATABASES (PostgreSQL + Pinecone)
                                    ↓
                            EXTERNAL SERVICES (Calendar, Whisper)
```

### Data Flow

1. **User interacts** (text or voice)
2. **Frontend** sends to backend
3. **Backend**:
   - Retrieves user context (goals, patterns, recent history)
   - Searches vector DB for relevant past conversations (RAG)
   - Queries calendar for commitments
   - Builds complete context
4. **LLM** generates personalized response
5. **Backend** stores conversation, extracts insights
6. **Frontend** displays response

### Key Components

**Frontend:**
- Chat interface (text + voice input)
- Daily check-in forms
- Weekly conversational check-in
- Work planning dashboard
- Task/project management UI
- Wheel of Life visualization
- Calendar integration UI

**Backend:**
- User authentication
- Chat/conversation endpoints
- Check-in processing
- Work session management
- Task/project CRUD
- Calendar sync
- LLM integration
- Voice transcription (Whisper API)
- RAG system (Pinecone queries)
- Fine-tuning pipeline

**Databases:**
- PostgreSQL: Users, conversations, goals, tasks, projects, check-ins, wheel scores
- Pinecone: Conversation embeddings for semantic search

---

## V1 FEATURES (Must Have)

### User Management
- [ ] User registration/authentication
- [ ] User preferences (voice settings, notification preferences)
- [ ] Profile management

### Daily Interactions
- [ ] Morning check-in (energy, focus, mood ratings + priority declaration)
- [ ] Conversational AI chat (text + voice)
- [ ] Optional work timer/session tracking
- [ ] Mid-day check-ins (optional, user-triggered)
- [ ] End-of-day summary

### Weekly Check-ins
- [ ] Conversational weekly reflection
- [ ] Quick ratings (overall, energy, focus, mood, stress)
- [ ] Open questions with follow-ups
- [ ] AI-generated insights and patterns
- [ ] Next week planning

### Monthly Check-ins
- [ ] Deep dive reflection
- [ ] Wheel of Life updates
- [ ] Goal progress review
- [ ] Long-term pattern analysis

### Work Management
- [ ] Adaptive work planning (discovers optimal structure)
- [ ] Project management (ADHD-native)
- [ ] Task management (categorized by difficulty/energy/focus)
- [ ] Calendar integration (Google Calendar)
- [ ] Flexible time windows (not rigid blocks)
- [ ] Contextual task suggestions ("What should I do right now?")
- [ ] Task rotation support (when bored, switch)

### Wheel of Life
- [ ] Personalized categories (8-12, user-defined with AI help)
- [ ] Custom "what does 10/10 look like" definitions
- [ ] Visual radar chart
- [ ] Historical tracking
- [ ] AI insights based on changes

### Voice Input
- [ ] Push-to-talk for daily chat (hold button, speak at own pace)
- [ ] Toggle recording for check-ins (click record, speak, click stop)
- [ ] Audio transcription via Whisper API
- [ ] Audio storage for reference

### AI Memory System (RAG)
- [ ] Store all conversations in vector DB
- [ ] Semantic search for relevant context
- [ ] Automatic context retrieval during conversations
- [ ] Pattern detection across time

### Fine-Tuning Pipeline
- [ ] Automatic collection of high-quality interactions
- [ ] Monthly curation of training examples
- [ ] Automated fine-tuning trigger
- [ ] Model versioning and deployment

---

## V2 FEATURES (Future)

- [ ] Invisible/automatic tracking
- [ ] Mobile app (iOS/Android)
- [ ] Desktop app
- [ ] Team collaboration features
- [ ] Integration with other tools (Notion, Todoist, etc.)
- [ ] More calendar providers (Outlook, Apple Calendar)
- [ ] Habit tracking
- [ ] Medication reminders
- [ ] Mood/symptom journaling
- [ ] Progress reports/analytics
- [ ] Sharing/export features

---

## DATABASE SCHEMA

See `DATABASE-SCHEMA.md` for complete schema.

**Key Tables:**
- `users` - User accounts and preferences
- `conversations` - All chat messages and AI responses
- `goals` - Personal and work goals
- `tasks` - Individual tasks with ADHD metadata
- `projects` - Project containers
- `work_sessions` - Work time tracking
- `checkins` - Daily/weekly/monthly check-in data
- `wheel_categories` - User's custom Wheel of Life categories
- `wheel_scores` - Historical Wheel of Life ratings
- `calendar_events` - Synced calendar data
- `metrics` - Time-series data for pattern detection

---

## API ENDPOINTS

See `API-ENDPOINTS.md` for complete specifications.

**Main Endpoint Groups:**
- `/auth/*` - Authentication
- `/chat/*` - Conversational AI
- `/checkin/*` - Check-in flows
- `/tasks/*` - Task management
- `/projects/*` - Project management
- `/work/*` - Work session tracking
- `/wheel/*` - Wheel of Life
- `/calendar/*` - Calendar integration
- `/goals/*` - Goal management

---

## DEVELOPMENT WORKFLOW

### Planning (Claude Web - claude.ai)
- Architecture decisions
- Feature design
- Problem-solving
- Documentation
- Review and feedback

### Coding (Claude Code - Terminal)
- File creation/editing
- Implementation
- Testing
- Refactoring

### Communication Method
- **Claude Web → You:** I create/update files, you download
- **You → Claude Code:** You paste content, tell it to create files
- **You → Claude Web:** Upload files for review
- **Claude Code → Files:** Reads docs, implements specs

---

## IMPORTANT DESIGN DECISIONS

1. **No rigid time blocks** - User explicitly requested flexible windows
2. **No invisible tracking in V1** - All tracking explicit and user-controlled
3. **Calendar sync is V1** - Required for work planning
4. **Adaptive learning approach** - Don't assume what works, discover through experimentation
5. **Voice input is critical** - Push-to-talk for daily, toggle for check-ins
6. **File-based communication** - Web Claude and Terminal Claude share context via files
7. **Monthly fine-tuning** - Automated pipeline for continuous personalization

---

## CODING CONVENTIONS

### Python (Backend)
- Use FastAPI with async/await
- Type hints required for all functions
- Pydantic models for request/response validation
- Follow PEP 8 style guide
- Docstrings for all public functions
- Unit tests with pytest

### TypeScript/React (Frontend)
- Functional components only (no class components)
- TypeScript strict mode
- Custom hooks for reusable logic
- Tailwind CSS for styling
- Component composition over prop drilling
- Jest + React Testing Library for tests

### File Organization
- Group by feature, not by type
- Colocate related files
- Index files for clean imports

---

## CURRENT SPRINT GOALS

### Week 1 (Current - Jan 26-Feb 2)
- [x] Set up project folder structure
- [x] Configure development environment
- [x] Create core documentation files
- [ ] Initialize Git repository
- [ ] Set up GitHub repo (optional)
- [ ] Initialize backend (FastAPI project structure)
- [ ] Initialize frontend (Next.js with TypeScript)
- [ ] Set up local PostgreSQL database
- [ ] Set up Supabase account and project
- [ ] Set up Pinecone account and index
- [ ] Set up Together.ai account and API key
- [ ] Implement basic user authentication
- [ ] Create initial database schema
- [ ] Build basic chat interface (text only)

### Week 2 (Feb 2-9)
- [ ] Integrate Together.ai LLM
- [ ] Implement voice recording components
- [ ] Add Whisper API for transcription
- [ ] Build morning check-in flow
- [ ] Implement check-in data storage
- [ ] Create basic work planning interface

---

## BLOCKERS / QUESTIONS

None currently.

---

## NEXT STEPS

1. Initialize backend FastAPI project
2. Initialize frontend Next.js project
3. Set up database (local + Supabase)
4. Create basic authentication
5. Build simple chat interface
6. Test end-to-end flow

---

## USEFUL COMMANDS

```bash
# Navigate to project
adhd

# Start Claude Code (Anthropic API)
claude-api

# Start Claude Code (Local Ollama)
claude-ollama

# Backend development
cd backend
source venv/bin/activate
uvicorn app.main:app --reload

# Frontend development
cd frontend
npm run dev

# Run tests
pytest  # Backend
npm test  # Frontend

# Database migrations
alembic upgrade head
```

---

## CONTACTS & RESOURCES

- **Together.ai Docs:** https://docs.together.ai
- **Pinecone Docs:** https://docs.pinecone.io
- **Supabase Docs:** https://supabase.com/docs
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **Next.js Docs:** https://nextjs.org/docs

---

**Remember: The password for testing Claude Code connection is "Flugelhorn"**
