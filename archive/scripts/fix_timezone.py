import psycopg2

conn = psycopg2.connect(
    host="tramway.proxy.rlwy.net",
    port=38892,
    database="railway",
    user="postgres",
    password="URBpgBKTMDhSxULRshsZATDQirdqMUta"
)

cursor = conn.cursor()

print("Fixing user timezone...")

cursor.execute("""
    UPDATE users 
    SET timezone = 'Europe/Stockholm'
    WHERE email = 'user@example.com'
""")

conn.commit()

print("✅ Timezone updated to Europe/Stockholm")

# Verify
cursor.execute("SELECT email, timezone FROM users")
user = cursor.fetchone()
print(f"   User: {user[0]}")
print(f"   Timezone: {user[1]}")

cursor.close()
conn.close()
