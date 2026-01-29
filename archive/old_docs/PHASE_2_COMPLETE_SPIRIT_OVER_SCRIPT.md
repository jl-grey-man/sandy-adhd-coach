# PHASE 2 COMPLETE: SPIRIT OVER SCRIPT REWRITE
**Date**: January 29, 2026
**Implementation**: Complete systematic rewrite of all prompt examples

---

## 🎯 THE PROBLEM WE SOLVED

**Original Issue**: Sandy was repeating exact phrases from examples
- "What's stopping you?" used verbatim
- "When specifically?" copied word-for-word
- Same greetings every time
- Sounded robotic and scripted

**Root Cause**: Prompt examples were formatted as scripts to memorize
```
✅ RIGHT: "What's stopping you?"
✅ RIGHT: "When specifically?"
```

Sandy interpreted these as lines to deliver, not principles to embody.

---

## 🔧 THE SOLUTION

**Complete Reformat**: Changed ALL examples from scripts to principles

### Before (Script Format):
```
SCENARIO: User says they'll do something "later"
✅ RIGHT: "When specifically?"
✅ RIGHT: "Right. So sometime never?"
✅ RIGHT: "Later today or later never?"
```

### After (Principle Format):
```
SCENARIO: User says they'll do something "later"
──────────────────────────────────────────────
WRONG APPROACH: Accept vague timing or encourage them
SPIRIT: Don't let "later" slide - it usually means never

RIGHT APPROACH: Pin down actual timing or call out the vagueness
SPIRIT: Make them commit to specific time or acknowledge they're avoiding
EXPRESS NATURALLY:
- Ask when specifically
- Playfully note that "later" often means never
- Get concrete timing

Remember the spirit: Don't let vague timing slide. Say it your own way.
```

---

## 📋 WHAT CHANGED

### 1. Added Meta-Instructions (Top of Prompt)

```markdown
═══════════════════════════════════════════════════════════════════
⚠️  CRITICAL: SPIRIT OVER SCRIPT
═══════════════════════════════════════════════════════════════════

Throughout this prompt, you'll see examples of responses and approaches.

**THESE ARE ILLUSTRATIONS, NOT SCRIPTS TO MEMORIZE.**

They demonstrate:
- The TONE you should strike
- The GOAL you're trying to achieve
- The SPIRIT of the interaction

**Express these principles naturally in YOUR OWN WORDS for EACH situation.**

If you find yourself repeating the same phrases across conversations, you're doing it wrong.

Think like an improv actor: given the scene and character, what would you naturally say?
```

### 2. Reformatted ALL Example Sections

**Changed 27 example sections** across both prompt files:

#### FULL Prompt (PART 1):
- Greeting variations → APPROACH (vary constantly)
- Response patterns → SPIRIT + EXPRESS naturally
- All 7 situation handlers → WRONG APPROACH + RIGHT APPROACH + SPIRIT
- All 5 scenario examples → SPIRIT + EXPRESS NATURALLY
- Hypothesis handling → SPIRIT + EXPRESS naturally

#### PART 2 Prompt:
- Action response format → SPIRIT + APPROACH
- Exploration flow → SPIRIT + FLOW
- Memory usage → APPROACH + SPIRIT
- 5 conversational patterns → FLOW SPIRIT (not dialogue)
- Tone calibration → SITUATIONS + SPIRIT + EXPRESS

### 3. Key Structural Changes

**Every example section now includes:**
1. **WRONG APPROACH**: What NOT to do (anti-pattern)
2. **SPIRIT**: The underlying principle/goal
3. **RIGHT APPROACH**: How to think about it
4. **EXPRESS NATURALLY**: Guidelines, NOT exact phrases
5. **Remember the spirit**: Reminder to adapt, not copy

**Removed**:
- All "✅ RIGHT: [exact quote]" format
- All prescriptive phrase lists
- All dialogue examples presented as scripts

**Added**:
- Emphasis on VARIATION
- "In your own words" reminders
- "Say it naturally" throughout
- Character embodiment language

---

## 📂 FILES CHANGED

### Main Changes:
```
SANDY_SYSTEM_PROMPT_FULL.md     - Complete rewrite (544 lines)
SANDY_SYSTEM_PROMPT_PART2.md    - Complete rewrite (321 lines)
```

### Backups Created:
```
SANDY_SYSTEM_PROMPT_FULL_OLD.md     - Original version
SANDY_SYSTEM_PROMPT_PART2_OLD.md    - Original version
```

---

## 🎭 THE NEW PHILOSOPHY

### Old Approach: "What's my line?"
Sandy saw examples as dialogue to memorize and repeat.

### New Approach: "What's my character?"
Sandy understands WHO she is and HOW she thinks, then responds authentically.

**Key Metaphor**: Improv actor vs. script reader
- Not: "Which example phrase should I use?"
- But: "What would Sandy naturally say here?"

---

## ✅ EXPECTED OUTCOMES

### What Should Improve:
1. **Natural Variation**: No two responses sound the same
2. **Contextual Adaptation**: Responses fit the specific situation
3. **Fresh Language**: Sandy sounds like a real person, not AI
4. **Authentic Personality**: Character shines through consistently

### What Should Stay Consistent:
1. **Core Personality**: Rachel Zane + Joan Holloway vibe
2. **Directness**: No fluff, cut to chase
3. **Brevity**: 1-3 sentences default
4. **Respect**: Treats Jens as capable equal

---

## 🧪 TESTING CHECKLIST

### Test for Variation:
- [ ] Have 5-6 conversations with similar scenarios
- [ ] Check if greetings are different each time
- [ ] Verify follow-up questions vary naturally
- [ ] Confirm no exact phrase repetition

### Test for Spirit:
- [ ] When user says "later", does Sandy pin down timing? (not exact words)
- [ ] When overwhelmed, does Sandy get specific? (not exact words)
- [ ] When task done, does Sandy acknowledge briefly + move forward? (not exact words)

### Test for Character:
- [ ] Does Sandy sound like a real work partner?
- [ ] Is personality consistent (direct, respectful, playful)?
- [ ] Are responses tailored to context?
- [ ] Does she embody character vs. recite lines?

---

## 🚀 DEPLOYMENT STEPS

```bash
cd /Users/jenslennartsson/Documents/-ai_projects-/adhd_coach/backend

# Verify changes
git diff SANDY_SYSTEM_PROMPT_FULL.md
git diff SANDY_SYSTEM_PROMPT_PART2.md

# Commit
git add SANDY_SYSTEM_PROMPT_FULL.md SANDY_SYSTEM_PROMPT_PART2.md
git commit -m "PHASE 2: Complete spirit-over-script rewrite

- Reformatted ALL 27+ example sections
- Changed from prescriptive quotes to adaptive principles
- Added SPIRIT/APPROACH/EXPRESS structure
- Emphasized natural variation and character embodiment
- Removed all verbatim dialogue examples
- Added meta-instructions on improv mindset

Goal: Sandy responds naturally with varied language,
not memorized phrases from examples."

# Push and deploy
git push origin main
```

---

## 📊 IMPACT SUMMARY

### Lines Changed:
- FULL prompt: ~540 lines (complete reformat)
- PART2 prompt: ~320 lines (complete reformat)
- Total: ~860 lines rewritten

### Concepts Added:
- SPIRIT over SCRIPT philosophy
- APPROACH vs. EXACT QUOTE distinction
- EXPRESS NATURALLY guidelines
- Character embodiment mindset
- Improv actor metaphor

### Removed:
- All ✅ RIGHT: "exact quote" formats
- Prescriptive phrase lists
- Dialogue scripts
- "Use these words" examples

---

## 🎯 SUCCESS CRITERIA

**Sandy is successful when**:
1. No conversation sounds like previous conversations
2. Responses feel tailored to specific context
3. Personality is consistent, language is varied
4. User can't predict exact phrasing
5. Character shines through authentically

**Sandy has failed if**:
1. Same phrases repeat across conversations
2. Responses feel templated or robotic
3. User hears exact examples from prompt
4. Language feels stiff or scripted
5. Personality inconsistent or lost

---

## 💡 KEY PRINCIPLE

> "The examples show you the character.  
> Now play the character authentically."

Sandy is an improv actor who knows her character deeply.
She doesn't need a script - she knows what Sandy would say.

---

**PHASE 2: COMPLETE ✅**
**Ready for deployment and testing.**
