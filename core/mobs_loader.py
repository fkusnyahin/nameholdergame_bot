import json
import os

def get_mobs_from_sheets():
    """Загружает мобов из mobs.json"""
    json_path = os.path.join(os.path.dirname(file), '..', 'mobs.json')
    try:
        with open(json_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Ошибка загрузки mobs.json: {e}")
        return []

def get_mobs_by_role(role):
    all_mobs = get_mobs_from_sheets()
    return [mob for mob in all_mobs if mob.get('role') == role]
