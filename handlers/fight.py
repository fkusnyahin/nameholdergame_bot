from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.database import load_player, save_player
from core.fight import fight

async def fight_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Шаг 1: выбор тира"""
    keyboard = [
        [
            InlineKeyboardButton("Тир 1 (Песок)", callback_data="tier_1"),
            InlineKeyboardButton("Тир 2 (Глина)", callback_data="tier_2"),
            InlineKeyboardButton("Тир 3 (Камень)", callback_data="tier_3"),
            InlineKeyboardButton("Тир 4 (Медь)", callback_data="tier_4"),
        ]
    ]
    await update.message.reply_text("Выбери тир моба:", reply_markup=InlineKeyboardMarkup(keyboard))

async def tier_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Шаг 2: выбран тир, показываем выбор типа моба"""
    query = update.callback_query
    await query.answer()
    
    tir = int(query.data.split("_")[1])
    context.user_data["fight_tir"] = tir
    
    keyboard = [
        [
            InlineKeyboardButton("🗡️ Танк", callback_data=f"fight_tank_{tir}"),
            InlineKeyboardButton("🏃 Слабый", callback_data=f"fight_slaby_{tir}"),
            InlineKeyboardButton("🔥 Маг", callback_data=f"fight_mag_{tir}"),
        ]
    ]
    await query.edit_message_text(f"Тир {tir} выбран. Теперь выбери тип моба:", reply_markup=InlineKeyboardMarkup(keyboard))

async def fight_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Шаг 3: выбран тип моба, запускаем бой"""
    query = update.callback_query
    await query.answer()
    
    parts = query.data.split("_")
    mob_type = parts[1]
    tir = int(parts[2])
    
    user_id = update.effective_user.id
    player_data = load_player(user_id)
    
    await query.edit_message_text(f"⚔️ Бой с {mob_type} тир {tir} начался...")
    
    victory, log_text, drop = fight(player_data, tir, mob_type)
    
    if victory:
        player_data["chastitsy"][str(tir)] += drop
        save_player(user_id, player_data)
        await query.message.reply_text(f"✅ ПОБЕДА!\n\n{log_text}\n\n🎁 Дроп: +{drop} частиц")
    else:
        for key in player_data["chastitsy"]:
            player_data["chastitsy"][key] //= 2
        save_player(user_id, player_data)
        await query.message.reply_text(f"💀 ПОРАЖЕНИЕ!\n\n{log_text}\n\n😵 Потеряно 50% частиц")
    
    context.user_data.pop("fight_tir", None)
