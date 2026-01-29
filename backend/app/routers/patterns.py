"""
Patterns API Router - Unified pattern learning endpoints for both Telegram and Web UI

These endpoints expose the pattern learning system so both interfaces can use the same logic.
"""
from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.dependencies import CurrentUser
from app.services.pattern_learning import PatternLearningService
from app.services.exploration import ExplorationService

router = APIRouter(prefix="/api/patterns", tags=["Patterns"])


@router.get("/confirmed")
async def get_confirmed_patterns(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
    min_confidence: int = 80
):
    """
    Get confirmed patterns for the current user.
    
    Args:
        min_confidence: Minimum confidence threshold (default: 80%)
    
    Returns:
        List of confirmed patterns with category, hypothesis, and confidence
    """
    learner = PatternLearningService(current_user.id, db)
    patterns = learner.get_confirmed_patterns(min_confidence=min_confidence)
    
    if not patterns:
        return {
            "has_patterns": False,
            "message": "Still learning! Keep chatting and I'll start identifying patterns.",
            "patterns": []
        }
    
    return {
        "has_patterns": True,
        "patterns": patterns,
        "count": len(patterns)
    }


@router.get("/explore")
async def get_exploration_guidance(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)],
    category: Optional[str] = None
):
    """
    Get exploration guidance for pattern learning.
    
    Args:
        category: Optional specific category to explore (e.g., "task_initiation")
    
    Returns:
        Category info with questions to explore, current understanding, and hypothesis
    """
    explorer = ExplorationService(current_user.id, db)
    
    # If category specified, get that one
    if category:
        category_data = explorer.get_category_by_name(category)
        if not category_data:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Category '{category}' not found"
            )
    else:
        # Pick next category needing exploration
        category_data = explorer.pick_next_category()
        if not category_data:
            return {
                "needs_exploration": False,
                "message": "You're doing great! No urgent areas to explore right now."
            }
    
    # Get exploration questions
    questions = explorer.get_exploration_guidance(category_data['category_name'])
    
    return {
        "needs_exploration": True,
        "category": category_data['category_name'],
        "description": category_data['description'],
        "confidence": category_data['confidence'],
        "observations": category_data['observations'],
        "hypothesis": category_data['hypothesis'],
        "questions": questions[:3]  # First 3 questions
    }


@router.get("/status")
async def get_learning_status(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Get overall pattern learning status across all categories.
    
    Returns:
        Summary of confirmed patterns and categories still learning
    """
    learner = PatternLearningService(current_user.id, db)
    explorer = ExplorationService(current_user.id, db)
    
    # Get confirmed patterns
    confirmed = learner.get_confirmed_patterns(min_confidence=80)
    
    # Get all categories status
    all_categories = explorer.get_all_categories_status()
    learning = [c for c in all_categories if c['confidence'] < 80]
    
    return {
        "confirmed_patterns": {
            "count": len(confirmed),
            "patterns": confirmed
        },
        "learning": {
            "count": len(learning),
            "categories": learning[:5]  # Top 5 still learning
        },
        "total_categories": len(all_categories),
        "overall_progress": sum(c['confidence'] for c in all_categories) / len(all_categories) if all_categories else 0
    }


@router.get("/categories")
async def get_all_categories(
    current_user: CurrentUser,
    db: Annotated[Session, Depends(get_db)]
):
    """
    Get all pattern categories with their current status.
    
    Returns:
        List of all 18 categories with confidence and observation counts
    """
    explorer = ExplorationService(current_user.id, db)
    categories = explorer.get_all_categories_status()
    
    return {
        "categories": categories,
        "count": len(categories)
    }
