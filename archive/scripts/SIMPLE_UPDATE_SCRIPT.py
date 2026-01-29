#!/usr/bin/env python3
"""
Simple script to update categories. Just needs DATABASE_URL.
"""

print("=" * 60)
print("SANDY CATEGORY UPDATER")
print("=" * 60)
print()
print("This will update all category descriptions from 'him/he' to 'you'")
print()
print("📍 Get your DATABASE_URL from Railway:")
print("   1. Go to: https://railway.app")
print("   2. Open project: sandy-adhd-coach")
print("   3. Click: Variables")
print("   4. Copy: DATABASE_URL value")
print()
print("-" * 60)
print()

DATABASE_URL = input("Paste DATABASE_URL here: ").strip()

if not DATABASE_URL:
    print("❌ No URL provided. Exiting.")
    exit(1)

print()
print("🔌 Connecting to database...")

try:
    import psycopg2
    from urllib.parse import urlparse
except ImportError:
    print("❌ Need psycopg2. Install with: pip install psycopg2-binary")
    exit(1)

# Parse connection
result = urlparse(DATABASE_URL)
username = result.username
password = result.password
database = result.path[1:]
hostname = result.hostname
port = result.port

UPDATED_DESCRIPTIONS = {
    "task_initiation": "What actually gets you started on tasks (body doubling, deadlines, accountability, momentum, triggers, etc.)",
    "hyperfocus_triggers": "What puts you in the zone (creative vs analytical, time pressure, interest, novelty, challenge level)",
    "avoidance_reasons": "WHY you avoid specific tasks (unclear done, too many steps, boring, uncertainty, perfectionism, fear)",
    "context_switching_cost": "How you handle switching between tasks (grouped better, needs transition, loses momentum, variety vs focus)",
    "energy_curves": "What drains vs energizes you beyond time of day (social, creative work, admin, movement, food/caffeine)",
    "motivation_sources": "What actually drives you to action (external validation, progress viz, competition, helping others, interest, money)",
    "reward_sensitivity": "What rewards motivate you (immediate gratification, long-term, social, financial, completion, new challenge)",
    "decision_fatigue": "When you hit decision paralysis (too many options, no clear best, high stakes, time of day, many small decisions)",
    "accountability_effectiveness": "What type of accountability works for you (hard deadlines, soft, check-ins, public commitment, consequences, rewards)",
    "task_breakdown_needs": "How much structure you need (overwhelmed by large, benefits from steps, prefers autonomy, needs first step only)",
    "interruption_recovery": "How you handle being interrupted (gets back quickly, loses session, needs warmup, benefits from breadcrumbs)",
    "momentum_building": "How you build work momentum (small wins cascade, needs warmup, goes straight for hard, routine/ritual)",
    "failure_response": "How you handle setbacks (catastrophizes, bounces back, needs processing, benefits from reframe)",
    "novelty_seeking": "How much novelty you need (bored quickly, thrives on routine, needs new challenge, explore vs exploit)",
    "sensory_environment": "What environment helps you work (music type, silence/noise, location, clean/messy, temperature/lighting)",
    "communication_response": "What tone/approach works for you (direct push, gentle, questions, playful, serious, data-driven)",
    "time_perception": "How you estimate time (optimistic/under, pessimistic/over, accurate, time blindness)",
    "urgency_response": "How you respond to urgency (thrives under pressure, freezes, last-minute rush, needs buffer)"
}

try:
    conn = psycopg2.connect(
        database=database,
        user=username,
        password=password,
        host=hostname,
        port=port
    )
    cursor = conn.cursor()
    
    print("✅ Connected!")
    print()
    print("🔧 Updating categories...")
    print()
    
    updated_count = 0
    
    for category_name, new_description in UPDATED_DESCRIPTIONS.items():
        cursor.execute("""
            UPDATE pattern_categories 
            SET description = %s 
            WHERE category_name = %s
            RETURNING id, user_id
        """, (new_description, category_name))
        
        results = cursor.fetchall()
        for row in results:
            print(f"  ✓ {category_name} (user_id={row[1]})")
            updated_count += 1
    
    conn.commit()
    
    print()
    print("=" * 60)
    print(f"✅ SUCCESS! Updated {updated_count} categories")
    print("=" * 60)
    print()
    print("All categories now use 'you' instead of 'him/he'")
    print()
    print("Test it: Send /explore to Sandy on Telegram!")
    print()
    
except Exception as e:
    print(f"❌ Error: {e}")
    if 'conn' in locals():
        conn.rollback()
finally:
    if 'cursor' in locals():
        cursor.close()
    if 'conn' in locals():
        conn.close()
