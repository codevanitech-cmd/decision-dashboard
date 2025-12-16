import sqlite3
from pathlib import Path

# STEP 3.1: Find current folder (backend)
BASE_DIR = Path(__file__).parent

# STEP 3.2: Build DB path
DB_PATH = BASE_DIR / "decision_intelligence.db"

# STEP 3.3: Function to connect to DB
def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

print("DB PATH:", DB_PATH)
print("DB EXISTS:", DB_PATH.exists())
