# Database Migrations Guide

## Overview

This project uses Alembic for database migrations. This guide documents critical best practices to avoid migration issues, particularly the "multiple heads" problem we encountered.

## Critical Rules

### 1. **NEVER Create Migrations with `down_revision = None`**

**Problem:** Multiple migrations with no parent create separate "heads" which Alembic cannot resolve.

**Example of WRONG migration:**
```python
revision: str = 'abc123'
down_revision: Union[str, None] = None  # ❌ WRONG - Creates orphaned head
```

**Correct approach:**
```python
revision: str = 'abc123'
down_revision: Union[str, None] = 'previous_revision_id'  # ✅ CORRECT - Links to chain
```

### 2. **Always Use `alembic revision --autogenerate`**

Don't manually create migration files. Use Alembic's autogenerate feature:

```bash
# From backend/ directory
alembic revision --autogenerate -m "description of changes"
```

This ensures:
- Proper revision linking
- Automatic detection of model changes
- Consistent migration structure

### 3. **Linear Migration Chain Only**

Migrations must form a **single linear chain**, not a tree:

```
✅ CORRECT (Linear):
None → rev1 → rev2 → rev3 → rev4 (HEAD)

❌ WRONG (Multiple heads):
None → rev1 → rev2 (HEAD)
None → rev3 → rev4 (HEAD)
None → rev5 (HEAD)
```

### 4. **Check for Multiple Heads Before Committing**

Before pushing migration changes, verify there's only ONE head:

```bash
cd backend/
alembic heads
```

**Expected output:**
```
abc123def456 (head)
```

**If you see multiple heads - STOP AND FIX:**
```
abc123 (head)
def456 (head)  # ❌ Problem!
```

## What Happened: The Multiple Heads Crisis (Feb 2026)

### The Problem

After removing the reminders feature, we encountered a critical migration issue:

1. **9 separate HEAD revisions** existed in the migrations folder
2. Most migrations had `down_revision = None` (orphaned roots)
3. Alembic error: `"Multiple head revisions are present for given argument 'head'"`
4. Deployment failed repeatedly even after database wipe

### Root Cause

Migrations were created manually or incorrectly, creating multiple disconnected chains:
- `ffef6934a016` (create_users_table) - down_revision: None
- `08088987b6e6` (add_telegram_fields) - down_revision: None
- `0c0ac3d95f10` (fix_telegram_chat_id) - down_revision: None
- `42f417f227b3` (add_session_id) - down_revision: None
- ... and 5 more orphaned heads

### The Solution

1. **Backed up all broken migrations** to `migrations/old_migrations_backup/`
2. **Created single initial migration** (`001_initial_schema.py`) with:
   - `down_revision = None` (only acceptable for THE FIRST migration)
   - All current tables included
   - Clean starting point
3. **Wiped database completely** using `DROP SCHEMA public CASCADE`
4. **Deployed fresh** - single migration ran successfully

## Migration Workflow

### Adding New Features

```bash
# 1. Update your models in app/models/
# Example: Add new field to User model

# 2. Generate migration
cd backend/
alembic revision --autogenerate -m "add user preferences field"

# 3. Review the generated migration file
# Check that down_revision points to current HEAD

# 4. Test locally (if possible)
alembic upgrade head

# 5. Commit and push
git add migrations/versions/
git commit -m "Add migration: user preferences"
git push
```

### Removing Features

When removing models/tables:

```bash
# 1. Remove the model from app/models/
# 2. Update __init__.py to remove imports

# 3. Generate migration
alembic revision --autogenerate -m "remove reminder feature"

# 4. Review generated migration - should contain drop_table()
# 5. Commit and push
```

### Checking Migration Status

```bash
# Show current database revision
alembic current

# Show all heads (should be ONE)
alembic heads

# Show full migration history
alembic history

# Show pending migrations
alembic history --verbose
```

## Emergency: Fixing Multiple Heads

If you encounter multiple heads:

### Option 1: Merge Branches (Preferred for Production)
```bash
alembic merge -m "merge migration branches" head1 head2
# Creates a merge migration that joins the branches
```

### Option 2: Clean Slate (Development/Testing Only)

**⚠️ DESTRUCTIVE - Only if no production data!**

```bash
# 1. Backup all migrations
mkdir migrations/old_migrations_backup
mv migrations/versions/*.py migrations/old_migrations_backup/

# 2. Drop database schema
# Connect to PostgreSQL and run:
# DROP SCHEMA public CASCADE;
# CREATE SCHEMA public;

# 3. Create fresh initial migration
alembic revision --autogenerate -m "initial_schema"

# 4. Deploy
git add -A
git commit -m "Reset migrations with clean initial schema"
git push
```

## Railway Deployment Notes

### Database Connection

Railway PostgreSQL details are in `CREDENTIALS.md`. The database URL format:
```
postgresql://postgres:PASSWORD@HOST:PORT/railway
```

### Automatic Migrations

The `start.sh` script runs migrations automatically on deploy:
```bash
echo "🔄 Running database migrations..."
alembic upgrade head
```

### Debugging Failed Deployments

If Railway crashes on migration:

1. **Check logs** for specific error
2. **Verify heads locally:**
   ```bash
   cd backend/
   alembic heads
   ```
3. **Check database state:**
   ```python
   from sqlalchemy import create_engine, text
   engine = create_engine(DATABASE_URL)
   with engine.connect() as conn:
       result = conn.execute(text("SELECT * FROM alembic_version"))
       for row in result:
           print(row)
   ```

## Best Practices Summary

✅ **DO:**
- Always use `alembic revision --autogenerate`
- Check `alembic heads` before committing
- Keep migrations in a single linear chain
- Review autogenerated migrations before committing
- Test migrations locally when possible

❌ **DON'T:**
- Manually create migration files
- Set `down_revision = None` (except for THE FIRST migration)
- Delete migration files that have run in production
- Modify migrations that have already been deployed
- Skip migration review

## References

- Alembic Documentation: https://alembic.sqlalchemy.org/
- SQLAlchemy Documentation: https://docs.sqlalchemy.org/
- Our Architecture Guide: `README_ARCHITECTURE.md`
- Database Schema: `DATABASE_SCHEMA.md`

## Questions?

If you encounter migration issues:
1. Check this guide first
2. Verify `alembic heads` output
3. Review Railway deployment logs
4. Check database state via `alembic current`

---

**Last Updated:** February 2, 2026
**Reason:** Documented resolution of multiple heads crisis and established best practices
