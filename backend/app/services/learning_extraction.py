"""
Learning extraction - Extract insights from conversations and save as observations.
This is the GLUE CODE that connects conversations to pattern learning.
"""
import re
from typing import List, Dict
from sqlalchemy.orm import Session

from app.services.pattern_learning import PatternLearningService
from app.services.subpatterns import get_subpattern


def extract_and_save_learnings(
    user_message: str,
    ai_response: str,
    user_id: int,
    db: Session,
    action_result: dict = None
) -> List[Dict]:
    """
    Extract learnings from a conversation and save them as observations.
    This is called after EVERY user interaction.
    
    NOW INCLUDES SUBPATTERN DETECTION!
    
    Returns list of learnings extracted.
    """
    learner = PatternLearningService(user_id, db)
    learnings_extracted = []
    
    user_lower = user_message.lower()
    combined_text = f"{user_message} {ai_response or ''}"
    
    # TASK INITIATION PATTERNS (with subpatterns!)
    if action_result and action_result.get('success') and action_result.get('action_type') == 'create_task':
        subpattern = get_subpattern('task_initiation', combined_text)
        learner.add_observation(
            category_name='task_initiation',
            sub_pattern=subpattern,  # ← Now includes specific trigger!
            observation=f"Created task: {user_message[:100]}",
            context={'action': 'task_creation', 'success': True, 'subpattern': subpattern}
        )
        learnings_extracted.append({
            'category': 'task_initiation',
            'subpattern': subpattern,
            'observation': 'task creation'
        })
    
    # AVOIDANCE PATTERNS (with subpatterns!)
    deflection_phrases = ['later', 'maybe', 'not sure', "i don't know", 'eventually', 'probably']
    for phrase in deflection_phrases:
        if phrase in user_lower:
            subpattern = get_subpattern('avoidance_reasons', combined_text)
            learner.add_observation(
                category_name='avoidance_reasons',
                sub_pattern=subpattern,
                observation=f"Used '{phrase}' - possible avoidance: {user_message[:100]}",
                context={'deflection_phrase': phrase, 'subpattern': subpattern}
            )
            learnings_extracted.append({
                'category': 'avoidance_reasons',
                'subpattern': subpattern,
                'observation': f'deflection: {phrase}'
            })
            break
    
    # TIME PERCEPTION (with subpatterns!)
    time_mentions = re.findall(r'(\d+)\s*(minute|min|hour|hr|day)s?', user_lower)
    if time_mentions:
        for amount, unit in time_mentions:
            subpattern = get_subpattern('time_perception', user_lower)
            learner.add_observation(
                category_name='time_perception',
                sub_pattern=subpattern,
                observation=f"Estimated {amount} {unit} for task",
                context={'amount': amount, 'unit': unit, 'subpattern': subpattern}
            )
            learnings_extracted.append({
                'category': 'time_perception',
                'subpattern': subpattern,
                'observation': f'{amount} {unit}'
            })
    
    # ENERGY PATTERNS (with subpatterns!)
    subpattern = get_subpattern('energy_patterns', user_lower)
    if subpattern:  # Only if we detected a specific energy signal
        learner.add_observation(
            category_name='energy_patterns',
            sub_pattern=subpattern,
            observation=f"Energy signal detected: {user_message[:100]}",
            context={'energy_indicator': subpattern}
        )
        learnings_extracted.append({
            'category': 'energy_patterns',
            'subpattern': subpattern,
            'observation': 'energy signal'
        })
    
    # COMMUNICATION RESPONSE (with subpatterns!)
    if ai_response:
        subpattern = get_subpattern('communication_response', ai_response.lower())
        if subpattern:
            learner.add_observation(
                category_name='communication_response',
                sub_pattern=subpattern,
                observation=f"Sandy used {subpattern} approach - observe user response",
                context={'sandy_approach': subpattern, 'user_response': user_message[:100]}
            )
            learnings_extracted.append({
                'category': 'communication_response',
                'subpattern': subpattern,
                'observation': f'approach: {subpattern}'
            })
    
    # MOTIVATION TRIGGERS (with subpatterns!)
    subpattern = get_subpattern('motivation_sources', user_lower)
    if subpattern:
        learner.add_observation(
            category_name='motivation_sources',
            sub_pattern=subpattern,
            observation=f"Motivation indicator: {user_message[:100]}",
            context={'motivation_type': subpattern}
        )
        learnings_extracted.append({
            'category': 'motivation_sources',
            'subpattern': subpattern,
            'observation': 'motivation signal'
        })
    
    # HYPERFOCUS TRIGGERS (with subpatterns!)
    if 'in the zone' in user_lower or 'flow' in user_lower or 'focused' in user_lower:
        subpattern = get_subpattern('hyperfocus_triggers', combined_text)
        learner.add_observation(
            category_name='hyperfocus_triggers',
            sub_pattern=subpattern,
            observation=f"Focus/flow state mentioned: {user_message[:100]}",
            context={'focus_indicator': True, 'subpattern': subpattern}
        )
        learnings_extracted.append({
            'category': 'hyperfocus_triggers',
            'subpattern': subpattern,
            'observation': 'focus state'
        })
    
    # URGENCY RESPONSE (with subpatterns!)
    if 'deadline' in user_lower or 'urgent' in user_lower or 'pressure' in user_lower:
        subpattern = get_subpattern('urgency_response', user_lower)
        learner.add_observation(
            category_name='urgency_response',
            sub_pattern=subpattern,
            observation=f"Urgency mentioned: {user_message[:100]}",
            context={'urgency_type': subpattern}
        )
        learnings_extracted.append({
            'category': 'urgency_response',
            'subpattern': subpattern,
            'observation': 'urgency signal'
        })
    
    # ACCOUNTABILITY (with subpatterns!)
    if any(word in user_lower for word in ['waiting', 'expecting', 'deadline', 'must', 'have to']):
        subpattern = get_subpattern('accountability_effectiveness', user_lower)
        if subpattern:
            learner.add_observation(
                category_name='accountability_effectiveness',
                sub_pattern=subpattern,
                observation=f"Accountability signal: {user_message[:100]}",
                context={'accountability_type': subpattern}
            )
            learnings_extracted.append({
                'category': 'accountability_effectiveness',
                'subpattern': subpattern,
                'observation': 'accountability signal'
            })
    
    return learnings_extracted
