"""
Feedback system - Allow users to give Sandy feedback and she adapts.

When user says:
- "Sandy, be less formal" → Updates tone preference
- "Sandy, stop asking so many questions" → Updates question frequency
- "Sandy, be more direct" → Updates communication style
- "Sandy, remember I work best in mornings" → Adds pattern observation

This is stored as observations and Sandy uses them in future responses.
"""

from typing import Dict, List
from sqlalchemy.orm import Session
import re

from app.services.pattern_learning import PatternLearningService


def detect_feedback(user_message: str) -> Dict:
    """
    Detect if user is giving feedback to Sandy.
    
    Returns:
    {
        'is_feedback': bool,
        'feedback_type': str,  # 'tone', 'style', 'pattern', 'correction', 'general'
        'instruction': str,
        'category': str  # pattern category if applicable
    }
    """
    
    msg_lower = user_message.lower()
    
    # Check for explicit feedback triggers
    feedback_triggers = [
        'sandy, ',
        'hey sandy,',
        'remember ',
        'don\'t forget',
        'please remember',
        'from now on',
        'stop ',
        'don\'t ',
        'i prefer',
        'i like when',
        'i don\'t like when',
        'be more',
        'be less',
        'you should',
        'can you be'
    ]
    
    is_feedback = any(trigger in msg_lower for trigger in feedback_triggers)
    
    if not is_feedback:
        return {'is_feedback': False}
    
    # Detect feedback type
    
    # TONE feedback
    tone_keywords = ['formal', 'casual', 'friendly', 'professional', 'playful', 'serious', 'tone']
    if any(word in msg_lower for word in tone_keywords):
        return {
            'is_feedback': True,
            'feedback_type': 'tone',
            'instruction': user_message,
            'category': 'communication_style'
        }
    
    # QUESTION frequency feedback
    question_keywords = ['questions', 'asking', 'stop asking', 'don\'t ask']
    if any(word in msg_lower for word in question_keywords):
        return {
            'is_feedback': True,
            'feedback_type': 'style',
            'instruction': user_message,
            'category': 'communication_style'
        }
    
    # DIRECTNESS feedback
    directness_keywords = ['direct', 'blunt', 'straight', 'to the point']
    if any(word in msg_lower for word in directness_keywords):
        return {
            'is_feedback': True,
            'feedback_type': 'style',
            'instruction': user_message,
            'category': 'communication_style'
        }
    
    # PATTERN observations (remember/don't forget)
    if 'remember' in msg_lower or 'don\'t forget' in msg_lower:
        
        # Work patterns
        if any(word in msg_lower for word in ['morning', 'afternoon', 'evening', 'night', 'time']):
            return {
                'is_feedback': True,
                'feedback_type': 'pattern',
                'instruction': user_message,
                'category': 'energy_patterns'
            }
        
        # Task preferences
        if any(word in msg_lower for word in ['task', 'work', 'project']):
            return {
                'is_feedback': True,
                'feedback_type': 'pattern',
                'instruction': user_message,
                'category': 'task_initiation'
            }
        
        # Communication preferences
        return {
            'is_feedback': True,
            'feedback_type': 'pattern',
            'instruction': user_message,
            'category': 'communication_style'
        }
    
    # General feedback
    return {
        'is_feedback': True,
        'feedback_type': 'general',
        'instruction': user_message,
        'category': 'communication_style'
    }


def apply_feedback(
    feedback_data: Dict,
    user_id: int,
    db: Session
) -> str:
    """
    Apply user feedback - save it as a high-confidence observation.
    
    Returns: Confirmation message for Sandy to include in response.
    """
    
    if not feedback_data.get('is_feedback'):
        return None
    
    learner = PatternLearningService(user_id, db)
    
    category = feedback_data.get('category', 'communication_style')
    instruction = feedback_data['instruction']
    feedback_type = feedback_data['feedback_type']
    
    # Save as HIGH confidence observation (user explicitly told us)
    learner.add_observation(
        category_name=category,
        observation=f"USER FEEDBACK: {instruction}",
        context={
            'feedback_type': feedback_type,
            'explicit_instruction': True,
            'confidence_boost': 40  # Higher confidence since user explicitly stated
        }
    )
    
    # Build hypothesis immediately from this feedback
    hypothesis = learner.build_hypothesis(category)
    if hypothesis:
        learner.save_hypothesis(
            category_name=category,
            hypothesis=hypothesis['hypothesis'],
            confidence=max(hypothesis['confidence'], 85)  # Boost confidence for explicit feedback
        )
    
    # Return confirmation based on feedback type
    if feedback_type == 'tone':
        return "Got it, adjusting my tone!"
    elif feedback_type == 'style':
        return "Understood, I'll adapt my style!"
    elif feedback_type == 'pattern':
        return "Noted! I'll remember that."
    else:
        return "Got it!"


# Example usage patterns:
FEEDBACK_EXAMPLES = """
User: "Sandy, be more direct with me"
→ Saves observation: "USER FEEDBACK: Sandy, be more direct with me"
→ Category: communication_style
→ Sandy responds: "Got it, adjusting my tone!"

User: "Remember I work best in the mornings"
→ Saves observation: "USER FEEDBACK: Remember I work best in the mornings"
→ Category: energy_patterns
→ Sandy responds: "Noted! I'll remember that."

User: "Stop asking so many questions, just tell me what to do"
→ Saves observation: "USER FEEDBACK: Stop asking so many questions, just tell me what to do"
→ Category: communication_style
→ Sandy responds: "Understood, I'll adapt my style!"

User: "I prefer when you're playful and tease me a bit"
→ Saves observation: "USER FEEDBACK: I prefer when you're playful and tease me a bit"
→ Category: communication_style
→ Sandy responds: "Got it, adjusting my tone!"
"""
