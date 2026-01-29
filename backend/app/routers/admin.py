"""
Admin endpoint to fix pattern category descriptions.
Call this once to update from 'him/he' to 'you'.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.pattern_tracking import PatternCategory
from app.dependencies import get_current_user
from app.models.user import User

router = APIRouter(prefix="/admin", tags=["admin"])

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


@router.post("/fix-descriptions")
async def fix_category_descriptions(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """
    Update pattern category descriptions from 'him/he' to 'you'.
    Run this once per user to fix existing categories.
    """
    
    updated_count = 0
    
    for category_name, new_description in UPDATED_DESCRIPTIONS.items():
        category = db.query(PatternCategory).filter(
            PatternCategory.user_id == current_user.id,
            PatternCategory.category_name == category_name
        ).first()
        
        if category:
            category.description = new_description
            updated_count += 1
    
    db.commit()
    
    return {
        "success": True,
        "message": f"Updated {updated_count} category descriptions from 'him/he' to 'you'",
        "updated_count": updated_count
    }
