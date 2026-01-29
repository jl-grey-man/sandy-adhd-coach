import psycopg2

conn = psycopg2.connect(
    host="tramway.proxy.rlwy.net",
    port=38892,
    database="railway",
    user="postgres",
    password="URBpgBKTMDhSxULRshsZATDQirdqMUta"
)

cursor = conn.cursor()

# Check all pattern categories
cursor.execute("SELECT COUNT(*) FROM pattern_categories")
total_count = cursor.fetchone()[0]
print(f"Total pattern categories in database: {total_count}")

cursor.execute("SELECT DISTINCT user_id FROM pattern_categories")
user_ids = cursor.fetchall()
print(f"User IDs with pattern categories: {[u[0] for u in user_ids]}")

# Check user_id 2 specifically
cursor.execute("SELECT COUNT(*) FROM pattern_categories WHERE user_id = 2")
count = cursor.fetchone()[0]
print(f"\nPattern categories for user_id=2: {count}")

if count > 0:
    cursor.execute("""
        SELECT category_name, description 
        FROM pattern_categories 
        WHERE user_id = 2
        ORDER BY category_name
        LIMIT 5
    """)
    
    print("\n✅ Sample categories:")
    for row in cursor.fetchall():
        print(f"  - {row[0]}: {row[1]}")

cursor.close()
conn.close()
