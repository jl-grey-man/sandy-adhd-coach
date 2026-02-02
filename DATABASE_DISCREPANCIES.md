# Database Schema Discrepancies Report

**Generated:** February 2, 2026
**Issue:** DATABASE_SCHEMA.md documentation does not match actual models

---

## ❌ TABLES IN DOCS BUT NOT IN CODE

### 1. `reminders` ❌ REMOVED
- **Status:** Documented but **feature was removed** (Feb 2, 2026)
- **Action Required:** Remove from DATABASE_SCHEMA.md

### 2. `pattern_hypotheses` ❌ NOT FOUND
- **Status:** Documented but model doesn't exist
- **Possible Reason:** Might be renamed to `pattern_tracking`?
- **Action Required:** Verify if `pattern_tracking` is the replacement

### 3. `user_feedback` ❌ NOT FOUND
- **Status:** Documented but model doesn't exist
- **Action Required:** Either implement or remove from docs

---

## ⚠️ TABLES IN CODE BUT NOT IN DOCS

### NEW TABLES (Not Documented):

1. **`backburner_items`** (BackburnerItem model)
   - Purpose: Unknown - needs documentation
   - Fields: Need to document

2. **`calendar_events`** (CalendarEvent model)
   - Purpose: Unknown - needs documentation
   - Fields: Need to document

3. **`checkins`** (Checkin model)
   - Purpose: Unknown - needs documentation
   - Fields: Need to document

4. **`conversations`** (Conversation model)
   - Purpose: Chat history storage (partially mentioned in docs)
   - Fields: Need full documentation

5. **`goals`** (Goal model)
   - Purpose: User goals (mentioned in relationships but no table def)
   - Fields: Need to document

6. **`metrics`** (Metric model)
   - Purpose: Unknown - needs documentation
   - Fields: Need to document

7. **`milestones`** (Milestone model)
   - Purpose: Project milestones (mentioned in relationships but no table def)
   - Fields: Need to document

8. **`pattern_tracking`** (PatternCategory model - DUPLICATE?)
   - Purpose: Might be replacement for pattern_hypotheses?
   - Fields: Need to verify and document
   - **WARNING:** Has same class name as pattern_category.py!

9. **`wheel_categories`** (WheelCategory model)
   - Purpose: Unknown - "Wheel of Life"?
   - Fields: Need to document

10. **`work_sessions`** (WorkSession model)
    - Purpose: Unknown - time tracking?
    - Fields: Need to document

---

## 🔍 DETAILED MODEL ANALYSIS NEEDED

Let me check each undocumented model's actual structure:
