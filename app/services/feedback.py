import json
import sqlite3
from pathlib import Path
DB_PATH = Path(__file__).resolve().parents[2]/"data"/"feedback.db"

def _conn():
  DB_PATH.parent.mkdir(parents=True,exist_ok=True)
  conn= sqlite3.connect(DB_PATH)
  conn.execute(
    """
    CREATE TABLE IF NOT EXISTS feedback (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    prediction_id TEXT NOT NULL UNIQUE,
    is_correct INTEGER NOT NULL,
    customer_input TEXT NOT NULL,
    prediction TEXT NOT NULL,
    churn_probability REAL NOT NULL,
    risk_level TEXT NOT NULL,
    created_at TEXT DEFAULT CURRENT_TIMESTAMP 
    )"""
  )
  return conn

def save_feedback(data: dict) ->bool:
    conn = _conn()
    try:
        with conn:
            conn.execute(
                "INSERT INTO feedback(prediction_id,is_correct,customer_input,"
                "prediction,churn_probability,risk_level) VALUES(?,?,?,?,?,?)",
                (
                    data["prediction_id"],
                    int(data["is_correct"]),
                    json.dumps(data["customer_input"]),
                    data["prediction"],
                    data["churn_probability"],
                    data["risk_level"],
                ),
            )
        return True
    except sqlite3.IntegrityError:
        return False
    finally:
        conn.close()

