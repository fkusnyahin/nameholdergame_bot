import random

def get_player_stats(data: dict) -> dict:
    """Рассчитывает урон и здоровье с учётом всех узлов"""
    ku = data["ku"]
    telo = data["telo"]
    mosch = data["mosch"]
    golova = data["golova"]
    duh = data["duh"]
    lovkost = data["lovkost"]
    krov = data["krov"]
    um = data["um"]
    glaza = data["glaza"]
    volya = data["volya"]
    zhizn = data["zhizn"]
    chuvstva = data["chuvstva"]
    energiya = data["energiya"]

    # Бонусы от Мощи (физический урон)
    mosch_fix = 2 * mosch
    mosch_percent = 0.05 * mosch

    # Бонусы от Ума (магический урон)
    um_fix = 2 * um
    um_percent = 0.05 * um

    # Бонусы от Головы (магический урон + кулдауны)
    golova_magic_fix = 2 * golova
    golova_magic_percent = 0.05 * golova
    golova_cd_reduction = 0.05 * golova   # -5% к кулдаунам за тир

    # Бонусы от Духа (лечение + мана)
    duh_heal_percent = 0.10 * duh
    duh_mana_percent = 0.10 * duh

    # Бонусы от Тела (здоровье)
    telo_fix = 20 * (telo - 1)
    telo_percent = 0.10 * (telo - 1)

    # Бонусы от Крови (лечение + сопротивление ядам)
    krov_heal_fix = 5 * krov
    krov_resist_percent = 0.05 * krov

    # Бонусы от Жизни (здоровье + лечение)
    zhizn_hp_fix = 10 * zhizn
    zhizn_heal_percent = 0.05 * zhizn

    # Бонусы от Ловкости (уклонение + скорость атаки)
    lovkost_dodge = 0.05 * lovkost
    lovkost_attack_speed = 1 + (0.05 * lovkost)

    # Бонусы от Глаз (точность + дальность)
    glaza_accuracy_fix = 1 * glaza
    glaza_range_percent = 0.05 * glaza

    # Бонусы от Воли (длительность баффов + сопротивление ментальным дебаффам)
    volya_duration_fix = 1 * volya
    volya_resist_percent = 0.05 * volya

    # Бонусы от Чувств (радиус обнаружения)
    chuvstva_radius_fix = 1 * chuvstva
    chuvstva_detect_percent = 0.05 * chuvstva

    # Бонусы от Энергии (мана + регенерация)
    energiya_mana_fix = 5 * energiya
    energiya_regen_percent = 0.05 * energiya

    # Бонусы от КУ
    ku_fix = ku
    ku_percent = 0.02 * ku

    # Итоговый физический урон (база 10)
    physical_damage = (10 + mosch_fix + ku_fix) * (1 + mosch_percent + ku_percent)

    # Итоговый магический урон (база 10, заменим позже отдельной формулой)
    magic_damage = (10 + um_fix + golova_magic_fix + ku_fix) * (1 + um_percent + golova_magic_percent + ku_percent)

    # Итоговое здоровье (база 100)
    hp = (100 + telo_fix + zhizn_hp_fix) * (1 + telo_percent + ku_percent)

    return {
        "damage": int(physical_damage),
        "magic_damage": int(magic_damage),
        "hp_max": int(hp),
        "dodge": 0.20 + lovkost_dodge,
        "attack_speed": lovkost_attack_speed,
        "heal_bonus": krov_heal_fix + zhizn_heal_percent + duh_heal_percent,
        "mana_max": 100 + energiya_mana_fix,
        "mana_regen": 0.05 + energiya_regen_percent,
        "accuracy": 1.0 + (glaza_accuracy_fix * 0.05),
        "cooldown_reduction": golova_cd_reduction
    }

def get_mob_stats(tir: int, mob_type: str) -> dict:
    """Характеристики мобов"""
    if mob_type == "tank":
        return {
            "name": f"Tank {tir}",
            "hp": 100 * tir,
            "damage": 5 * tir,
            "armor": 20 * tir,
            "armor_type": "percent",
            "initiative": 0.8,
            "dot_per_sec": 0,
            "dot_duration": 0
        }
    elif mob_type == "slaby":
        return {
            "name": f"Weak {tir}",
            "hp": 30 * tir,
            "damage": 8 * tir,
            "armor": 5 * tir,
            "armor_type": "flat",
            "initiative": 1.5,
            "dot_per_sec": 0,
            "dot_duration": 0
        }
    elif mob_type == "mag":
        return {
            "name": f"Mage {tir}",
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
    """Урон после брони моба"""
    if mob["armor_type"] == "percent":
        return max(1, int(damage / (1 + mob["armor"] / 100)))
    else:
        return max(1, damage - mob["armor"])