import psycopg2
try:
    conn = psycopg2.connect(
        dbname="hemobank_db", 
        user="hemobank_user", 
        password="secure_password_123", 
        host="localhost"
    )
    print("✅ Success! Your database is working and credentials are correct.")
    conn.close()
except Exception as e:
    print(f"❌ Database Error: {e}")