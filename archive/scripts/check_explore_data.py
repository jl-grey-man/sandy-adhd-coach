import psycopg2
from datetime import datetime

conn = psycopg2.connect(
    host="tramway.proxy.rlwy.net",
    port=38892,
    database="railway",
    user="postgres",
    password="URBpgBKTMDhSxULRshsZATDQirdqMUta"
)

cursor = conn.cursor()

print("=" * 80)
print("EXPLORE SESSION DATA INVESTIGATION")
print("=" * 80)

# Check pattern observations
cursor.execute("SELECT COUNT(*) FROM pattern_observations")
obs_count = cursor.fetchone()[0]
print(f"\n📊 Total Pattern Observations: {obs_count}")

if obs_count > 0:
    cursor.execute("""
        SELECT po.id, pc.category_name, po.observation, po.observed_at, po.context
        FROM pattern_observations po
        JOIN pattern_categories pc ON po.category_id = pc.id
        ORDER BY po.observed_at DESC
        LIMIT 20
    """)
    
    print("\n✅ Recent observations:")
    for obs_id, cat_name, observation, observed_at, context in cursor.fetchall():
        print(f"\n  ID {obs_id} - {cat_name}")
        print(f"  Time: {observed_at}")
        print(f"  Observation: {observation[:100]}...")
        if context:
            print(f"  Context: {context}")
else:
    print("\n❌ NO OBSERVATIONS FOUND!")

# Check pattern hypotheses
cursor.execute("SELECT COUNT(*) FROM pattern_hypotheses")
hyp_count = cursor.fetchone()[0]
print(f"\n📊 Total Pattern Hypotheses: {hyp_count}")

if hyp_count > 0:
    cursor.execute("""
        SELECT ph.id, pc.category_name, ph.hypothesis, ph.confidence, 
               ph.supporting_observations, ph.contradicting_observations, ph.status
        FROM pattern_hypotheses ph
        JOIN pattern_categories pc ON ph.category_id = pc.id
        ORDER BY ph.confidence DESC
        LIMIT 20
    """)
    
    print("\n✅ Hypotheses:")
    for hyp_id, cat_name, hypothesis, confidence, supporting, contradicting, status in cursor.fetchall():
        print(f"\n  {cat_name} ({confidence}% confidence)")
        print(f"  Hypothesis: {hypothesis[:100]}...")
        print(f"  Supporting: {supporting}, Contradicting: {contradicting}")
        print(f"  Status: {status}")
else:
    print("\n❌ NO HYPOTHESES FOUND!")

# Check recent conversations
cursor.execute("""
    SELECT COUNT(*) FROM conversations 
    WHERE input_type = 'telegram'
""")
telegram_convs = cursor.fetchone()[0]

cursor.execute("""
    SELECT COUNT(*) FROM conversations 
    WHERE input_type = 'web'
""")
web_convs = cursor.fetchone()[0]

print(f"\n📊 Conversations:")
print(f"  Telegram: {telegram_convs}")
print(f"  Web: {web_convs}")

# Check last 10 conversations
cursor.execute("""
    SELECT input_type, user_message, ai_response, created_at
    FROM conversations
    ORDER BY created_at DESC
    LIMIT 10
""")

print(f"\n📝 Last 10 conversations:")
for input_type, user_msg, ai_response, created_at in cursor.fetchall():
    print(f"\n  [{input_type}] {created_at}")
    print(f"  User: {user_msg[:60]}...")
    print(f"  Sandy: {ai_response[:60]}...")

cursor.close()
conn.close()
