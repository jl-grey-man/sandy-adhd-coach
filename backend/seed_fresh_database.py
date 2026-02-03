#!/usr/bin/env python3
"""
Seed fresh database with required data:
1. 18 pattern categories (system-defined)
2. Test user account

Run after: alembic upgrade head
"""
import sys
import bcrypt
from datetime import datetime

# Add app to path
sys.path.insert(0, '.')

from app.database import SessionLocal
from app.models.user import User
from app.models.pattern_category import PatternCategory

# 18 system pattern categories
PATTERN_CATEGORIES = [
    {
        "category_name": "task_initiation",
        "description": "Getting started on tasks, overcoming initial resistance"
    },
    {
        "category_name": "task_completion",
        "description": "Finishing tasks once started, follow-through patterns"
    },
    {
        "category_name": "time_blindness",
        "description": "Time perception, estimation accuracy, time tracking habits"
    },
    {
        "category_name": "energy_patterns",
        "description": "Energy levels throughout day, what affects energy"
    },
    {
        "category_name": "focus_patterns",
        "description": "When focus is best/worst, what helps/hurts concentration"
    },
    {
        "category_name": "overwhelm_triggers",
        "description": "What causes overwhelm, early warning signs"
    },
    {
        "category_name": "working_memory_challenges",
        "description": "Forgetting steps, losing track mid-task, memory aids that help"
    },
    {
        "category_name": "emotional_regulation",
        "description": "Emotional responses to tasks, frustration tolerance"
    },
    {
        "category_name": "hyperfocus_episodes",
        "description": "When hyperfocus happens, triggers, benefits and costs"
    },
    {
        "category_name": "context_switching",
        "description": "Difficulty switching between tasks, transition challenges"
    },
    {
        "category_name": "morning_vs_evening_productivity",
        "description": "Best/worst times of day for different work types"
    },
    {
        "category_name": "social_energy",
        "description": "Impact of social interaction on energy and focus"
    },
    {
        "category_name": "impulsivity_patterns",
        "description": "Impulsive decisions, task-switching, distraction patterns"
    },
    {
        "category_name": "avoidance_behaviors",
        "description": "What tasks get avoided, avoidance strategies used"
    },
    {
        "category_name": "reward_sensitivity",
        "description": "What motivates, what rewards work, dopamine triggers"
    },
    {
        "category_name": "novelty_seeking",
        "description": "Attraction to new tasks/projects, boredom thresholds"
    },
    {
        "category_name": "perfectionism_paralysis",
        "description": "Perfectionism preventing action, 'good enough' challenges"
    },
    {
        "category_name": "external_structure_needs",
        "description": "Need for deadlines, accountability, external pressure"
    }
]


def seed_database():
    """Seed database with required data."""
    db = SessionLocal()

    try:
        print("=" * 70)
        print("SEEDING FRESH DATABASE")
        print("=" * 70)
        print()

        # 1. Create test user
        print("1. Creating test user...")
        existing_user = db.query(User).filter(User.email == "user@example.com").first()

        if existing_user:
            print(f"   ⚠️  User already exists: {existing_user.email}")
            user = existing_user
        else:
            password_hash = bcrypt.hashpw(b"string", bcrypt.gensalt()).decode('utf-8')

            user = User(
                email="user@example.com",
                password_hash=password_hash,
                name="Test User",
                timezone="UTC",
                created_at=datetime.utcnow(),
                updated_at=datetime.utcnow(),
                morning_briefing_time="09:00"
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"   ✅ Created user: {user.email} (id={user.id})")

        # 2. Seed pattern categories for test user
        print()
        print("2. Seeding pattern categories...")

        existing_count = db.query(PatternCategory).filter(
            PatternCategory.user_id == user.id
        ).count()

        if existing_count > 0:
            print(f"   ⚠️  {existing_count} categories already exist for user")
        else:
            for cat_data in PATTERN_CATEGORIES:
                category = PatternCategory(
                    user_id=user.id,
                    category_name=cat_data["category_name"],
                    description=cat_data["description"],
                    understanding_level=0,
                    observations_count=0,
                    confidence=0,
                    evidence=[],
                    needs_exploration=True,
                    created_at=datetime.utcnow(),
                    updated_at=datetime.utcnow()
                )
                db.add(category)

            db.commit()
            print(f"   ✅ Created {len(PATTERN_CATEGORIES)} pattern categories")

        # Summary
        print()
        print("=" * 70)
        print("SEED COMPLETE")
        print("=" * 70)
        print()
        print(f"Test User:")
        print(f"  Email: user@example.com")
        print(f"  Password: string")
        print(f"  User ID: {user.id}")
        print()
        print(f"Pattern Categories: {len(PATTERN_CATEGORIES)} seeded")
        print()

    except Exception as e:
        print(f"❌ Error seeding database: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()
