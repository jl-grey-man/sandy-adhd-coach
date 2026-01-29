import psycopg2
from tabulate import tabulate

conn = psycopg2.connect(
    host="tramway.proxy.rlwy.net",
    port=38892,
    database="railway",
    user="postgres",
    password="URBpgBKTMDhSxULRshsZATDQirdqMUta"
)

cursor = conn.cursor()

print("=" * 80)
print("RAILWAY DATABASE AUDIT")
print("=" * 80)

# 1. List all tables
print("\n📊 ALL TABLES IN DATABASE:")
cursor.execute("""
    SELECT table_name 
    FROM information_schema.tables 
    WHERE table_schema = 'public'
    ORDER BY table_name
""")
tables = cursor.fetchall()
for table in tables:
    print(f"  ✓ {table[0]}")

# 2. Check each table has data or structure
print("\n📈 TABLE ROW COUNTS:")
table_stats = []
for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
    count = cursor.fetchone()[0]
    table_stats.append([table[0], count])

print(tabulate(table_stats, headers=["Table", "Rows"], tablefmt="simple"))

# 3. Pattern categories check
print("\n🧠 PATTERN CATEGORIES:")
cursor.execute("SELECT category_name, description FROM pattern_categories ORDER BY category_name")
cats = cursor.fetchall()
for cat in cats:
    print(f"  ✓ {cat[0]}: {cat[1]}")

# 4. Check users
print("\n👤 USERS:")
cursor.execute("SELECT id, email, name, telegram_chat_id FROM users")
users = cursor.fetchall()
for user in users:
    print(f"  User {user[0]}: {user[1]} ({user[2]}) - Telegram: {user[3] or 'Not connected'}")

# 5. Check if alembic_version matches
print("\n🔄 DATABASE VERSION:")
cursor.execute("SELECT version_num FROM alembic_version")
version = cursor.fetchone()
if version:
    print(f"  Current migration: {version[0]}")
else:
    print("  ⚠️ No alembic version found")

cursor.close()
conn.close()

print("\n" + "=" * 80)
