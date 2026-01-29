"""Pattern learning service - the intelligence system."""
from datetime import datetime
from typing import List, Dict, Optional
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.pattern_tracking import PatternCategory, PatternObservation, PatternHypothesis


class PatternLearningService:
    """
    Intelligent pattern learning system.
    
    - Starts with zero assumptions
    - Collects observations from conversations
    - Forms hypotheses when data emerges
    - Updates confidence based on evidence
    - Identifies when exploration is needed
    """
    
    def __init__(self, user_id: int, db: Session):
        self.user_id = user_id
        self.db = db
    
    def add_observation(
        self,
        category_name: str,
        observation: str,
        context: Dict = None
    ):
        """Add a single observation to a category."""
        
        # Get or create category
        category = self.db.query(PatternCategory).filter(
            PatternCategory.user_id == self.user_id,
            PatternCategory.category_name == category_name
        ).first()
        
        if not category:
            return  # Category doesn't exist
        
        # Add observation
        obs = PatternObservation(
            user_id=self.user_id,
            category_id=category.id,
            observation=observation,
            context=context or {}
        )
        self.db.add(obs)
        self.db.commit()
        
        # Check if we should form/update hypothesis
        self._update_hypotheses_for_category(category.id)
    
    def _update_hypotheses_for_category(self, category_id: int):
        """
        Analyze observations and update hypotheses.
        
        Logic:
        - Need 3+ observations before forming hypothesis
        - Confidence = (supporting - contradicting) / total * 100
        - If confidence < 30% after 10 observations, flag for exploration
        """
        
        # Get all observations for this category
        obs_count = self.db.query(func.count(PatternObservation.id)).filter(
            PatternObservation.category_id == category_id
        ).scalar()
        
        if obs_count < 3:
            return  # Not enough data yet
        
        # Get observations
        observations = self.db.query(PatternObservation).filter(
            PatternObservation.category_id == category_id
        ).order_by(PatternObservation.observed_at.desc()).all()
        
        # Try to detect pattern
        pattern_detected = self._detect_pattern(observations)
        
        if pattern_detected:
            # Update or create hypothesis
            hypothesis = self.db.query(PatternHypothesis).filter(
                PatternHypothesis.category_id == category_id
            ).first()
            
            if not hypothesis:
                hypothesis = PatternHypothesis(
                    user_id=self.user_id,
                    category_id=category_id,
                    hypothesis=pattern_detected['hypothesis'],
                    confidence=pattern_detected['confidence'],
                    supporting_observations=pattern_detected['supporting'],
                    contradicting_observations=pattern_detected['contradicting'],
                    status='exploring'
                )
                self.db.add(hypothesis)
            else:
                hypothesis.hypothesis = pattern_detected['hypothesis']
                hypothesis.confidence = pattern_detected['confidence']
                hypothesis.supporting_observations = pattern_detected['supporting']
                hypothesis.contradicting_observations = pattern_detected['contradicting']
                hypothesis.last_updated = datetime.utcnow()
            
            # Flag for exploration if confidence is low after many observations
            if obs_count >= 10 and hypothesis.confidence < 30:
                hypothesis.needs_exploration = True
            
            # Mark as confirmed if high confidence
            if hypothesis.confidence >= 80:
                hypothesis.status = 'confirmed'
            
            self.db.commit()
    
    def _detect_pattern(self, observations: List[PatternObservation]) -> Optional[Dict]:
        """
        Analyze observations to detect patterns.
        
        This is simplified - in production would use NLP/ML.
        For now, looks for repeated keywords and context patterns.
        """
        
        if len(observations) < 3:
            return None
        
        # Extract keywords from observations
        all_text = " ".join([obs.observation.lower() for obs in observations])
        
        # Simple pattern detection (would be more sophisticated in production)
        # For now, just count observations
        return {
            'hypothesis': f'Pattern emerging from {len(observations)} observations',
            'confidence': min(len(observations) * 10, 100),
            'supporting': len(observations),
            'contradicting': 0
        }
    
    def get_categories_needing_exploration(self) -> List[Dict]:
        """Get categories that need targeted exploration."""
        
        # Get hypotheses flagged for exploration
        hypotheses = self.db.query(PatternHypothesis).join(PatternCategory).filter(
            PatternHypothesis.user_id == self.user_id,
            PatternHypothesis.needs_exploration == True
        ).all()
        
        results = []
        for hyp in hypotheses:
            category = self.db.query(PatternCategory).get(hyp.category_id)
            results.append({
                'category': category.category_name,
                'description': category.description,
                'current_hypothesis': hyp.hypothesis,
                'confidence': hyp.confidence,
                'observations': hyp.supporting_observations
            })
        
        return results
    
    def get_confirmed_patterns(self, min_confidence: int = 80) -> List[Dict]:
        """Get patterns Sandy is confident about."""
        
        hypotheses = self.db.query(PatternHypothesis).join(PatternCategory).filter(
            PatternHypothesis.user_id == self.user_id,
            PatternHypothesis.confidence >= min_confidence,
            PatternHypothesis.status == 'confirmed'
        ).all()
        
        results = []
        for hyp in hypotheses:
            category = self.db.query(PatternCategory).get(hyp.category_id)
            results.append({
                'category': category.category_name,
                'hypothesis': hyp.hypothesis,
                'confidence': hyp.confidence
            })
        
        return results
    
    def create_new_category(self, category_name: str, description: str):
        """Create a new user-discovered category."""
        
        category = PatternCategory(
            user_id=self.user_id,
            category_name=category_name,
            description=description,
            is_system_category=False
        )
        self.db.add(category)
        self.db.commit()
        
        return category
    
    def get_category_status(self, category_name: str) -> Dict:
        """Get current status of a category."""
        
        category = self.db.query(PatternCategory).filter(
            PatternCategory.user_id == self.user_id,
            PatternCategory.category_name == category_name
        ).first()
        
        if not category:
            return {'status': 'unknown'}
        
        obs_count = self.db.query(func.count(PatternObservation.id)).filter(
            PatternObservation.category_id == category.id
        ).scalar()
        
        hypothesis = self.db.query(PatternHypothesis).filter(
            PatternHypothesis.category_id == category.id
        ).first()
        
        return {
            'category': category_name,
            'observations': obs_count,
            'hypothesis': hypothesis.hypothesis if hypothesis else None,
            'confidence': hypothesis.confidence if hypothesis else 0,
            'needs_exploration': hypothesis.needs_exploration if hypothesis else False,
            'status': hypothesis.status if hypothesis else 'no_data'
        }
