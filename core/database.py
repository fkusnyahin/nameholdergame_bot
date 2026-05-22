import json
import sqlite3
import os

# Путь к файлу базы данных (будет лежать в папке data)
DB_PATH = os.path.join(os.path.dirname(__file__), '..', 'data', 'players.db')

def init_db():
    """Создаёт таблицу игроков при первом запуске"""
    # Убедимся, что папка data существует
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
    print("✅ База данных готова")

def load_player(user_id: int) -> dict:
    """Загружает данные игрока. Если игрок новый — создаёт со стартовыми значениями"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT data FROM players WHERE user_id = ?", (user_id,))
    row = c.fetchone()
    conn.close()
    
    if row:
        return json.loads(row[0])
    else:
        # Новый игрок — стартовые значения (глава 18)
        return {
            "ku": 1,                      # Корневой узел (тир 1 = Песок)
            "telo": 1,                   # Тело (тир 1)
            "mosch": 1,                  # Мощь (тир 1)
            "chastitsy": {               # Частицы по тирам
                "1": 0,   # Песок
                "2": 0,   # Глина
                "3": 0,   # Камень
                "4": 0    # Медь
            },
            "rules": [                   # Правила автомата (пока просто атака)
                {"action": "attack", "condition": "always", "priority": 1}
            ]
        }

def save_player(user_id: int, data: dict):
    """Сохраняет данные игрока в базу"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("REPLACE INTO players (user_id, data) VALUES (?, ?)",
              (user_id, json.dumps(data)))
    conn.commit()
    conn.close()