import psycopg2

conn = psycopg2.connect(
    host="tramway.proxy.rlwy.net",
    port=38892,
    database="railway",
    user="postgres",
    password="URBpgBKTMDhSxULRshsZATDQirdqMUta"
)

cursor = conn.cursor()

# Check pattern categories
cursor.execute("SELECT COUNT(*) FROM pattern_categories WHERE user_id = 2")
count = cursor.fetchone()[0]

print(f"Pattern categories in database: {count}")

if count == 0:
    print("\n❌ NO PATTERN CATEGORIES FOUND - This is the problem!")
else:
    cursor.execute("""
        SELECT category_name, description 
        FROM pattern_categories 
        WHERE user_id = 2
        ORDER BY category_name
    """)
    
    print("\n✅ Pattern categories:")
    for row in cursor.fetchall():
        print(f"  - {row[0]}: {row[1]}")

cursor.close()
conn.close()
