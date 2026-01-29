"""
Learning extraction - Extract insights from conversations and save as observations.
This is the GLUE CODE that connects conversations to pattern learning.
"""
import re
from typing import List, Dict
from sqlalchemy.orm import Session

from app.services.pattern_learning import PatternLearningService


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
    
    Returns list of learnings extracted.
    """
    learner = PatternLearningService(user_id, db)
    learnings_extracted = []
    
    user_lower = user_message.lower()
    
    # TASK INITIATION PATTERNS
    if action_result and action_result.get('success') and action_result.get('action_type') == 'create_task':
        learner.add_observation(
            category_name='task_initiation',
            observation=f"Created task proactively when discussing: {user_message[:100]}",
            context={'action': 'task_creation', 'success': True}
        )
        learnings_extracted.append({'category': 'task_initiation', 'observation': 'proactive task creation'})
    
    # AVOIDANCE PATTERNS
    deflection_phrases = ['later', 'maybe', 'not sure', "i don't know", 'eventually', 'probably']
    for phrase in deflection_phrases:
        if phrase in user_lower:
            learner.add_observation(
                category_name='avoidance_reasons',
                observation=f"Used '{phrase}' when discussing tasks - possible avoidance",
                context={'deflection_phrase': phrase, 'message': user_message[:100]}
            )
            learnings_extracted.append({'category': 'avoidance_reasons', 'observation': f'uses {phrase}'})
            break
    
    # TIME PERCEPTION
    time_mentions = re.findall(r'(\d+)\s*(minute|min|hour|hr|day)s?', user_lower)
    if time_mentions:
        for amount, unit in time_mentions:
            learner.add_observation(
                category_name='time_perception',
                observation=f"Mentioned {amount} {unit} for task estimation",
                context={'amount': amount, 'unit': unit}
            )
            learnings_extracted.append({'category': 'time_perception', 'observation': f'{amount} {unit}'})
    
    # ENERGY PATTERNS
    high_energy_words = ['ready', 'pumped', 'energized', 'motivated', 'let\'s go', 'excited']
    low_energy_words = ['tired', 'exhausted', 'drained', 'overwhelmed', 'can\'t', 'struggling']
    
    for word in high_energy_words:
        if word in user_lower:
            learner.add_observation(
                category_name='energy_patterns',
                observation=f"High energy signal: used '{word}'",
                context={'energy_level': 'high', 'indicator': word}
            )
            learnings_extracted.append({'category': 'energy_patterns', 'observation': 'high energy'})
            break
    
    for word in low_energy_words:
        if word in user_lower:
            learner.add_observation(
                category_name='energy_patterns',
                observation=f"Low energy signal: used '{word}'",
                context={'energy_level': 'low', 'indicator': word}
            )
            learnings_extracted.append({'category': 'energy_patterns', 'observation': 'low energy'})
            break
    
    # COMMUNICATION RESPONSE
    if ai_response:
        # Check if Sandy used direct push
        if any(phrase in ai_response.lower() for phrase in ['what\'s actually', 'real reason', 'and when']):
            learner.add_observation(
                category_name='communication_response',
                observation="Sandy used direct push - observe user's response",
                context={'sandy_approach': 'direct_push', 'user_response': user_message[:100]}
            )
            learnings_extracted.append({'category': 'communication_response', 'observation': 'direct push used'})
    
    # MOTIVATION TRIGGERS
    motivation_words = ['want to', 'need to', 'have to', 'should', 'must', 'deadline']
    for word in motivation_words:
        if word in user_lower:
            learner.add_observation(
                category_name='motivation_sources',
                observation=f"Motivation indicator: '{word}' mentioned",
                context={'motivation_type': word, 'context': user_message[:100]}
            )
            learnings_extracted.append({'category': 'motivation_sources', 'observation': word})
            break
    
    # HYPERFOCUS TRIGGERS (if user completed something quickly or mentions flow)
    if 'in the zone' in user_lower or 'flow' in user_lower or 'focused' in user_lower:
        learner.add_observation(
            category_name='hyperfocus_triggers',
            observation=f"User mentioned focus/flow state: {user_message[:100]}",
            context={'focus_indicator': True}
        )
        learnings_extracted.append({'category': 'hyperfocus_triggers', 'observation': 'focus state mentioned'})
    
    return learnings_extracted
