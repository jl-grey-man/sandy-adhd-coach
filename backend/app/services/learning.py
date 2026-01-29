"""Real-time learning system for Sandy."""
from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy.orm import Session

from app.models.learned_pattern import LearnedPattern
from app.models.exploration_topic import ExplorationTopic


class RealTimeLearning:
    """Analyzes interactions and updates learned patterns in real-time."""
    
    def __init__(self, user_id: int, db: Session):
        self.user_id = user_id
        self.db = db
    
    def analyze_interaction(
        self,
        user_message: str,
        sandy_response: str,
        action_taken: Dict = None
    ) -> List[Dict]:
        """Extract learnings from a single interaction."""
        
        learnings = []
        user_lower = user_message.lower()
        
        # COMPLETION PATTERNS
        if action_taken and action_taken.get('success'):
            action_type = action_taken.get('action_type')
            
            if action_type == 'create_task':
                learnings.append({
                    'category': 'task_creation',
                    'pattern': 'Creates tasks proactively when discussing work',
                    'confidence': 55,
                    'evidence': f'Created task: {action_taken.get("details", {}).get("title")}'
                })
        
        # DEFLECTION PATTERNS
        deflection_phrases = ['later', 'maybe', 'not sure', "i don't know", 'eventually']
        if any(phrase in user_lower for phrase in deflection_phrases):
            matched = [p for p in deflection_phrases if p in user_lower][0]
            learnings.append({
                'category': 'avoidance_patterns',
                'pattern': f'Uses "{matched}" when avoiding tasks',
                'confidence': 50,
                'evidence': user_message[:100]
            })
        
        # ENGAGEMENT PATTERNS
        if len(user_message) > 100:
            learnings.append({
                'category': 'communication_style',
                'pattern': 'Engages deeply with open-ended questions',
                'confidence': 55
            })
        elif len(user_message) < 20:
            learnings.append({
                'category': 'communication_style',
                'pattern': 'Prefers brief, direct exchanges',
                'confidence': 52
            })
        
        # TIME-BASED PRODUCTIVITY
        hour = datetime.now().hour
        if action_taken and action_taken.get('success'):
            if 6 <= hour <= 11:
                learnings.append({
                    'category': 'productivity_time',
                    'pattern': 'Most productive in morning hours (6am-11am)',
                    'confidence': 60
                })
            elif 14 <= hour <= 17:
                learnings.append({
                    'category': 'productivity_time',
                    'pattern': 'Productive in afternoon hours (2pm-5pm)',
                    'confidence': 58
                })
            elif hour >= 20 or hour <= 5:
                learnings.append({
                    'category': 'productivity_time',
                    'pattern': 'Active during late evening/night hours',
                    'confidence': 55
                })
        
        # ENERGY INDICATORS
        energy_low = ['tired', 'exhausted', 'drained', 'no energy', 'burned out']
        energy_high = ['energized', 'ready', 'pumped', 'motivated', 'focused']
        
        if any(phrase in user_lower for phrase in energy_low):
            learnings.append({
                'category': 'energy_patterns',
                'pattern': f'Reports low energy - mentioned: {[p for p in energy_low if p in user_lower][0]}',
                'confidence': 65
            })
        elif any(phrase in user_lower for phrase in energy_high):
            learnings.append({
                'category': 'energy_patterns',
                'pattern': 'Reports high energy when motivated',
                'confidence': 62
            })
        
        # OVERWHELM INDICATORS
        overwhelm_phrases = ['overwhelmed', 'too much', 'so much to do', 'drowning', "can't handle"]
        if any(phrase in user_lower for phrase in overwhelm_phrases):
            learnings.append({
                'category': 'stress_triggers',
                'pattern': 'Experiences overwhelm when workload is high',
                'confidence': 70
            })
        
        return learnings
    
    def apply_learnings(self, learnings: List[Dict]):
        """Update database with extracted learnings."""
        
        for learning in learnings:
            # Check if similar pattern exists
            existing = self.db.query(LearnedPattern).filter(
                LearnedPattern.user_id == self.user_id,
                LearnedPattern.category == learning['category'],
                LearnedPattern.pattern.ilike(f"%{learning['pattern'][:30]}%")
            ).first()
            
            if existing:
                # Reinforce existing pattern
                existing.confidence = min(existing.confidence + 5, 100)
                existing.updated_at = datetime.utcnow()
                if learning.get('evidence'):
                    existing.evidence = learning['evidence']
            else:
                # Create new pattern
                new_pattern = LearnedPattern(
                    user_id=self.user_id,
                    category=learning['category'],
                    pattern=learning['pattern'],
                    evidence=learning.get('evidence'),
                    confidence=learning['confidence']
                )
                self.db.add(new_pattern)
        
        self.db.commit()
    
    def get_high_confidence_patterns(self, min_confidence: int = 75) -> List[LearnedPattern]:
        """Get patterns Sandy is confident about."""
        return self.db.query(LearnedPattern).filter(
            LearnedPattern.user_id == self.user_id,
            LearnedPattern.confidence >= min_confidence
        ).order_by(LearnedPattern.confidence.desc()).all()
    
    def update_exploration_score(self, topic: str, insights: Dict = None):
        """Update understanding score for an exploration topic."""
        
        topic_record = self.db.query(ExplorationTopic).filter(
            ExplorationTopic.user_id == self.user_id,
            ExplorationTopic.topic == topic
        ).first()
        
        if topic_record:
            # Increase understanding by 15 points per exploration
            topic_record.understanding_score = min(
                topic_record.understanding_score + 15,
                100
            )
            
            # Add insights
            if insights:
                current_insights = topic_record.key_insights or {}
                current_insights.update(insights)
                topic_record.key_insights = current_insights
            
            # Mark as discussed
            topic_record.last_discussed = datetime.utcnow()
            
            self.db.commit()
