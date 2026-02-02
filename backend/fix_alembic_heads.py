"""
Fix Alembic multiple heads issue by cleaning up the alembic_version table.

This script removes old/invalid migration heads from the database that are
causing the "Multiple head revisions" error after we deleted old reminder migrations.
"""
import os
from sqlalchemy import create_engine, text

# Get database URL from environment
DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable not set")
    exit(1)

print("🔧 Fixing Alembic migration heads...")
print(f"📊 Connecting to database...")

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    # Check current heads in database
    result = conn.execute(text("SELECT * FROM alembic_version"))
    current_heads = [row[0] for row in result]

    print(f"\n📋 Current heads in database: {current_heads}")

    # These are the OLD heads we want to remove (they reference deleted migrations)
    invalid_heads = [
        '3e0577824795',  # old drop_and_recreate_reminders
        'add_reminders_table',  # old add_reminders_table
        '3b066e50a3e4',  # old add_reminders_table_with_timezone
    ]

    # Remove invalid heads
    removed = []
    for head in invalid_heads:
        if head in current_heads:
            conn.execute(text("DELETE FROM alembic_version WHERE version_num = :head"), {"head": head})
            removed.append(head)
            print(f"  ✅ Removed invalid head: {head}")

    # Commit changes
    conn.commit()

    # Verify current state
    result = conn.execute(text("SELECT * FROM alembic_version"))
    remaining_heads = [row[0] for row in result]

    print(f"\n✅ Cleanup complete!")
    print(f"📋 Remaining heads: {remaining_heads}")

    if len(remaining_heads) <= 1:
        print("✅ Database is ready! Should have 0 or 1 head.")
    else:
        print(f"⚠️  Still have {len(remaining_heads)} heads. Manual intervention may be needed.")
        print(f"   Heads: {remaining_heads}")

print("\n🎯 You can now run 'alembic upgrade head' successfully!")
