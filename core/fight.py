import random
from core.formulas import get_player_stats, get_mob_stats, damage_after_armor

def fight(player_data: dict, mob_tir: int, mob_type: str) -> tuple:
    """
    Симуляция боя
    Возвращает: (победа: bool, лог: str, дроп: int)
    """
    log = []
    
    # Загружаем характеристики участников
    player = get_player_stats(player_data)
    player_hp = player["hp_max"]
    mob = get_mob_stats(mob_tir, mob_type)
    mob_hp = mob["hp"]
    
    log.append(f"[0.0] Бой начался! Игрок ({player_hp} HP) vs {mob['name']} ({mob_hp} HP)")
    
    # ДОТ от мага (накладывается в начале боя)
    dot_remaining = 0
    dot_per_sec = 0
    if mob_type == "mag" and mob["dot_duration"] > 0:
        dot_per_sec = mob["dot_per_sec"]
        dot_remaining = mob["dot_duration"]
        log.append(f"[0.0] 🔥 Маг накладывает ДОТ: {dot_per_sec} урона/сек на {dot_remaining} сек")
    
    # Инициатива (скорость атак)
    # Интервал между атаками в секундах
    if mob_type == "tank":
        player_interval = 0.5   # игрок бьёт каждые 0.5 сек
        mob_interval = 0.625    # моб бьёт реже
    elif mob_type == "slaby":
        player_interval = 0.5
        mob_interval = 0.33     # Слабый бьёт чаще
    else:  # mag
        player_interval = 0.5
        mob_interval = 0.5
    
    # Таймеры следующей атаки
    next_player_attack = 0.0
    next_mob_attack = 0.0
    last_dot_time = 0.0
    time = 0.0
    
    # Симуляция (максимум 30 секунд)
    for step in range(300):  # 300 шагов по 0.1 сек = 30 сек
        time = step * 0.1
        
        # ДОТ урон (раз в секунду)
        if dot_remaining > 0 and time - last_dot_time >= 1.0:
            player_hp -= dot_per_sec
            last_dot_time = time
            dot_remaining -= 1
            log.append(f"[{time:.1f}] 💀 ДОТ: -{dot_per_sec} HP. Игрок: {player_hp} HP")
            if player_hp <= 0:
                log.append(f"[{time:.1f}] ❌ Игрок умер от ДОТа!")
                return False, "\n".join(log), 0
        
        # Атака игрока
        if time >= next_player_attack and player_hp > 0 and mob_hp > 0:
            damage = player["damage"]
            damage = damage_after_armor(damage, mob)
            
            # Крит (15% шанс, x1.5)
            is_crit = random.random() < 0.15
            if is_crit:
                damage = int(damage * 1.5)
            
            mob_hp -= damage
            crit_text = " 🔥 КРИТ!" if is_crit else ""
            log.append(f"[{time:.1f}] ⚔️ Игрок: -{damage}{crit_text}. {mob['name']}: {max(0, mob_hp)} HP")
            next_player_attack = time + player_interval
            
            if mob_hp <= 0:
                log.append(f"[{time:.1f}] ✅ ПОБЕДА!")
                drop_amount = mob_tir
                return True, "\n".join(log), drop_amount
        
        # Атака моба
        if time >= next_mob_attack and player_hp > 0 and mob_hp > 0:
            damage = mob["damage"]
            
            # Уклонение (20% шанс)
            if random.random() < 0.2:
                log.append(f"[{time:.1f}] 🌀 Игрок уклонился!")
            else:
                player_hp -= damage
                log.append(f"[{time:.1f}] 👊 {mob['name']}: -{damage} HP. Игрок: {player_hp} HP")
            
            next_mob_attack = time + mob_interval
            
            if player_hp <= 0:
                log.append(f"[{time:.1f}] ❌ ПОРАЖЕНИЕ!")
                return False, "\n".join(log), 0
    
    # Если время вышло
    log.append("[30.0] ⏰ Время боя истекло!")
    return False, "\n".join(log), 0