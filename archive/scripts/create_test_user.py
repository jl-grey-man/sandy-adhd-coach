#!/usr/bin/env python3
"""Create test user in Railway database"""
import sys
import os

# Add backend to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'backend'))

from sqlalchemy import create_engine, text
from werkzeug.security import generate_password_hash

# Database connection
DATABASE_URL = "postgresql://postgres:URBpgBKTMDhSxULRshsZATDQirdqMUta@tramway.proxy.rlwy.net:38892/railway"

engine = create_engine(DATABASE_URL)

# Create test user
email = "test@example.com"
password = "string"
password_hash = generate_password_hash(password)

with engine.connect() as conn:
    # Check if user exists
    result = conn.execute(text("SELECT id, email FROM users WHERE email = :email"), {"email": email})
    existing = result.fetchone()
    
    if existing:
        print(f"✅ User already exists!")
        print(f"   Email: {existing[1]}")
        print(f"   Password: {password}")
    else:
        # Create user
        conn.execute(
            text("""
                INSERT INTO users (email, password_hash, name, timezone, created_at, updated_at, preferences)
                VALUES (:email, :password_hash, 'Test User', 'UTC', NOW(), NOW(), '{}')
            """),
            {"email": email, "password_hash": password_hash}
        )
        conn.commit()
        print(f"✅ Created test user:")
        print(f"   Email: {email}")
        print(f"   Password: {password}")
        
print("\nLogin at: https://sandy-adhd-coach-production.up.railway.app/")
