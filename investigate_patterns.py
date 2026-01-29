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
print("PATTERN LEARNING INVESTIGATION")
print("=" * 80)

# Check pattern observations
print("\n1. PATTERN OBSERVATIONS")
print("-" * 80)
cursor.execute("""
    SELECT 
        po.id,
        pc.category_name,
        po.observation,
        po.observed_at,
        po.context
    FROM pattern_observations po
    JOIN pattern_categories pc ON po.category_id = pc.id
    ORDER BY po.observed_at DESC
    LIMIT 20
""")

observations = cursor.fetchall()
if observations:
    print(f"✅ Found {len(observations)} observations:")
    for obs_id, cat_name, obs_text, obs_time, context in observations:
        print(f"\n  ID: {obs_id}")
        print(f"  Category: {cat_name}")
        print(f"  Observation: {obs_text[:100]}...")
        print(f"  Time: {obs_time}")
else:
    print("❌ NO OBSERVATIONS FOUND!")
    print("   This means explore sessions are NOT being saved!")

# Check pattern hypotheses
print("\n" + "=" * 80)
print("2. PATTERN HYPOTHESES")
print("-" * 80)
cursor.execute("""
    SELECT 
        ph.id,
        pc.category_name,
        ph.hypothesis,
        ph.confidence,
        ph.supporting_observations,
        ph.contradicting_observations,
        ph.status,
        ph.needs_exploration
    FROM pattern_hypotheses ph
    JOIN pattern_categories pc ON ph.category_id = pc.id
    ORDER BY ph.confidence DESC
""")

hypotheses = cursor.fetchall()
if hypotheses:
    print(f"✅ Found {len(hypotheses)} hypotheses:")
    for hyp_id, cat_name, hyp, conf, supp, contra, status, needs_exp in hypotheses:
        print(f"\n  Category: {cat_name}")
        print(f"  Hypothesis: {hyp}")
        print(f"  Confidence: {conf}%")
        print(f"  Supporting: {supp}, Contradicting: {contra}")
        print(f"  Status: {status}, Needs exploration: {needs_exp}")
else:
    print("❌ NO HYPOTHESES FOUND!")
    print("   Pattern learning system hasn't formed any patterns yet")

# Check recent conversations
print("\n" + "=" * 80)
print("3. RECENT CONVERSATIONS")
print("-" * 80)
cursor.execute("""
    SELECT 
        id,
        user_message,
        ai_response,
        input_type,
        created_at
    FROM conversations
    ORDER BY created_at DESC
    LIMIT 10
""")

convos = cursor.fetchall()
print(f"Found {len(convos)} recent conversations:")
for conv_id, user_msg, ai_msg, input_type, created in convos:
    print(f"\n  [{input_type}] {created}")
    print(f"  User: {user_msg[:80]}...")
    print(f"  Sandy: {ai_msg[:80]}...")

# Check user timezone
print("\n" + "=" * 80)
print("4. USER TIMEZONE SETTINGS")
print("-" * 80)
cursor.execute("""
    SELECT 
        id,
        email,
        name,
        timezone,
        morning_briefing_time,
        created_at
    FROM users
""")

user = cursor.fetchone()
if user:
    user_id, email, name, tz, morning_time, created = user
    print(f"User ID: {user_id}")
    print(f"Email: {email}")
    print(f"Timezone: {tz}")
    print(f"Morning briefing: {morning_time}")
    print(f"Current server time: {datetime.utcnow()} UTC")
    
    if tz:
        import pytz
        user_tz = pytz.timezone(tz)
        local_time = datetime.now(user_tz)
        print(f"User local time: {local_time}")
        print(f"Time of day: {local_time.strftime('%H:%M')}")
    else:
        print("⚠️  NO TIMEZONE SET!")

cursor.close()
conn.close()

print("\n" + "=" * 80)
print("INVESTIGATION COMPLETE")
print("=" * 80)
