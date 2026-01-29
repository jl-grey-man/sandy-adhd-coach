"""Seed 18 base pattern categories."""
from app.database import get_db
from app.models.user import User
from app.models.pattern_tracking import PatternCategory


CATEGORIES = [
    ("task_initiation", "What actually gets him started on tasks"),
    ("hyperfocus_triggers", "What puts him in the zone"),
    ("avoidance_reasons", "WHY he avoids specific tasks"),
    ("context_switching_cost", "How he handles switching between tasks"),
    ("energy_curves", "What drains vs energizes beyond time of day"),
    ("motivation_sources", "What actually drives action"),
    ("reward_sensitivity", "What rewards motivate"),
    ("decision_fatigue", "When decision paralysis hits"),
    ("accountability_effectiveness", "What type of accountability works"),
    ("task_breakdown_needs", "How much structure he needs"),
    ("interruption_recovery", "How he handles being interrupted"),
    ("momentum_building", "How he builds work momentum"),
    ("failure_response", "How he handles setbacks"),
    ("novelty_seeking", "How much novelty he needs"),
    ("sensory_environment", "What environment helps him work"),
    ("communication_response", "What tone/approach works"),
    ("time_perception", "How he estimates time"),
    ("urgency_response", "How he responds to urgency")
]


def seed(user_id: int):
    db = next(get_db())
    
    try:
        for name, desc in CATEGORIES:
            cat = PatternCategory(
                user_id=user_id,
                category_name=name,
                description=desc
            )
            db.add(cat)
        
        db.commit()
        print(f"✅ Seeded {len(CATEGORIES)} pattern categories")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    db = next(get_db())
    user = db.query(User).filter(User.email == "user@example.com").first()
    if user:
        seed(user.id)
