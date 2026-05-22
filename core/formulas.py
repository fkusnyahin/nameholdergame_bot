import random

def get_player_stats(data: dict) -> dict:
    """
    Рассчитывает урон и здоровье игрока по главам 10 и 18
    """
    ku = data["ku"]
    telo = data["telo"]
    mosch = data["mosch"]
    
    # Бонусы от Мощи
    mosch_fix = 2 * mosch          # тир1:+2, тир2:+4, тир3:+6, тир4:+8
    mosch_percent = 0.05 * mosch   # 5%, 10%, 15%, 20%
    
    # Бонусы от КУ
    ku_fix = ku                    # +1,+2,+3,+4
    ku_percent = 0.02 * ku         # 2%,4%,6%,8%
    
    # Бонусы от Тела
    telo_fix = 20 * (telo - 1)     # 0,20,40,60
    telo_percent = 0.10 * (telo - 1)  # 0%,10%,20%,30%
    
    # Урон (база 10)
    damage = (10 + mosch_fix + ku_fix) * (1 + mosch_percent + ku_percent)
    
    # Здоровье (база 100)
    hp = (100 + telo_fix) * (1 + telo_percent + ku_percent)
    
    return {
        "damage": int(damage),
        "hp_max": int(hp)
    }


def get_mob_stats(tir: int, mob_type: str) -> dict:
    """
    Мобы по главам 11 и 19
    mob_type: "tank", "slaby", "mag"
    """
    if mob_type == "tank":
        return {
            "name": f"Танк {tir}",
            "hp": 100 * tir,
            "damage": 5 * tir,
            "armor": 20 * tir,
            "armor_type": "percent",   # деление
            "initiative": 0.8,
            "dot_per_sec": 0,
            "dot_duration": 0
        }
    elif mob_type == "slaby":
        return {
            "name": f"Слабый {tir}",
            "hp": 30 * tir,
            "damage": 8 * tir,
            "armor": 5 * tir,
            "armor_type": "flat",       # вычитание
            "initiative": 1.5,
            "dot_per_sec": 0,
            "dot_duration": 0
        }
    elif mob_type == "mag":
        return {
            "name": f"Маг {tir}",
            "hp": 50 * tir,
            "damage": 0,
            "armor": 0,
            "armor_type": "percent",
            "initiative": 1.0,
            "dot_per_sec": 10 * tir,
            "dot_duration": tir
        }
    return None


def damage_after_armor(damage: int, mob: dict) -> int:
    """Урон после брони моба (глава 10.4)"""
    if mob["armor_type"] == "percent":
        # Танк: урон / (1 + броня/100)
        return max(1, int(damage / (1 + mob["armor"] / 100)))
    else:
        # Слабый: урон - броня
        return max(1, damage - mob["armor"])