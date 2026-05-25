import json
import sqlite3
import os

DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'players.db')

def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS players (
            user_id INTEGER PRIMARY KEY,
            data TEXT
        )
    ''')
    conn.commit()
    conn.close()
    print("DB ready")

def load_player(user_id: int) -> dict:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT data FROM players WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    if row:
        return json.loads(row[0])
    else:
        return {
            "ku": 1,
            "telo": 1,
            "mosch": 1,
            "chastitsy": {"1": 0, "2": 0, "3": 0, "4": 0},
            "rules": [{"action": "attack", "condition": "always", "priority": 1}]
        }

def save_player(user_id: int, data: dict):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("REPLACE INTO players (user_id, data) VALUES (?, ?)",
              (user_id, json.dumps(data)))
    conn.commit()
    conn.close()
