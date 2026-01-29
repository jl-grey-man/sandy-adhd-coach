"""
ADVANCED LEARNING CATEGORIES FOR SANDY
=======================================

Beyond basic patterns, track these ADHD-specific behaviors:
"""

LEARNING_CATEGORIES = {
    # TASK EXECUTION
    "task_initiation": {
        "description": "What actually gets you started on tasks",
        "patterns": [
            "Body doubling (working while on call)",
            "External deadline pressure",
            "Accountability (someone waiting)",
            "Momentum from small win",
            "After specific trigger (coffee, walk)",
            "Curiosity/novelty",
            "Spite/proving something"
        ],
        "example": "Completes tasks 80% more with external accountability"
    },
    
    "hyperfocus_triggers": {
        "description": "What puts you in the zone",
        "patterns": [
            "Creative vs analytical tasks",
            "Time pressure (deadline dopamine)",
            "High interest level",
            "Novelty factor",
            "Optimal challenge level"
        ],
        "example": "Hyperfocuses on creative tasks with music and tight deadline"
    },
    
    "avoidance_reasons": {
        "description": "WHY you avoid specific tasks",
        "patterns": [
            "Unclear what 'done' looks like",
            "Too many steps (needs breakdown)",
            "Boring/tedious nature",
            "Decision paralysis",
            "Perfectionism trap",
            "Fear of judgment",
            "Requires sustained attention"
        ],
        "example": "Avoids tasks with 'research' - needs structure first"
    },
    
    # ENERGY & CONTEXT
    "context_switching_cost": {
        "description": "How you handle switching between tasks",
        "patterns": [
            "Better with similar tasks grouped",
            "Needs transition time",
            "Loses momentum with interruptions",
            "Thrives on variety vs deep focus"
        ],
        "example": "Works best on 1 project per day, switching kills momentum"
    },
    
    "energy_curves": {
        "description": "What drains vs energizes you beyond time of day",
        "patterns": [
            "Social interaction effect",
            "Creative work impact",
            "Admin task drain",
            "Movement/exercise boost",
            "Food/caffeine timing"
        ],
        "example": "Energy crashes after meetings, needs 30min buffer"
    },
    
    # MOTIVATION
    "motivation_sources": {
        "description": "What actually drives you to action",
        "patterns": [
            "External validation",
            "Progress visualization",
            "Competition/challenge",
            "Helping others",
            "Personal interest",
            "Financial pressure"
        ],
        "example": "Motivated by external validation > internal goals"
    },
    
    "reward_sensitivity": {
        "description": "What rewards motivate you",
        "patterns": [
            "Immediate gratification",
            "Long-term payoff",
            "Social approval",
            "Financial gain",
            "Completion satisfaction",
            "New challenge unlocked"
        ],
        "example": "Works best when task = ticket to something he wants"
    },
    
    # DECISION MAKING
    "decision_fatigue": {
        "description": "When you hit decision paralysis",
        "patterns": [
            "Too many options",
            "No clear best choice",
            "High stakes pressure",
            "End of day depletion",
            "After many small decisions"
        ],
        "example": "Makes best decisions in morning, struggles after 3pm"
    },
    
    # ACCOUNTABILITY
    "accountability_effectiveness": {
        "description": "What type of accountability works for you",
        "patterns": [
            "Hard deadlines (external)",
            "Soft deadlines (self-imposed)",
            "Check-ins with someone",
            "Public commitment",
            "Consequences",
            "Rewards"
        ],
        "example": "External deadlines work 90%, self-imposed 20%"
    },
    
    # TASK STRUCTURE
    "task_breakdown_needs": {
        "description": "How much structure you need",
        "patterns": [
            "Overwhelmed by large projects",
            "Benefits from step-by-step",
            "Prefers autonomy",
            "Needs only first step clear"
        ],
        "example": "Completes when first step crystal clear, doesn't need full breakdown"
    },
    
    # RECOVERY & MOMENTUM
    "interruption_recovery": {
        "description": "How you handle being interrupted",
        "patterns": [
            "Gets back on track quickly",
            "Loses entire session",
            "Needs warmup time",
            "Benefits from breadcrumbs/notes"
        ],
        "example": "Interruptions kill session, best to batch uninterrupted time"
    },
    
    "momentum_building": {
        "description": "How you build work momentum",
        "patterns": [
            "Small wins cascade",
            "Needs warm-up tasks",
            "Goes straight for hard stuff",
            "Benefits from routine/ritual"
        ],
        "example": "Momentum from 2-3 quick wins, then tackles big stuff"
    },
    
    # EMOTIONAL
    "failure_response": {
        "description": "How you handle setbacks",
        "patterns": [
            "Catastrophizes and spirals",
            "Bounces back quickly",
            "Needs processing time",
            "Benefits from reframe"
        ],
        "example": "After missing deadline, needs 1 day before pushing again"
    },
    
    # NOVELTY & EXPLORATION
    "novelty_seeking": {
        "description": "How much novelty you need",
        "patterns": [
            "Gets bored quickly with repetition",
            "Thrives on routine/structure",
            "Needs new challenge regularly",
            "Explore vs exploit balance"
        ],
        "example": "Loses interest after 3 weeks on same project"
    },
    
    # ENVIRONMENT
    "sensory_environment": {
        "description": "What environment helps you work",
        "patterns": [
            "Music type/volume",
            "Silence vs background noise",
            "Specific location",
            "Clean vs messy space",
            "Temperature/lighting"
        ],
        "example": "Works best with instrumental music, clean desk"
    },
    
    # COMMUNICATION
    "communication_response": {
        "description": "What tone/approach works for you",
        "patterns": [
            "Direct push",
            "Gentle suggestion",
            "Question-based",
            "Playful teasing",
            "Serious concern",
            "Data-driven logic"
        ],
        "example": "Responds best to playful challenge, not soft suggestions"
    },
    
    # TIME
    "time_perception": {
        "description": "How you estimate time",
        "patterns": [
            "Optimistic (underestimates)",
            "Pessimistic (overestimates)",
            "Accurate",
            "Time blindness"
        ],
        "example": "Estimates tasks at 50% of actual time needed"
    },
    
    "urgency_response": {
        "description": "How you respond to urgency",
        "patterns": [
            "Thrives under pressure",
            "Freezes/panics",
            "Last-minute rush saves him",
            "Needs buffer time"
        ],
        "example": "Waits until last 20% of time, then executes perfectly"
    }
}


# How to track these in real-time:

def analyze_advanced_patterns(interaction_history, task_completion_data):
    """
    Examples of what to detect:
    
    TASK INITIATION:
    - If tasks with external deadline complete 80% vs self-imposed 20%
      → Learn: "External deadlines are key trigger"
    
    HYPERFOCUS:
    - If tasks labeled "creative" take 50% estimated time when completed
      → Learn: "Hyperfocuses on creative work"
    
    AVOIDANCE:
    - If tasks with "research" sit 2x longer than other tasks
      → Learn: "Avoids research tasks - needs structure"
    
    ENERGY:
    - If completion rate drops 60% after 3pm
      → Learn: "Energy crashes afternoon"
    
    COMMUNICATION:
    - If playful push → 70% completion vs gentle suggestion → 30%
      → Learn: "Responds best to direct challenge"
    
    TIME PERCEPTION:
    - If actual time = 2x estimated time consistently
      → Learn: "Underestimates by 50% - double his estimates"
    """
    pass
