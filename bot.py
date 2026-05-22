import sys
import os

# Добавляем папку проекта в путь (чтобы Python находил наши модули)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import TOKEN
from core.database import init_db, load_player, save_player
from core.fight import fight
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

# ==================== КОМАНДЫ БОТА ====================

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /start — приветствие"""
    user_id = update.effective_user.id
    load_player(user_id)  # Создаём игрока, если новый
    await update.message.reply_text(
        "🎮 Добро пожаловать в RPG бот!\n\n"
        "📋 Команды:\n"
        "/status — посмотреть своего персонажа\n"
        "/fight <тир> <тип> — начать бой\n"
        "/upgrade_ku — повысить Корневой узел\n"
        "/upgrade_telo — повысить Тело\n"
        "/upgrade_mosch — повысить Мощь\n"
        "/add_pesok <число> — добавить песок (тест)\n"
        "/add_glina <число> — добавить глину (тест)\n"
        "/add_kamen <число> — добавить камень (тест)\n"
        "/add_med <число> — добавить медь (тест)\n"
        "/reset — сбросить прогресс"
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /status — показать характеристики"""
    user_id = update.effective_user.id
    data = load_player(user_id)
    from core.formulas import get_player_stats
    stats = get_player_stats(data)
    
    text = f"📊 **Статус персонажа**\n\n"
    text += f"🔹 Корневой узел: тир {data['ku']}\n"
    text += f"🔹 Тело: тир {data['telo']}\n"
    text += f"🔹 Мощь: тир {data['mosch']}\n"
    text += f"⚔️ Урон: {stats['damage']}\n"
    text += f"❤️ Здоровье: {stats['hp_max']}\n\n"
    text += f"💎 **Частицы:**\n"
    text += f"  🟤 Песок: {data['chastitsy']['1']}\n"
    text += f"  🟠 Глина: {data['chastitsy']['2']}\n"
    text += f"  ⚪ Камень: {data['chastitsy']['3']}\n"
    text += f"  🟡 Медь: {data['chastitsy']['4']}"
    
    await update.message.reply_text(text, parse_mode="Markdown")


async def fight_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Команда /fight <тир> <тип>"""
    args = context.args
    if len(args) < 2:
        await update.message.reply_text("❌ Использование: /fight <тир 1-4> <tank/slaby/mag>")
        return
    
    try:
        tir = int(args[0])
        mob_type = args[1].lower()
    except:
        await update.message.reply_text("❌ Ошибка в параметрах")
        return
    
    if tir < 1 or tir > 4:
        await update.message.reply_text("❌ Тир должен быть 1, 2, 3 или 4")
        return
    if mob_type not in ["tank", "slaby", "mag"]:
        await update.message.reply_text("❌ Тип: tank, slaby, mag")
        return
    
    user_id = update.effective_user.id
    data = load_player(user_id)
    
    await update.message.reply_text(f"⚔️ Начинается бой с {mob_type} тир {tir}...")
    
    # Запускаем симуляцию боя
    victory, log_text, drop_amount = fight(data, tir, mob_type)
    
    if victory:
        # Добавляем дроп
        data["chastitsy"][str(tir)] += drop_amount
        save_player(user_id, data)
        await update.message.reply_text(
            f"✅ **ПОБЕДА!**\n\n{log_text}\n\n🎁 Дроп: +{drop_amount} частиц",
            parse_mode="Markdown"
        )
    else:
        # Потеря 50% частиц при смерти
        for key in data["chastitsy"]:
            data["chastitsy"][key] = data["chastitsy"][key] // 2
        save_player(user_id, data)
        await update.message.reply_text(
            f"💀 **ПОРАЖЕНИЕ!**\n\n{log_text}\n\n😵 Вы потеряли 50% частиц!",
            parse_mode="Markdown"
        )


async def upgrade_ku(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Повышение Корневого узла"""
    user_id = update.effective_user.id
    data = load_player(user_id)
    
    current = data["ku"]
    if current >= 4:
        await update.message.reply_text("❌ Вы уже на максимальном тире (Медь)")
        return
    
    cost_map = {1: 10, 2: 20, 3: 40}  # Глина, Камень, Медь
    cost = cost_map[current]
    cost_tier = current + 1
    
    if data["chastitsy"][str(cost_tier)] >= cost:
        data["chastitsy"][str(cost_tier)] -= cost
        data["ku"] = current + 1
        save_player(user_id, data)
        await update.message.reply_text(f"✅ Корневой узел повышен до тира {current + 1}!")
    else:
        await update.message.reply_text(f"❌ Нужно {cost} частиц тира {cost_tier}")


async def upgrade_telo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Повышение Тела"""
    user_id = update.effective_user.id
    data = load_player(user_id)
    
    current = data["telo"]
    if current >= 4:
        await update.message.reply_text("❌ Тело уже на максимальном тире")
        return
    if current >= data["ku"] + 1:
        await update.message.reply_text(f"❌ Тело не может быть выше КУ+1 (КУ={data['ku']})")
        return
    
    next_tier = current + 1
    cost = 10 * next_tier  # 20, 30, 40
    
    if data["chastitsy"][str(next_tier)] >= cost:
        data["chastitsy"][str(next_tier)] -= cost
        data["telo"] = next_tier
        save_player(user_id, data)
        await update.message.reply_text(f"✅ Тело повышено до тира {next_tier}!")
    else:
        await update.message.reply_text(f"❌ Нужно {cost} частиц тира {next_tier}")


async def upgrade_mosch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Повышение Мощи"""
    user_id = update.effective_user.id
    data = load_player(user_id)
    
    current = data["mosch"]
    if current >= 4:
        await update.message.reply_text("❌ Мощь уже на максимальном тире")
        return
    if current >= data["ku"] + 1:
        await update.message.reply_text(f"❌ Мощь не может быть выше КУ+1 (КУ={data['ku']})")
        return
    
    next_tier = current + 1
    cost = 5 * next_tier  # 10, 15, 20
    
    if data["chastitsy"][str(next_tier)] >= cost:
        data["chastitsy"][str(next_tier)] -= cost
        data["mosch"] = next_tier
        save_player(user_id, data)
        await update.message.reply_text(f"✅ Мощь повышена до тира {next_tier}!")
    else:
        await update.message.reply_text(f"❌ Нужно {cost} частиц тира {next_tier}")


# Тестовые команды для добавления частиц
async def add_pesok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_player(user_id)
    try:
        amount = int(context.args[0])
        data["chastitsy"]["1"] += amount
        save_player(user_id, data)
        await update.message.reply_text(f"➕ Добавлено {amount} песка")
    except:
        await update.message.reply_text("❌ /add_pesok <число>")

async def add_glina(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_player(user_id)
    try:
        amount = int(context.args[0])
        data["chastitsy"]["2"] += amount
        save_player(user_id, data)
        await update.message.reply_text(f"➕ Добавлено {amount} глины")
    except:
        await update.message.reply_text("❌ /add_glina <число>")

async def add_kamen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_player(user_id)
    try:
        amount = int(context.args[0])
        data["chastitsy"]["3"] += amount
        save_player(user_id, data)
        await update.message.reply_text(f"➕ Добавлено {amount} камня")
    except:
        await update.message.reply_text("❌ /add_kamen <число>")

async def add_med(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_player(user_id)
    try:
        amount = int(context.args[0])
        data["chastitsy"]["4"] += amount
        save_player(user_id, data)
        await update.message.reply_text(f"➕ Добавлено {amount} меди")
    except:
        await update.message.reply_text("❌ /add_med <число>")


async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Сброс прогресса"""
    user_id = update.effective_user.id
    import sqlite3
    from core.database import DB_PATH
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM players WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    await update.message.reply_text("🔄 Прогресс сброшен! Используйте /start для начала.")


# ==================== ЗАПУСК БОТА ====================

def main():
    # Создаём базу данных
    init_db()
    
    # Создаём приложение
    app = Application.builder().token(TOKEN).build()
    
    # Регистрируем команды
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("fight", fight_command))
    app.add_handler(CommandHandler("upgrade_ku", upgrade_ku))
    app.add_handler(CommandHandler("upgrade_telo", upgrade_telo))
    app.add_handler(CommandHandler("upgrade_mosch", upgrade_mosch))
    app.add_handler(CommandHandler("add_pesok", add_pesok))
    app.add_handler(CommandHandler("add_glina", add_glina))
    app.add_handler(CommandHandler("add_kamen", add_kamen))
    app.add_handler(CommandHandler("add_med", add_med))
    app.add_handler(CommandHandler("reset", reset))
    
    print("🚀 Бот запущен! Нажми Ctrl+C для остановки.")
    app.run_polling()


if __name__ == "__main__":
    main()