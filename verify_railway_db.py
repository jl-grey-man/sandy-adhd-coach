import psycopg2

conn = psycopg2.connect(
    host="tramway.proxy.rlwy.net",
    port=38892,
    database="railway",
    user="postgres",
    password="URBpgBKTMDhSxULRshsZATDQirdqMUta"
)

cursor = conn.cursor()

print("=" * 80)
print("RAILWAY DATABASE VERIFICATION")
print("=" * 80)

# Get all tables
cursor.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public' 
    ORDER BY table_name
""")

tables = cursor.fetchall()
print(f"\n✅ Total tables: {len(tables)}")
print("\nTables in database:")
for table in tables:
    print(f"  - {table[0]}")

# Check each important table
print("\n" + "=" * 80)
print("TABLE ROW COUNTS")
print("=" * 80)

important_tables = [
    'users',
    'pattern_categories', 
    'pattern_observations',
    'pattern_hypotheses',
    'conversations',
    'tasks',
    'projects',
    'reminders',
    'goals',
    'work_sessions',
    'exploration_topics',
    'backburner_items',
    'calendar_events',
    'milestones',
    'metrics'
]

for table_name in important_tables:
    cursor.execute(f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{table_name}')")
    exists = cursor.fetchone()[0]
    
    if exists:
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        count = cursor.fetchone()[0]
        print(f"  {table_name}: {count} rows")
    else:
        print(f"  {table_name}: ❌ MISSING")

# Check pattern categories specifically
print("\n" + "=" * 80)
print("PATTERN CATEGORIES")
print("=" * 80)

cursor.execute("SELECT category_name, description FROM pattern_categories ORDER BY category_name")
categories = cursor.fetchall()

if categories:
    print(f"\n✅ {len(categories)} pattern categories:")
    for cat_name, desc in categories:
        print(f"  - {cat_name}: {desc}")
else:
    print("\n❌ No pattern categories found!")

# Check user
print("\n" + "=" * 80)
print("USERS")
print("=" * 80)

cursor.execute("SELECT id, email, name, telegram_chat_id FROM users")
users = cursor.fetchall()

print(f"\n✅ {len(users)} users:")
for user_id, email, name, telegram_id in users:
    telegram_status = f"Telegram: {telegram_id}" if telegram_id else "No Telegram"
    print(f"  - ID {user_id}: {email} ({name}) - {telegram_status}")

cursor.close()
conn.close()

print("\n" + "=" * 80)
print("VERIFICATION COMPLETE")
print("=" * 80)
