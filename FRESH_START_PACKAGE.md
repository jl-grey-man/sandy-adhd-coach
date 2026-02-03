# Fresh Start Package - Sandy ADHD Coach
**Created**: February 3, 2026
**Purpose**: Complete database reset with clean schema matching current models

## What This Package Contains

1. ✅ **Schema Analysis**: Full expected database schema from models
2. ✅ **Clean Migration**: ONE migration that creates everything correctly
3. ✅ **Seed Script**: Populates required data (pattern_categories, test user)
4. ✅ **Test Script**: Verifies bot works with fresh database
5. ✅ **Deployment Guide**: Step-by-step Railway setup

## Expected Database Schema

**Total Tables**: 16

### Core Tables
1. **users** - User accounts with Telegram integration
2. **conversations** - Chat history (user_message, ai_response, input_type, context)
3. **goals** - User goals
4. **projects** - Multi-step projects (uses `name` not `title`)
5. **tasks** - Individual tasks (has `project_id`, no `goal_id`)
6. **milestones** - Project milestones

### Feature Tables
7. **backburner_items** - Postponed items
8. **calendar_events** - Calendar integration
9. **checkins** - Daily/weekly check-ins
10. **metrics** - Performance metrics
11. **work_sessions** - Task timing
12. **wheel_categories** - Life wheel categories
13. **wheel_scores** - Life wheel scores

### Pattern Learning Tables
14. **pattern_categories** - Learning categories (18 system categories)
15. **pattern_observations** - Individual learnings
16. **conversation_embeddings** - Pinecone vector mappings

## Key Schema Differences from Old Migrations

### ✅ conversations (FIXED)
- Has: `user_message`, `ai_response`, `input_type`, `context`, `suggestions`
- NOT: `role`, `content` (old schema)

### ✅ tasks (FIXED)
- Has: `project_id` (ForeignKey to projects)
- NOT: `goal_id` (old schema)
- NO `updated_at` column

### ✅ projects (CORRECT)
- Column is `name` not `title`
- Has: `deadline`, `estimated_hours`, `actual_hours`, `moved_to_backburner_at`, `backburner_reason`

### ✅ backburner_items (CORRECT)
- Has: `title`, `description`, `context_tags`, `reason`

## Files in This Package

```
backend/
├── migrations/versions/
│   └── 001_clean_schema.py          # NEW: Creates all 16 tables correctly
├── seed_fresh_database.py            # Seeds pattern_categories + test user
├── test_bot_local.py                 # Tests bot functionality
└── FRESH_START_INSTRUCTIONS.md       # Step-by-step guide
```

## Next Steps

1. **Delete old migrations** (keep folder structure)
2. **Create clean migration** from expected schema
3. **Create seed script** for pattern_categories
4. **Create test script** for bot verification
5. **Test locally first** before touching Railway
6. **Document Railway deployment** steps

## Pattern Categories to Seed

The system requires 18 pre-defined pattern categories:
- task_initiation, task_completion, time_blindness
- energy_patterns, focus_patterns, overwhelm_triggers
- working_memory_challenges, emotional_regulation
- hyperfocus_episodes, context_switching
- morning_vs_evening_productivity, social_energy
- impulsivity_patterns, avoidance_behaviors
- reward_sensitivity, novelty_seeking
- perfectionism_paralysis, external_structure_needs

## Test User

Email: `user@example.com`
Password: `string`
Telegram: Will auto-link on /start

## Success Criteria

✅ All 16 tables created with correct schema
✅ Pattern categories seeded (18 rows)
✅ Test user created
✅ Bot responds to Telegram messages
✅ Conversations saved correctly
✅ Context building works (tasks, projects)
✅ No schema mismatch errors
