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
        context: Dict = None,
        sub_pattern: str = None  # NEW: Specific subpattern detected
    ):
        """Add a single observation to a category with optional subpattern."""
        
        # Get or create category
        category = self.db.query(PatternCategory).filter(
            PatternCategory.user_id == self.user_id,
            PatternCategory.category_name == category_name
        ).first()
        
        if not category:
            return  # Category doesn't exist
        
        # Add observation with subpattern
        obs = PatternObservation(
            user_id=self.user_id,
            category_id=category.id,
            sub_pattern=sub_pattern,  # ← Now saves specific subpattern!
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
        
        NOW CONSIDERS SUBPATTERNS!
        - Groups observations by subpattern
        - Forms hypothesis per subpattern when ≥3 observations
        - Also forms general category hypothesis
        """
        
        # Get all observations for this category
        observations = self.db.query(PatternObservation).filter(
            PatternObservation.category_id == category_id
        ).order_by(PatternObservation.observed_at.desc()).all()
        
        if len(observations) < 3:
            return  # Not enough data yet
        
        # Group by subpattern
        subpattern_groups = {}
        for obs in observations:
            sp = obs.sub_pattern or 'general'
            if sp not in subpattern_groups:
                subpattern_groups[sp] = []
            subpattern_groups[sp].append(obs)
        
        # Form hypothesis for each subpattern with ≥3 observations
        for sub_pattern, obs_list in subpattern_groups.items():
            if len(obs_list) >= 3:
                pattern_detected = self._detect_pattern(obs_list, sub_pattern)
                
                if pattern_detected:
                    # Find or create hypothesis for this subpattern
                    sp_value = None if sub_pattern == 'general' else sub_pattern
                    hypothesis = self.db.query(PatternHypothesis).filter(
                        PatternHypothesis.category_id == category_id,
                        PatternHypothesis.sub_pattern == sp_value
                    ).first()
                    
                    if not hypothesis:
                        hypothesis = PatternHypothesis(
                            user_id=self.user_id,
                            category_id=category_id,
                            sub_pattern=sp_value,
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
                    
                    # Flag for exploration if confidence is low
                    if len(obs_list) >= 10 and hypothesis.confidence < 30:
                        hypothesis.needs_exploration = True
                    
                    # Mark as confirmed if high confidence
                    if hypothesis.confidence >= 80:
                        hypothesis.status = 'confirmed'
        
        self.db.commit()
    
    def _detect_pattern(self, observations: List[PatternObservation], sub_pattern: str = None) -> Optional[Dict]:
        """
        Analyze observations to detect patterns.
        
        Enhanced with subpattern awareness!
        """
        
        if len(observations) < 3:
            return None
        
        # Get category
        category = self.db.query(PatternCategory).get(observations[0].category_id)
        
        # Import subpattern descriptions
        from app.services.subpatterns import get_subpattern_description
        
        # Build hypothesis text
        if sub_pattern and sub_pattern != 'general':
            sp_desc = get_subpattern_description(category.category_name, sub_pattern)
            if sp_desc:
                hypothesis_text = f"{sp_desc} (observed {len(observations)} times)"
            else:
                hypothesis_text = f"Pattern: {sub_pattern} (observed {len(observations)} times)"
        else:
            # General category hypothesis
            hypothesis_text = f"Pattern emerging in {category.category_name.replace('_', ' ')} ({len(observations)} observations)"
        
        # Calculate confidence (simple for now)
        # Base: 10 per observation, max 100
        # Adjusted by recency (more recent = higher confidence)
        base_confidence = min(len(observations) * 10, 100)
        
        return {
            'hypothesis': hypothesis_text,
            'confidence': base_confidence,
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
        """Get patterns Sandy is confident about (including subpatterns)."""
        
        hypotheses = self.db.query(PatternHypothesis).join(PatternCategory).filter(
            PatternHypothesis.user_id == self.user_id,
            PatternHypothesis.confidence >= min_confidence,
            PatternHypothesis.status == 'confirmed'
        ).order_by(PatternHypothesis.confidence.desc()).all()
        
        results = []
        for hyp in hypotheses:
            category = self.db.query(PatternCategory).get(hyp.category_id)
            results.append({
                'category': category.category_name,
                'sub_pattern': hyp.sub_pattern,  # NEW: Include subpattern
                'hypothesis': hyp.hypothesis,
                'confidence': hyp.confidence,
                'supporting_observations': hyp.supporting_observations
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
