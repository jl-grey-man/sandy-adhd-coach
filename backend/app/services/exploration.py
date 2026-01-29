"""Exploration system using pattern_categories."""
from datetime import datetime
from typing import Optional, List, Dict
from sqlalchemy.orm import Session
from sqlalchemy import func

from app.models.pattern_tracking import PatternCategory, PatternObservation, PatternHypothesis


class ExplorationService:
    """Manage exploration using the pattern learning system."""
    
    def __init__(self, user_id: int, db: Session):
        self.user_id = user_id
        self.db = db
    
    def pick_next_category(self) -> Optional[Dict]:
        """
        Pick next category to explore based on:
        - Needs exploration flag (highest priority)
        - Low confidence with few observations
        - Never explored categories
        
        Returns category info ready for exploration.
        """
        
        # First priority: Categories explicitly flagged for exploration
        flagged = self.db.query(PatternHypothesis).join(PatternCategory).filter(
            PatternHypothesis.user_id == self.user_id,
            PatternHypothesis.needs_exploration == True
        ).first()
        
        if flagged:
            category = self.db.query(PatternCategory).get(flagged.category_id)
            return self._format_for_exploration(category, flagged)
        
        # Second priority: Categories with low observations (<3)
        categories = self.db.query(PatternCategory).filter(
            PatternCategory.user_id == self.user_id
        ).all()
        
        for category in categories:
            obs_count = self.db.query(func.count(PatternObservation.id)).filter(
                PatternObservation.category_id == category.id
            ).scalar()
            
            if obs_count < 3:
                return self._format_for_exploration(category, None)
        
        # Third priority: Low confidence categories
        low_confidence = self.db.query(PatternHypothesis).join(PatternCategory).filter(
            PatternHypothesis.user_id == self.user_id,
            PatternHypothesis.confidence < 50
        ).order_by(PatternHypothesis.confidence.asc()).first()
        
        if low_confidence:
            category = self.db.query(PatternCategory).get(low_confidence.category_id)
            return self._format_for_exploration(category, low_confidence)
        
        return None
    
    def get_category_by_name(self, category_name: str) -> Optional[Dict]:
        """Get specific category for exploration."""
        
        category = self.db.query(PatternCategory).filter(
            PatternCategory.user_id == self.user_id,
            PatternCategory.category_name.ilike(f"%{category_name}%")
        ).first()
        
        if not category:
            return None
        
        hypothesis = self.db.query(PatternHypothesis).filter(
            PatternHypothesis.category_id == category.id
        ).first()
        
        return self._format_for_exploration(category, hypothesis)
    
    def _format_for_exploration(
        self,
        category: PatternCategory,
        hypothesis: Optional[PatternHypothesis]
    ) -> Dict:
        """Format category info for exploration prompt."""
        
        obs_count = self.db.query(func.count(PatternObservation.id)).filter(
            PatternObservation.category_id == category.id
        ).scalar()
        
        return {
            'category_id': category.id,
            'category_name': category.category_name,
            'description': category.description,
            'observations': obs_count,
            'hypothesis': hypothesis.hypothesis if hypothesis else None,
            'confidence': hypothesis.confidence if hypothesis else 0,
            'needs_exploration': hypothesis.needs_exploration if hypothesis else False
        }
    
    def get_exploration_guidance(self, category_name: str) -> str:
        """
        Get exploration questions/guidance for a specific category.
        
        Based on 18_CATEGORIES_WITH_SUBPATTERNS.md
        """
        
        questions = {
            'task_initiation': [
                "What actually gets you started on tasks?",
                "Do you work better when someone else is around or on a call?",
                "Are external deadlines more effective than self-imposed ones?",
                "Do you need a specific routine or trigger before starting work?"
            ],
            'hyperfocus_triggers': [
                "When do you get into deep focus - what's different about those times?",
                "Is it the type of work (creative vs analytical) or something else?",
                "Does time pressure help you focus or make it harder?",
                "What's the sweet spot between too easy and too hard for you?"
            ],
            'avoidance_reasons': [
                "When you avoid a task, what's usually the real reason?",
                "Is it that you don't know how to start, or something else?",
                "Do you avoid boring tasks differently than scary ones?",
                "Does not knowing exactly what 'done' looks like make you avoid it?"
            ],
            'context_switching_cost': [
                "How do you handle switching between different types of tasks?",
                "Do interruptions kill your entire session or can you recover?",
                "Is it easier to switch between similar tasks than totally different ones?",
                "How much time do you need between different projects?"
            ],
            'energy_curves': [
                "What drains your energy the most?",
                "Do meetings energize you or wipe you out?",
                "How does food timing affect your energy?",
                "Does creative work give you energy or take it?"
            ],
            'motivation_sources': [
                "What actually motivates you to complete tasks?",
                "Is external validation important or not really?",
                "Do you work better on tasks that help others vs. yourself?",
                "Does competition or challenge drive you?"
            ],
            'reward_sensitivity': [
                "What kind of rewards actually motivate you?",
                "Do you need immediate rewards or does long-term payoff work?",
                "Is finishing a task itself satisfying, or do you need something else?",
                "Can you self-reward effectively or needs external?"
            ],
            'decision_fatigue': [
                "When do you notice your decision-making gets harder?",
                "Do too many options make it harder to choose?",
                "What time of day are decisions easiest for you?",
                "Do small decisions throughout the day drain you?"
            ],
            'accountability_effectiveness': [
                "What type of accountability actually works for you?",
                "Are hard external deadlines more effective than soft ones?",
                "Do check-ins help or just add pressure?",
                "Does public commitment motivate you or create anxiety?"
            ],
            'task_breakdown_needs': [
                "Do large projects overwhelm you without structure?",
                "Do you prefer detailed steps or general direction?",
                "Is it just the first step that needs to be clear?",
                "Do you like figuring it out yourself or want guidance?"
            ],
            'interruption_recovery': [
                "When you're interrupted, how long does it take to get back?",
                "Do interruptions kill your session or can you recover?",
                "Does leaving notes help you resume?",
                "Are some types of interruptions worse than others?"
            ],
            'momentum_building': [
                "How do you build momentum for work?",
                "Do quick wins help you tackle bigger tasks?",
                "Do you need a warmup or go straight for hard stuff?",
                "Is there a routine that gets you into work mode?"
            ],
            'failure_response': [
                "How do you handle it when things don't go as planned?",
                "Do you bounce back quickly or need processing time?",
                "Does 'what did we learn' help or feel patronizing?",
                "Do small failures hit harder than big ones?"
            ],
            'novelty_seeking': [
                "How quickly do you get bored with the same project?",
                "Do you thrive on routine or need constant newness?",
                "Do you prefer mastering one thing or exploring many?",
                "How often do you need a new challenge?"
            ],
            'sensory_environment': [
                "What environment helps you work best?",
                "Music, silence, or background noise?",
                "Does a clean or messy desk make a difference?",
                "Specific location or doesn't matter?"
            ],
            'communication_response': [
                "What tone works best when I'm pushing you on something?",
                "Do you respond better to direct push or gentle suggestion?",
                "Does playful teasing work or shut you down?",
                "Do you want data/logic or emotional support?"
            ],
            'time_perception': [
                "How accurate are you at estimating how long tasks take?",
                "Do you usually under or overestimate?",
                "Does it depend on the type of task?",
                "Do you have time blindness during hyperfocus?"
            ],
            'urgency_response': [
                "How do you respond to deadline pressure?",
                "Do you thrive under pressure or freeze up?",
                "Do you wait until the last minute then execute perfectly?",
                "Is slight pressure helpful but extreme panic bad?"
            ]
        }
        
        return questions.get(category_name, [
            "Tell me more about this area",
            "When have you noticed patterns here?",
            "What works and what doesn't?"
        ])
    
    def record_exploration_session(
        self,
        category_id: int,
        insights: List[str],
        confidence_increase: int = 15
    ):
        """
        Record exploration session results.
        
        - Adds observations from insights
        - Increases hypothesis confidence
        - Clears needs_exploration flag if confidence high enough
        """
        
        from app.services.pattern_learning import PatternLearningService
        
        learner = PatternLearningService(self.user_id, self.db)
        category = self.db.query(PatternCategory).get(category_id)
        
        # Add each insight as an observation
        for insight in insights:
            learner.add_observation(
                category_name=category.category_name,
                observation=insight,
                context={'source': 'exploration_session'}
            )
        
        # Update hypothesis confidence
        hypothesis = self.db.query(PatternHypothesis).filter(
            PatternHypothesis.category_id == category_id
        ).first()
        
        if hypothesis:
            hypothesis.confidence = min(hypothesis.confidence + confidence_increase, 100)
            
            # Clear exploration flag if confidence now high
            if hypothesis.confidence >= 70:
                hypothesis.needs_exploration = False
            
            hypothesis.last_updated = datetime.utcnow()
            self.db.commit()
    
    def get_all_categories_status(self) -> List[Dict]:
        """Get status of all pattern categories."""
        
        categories = self.db.query(PatternCategory).filter(
            PatternCategory.user_id == self.user_id
        ).all()
        
        results = []
        for cat in categories:
            obs_count = self.db.query(func.count(PatternObservation.id)).filter(
                PatternObservation.category_id == cat.id
            ).scalar()
            
            hyp = self.db.query(PatternHypothesis).filter(
                PatternHypothesis.category_id == cat.id
            ).first()
            
            results.append({
                'category': cat.category_name,
                'description': cat.description,
                'observations': obs_count,
                'confidence': hyp.confidence if hyp else 0,
                'hypothesis': hyp.hypothesis if hyp else None,
                'needs_exploration': hyp.needs_exploration if hyp else False
            })
        
        return results
