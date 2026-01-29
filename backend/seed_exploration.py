"""Seed initial exploration topics for users."""
from app.database import get_db
from app.models.user import User
from app.models.exploration_topic import ExplorationTopic


def seed_exploration_topics(user_id: int):
    """Add initial exploration topics for a user."""
    
    db = next(get_db())
    
    initial_topics = [
        {
            "topic": "work_style",
            "priority": 10,
            "key_insights": {
                "description": "How you work best, focus patterns, productive times"
            }
        },
        {
            "topic": "motivation_triggers",
            "priority": 9,
            "key_insights": {
                "description": "What gets you moving vs. what makes you avoid tasks"
            }
        },
        {
            "topic": "energy_patterns",
            "priority": 9,
            "key_insights": {
                "description": "When you have energy, sleep patterns, focus times"
            }
        },
        {
            "topic": "relationships",
            "priority": 7,
            "key_insights": {
                "description": "Family, friends, team dynamics, social energy"
            }
        },
        {
            "topic": "goals_dreams",
            "priority": 8,
            "key_insights": {
                "description": "What you're working toward, big picture vision"
            }
        },
        {
            "topic": "stress_triggers",
            "priority": 8,
            "key_insights": {
                "description": "What causes anxiety, overwhelm, or avoidance"
            }
        },
        {
            "topic": "hobbies_interests",
            "priority": 6,
            "key_insights": {
                "description": "What you enjoy, creative outlets, side interests"
            }
        },
        {
            "topic": "health_physical",
            "priority": 7,
            "key_insights": {
                "description": "Exercise, diet, physical state, health routines"
            }
        },
    ]
    
    try:
        for topic_data in initial_topics:
            topic = ExplorationTopic(
                user_id=user_id,
                topic=topic_data["topic"],
                priority=topic_data["priority"],
                understanding_score=0,
                key_insights=topic_data["key_insights"]
            )
            db.add(topic)
        
        db.commit()
        print(f"✅ Seeded {len(initial_topics)} exploration topics for user {user_id}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    # Seed for the test user
    db = next(get_db())
    user = db.query(User).filter(User.email == "user@example.com").first()
    
    if user:
        seed_exploration_topics(user.id)
    else:
        print("❌ User not found")
