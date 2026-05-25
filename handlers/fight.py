from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.database import load_player, save_player
from core.fight import fight

async def fight_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Тир 1 (Песок)", callback_data="tier_1"),
            InlineKeyboardButton("Тир 2 (Глина)", callback_data="tier_2"),
            InlineKeyboardButton("Тир 3 (Камень)", callback_data="tier_3"),
            InlineKeyboardButton("Тир 4 (Медь)", callback_data="tier_4"),
        ],
        [InlineKeyboardButton("⬅️ Назад в меню", callback_data="main_menu_back")]
    ]
    await update.message.reply_text("Выбери тир моба:", reply_markup=InlineKeyboardMarkup(keyboard))

async def tier_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    tir = int(query.data.split("_")[1])
    context.user_data["fight_tir"] = tir
    
    tier_names = {1: "Песок", 2: "Глина", 3: "Камень", 4: "Медь"}
    tier_name = tier_names.get(tir, str(tir))
    
    keyboard = [
        [
            InlineKeyboardButton("🗡️ Танк", callback_data=f"select_tank_{tir}"),
            InlineKeyboardButton("🏃 Слабый", callback_data=f"select_slaby_{tir}"),
            InlineKeyboardButton("🔥 Маг", callback_data=f"select_mag_{tir}"),
        ],
        [InlineKeyboardButton("⬅️ Назад к тирам", callback_data="back_to_tiers")]
    ]
    await query.edit_message_text(f"Тир {tir} ({tier_name}) выбран. Теперь выбери тип моба:", reply_markup=InlineKeyboardMarkup(keyboard))

async def type_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    parts = query.data.split("_")
    mob_type = parts[1]
    tir = int(parts[2])
    
    context.user_data["fight_mob_type"] = mob_type
    
    tier_names = {1: "Песок", 2: "Глина", 3: "Камень", 4: "Медь"}
    tier_name = tier_names.get(tir, str(tir))
    
    mob_names = {"tank": "Танк", "slaby": "Слабый", "mag": "Маг"}
    mob_name = mob_names.get(mob_type, mob_type)
    
    keyboard = [
        [InlineKeyboardButton("✅ Начать бой", callback_data=f"fight_start_{tir}_{mob_type}")],
        [InlineKeyboardButton("⬅️ Назад к типам", callback_data=f"back_to_types_{tir}")]
    ]
    await query.edit_message_text(f"⚔️ **Противник: {tier_name} {mob_name}**\n\nНажми «Начать бой» для сражения.", parse_mode="Markdown", reply_markup=InlineKeyboardMarkup(keyboard))

async def fight_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    parts = query.data.split("_")
    tir = int(parts[2])
    mob_type = parts[3]
    
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
    context.user_data.pop("fight_mob_type", None)

async def back_to_tiers(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await fight_command(update, context)

async def back_to_types(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split("_")
    tir = int(parts[3])
    context.user_data["fight_tir"] = tir
    await tier_selected(update, context)

async def main_menu_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    from handlers.menu import menu
    await menu(update, context)