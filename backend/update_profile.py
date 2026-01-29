"""
Quick script to update the test user with Jens's ADHD profile
"""
import psycopg2
import json

# Your ADHD profile
profile = {
    "name": "Jens",
    "location": "Göteborg, Sweden",
    "timezone": "Europe/Stockholm",
    
    "professional_context": {
        "role": "Entrepreneur with own business",
        "current_phase": "Returning to work after 2-year burnout",
        "just_starting_again": True
    },
    
    "mental_health_context": {
        "history": ["depression", "anxiety"],
        "recent_burnout": "2 years",
        "recovery_phase": "Currently rebuilding work capacity"
    },
    
    "current_challenges": [
        "Unclear company direction",
        "Don't know where to start/focus",
        "Overwhelm about next steps",
        "Rebuilding work capacity post-burnout"
    ],
    
    "adhd_context": {
        "diagnosis_status": "Has ADHD",
        "has_tried_classic_tactics": True,
        "seeking": "Personalized approach, not textbook advice"
    },
    
    "work_patterns": {
        "capable_of_hyperfocus": True,
        "works_on_passion_projects": True,
        "iterative_approach": "Build, see, refine"
    },
    
    "what_doesnt_work": [
        {
            "category": "generic_advice",
            "note": "Has tried all classic ADHD tactics, they don't work or only partially work"
        }
    ],
    
    "what_works": [],
    
    "preferences": {
        "no_generic_advice": True,
        "ask_questions_first": True,
        "understand_root_cause": True,
        "communication_style": "direct, casual, no fluff",
        "wants_therapist_approach": "Dig deep, understand underlying causes before suggesting"
    },
    
    "ai_behavior_requirements": {
        "self_challenge": "Before answering, AI must ask itself: 'Is this really the best suggestion? Could I give something less usual/generic?'",
        "avoid_typical_responses": True,
        "prioritize_creative_solutions": True,
        "no_fake_positivity": True,
        "no_cheerleading": True,
        "straight_talking": True
    },
    
    "exploration_needed": [
        "What specific tactics have you tried and why didn't they work?",
        "What are your main blockers? (planning paralysis, execution, something else?)",
        "What contexts do you struggle in most?",
        "What's the nature of your business? What directions are you considering?",
        "What does 'starting again' after burnout feel like for you?",
        "What made you burn out in the first place?",
        "What strategies have worked even slightly?"
    ]
}

# Connect to database
conn = psycopg2.connect("dbname=adhd_coach_dev")
cur = conn.cursor()

# Update the test user
cur.execute(
    "UPDATE users SET adhd_profile = %s, name = %s WHERE email = %s",
    (json.dumps(profile), "Jens", "user@example.com")
)

conn.commit()
cur.close()
conn.close()

print("✅ Profile updated for user@example.com")
