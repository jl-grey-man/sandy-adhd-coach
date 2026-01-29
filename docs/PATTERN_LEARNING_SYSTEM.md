# PATTERN LEARNING SYSTEM - Quick Reference

**For complete implementation, read the code files:**

1. **`backend/app/services/pattern_learning.py`**
   - Pattern hypothesis formation
   - Confidence scoring
   - Observation aggregation

2. **`backend/app/services/subpatterns.py`**
   - All 90 subpattern definitions
   - Keyword detection logic

3. **`backend/app/services/learning_extraction.py`**
   - Extracts observations from conversations
   - Detects categories and subpatterns

---

## Quick Overview

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

### 18 Pattern Categories
1. task_initiation
2. hyperfocus
3. time_perception
4. urgency_response
5. avoidance
6. completion_triggers
7. emotional_regulation
8. accountability
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

### 90 Subpatterns
Each category has 3-7 specific subpatterns.

**Example** (task_initiation has 7):
- body_doubling: Working while on call
- external_deadline: Deadline pressure
- accountability: Someone waiting
- momentum: Small win triggers action
- trigger: After specific event (coffee, walk)
- curiosity: Novelty-driven
- spite: Proving something

**See complete list**: `backend/app/services/subpatterns.py`

### Confidence Scoring
```python
3 observations  = 50% confidence
5 observations  = 70% confidence
7 observations  = 85% confidence
10+ observations = 95% confidence
```

---

**READ THE CODE** for complete implementation details:
- `backend/app/services/pattern_learning.py`
- `backend/app/services/subpatterns.py`
- `backend/app/services/learning_extraction.py`
