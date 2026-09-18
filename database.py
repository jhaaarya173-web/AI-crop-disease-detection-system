import sqlite3

# ================= CONNECT DATABASE =================
conn = sqlite3.connect("crop_disease.db")

cursor = conn.cursor()

# ================= USERS TABLE =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name TEXT,
    last_name TEXT,
    email TEXT UNIQUE,
    contact TEXT,
    password TEXT
)
""")

# ================= DETECTION TABLE =================
cursor.execute("""
CREATE TABLE IF NOT EXISTS detections(
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    crop TEXT,
    disease TEXT,
    confidence REAL,
    date TEXT
)
""")

# ================= SAVE =================
conn.commit()

conn.close()

print("Database and tables created successfully")