import psycopg2

CATEGORIES = [
    ("task_initiation", "What actually gets him started on tasks"),
    ("hyperfocus_triggers", "What puts him in the zone"),
    ("avoidance_reasons", "WHY he avoids specific tasks"),
    ("context_switching_cost", "How he handles switching between tasks"),
    ("energy_curves", "What drains vs energizes beyond time of day"),
    ("motivation_sources", "What actually drives action"),
    ("reward_sensitivity", "What rewards motivate"),
    ("decision_fatigue", "When decision paralysis hits"),
    ("accountability_effectiveness", "What type of accountability works"),
    ("task_breakdown_needs", "How much structure he needs"),
    ("interruption_recovery", "How he handles being interrupted"),
    ("momentum_building", "How he builds work momentum"),
    ("failure_response", "How he handles setbacks"),
    ("novelty_seeking", "How much novelty he needs"),
    ("sensory_environment", "What environment helps him work"),
    ("communication_response", "What tone/approach works"),
    ("time_perception", "How he estimates time"),
    ("urgency_response", "How he responds to urgency")
]

conn = psycopg2.connect(
    host="tramway.proxy.rlwy.net",
    port=38892,
    database="railway",
    user="postgres",
    password="URBpgBKTMDhSxULRshsZATDQirdqMUta"
)

cursor = conn.cursor()

# Get user_id
cursor.execute("SELECT id FROM users WHERE email = 'user@example.com'")
user_id = cursor.fetchone()[0]

print(f"Seeding pattern categories for user_id={user_id}...")

try:
    for name, desc in CATEGORIES:
        cursor.execute("""
            INSERT INTO pattern_categories (user_id, category_name, description, created_at)
            VALUES (%s, %s, %s, NOW())
        """, (user_id, name, desc))
    
    conn.commit()
    print(f"✅ Seeded {len(CATEGORIES)} pattern categories to Railway database!")
    
except Exception as e:
    print(f"❌ Error: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()
