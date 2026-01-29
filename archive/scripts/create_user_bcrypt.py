import psycopg2
from passlib.context import CryptContext

# Use bcrypt like the app does
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Connect to Railway database
conn = psycopg2.connect(
    host="tramway.proxy.rlwy.net",
    port=38892,
    database="railway",
    user="postgres",
    password="URBpgBKTMDhSxULRshsZATDQirdqMUta"
)

cursor = conn.cursor()

# Create user with bcrypt hash
email = "user@example.com"
password = "string"
password_hash = pwd_context.hash(password)

try:
    # First, try to delete existing user if exists
    cursor.execute("DELETE FROM users WHERE email = %s", (email,))
    
    # Now insert with correct bcrypt hash
    cursor.execute("""
        INSERT INTO users (email, password_hash, name, timezone, created_at, updated_at, preferences)
        VALUES (%s, %s, %s, %s, NOW(), NOW(), %s)
    """, (email, password_hash, "Test User", "UTC", "{}"))
    
    conn.commit()
    print(f"✅ Created user with bcrypt hash:")
    print(f"   Email: {email}")
    print(f"   Password: {password}")
    print(f"   Hash: {password_hash[:50]}...")
except Exception as e:
    print(f"❌ Error: {e}")
    conn.rollback()
finally:
    cursor.close()
    conn.close()
