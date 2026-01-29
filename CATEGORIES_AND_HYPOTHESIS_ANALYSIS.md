# 📊 CATEGORIES & SUBCATEGORIES ANALYSIS

**Date:** January 29, 2026, 20:15 GMT+1

---

## Question 1: Are All Categories and Subcategories in Database?

### ✅ Main Categories: 18 (ALL in database)

1. task_initiation
2. hyperfocus_triggers  
3. avoidance_reasons
4. context_switching_cost
5. energy_curves
6. motivation_sources
7. reward_sensitivity
8. decision_fatigue
9. accountability_effectiveness
10. task_breakdown_needs
11. interruption_recovery
12. momentum_building
13. failure_response
14. novelty_seeking
15. sensory_environment
16. communication_response
17. time_perception
18. urgency_response

### 📝 Subcategories: 90 Defined in Code

**Breakdown per category:**

| Category | Subpatterns |
|----------|-------------|
| task_initiation | 7 (body doubling, deadline pressure, accountability, etc.) |
| hyperfocus_triggers | 5 (creative tasks, time pressure, novelty, etc.) |
| avoidance_reasons | 7 (unclear goals, too many steps, boring, etc.) |
| context_switching_cost | 4 (needs transition, loses momentum, etc.) |
| energy_curves | 5 (social effect, creative boost, admin drain, etc.) |
| motivation_sources | 6 (validation, progress, competition, etc.) |
| reward_sensitivity | 6 (immediate, long-term, social, etc.) |
| decision_fatigue | 5 (too many options, high stakes, etc.) |
| accountability_effectiveness | 6 (hard deadlines, check-ins, etc.) |
| task_breakdown_needs | 4 (overwhelmed by large, needs steps, etc.) |
| interruption_recovery | 4 (quick recovery, loses session, etc.) |
| momentum_building | 4 (small wins, warm-up, etc.) |
| failure_response | 4 (catastrophizes, bounces back, etc.) |
| novelty_seeking | 4 (bores quickly, thrives on routine, etc.) |
| sensory_environment | 5 (music, silence, clean space, etc.) |
| communication_response | 6 (direct push, gentle, playful, etc.) |
| time_perception | 4 (optimistic, pessimistic, accurate, etc.) |
| urgency_response | 4 (thrives under pressure, freezes, etc.) |

**Total: 90 subpatterns**

---

## Database Schema Status

### ✅ GOOD NEWS: Schema Already Supports Subcategories!

```sql
-- pattern_observations table
sub_pattern VARCHAR(100)  -- ✅ Field exists!

-- pattern_hypotheses table  
sub_pattern VARCHAR(100)  -- ✅ Field exists!
```

### ⚠️ CURRENT ISSUE: Not Being Used

**Problem:** 
- Schema has `sub_pattern` field ✅
- Code doesn't populate it ❌
- Learning extraction doesn't specify which subpattern ❌

**Example:**

Current (vague):
```python
learner.add_observation(
    category_name='task_initiation',
    observation="Created task when discussing X"
)
# sub_pattern = None
```

Should be (specific):
```python
learner.add_observation(
    category_name='task_initiation',
    sub_pattern='external_deadline_pressure',  # ← Specify which!
    observation="Created task when discussing deadline"
)
```

---

## Fix Needed: Connect Subcategories

### What to Update:

**File: `app/services/learning_extraction.py`**

Add subpattern detection:

```python
def extract_and_save_learnings(...):
    # Current: Only saves category
    learner.add_observation(
        category_name='task_initiation',
        observation="..."
    )
    
    # Should: Detect and save specific subpattern
    if 'deadline' in user_lower:
        learner.add_observation(
            category_name='task_initiation',
            sub_pattern='external_deadline_pressure',
            observation="..."
        )
    elif 'call' in user_lower or 'zoom' in user_lower:
        learner.add_observation(
            category_name='task_initiation',
            sub_pattern='body_doubling',
            observation="..."
        )
```

---

## Question 2: Hypothesis Challenge Behavior

### Current Behavior ❌ (Too Confident)

**In `context.py` - Lines 155-165:**
```python
if confirmed:
    learned_section = "WHAT YOU KNOW ABOUT JENS:\n"
    for p in confirmed[:15]:
        learned_section += f"• {p['hypothesis']}\n"
```

**Problem:** Presents hypotheses as FACTS, not guesses!

### What Sandy Should Do ✅ (Open & Curious)

**Principle:** Every hypothesis is a WORKING THEORY to be tested, not gospel truth.

**Examples:**

❌ **WRONG (Treating as Fact):**
```
Sandy: "You work best in mornings. Let's tackle the hard stuff now."
[Assumes pattern is correct]
```

✅ **RIGHT (Open & Curious):**
```
Sandy: "I think you might work best in mornings - I've seen you tackle 
hard tasks then 3 times. Is that actually true for you?"
[Invites challenge/correction]
```

❌ **WRONG:**
```
Sandy: "You avoid research tasks. Here's a creative one instead."
[Assumes avoidance is permanent]
```

✅ **RIGHT:**
```
Sandy: "You've deflected on research tasks twice. What's making 
those hard? Or am I reading this wrong?"
[Explores the pattern, allows correction]
```

---

## Fix: Add Hypothesis Challenge to System Prompt

### Update `SANDY_SYSTEM_PROMPT_FULL.md`:

Add new section:

```markdown
═══════════════════════════════════════════════════════════════════
WORKING WITH HYPOTHESES
═══════════════════════════════════════════════════════════════════

YOUR HYPOTHESES ARE GUESSES, NOT FACTS.

When you have a learned pattern (even 80%+ confidence):
- Present it as a working theory
- Invite challenge or correction
- Stay curious about exceptions
- Ask if the pattern feels accurate

EXAMPLES:

❌ WRONG (Too Confident):
"You work best in mornings, so let's do the hard stuff now."

✅ RIGHT (Open & Curious):
"I think you might work best in mornings - seen that pattern 3 times. 
Ring true?"

❌ WRONG:
"You avoid research tasks."

✅ RIGHT:
"You've deflected on research stuff twice. What makes those hard, 
or am I misreading?"

CONFIDENCE LEVELS:

50-70% = "I might be noticing..."
70-85% = "I think I'm seeing a pattern..."
85-95% = "This seems to be a pattern..."
95%+ = "This consistently happens..."

ALWAYS leave room for:
- You being wrong
- Pattern changing
- Situational factors
- Him knowing himself better

If he challenges a hypothesis:
✓ "Oh interesting, tell me more"
✓ "Good to know - updating that"
✓ "What's different about this case?"

NEVER:
✗ "But I've observed..."
✗ "The data shows..."
✗ Defend the hypothesis
```

---

## Implementation Plan

### Priority 1: Add Hypothesis Challenge Behavior ⚡ CRITICAL

**Why Critical:** Sandy treating patterns as facts reduces trust

**Files to Update:**
1. `SANDY_SYSTEM_PROMPT_FULL.md` - Add section above
2. `app/services/context.py` - Change how patterns are presented

**In context.py:**
```python
# BEFORE (too confident):
learned_section = "WHAT YOU KNOW ABOUT JENS:\n"
for p in confirmed:
    learned_section += f"• {p['hypothesis']}\n"

# AFTER (open & curious):
learned_section = "WORKING HYPOTHESES ABOUT JENS (Stay curious, invite challenge):\n"
for p in confirmed:
    confidence_phrase = get_confidence_phrase(p['confidence'])
    learned_section += f"• {confidence_phrase}: {p['hypothesis']}\n"
    learned_section += f"  (Based on {p['supporting_observations']} observations)\n"

def get_confidence_phrase(confidence):
    if confidence < 70: return "Maybe noticing"
    elif confidence < 85: return "Think I'm seeing"
    elif confidence < 95: return "Pattern seems to be"
    else: return "Consistently happens"
```

---

### Priority 2: Connect Subcategories ⚡ IMPORTANT

**Why Important:** Granular learning → better insights

**Files to Update:**
1. `app/services/learning_extraction.py` - Add subpattern detection
2. `ADVANCED_LEARNING_CATEGORIES.py` - Make patterns machine-readable

**Benefits:**
- "Avoids research tasks" → "Avoids tasks: unclear goals" (specific!)
- "Works best mornings" → "Works best mornings: after coffee" (detailed!)
- "Responds to push" → "Responds to: playful teasing" (actionable!)

---

### Priority 3: Pattern Challenge Tracking 📊 NICE-TO-HAVE

**Track when user challenges a hypothesis:**

```python
class PatternChallenge(Base):
    """User challenged/corrected a hypothesis"""
    hypothesis_id = Column(Integer, ForeignKey("pattern_hypotheses.id"))
    challenge_text = Column(Text)  # What user said
    action_taken = Column(String)  # 'invalidated', 'refined', 'noted_exception'
    challenged_at = Column(DateTime)
```

**Use to:**
- Lower confidence when challenged
- Mark hypothesis as "needs_refinement"
- Learn from corrections

---

## Summary

### Current State:
✅ 18 main categories in database  
✅ 90 subpatterns defined in code  
✅ Schema supports subcategories (`sub_pattern` field)  
❌ Subcategories not being saved  
❌ Hypotheses presented as facts (not open/curious)  

### Quick Wins:
1. **Add hypothesis challenge section to prompt** (15 min)
2. **Update context.py to present patterns as theories** (15 min)
3. **Test Sandy's curiosity** (5 min)

### Bigger Task:
4. **Connect subcategory detection to learning extraction** (2 hours)

---

**Want me to implement the hypothesis challenge behavior now? That's the most critical piece for Sandy's trustworthiness.**

