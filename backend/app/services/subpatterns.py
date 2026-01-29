"""
SUBPATTERN DEFINITIONS - Machine-readable format for learning system
"""

# Map of category -> list of (subpattern_key, keywords, description)
SUBPATTERNS = {
    "task_initiation": [
        ("body_doubling", ["call", "zoom", "working with", "on call"], "Working while on call with someone"),
        ("external_deadline", ["deadline", "due", "urgency", "urgent"], "External deadline pressure"),
        ("accountability", ["waiting", "expecting", "someone needs"], "Someone waiting/expecting it"),
        ("momentum", ["small win", "quick", "easy one"], "Momentum from small win"),
        ("trigger", ["coffee", "walk", "after", "shower"], "After specific trigger (coffee, walk)"),
        ("curiosity", ["interesting", "curious", "want to know"], "Curiosity/novelty driven"),
        ("spite", ["prove", "show them", "wrong"], "Spite/proving something")
    ],
    
    "hyperfocus_triggers": [
        ("creative", ["creative", "design", "write", "build"], "Creative tasks"),
        ("time_pressure", ["deadline", "rush", "last minute"], "Time pressure"),
        ("high_interest", ["interesting", "exciting", "fun"], "High interest level"),
        ("novelty", ["new", "novel", "different", "first time"], "Novelty factor"),
        ("challenge", ["challenge", "hard", "complex"], "Optimal challenge level")
    ],
    
    "avoidance_reasons": [
        ("unclear_done", ["don't know", "unclear", "what does done"], "Unclear what 'done' looks like"),
        ("too_many_steps", ["too much", "so many", "steps", "complicated"], "Too many steps"),
        ("boring", ["boring", "tedious", "dull", "monotonous"], "Boring/tedious nature"),
        ("decision_paralysis", ["don't know which", "options", "choose"], "Decision paralysis"),
        ("perfectionism", ["perfect", "not ready", "not good enough"], "Perfectionism trap"),
        ("fear_judgment", ["what will they", "worried", "scared"], "Fear of judgment"),
        ("sustained_attention", ["focus", "concentration", "attention"], "Requires sustained attention")
    ],
    
    "energy_patterns": [
        ("high_energy", ["ready", "pumped", "energized", "motivated", "let's go"], "High energy state"),
        ("low_energy", ["tired", "exhausted", "drained", "overwhelmed"], "Low energy state"),
        ("after_social", ["after meeting", "after call", "socializing"], "Energy after social interaction"),
        ("creative_boost", ["creative work", "designing", "writing"], "Creative work energy impact"),
        ("admin_drain", ["admin", "emails", "paperwork"], "Admin task energy drain")
    ],
    
    "motivation_sources": [
        ("external_validation", ["they'll like", "approval", "impress"], "External validation"),
        ("progress_viz", ["see progress", "tracking", "checking off"], "Progress visualization"),
        ("competition", ["compete", "challenge", "beat", "win"], "Competition/challenge"),
        ("helping_others", ["help", "for them", "they need"], "Helping others"),
        ("personal_interest", ["interested", "want to", "curious"], "Personal interest"),
        ("financial", ["money", "paid", "income", "revenue"], "Financial pressure")
    ],
    
    "communication_response": [
        ("direct_push", ["real reason", "actually", "what's really"], "Direct push/challenge"),
        ("gentle", ["maybe", "perhaps", "could"], "Gentle suggestion"),
        ("question_based", ["what if", "have you", "would it"], "Question-based"),
        ("playful", ["really?", "sure about that", "right..."], "Playful teasing"),
        ("serious", ["this is important", "needs to happen"], "Serious concern"),
        ("data_driven", ["data shows", "numbers", "evidence"], "Data-driven logic")
    ],
    
    "time_perception": [
        ("optimistic", ["just", "only", "quick"], "Optimistic/underestimates"),
        ("pessimistic", ["long", "forever", "takes ages"], "Pessimistic/overestimates"),
        ("accurate", ["about", "roughly", "around"], "Accurate estimation"),
        ("time_blindness", ["lose track", "didn't realize", "flew by"], "Time blindness")
    ],
    
    "urgency_response": [
        ("thrives_pressure", ["deadline helps", "pressure works", "best under"], "Thrives under pressure"),
        ("freezes", ["panic", "overwhelm", "can't"], "Freezes/panics"),
        ("last_minute", ["last minute", "wait until", "night before"], "Last-minute rush"),
        ("needs_buffer", ["need time", "cushion", "backup time"], "Needs buffer time")
    ],
    
    "accountability_effectiveness": [
        ("hard_deadlines", ["deadline", "due date", "must be"], "Hard external deadlines"),
        ("soft_deadlines", ["should", "hoping to", "trying to"], "Soft self-imposed deadlines"),
        ("check_ins", ["check in", "update", "report"], "Check-ins with someone"),
        ("public", ["told people", "public", "announced"], "Public commitment"),
        ("consequences", ["lose", "miss out", "penalty"], "Consequences"),
        ("rewards", ["get", "earn", "treat"], "Rewards")
    ],
    
    "context_switching_cost": [
        ("grouped_similar", ["batch", "group", "similar"], "Better with tasks grouped"),
        ("needs_transition", ["transition", "switch", "change"], "Needs transition time"),
        ("loses_momentum", ["momentum", "flow", "zone"], "Loses momentum with interruptions"),
        ("variety_thrives", ["variety", "different", "mix"], "Thrives on variety")
    ],
    
    "momentum_building": [
        ("small_wins", ["quick win", "easy one", "small"], "Small wins cascade"),
        ("warmup", ["warm up", "ease in", "start small"], "Needs warm-up tasks"),
        ("hard_first", ["hardest first", "big one", "tackle"], "Goes for hard stuff first"),
        ("routine", ["routine", "ritual", "always"], "Benefits from routine")
    ],
    
    "novelty_seeking": [
        ("bores_quickly", ["bored", "same thing", "repetitive"], "Gets bored with repetition"),
        ("thrives_routine", ["routine", "structure", "same"], "Thrives on routine/structure"),
        ("new_challenge", ["new", "different", "challenge"], "Needs new challenge regularly"),
        ("explore_exploit", ["explore", "try new", "experiment"], "Explore vs exploit balance")
    ],
    
    "sensory_environment": [
        ("music", ["music", "playlist", "listening"], "Music preferences"),
        ("silence", ["quiet", "silence", "no noise"], "Silence needs"),
        ("location", ["office", "cafe", "home"], "Location preferences"),
        ("clean_space", ["clean", "organized", "tidy"], "Clean vs messy space"),
        ("temperature", ["warm", "cold", "hot"], "Temperature needs")
    ],
    
    "decision_fatigue": [
        ("too_many_options", ["so many", "options", "choices"], "Too many options"),
        ("no_clear_best", ["don't know which", "unclear", "all seem"], "No clear best choice"),
        ("high_stakes", ["important", "big decision", "matters"], "High stakes pressure"),
        ("time_depletion", ["afternoon", "end of day", "tired"], "End of day depletion"),
        ("many_small", ["so many little", "decisions"], "After many small decisions")
    ],
    
    "task_breakdown_needs": [
        ("overwhelmed_large", ["too big", "huge", "overwhelming"], "Overwhelmed by large projects"),
        ("step_by_step", ["steps", "breakdown", "sequence"], "Benefits from step-by-step"),
        ("autonomy", ["figure it out", "own way", "freedom"], "Prefers autonomy"),
        ("first_step", ["first step", "start", "beginning"], "Needs only first step clear")
    ],
    
    "interruption_recovery": [
        ("quick_recovery", ["back to it", "resume", "continue"], "Gets back on track quickly"),
        ("loses_session", ["lost it", "momentum gone", "can't get back"], "Loses entire session"),
        ("warmup_needed", ["need to", "get back into"], "Needs warmup time"),
        ("breadcrumbs", ["notes", "where was I", "reminder"], "Benefits from breadcrumbs")
    ],
    
    "failure_response": [
        ("catastrophizes", ["everything", "all", "disaster"], "Catastrophizes and spirals"),
        ("bounces_back", ["next", "try again", "keep going"], "Bounces back quickly"),
        ("needs_processing", ["need time", "process", "think about"], "Needs processing time"),
        ("reframe", ["different way", "perspective", "look at"], "Benefits from reframe")
    ],
    
    "reward_sensitivity": [
        ("immediate", ["now", "right away", "instant"], "Immediate gratification"),
        ("long_term", ["later", "eventually", "future"], "Long-term payoff"),
        ("social", ["they'll", "people", "approval"], "Social approval"),
        ("financial", ["money", "paid", "earn"], "Financial gain"),
        ("completion", ["done", "finished", "complete"], "Completion satisfaction"),
        ("unlock", ["unlock", "access", "open"], "New challenge unlocked")
    ]
}


def get_subpattern(category: str, text: str) -> str:
    """
    Detect which subpattern matches the text.
    
    Args:
        category: Main category name (e.g., 'task_initiation')
        text: User message or context text (lowercased)
    
    Returns:
        Subpattern key (e.g., 'body_doubling') or None
    """
    if category not in SUBPATTERNS:
        return None
    
    text_lower = text.lower()
    
    for subpattern_key, keywords, _ in SUBPATTERNS[category]:
        if any(keyword in text_lower for keyword in keywords):
            return subpattern_key
    
    return None


def get_subpattern_description(category: str, subpattern_key: str) -> str:
    """Get human-readable description of a subpattern."""
    if category not in SUBPATTERNS:
        return None
    
    for key, _, description in SUBPATTERNS[category]:
        if key == subpattern_key:
            return description
    
    return None
