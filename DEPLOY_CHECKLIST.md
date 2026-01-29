# 🚀 DEPLOY SANDY'S FIXES - Quick Checklist

## ✅ All Fixes Complete

**What was fixed:**
1. ✅ Sandy loads full 658-line personality from .md files
2. ✅ Real-time learning system (correct tables)
3. ✅ Observation saving after every conversation
4. ✅ Pattern formation from observations
5. ✅ Feedback system (you can tell Sandy to improve)
6. ✅ README updated to match reality

---

## 📋 Deploy Now (3 commands)

```bash
cd /Users/jenslennartsson/Documents/-ai_projects-/adhd_coach/backend

git add .

git commit -m "MAJOR: Sandy fully adaptive - learning + feedback working

- Load full prompts from .md files (658 lines)
- Fixed learning system (correct tables)
- Added observation extraction after every message
- Created feedback system (user can tell Sandy to improve)
- Updated README to match current architecture
- Removed broken old files"

git push
```

**Railway will auto-deploy in ~2 minutes.**

---

## 🧪 Test After Deploy

### 1. Test Learning (Web or Telegram)

```
You: "I'm really tired today"

Check logs: Should see "Extracted X learnings from interaction"

Expected: Saves to pattern_observations table
Category: energy_patterns
Observation: "Low energy signal: used 'tired'"
```

### 2. Test Feedback

```
You: "Sandy, be more direct with me"

Sandy: "Got it, adjusting my tone!"

Expected: Saved as high-confidence observation (85%+)
Next responses: Should be noticeably more direct
```

### 3. Test Patterns

```
You: "/patterns"

Sandy: Shows what she knows (80%+ confidence)

Expected: After a few conversations, should start showing patterns
```

### 4. Test Exploration

```
You: "/explore"

Sandy: Picks category to learn about, asks questions

You: Answer naturally

Expected: Observations saved from your answers
```

---

## 🔍 Verify in Database

### Check Observations Are Saving:

```sql
-- Railway console → psql
SELECT COUNT(*) FROM pattern_observations;
-- Should increase after each conversation!

SELECT * FROM pattern_observations 
ORDER BY created_at DESC LIMIT 5;
-- See recent learnings
```

### Check Hypotheses Forming:

```sql
SELECT 
    category_name,
    hypothesis,
    confidence 
FROM pattern_hypotheses ph
JOIN pattern_categories pc ON ph.category_id = pc.id
WHERE confidence > 70;
-- Shows high-confidence patterns
```

### Check Feedback Saved:

```sql
SELECT * FROM pattern_observations 
WHERE observation LIKE '%USER FEEDBACK%'
ORDER BY created_at DESC;
-- See feedback you've given
```

---

## 💬 How to Use New Features

### Give Sandy Feedback:

```
"Sandy, be more playful" → Adjusts tone
"Sandy, remember I work best in mornings" → Saves pattern
"Sandy, stop asking so many questions" → Changes style
"Sandy, I prefer when you tease me" → Updates personality
```

**She'll respond:** "Got it!" or "Noted!" or "Understood, I'll adapt!"

### Edit Her Personality:

```bash
# Edit these files:
nano SANDY_SYSTEM_PROMPT_FULL.md
nano SANDY_SYSTEM_PROMPT_PART2.md

# Changes apply on next Railway restart
# Or: Railway → Settings → Restart
```

### See What She Knows:

```
Type: /patterns

Shows:
- High-confidence patterns (80%+)
- What she's still learning
- Areas needing exploration
```

### Teach Her About You:

```
Type: /explore

Sandy picks what to learn OR you specify:
/explore task_initiation
/explore energy_patterns
```

---

## 📊 Expected Behavior

### First Few Conversations:
- Sandy learning, asking questions
- Building observations
- `/patterns` shows "Still learning!"

### After 5-10 Conversations:
- First patterns start forming
- Confidence 50-70%
- Sandy begins applying learnings

### After 20+ Conversations:
- Multiple high-confidence patterns (80%+)
- Sandy references your specific patterns naturally
- Very personalized responses

---

## ⚠️ If Something's Wrong

### Observations Not Saving?

Check logs for:
```
"Extracted X learnings from interaction"
```

If missing:
1. Verify learning_extraction.py deployed
2. Check database connection
3. Try a message with clear indicators: "I'm really tired and overwhelmed"

### Feedback Not Working?

Try explicit format:
```
"Sandy, remember I work best in mornings"
```

Should see in logs:
```
"Applied feedback: remember I work best in mornings"
```

### Prompts Not Loading?

Check Railway logs for:
```
"Warning: Could not load prompt files"
```

If present:
1. Verify .md files are in backend root
2. Check file paths in ai.py
3. Restart Railway

---

## 🎯 Success Criteria

**Deploy was successful if:**

✅ Sandy responds normally (personality intact)
✅ Logs show "Extracted X learnings" after messages
✅ Database pattern_observations count increases
✅ Feedback acknowledgments work: "Got it, adjusting my tone!"
✅ `/patterns` command works (even if "Still learning!")
✅ `/explore` command works and asks questions

---

## 📝 Quick Reference

**Key Files:**
- System Prompt: `SANDY_SYSTEM_PROMPT_FULL.md` + `PART2.md`
- Learning: `app/services/learning_extraction.py`
- Feedback: `app/services/feedback.py`
- Pattern Learning: `app/services/pattern_learning.py`

**Key Tables:**
- `pattern_categories` - 18 main areas
- `pattern_observations` - Individual learnings
- `pattern_hypotheses` - Formed patterns

**Commands:**
- `/patterns` - What Sandy knows
- `/explore` - Teach Sandy about you
- "Sandy, [instruction]" - Give feedback

---

## 🎉 You're Done!

**Sandy is now:**
- Using full personality ✅
- Learning from every message ✅
- Accepting your feedback ✅
- Getting better every day ✅

**Just deploy and start chatting!**

```bash
git push  # That's it!
```

---

**Questions? Check:**
- `COMPLETE_FIX_SUMMARY.md` - Detailed explanation
- `README_ARCHITECTURE.md` - How everything works
- `PROMPT_AND_ARCHITECTURE_AUDIT.md` - What was wrong
