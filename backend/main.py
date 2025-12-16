# ---------- IMPORTS ----------
import sqlite3
import os
from fastapi import FastAPI

# ---------- APP INIT ----------
app = FastAPI()

# ---------- DATABASE CONNECTION ----------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "decision_intelligence.db")

print("DB PATH USED BY API:", DB_PATH)

conn = sqlite3.connect(DB_PATH, check_same_thread=False)
cursor = conn.cursor()

# ---------- API ROUTES ----------
@app.get("/")
def root():
    return {"status": "API is running"}

@app.get("/metrics")
def get_metrics():
    cursor.execute("""
        SELECT
            supplier_id,
            month,
            orders,
            on_time_deliveries,
            delayed_deliveries,
            rejections,
            total_cost
        FROM performance_metrics
        LIMIT 20
    """)
    return cursor.fetchall()

@app.get("/debug/db-check")
def db_check():
    cursor.execute("SELECT COUNT(*) FROM suppliers")
    suppliers_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM performance_metrics")
    metrics_count = cursor.fetchone()[0]

    return {
        "suppliers_count": suppliers_count,
        "metrics_count": metrics_count
    }

