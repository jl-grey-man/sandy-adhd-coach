"""
Stamp the database with the current migration head.

This tells Alembic what migration state the database is currently at.
"""
import os
from sqlalchemy import create_engine, text

DATABASE_URL = os.environ.get('DATABASE_URL')
if not DATABASE_URL:
    print("ERROR: DATABASE_URL environment variable not set")
    exit(1)

print("🔧 Stamping database with current migration head...")
print(f"📊 Connecting to database...")

engine = create_engine(DATABASE_URL)

with engine.connect() as conn:
    # Check current state
    result = conn.execute(text("SELECT * FROM alembic_version"))
    current = [row[0] for row in result]
    print(f"Current alembic_version entries: {current}")

    # Clear it
    conn.execute(text("DELETE FROM alembic_version"))

    # Stamp with the actual latest revision that exists in the database
    # Since we've been running migrations, the database should have the tables
    # We'll stamp it with 3d8c242a2745 (the revision before our drop_reminders migration)
    conn.execute(
        text("INSERT INTO alembic_version (version_num) VALUES (:version)"),
        {"version": "3d8c242a2745"}
    )

    conn.commit()

    # Verify
    result = conn.execute(text("SELECT * FROM alembic_version"))
    final = [row[0] for row in result]
    print(f"✅ Database stamped with: {final}")
    print(f"🎯 Now run: alembic upgrade head")
