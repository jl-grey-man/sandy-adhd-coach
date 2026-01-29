"""
Update pattern category descriptions from 'him/he' to 'you'.
Run this once to fix existing database.
"""
import sys
sys.path.insert(0, '/Users/jenslennartsson/Documents/-ai_projects-/adhd_coach/backend')

from app.database import SessionLocal
from app.models.pattern_tracking import PatternCategory

# Updated descriptions (using "you" instead of "him/he")
UPDATED_DESCRIPTIONS = {
    "task_initiation": "What actually gets you started on tasks (body doubling, deadlines, accountability, momentum, triggers, etc.)",
    "hyperfocus_triggers": "What puts you in the zone (creative vs analytical, time pressure, interest, novelty, challenge level)",
    "avoidance_reasons": "WHY you avoid specific tasks (unclear done, too many steps, boring, uncertainty, perfectionism, fear)",
    "context_switching_cost": "How you handle switching between tasks (grouped better, needs transition, loses momentum, variety vs focus)",
    "energy_curves": "What drains vs energizes you beyond time of day (social, creative work, admin, movement, food/caffeine)",
    "motivation_sources": "What actually drives you to action (external validation, progress viz, competition, helping others, interest, money)",
    "reward_sensitivity": "What rewards motivate you (immediate gratification, long-term, social, financial, completion, new challenge)",
    "decision_fatigue": "When you hit decision paralysis (too many options, no clear best, high stakes, time of day, many small decisions)",
    "accountability_effectiveness": "What type of accountability works for you (hard deadlines, soft, check-ins, public commitment, consequences, rewards)",
    "task_breakdown_needs": "How much structure you need (overwhelmed by large, benefits from steps, prefers autonomy, needs first step only)",
    "interruption_recovery": "How you handle being interrupted (gets back quickly, loses session, needs warmup, benefits from breadcrumbs)",
    "momentum_building": "How you build work momentum (small wins cascade, needs warmup, goes straight for hard, routine/ritual)",
    "failure_response": "How you handle setbacks (catastrophizes, bounces back, needs processing, benefits from reframe)",
    "novelty_seeking": "How much novelty you need (bored quickly, thrives on routine, needs new challenge, explore vs exploit)",
    "sensory_environment": "What environment helps you work (music type, silence/noise, location, clean/messy, temperature/lighting)",
    "communication_response": "What tone/approach works for you (direct push, gentle, questions, playful, serious, data-driven)",
    "time_perception": "How you estimate time (optimistic/under, pessimistic/over, accurate, time blindness)",
    "urgency_response": "How you respond to urgency (thrives under pressure, freezes, last-minute rush, needs buffer)"
}

db = SessionLocal()

try:
    print("🔧 Updating pattern category descriptions...")
    print()
    
    for category_name, new_description in UPDATED_DESCRIPTIONS.items():
        categories = db.query(PatternCategory).filter(
            PatternCategory.category_name == category_name
        ).all()
        
        for cat in categories:
            old = cat.description
            cat.description = new_description
            print(f"✓ {category_name} (user {cat.user_id})")
            print(f"  Old: {old}")
            print(f"  New: {new_description}")
            print()
    
    db.commit()
    print("✅ All descriptions updated successfully!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    db.rollback()
finally:
    db.close()
