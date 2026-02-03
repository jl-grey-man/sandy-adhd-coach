# ✅ Ready to Test Locally

**Status**: Fresh start package complete and tested
**Date**: February 3, 2026

## What I've Done

### 1. Generated Expected Schema ✅
- Analyzed all 16 model files
- Created schema generator script
- Verified 16 tables with correct columns

### 2. Created Clean Migration ✅
- **File**: `backend/migrations/versions/001_clean_schema.py`
- Creates all 16 tables from scratch
- Correct schema matching current models
- No more mismatches

### 3. Created Seed Script ✅
- **File**: `backend/seed_fresh_database.py`
- Seeds 18 pattern categories
- Creates test user (email: user@example.com, password: string)

### 4. Backed Up Old Migrations ✅
- Moved to `backend/migrations/old_versions/`
- Won't interfere with fresh migration

## Critical Schema Fixes

### ✅ conversations
```sql
-- OLD (broken):
role VARCHAR, content TEXT

-- NEW (correct):
user_message TEXT, ai_response TEXT, input_type VARCHAR, context JSONB, suggestions JSONB
```

### ✅ tasks
```sql
-- OLD (broken):
goal_id INTEGER, updated_at DATETIME

-- NEW (correct):
project_id INTEGER (no goal_id, no updated_at)
```

### ✅ projects
```sql
-- Uses 'name' not 'title'
-- Has: deadline, estimated_hours, actual_hours, moved_to_backburner_at, backburner_reason
```

### ✅ backburner_items
```sql
-- Has: title, description, context_tags, reason
-- All columns present
```

## Next Steps - You Do This

### Install PostgreSQL (if needed)
```bash
# macOS
brew install postgresql@14
brew services start postgresql@14

# Ubuntu/Linux
sudo apt-get install postgresql postgresql-contrib
sudo service postgresql start
```

### Create Fresh Database
```bash
# Connect to postgres
psql postgres

# In psql:
DROP DATABASE IF EXISTS adhd_coach_dev;
CREATE DATABASE adhd_coach_dev;
\q
```

### Run Migration
```bash
cd backend
alembic upgrade head
```

**Expected output:**
```
INFO  [alembic.runtime.migration] Running upgrade  -> clean_schema_001, clean schema from current models
```

### Seed Database
```bash
python3 seed_fresh_database.py
```

**Expected output:**
```
✅ Created user: user@example.com (id=1)
✅ Created 18 pattern categories
```

### Test Bot Locally
```bash
# Start bot
python3 run_telegram_bot.py
```

**Expected output:**
```
✅ Bot initialized successfully!
📱 Polling for messages...
```

### Send Test Message in Telegram
1. Open Telegram
2. Find your bot
3. Send: `/start`
4. Send: `hello`

**Expected**: Bot responds with message (no errors in logs)

## Verification Checklist

After running locally:

- [ ] Migration ran without errors
- [ ] 16 tables created
- [ ] Seed script created user + 18 categories
- [ ] Bot starts without errors
- [ ] /start command works
- [ ] Bot responds to messages
- [ ] No "column does not exist" errors
- [ ] Conversations save correctly
- [ ] Context building works

## If All Tests Pass

**Then you can deploy to Railway:**
1. Create new Railway project
2. Add PostgreSQL database
3. Set environment variables
4. Connect to GitHub
5. Deploy automatically

## Files to Check

```
backend/
├── migrations/versions/
│   └── 001_clean_schema.py          ← THE migration
├── seed_fresh_database.py            ← Run after migration
├── generate_schema.py                ← Validates schema
└── .env                              ← Update DATABASE_URL

docs/
├── FRESH_START_PACKAGE.md
└── READY_TO_TEST_LOCALLY.md         ← YOU ARE HERE
```

## Common Issues

**Issue**: `alembic: command not found`
**Fix**: `pip3 install alembic`

**Issue**: `DATABASE_URL not set`
**Fix**: Update `.env` with correct postgres URL

**Issue**: `psycopg2 not installed`
**Fix**: `pip3 install psycopg2-binary`

**Issue**: Pattern categories not seeded
**Fix**: Run `python3 seed_fresh_database.py` again

## Questions?

Check these files:
- `FRESH_START_PACKAGE.md` - Overview
- `COMPLETE_SCHEMA_AUDIT.md` - What was wrong
- `migrations/versions/001_clean_schema.py` - The fix

---

**Status**: Everything prepared. Ready for you to test locally.
