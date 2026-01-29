# SANDY - COMPLETE SYSTEM ARCHITECTURE (Updated Jan 29, 2026)

## ✅ What's Actually Implemented

### 1. **COMPREHENSIVE SYSTEM PROMPT** ✅
Location: `SANDY_SYSTEM_PROMPT_FULL.md` + `SANDY_SYSTEM_PROMPT_PART2.md`

**How it works:**
- Both .md files are loaded at startup by `ai.py`
- Combined into single comprehensive prompt (658 lines total)
- Can be edited and Sandy will use changes on next restart

**Contains:**
- Core identity & personality (Rachel Zane + Joan Holloway)
- Communication style with natural variation rules
- Critical rules (never hallucinate, always acknowledge, ground in reality)
- Situation handling guide (procrastination, struggle, overload, etc.)
- Response examples (good vs bad) for every scenario
- Question strategy (when to ask, when not to)
- Actions & task management rules
- Exploration mode guidelines
- Multi-turn conversation examples
- Tone calibration by context

---

### 2. **PATTERN LEARNING SYSTEM** 🧠 (Fixed & Working)
Location: `app/services/pattern_learning.py`

**Database Tables:**
- `pattern_categories` - 18 main ADHD pattern areas (task_initiation, hyperfocus, etc.)
- `pattern_observations` - Individual learnings from conversations
- `pattern_hypotheses` - Formed patterns with confidence scores

**How Learning Works:**

```
User Message
     ↓
[AI Response Generated]
     ↓
[learning_extraction.py] ← Analyzes conversation:
     ├─ Detects avoidance phrases ("later", "maybe")
     ├─ Identifies energy indicators ("tired", "pumped")
     ├─ Tracks time mentions
     ├─ Records completion patterns
     └─ Detects motivation triggers
     ↓
[PatternLearningService.add_observation()] ← Saves to database
     ↓
[Hypothesis Formation] ← After 3-5 observations:
     ├─ Analyzes patterns
     ├─ Calculates confidence (0-100%)
     └─ Stores hypothesis
     ↓
[Next Response] ← Sandy uses high-confidence patterns (80%+)
```

**What Gets Learned:**
- Task initiation triggers (what makes you start)
- Avoidance patterns (deflection phrases, resistance)
- Energy patterns (when high/low energy occurs)
- Time perception (estimation accuracy)
- Communication responses (what tone works)
- Motivation sources (deadlines, accountability, etc.)
- Hyperfocus triggers (what creates flow)

**Confidence Scoring:**
- New observation: Start at 50%
- More observations: Confidence increases
- High confidence (80%+): Used prominently in responses
- Low confidence (<50%): Triggers exploration mode

---

### 3. **REAL-TIME LEARNING** 🔄 (Now Working!)
Location: `app/services/learning_extraction.py`

**Learning Loop:**

```
1. User sends message (Web or Telegram)
   ↓
2. Sandy responds  
   ↓
3. [extract_and_save_learnings()] analyzes:
   - User's exact words
   - Sandy's approach
   - Any actions taken
   - Emotional indicators
   ↓
4. Observations saved to database IMMEDIATELY
   ↓
5. Hypotheses formed after enough observations
   ↓
6. Next response uses updated knowledge
```

**Applied to:**
- ✅ Web chat (`app/routers/chat.py`)
- ✅ Telegram bot (`app/services/telegram_service.py`)
- ✅ Every single conversation

---

### 4. **FEEDBACK SYSTEM** 💬 (New Feature!)
Location: `app/services/feedback.py`

**You can tell Sandy how to improve!**

Examples:
```
You: "Sandy, be more direct with me"
Sandy: "Got it, adjusting my tone!" [Saves as high-confidence observation]

You: "Remember I work best in mornings"
Sandy: "Noted! I'll remember that." [Saves to energy_patterns]

You: "Stop asking so many questions"
Sandy: "Understood, I'll adapt my style!" [Saves to communication_style]

You: "I prefer when you're playful and tease me"
Sandy: "Got it!" [Updates tone preferences]
```

**How it works:**
- Detects feedback triggers ("Sandy,", "remember", "be more/less", etc.)
- Saves as HIGH confidence observation (85%+)
- Sandy applies it immediately in future responses
- You can correct her anytime

---

### 5. **EXPLORATION MODE** 🔍
Location: `app/services/exploration.py`

**Commands:**
- `/explore` - Let Sandy pick what to learn
- `/explore [category]` - Explore specific area
- `/patterns` - See what Sandy knows (80%+ confidence)

**How it works:**

```
User: "/explore"
     ↓
[ExplorationService.pick_next_category()]
     ├─ Finds area with <3 observations
     ├─ Or lowest confidence category
     └─ Returns targeted questions
     ↓
Sandy asks natural questions
     ↓
User answers normally
     ↓
[record_exploration_session()]
     ├─ Saves each insight as observation
     ├─ Increases hypothesis confidence +15%
     └─ Clears "needs exploration" flag at 70%+
```

**18 Pattern Categories:**
1. task_initiation
2. hyperfocus
3. time_perception
4. urgency_response
5. avoidance_reasons
6. completion_triggers
7. emotional_regulation
8. accountability_response
9. novelty_seeking
10. transition_difficulty
11. working_memory
12. sensory_sensitivity
13. rejection_sensitivity
14. impulsivity
15. overthinking
16. energy_patterns
17. social_patterns
18. executive_dysfunction

---

### 6. **MEMORY INTEGRATION** 🧠
Location: `app/services/memory.py` (Pinecone)

**How Memory Works:**

```
Conversation happens
     ↓
[Saved to PostgreSQL] ← Short-term storage
     ↓
[Saved to Pinecone] ← Long-term vector memory
     ↓
Future conversation starts
     ↓
[Pinecone search] ← Finds relevant past conversations
     ↓
[Context injected] ← Added to Sandy's prompt
     ↓
Sandy references past naturally
```

**Memory Scope:**
- Works across Web and Telegram
- Shared session ID: `user_{user_id}_global`
- No 2-hour time limit (fixed!)
- Searches semantically (meaning, not keywords)

---

### 7. **CONTEXT BUILDING** 📊
Location: `app/services/context.py`

**What Sandy Knows Each Response:**

```python
context = {
    'tasks': [...],           # Current tasks
    'projects': [...],        # Active projects
    'capacity_analysis': {    # Workload vs availability
        'available_hours': 56,
        'required_hours': 180
    },
    'learned_patterns': [     # High-confidence patterns
        {
            'category': 'task_initiation',
            'hypothesis': 'Starts tasks after accountability check',
            'confidence': 85
        }
    ],
    'exploration_status': [...] # What needs learning
}
```

---

## The Complete Flow

### Example: User Says "I should email the accountant"

**Behind the scenes:**

1. **Feedback Detection**
   - Not feedback (no trigger words)
   - Continue normally

2. **Context Builder** retrieves:
   - Task mentioned 3 times this week (from conversations)
   - User responds well to direct push (learned pattern 82%)
   - Morning time = high productivity (learned pattern 78%)

3. **Memory Search** (Pinecone):
   - Finds: "User mentioned accountant fear twice before"
   - Finds: "User completed tasks when given direct push"

4. **Prompt Injection**:
   ```
   LEARNED PATTERNS:
   - Responds well to playful directness (82%)
   - Mentions tasks 2-3 times before doing (78%)
   - Morning productivity is high (75%)
   
   CONTEXT:
   - Mentioned "email accountant" 3 times this week
   - No other urgent deadlines
   ```

5. **Sandy Responds:**
   "You've mentioned the accountant three times this week. What's actually stopping you?"

6. **User:** "I don't know what to say"

7. **Learning Extraction** analyzes:
   - Avoidance detected: "I don't know"
   - Block identified: Uncertainty about content
   - Energy level: Normal (no indicators)

8. **Observations Saved:**
   ```python
   [
       {
           'category': 'avoidance_reasons',
           'observation': 'Uses "I don\'t know" when discussing tasks',
           'confidence': 50
       },
       {
           'category': 'task_initiation',
           'observation': 'Blocked by uncertainty about task content',
           'confidence': 50
       }
   ]
   ```

9. **Next Interaction** will use these new observations!

---

## Why This Makes Sandy Actually Intelligent

### Traditional AI:
- Same responses for everyone
- No memory of what works
- Generic advice
- Doesn't improve over time

### Sandy:
- Remembers YOUR patterns ✅
- Learns what works WITH YOU specifically ✅
- Adapts approach based on observations ✅
- Accepts feedback and changes ✅
- Gets better every single day ✅

---

## Implementation Status

### ✅ Fully Working:
- System prompt loading from .md files
- Pattern learning system
- Real-time observation extraction
- Memory integration (Pinecone)
- Exploration mode
- Feedback system
- Web chat integration
- Telegram bot integration
- Context building
- Hypothesis formation

### ⚠️ Needs More Data:
- Pattern confidence (need conversations)
- Hypothesis refinement (need observations)
- Outcome tracking (future enhancement)

### 🔨 Future Enhancements:
- Outcome success tracking (what approaches actually worked)
- Pattern subcategories (more granular learning)
- Multi-user comparison (anonymized pattern insights)
- Adaptive question generation
- Predictive task suggestions

---

## Key Innovation

**Most AI assistants are STATELESS:**
- No memory between conversations
- No learning from outcomes
- Same behavior for everyone

**Sandy is STATEFUL & ADAPTIVE:**
- Remembers everything ✅
- Learns from every interaction ✅
- Adapts to YOUR specific patterns ✅
- You can give her feedback and she changes ✅
- Becomes YOUR personal Sandy ✅

**Result:** An assistant that actually gets better at serving YOU specifically, not just responding well in general.

---

## Files Overview

**System Prompt:**
- `SANDY_SYSTEM_PROMPT_FULL.md` - Core personality & rules (337 lines)
- `SANDY_SYSTEM_PROMPT_PART2.md` - Actions, learning, examples (321 lines)

**Core Services:**
- `app/services/ai.py` - Loads prompts, builds responses
- `app/services/pattern_learning.py` - Main learning engine
- `app/services/learning_extraction.py` - Extract insights from conversations
- `app/services/feedback.py` - Handle user feedback to Sandy
- `app/services/exploration.py` - Exploration mode management
- `app/services/context.py` - Build context for each response
- `app/services/memory.py` - Pinecone long-term memory

**Interfaces:**
- `app/routers/chat.py` - Web chat endpoint
- `app/services/telegram_service.py` - Telegram bot

**Database Models:**
- `app/models/pattern_tracking.py` - PatternCategory, PatternObservation, PatternHypothesis

---

## How to Give Sandy Feedback

Just talk to her naturally:

- **"Sandy, be more direct"** → She adjusts tone
- **"Remember I work best in mornings"** → Saved to patterns
- **"Stop asking so many questions"** → Changes style
- **"I prefer when you tease me"** → Updates personality
- **"Don't forget I hate long lists"** → Communication preference saved

She'll acknowledge and adapt immediately!

---

**Total:** 1,500+ lines of specifications + working implementation for making Sandy genuinely intelligent and adaptive.
