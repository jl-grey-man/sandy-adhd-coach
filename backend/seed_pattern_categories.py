"""Seed initial pattern categories for ADHD learning."""
from app.database import get_db
from app.models.user import User
from app.models.pattern_category import PatternCategory


INITIAL_CATEGORIES = [
    {
        "category_name": "task_initiation",
        "description": "What actually gets him started on tasks (body doubling, deadlines, accountability, momentum, triggers, etc.)"
    },
    {
        "category_name": "hyperfocus_triggers",
        "description": "What puts him in the zone (creative vs analytical, time pressure, interest, novelty, challenge level)"
    },
    {
        "category_name": "avoidance_reasons",
        "description": "WHY he avoids specific tasks (unclear done, too many steps, boring, uncertainty, perfectionism, fear)"
    },
    {
        "category_name": "context_switching_cost",
        "description": "How he handles switching between tasks (grouped better, needs transition, loses momentum, variety vs focus)"
    },
    {
        "category_name": "energy_curves",
        "description": "What drains vs energizes beyond time of day (social, creative work, admin, movement, food/caffeine)"
    },
    {
        "category_name": "motivation_sources",
        "description": "What actually drives action (external validation, progress viz, competition, helping others, interest, money)"
    },
    {
        "category_name": "reward_sensitivity",
        "description": "What rewards motivate (immediate gratification, long-term, social, financial, completion, new challenge)"
    },
    {
        "category_name": "decision_fatigue",
        "description": "When decision paralysis hits (too many options, no clear best, high stakes, time of day, many small decisions)"
    },
    {
        "category_name": "accountability_effectiveness",
        "description": "What type of accountability works (hard deadlines, soft, check-ins, public commitment, consequences, rewards)"
    },
    {
        "category_name": "task_breakdown_needs",
        "description": "How much structure he needs (overwhelmed by large, benefits from steps, prefers autonomy, needs first step only)"
    },
    {
        "category_name": "interruption_recovery",
        "description": "How he handles being interrupted (gets back quickly, loses session, needs warmup, benefits from breadcrumbs)"
    },
    {
        "category_name": "momentum_building",
        "description": "How he builds work momentum (small wins cascade, needs warmup, goes straight for hard, routine/ritual)"
    },
    {
        "category_name": "failure_response",
        "description": "How he handles setbacks (catastrophizes, bounces back, needs processing, benefits from reframe)"
    },
    {
        "category_name": "novelty_seeking",
        "description": "How much novelty he needs (bored quickly, thrives on routine, needs new challenge, explore vs exploit)"
    },
    {
        "category_name": "sensory_environment",
        "description": "What environment helps him work (music type, silence/noise, location, clean/messy, temperature/lighting)"
    },
    {
        "category_name": "communication_response",
        "description": "What tone/approach works (direct push, gentle, questions, playful, serious, data-driven)"
    },
    {
        "category_name": "time_perception",
        "description": "How he estimates time (optimistic/under, pessimistic/over, accurate, time blindness)"
    },
    {
        "category_name": "urgency_response",
        "description": "How he responds to urgency (thrives under pressure, freezes, last-minute rush, needs buffer)"
    }
]


def seed_pattern_categories(user_id: int):
    """Seed all 18 initial pattern categories for a user."""
    
    db = next(get_db())
    
    try:
        for cat_data in INITIAL_CATEGORIES:
            category = PatternCategory(
                user_id=user_id,
                category_name=cat_data["category_name"],
                description=cat_data["description"],
                understanding_level=0,  # Blank slate
                observations_count=0,
                confidence=0,
                evidence=[],
                needs_exploration=False
            )
            db.add(category)
        
        db.commit()
        print(f"✅ Seeded {len(INITIAL_CATEGORIES)} pattern categories for user {user_id}")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    db = next(get_db())
    user = db.query(User).filter(User.email == "user@example.com").first()
    
    if user:
        seed_pattern_categories(user.id)
    else:
        print("❌ User not found")
