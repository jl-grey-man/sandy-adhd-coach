import psycopg2
from werkzeug.security import generate_password_hash

# Connect to Railway database
conn = psycopg2.connect(
    host="tramway.proxy.rlwy.net",
    port=38892,
    database="railway",
    user="postgres",
    password="URBpgBKTMDhSxULRshsZATDQirdqMUta"
)

cursor = conn.cursor()

# Create user
email = "user@example.com"
password = "string"
password_hash = generate_password_hash(password)

try:
    cursor.execute("""
        INSERT INTO users (email, password_hash, name, timezone, created_at, updated_at, preferences)
        VALUES (%s, %s, %s, %s, NOW(), NOW(), %s)
    """, (email, password_hash, "Test User", "UTC", "{}"))
    
    conn.commit()
    print(f"✅ Created user:")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
except Exception as e:
    if "duplicate key" in str(e):
        print(f"✅ User {email} already exists!")
    else:
        print(f"❌ Error: {e}")
finally:
    cursor.close()
    conn.close()
