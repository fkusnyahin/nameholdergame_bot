from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes, CallbackQueryHandler
from core.database import load_player, save_player
from core.fight import fight

async def fight_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Тир 1 (Песок)", callback_data="fight_1"),
            InlineKeyboardButton("Тир 2 (Глина)", callback_data="fight_2"),
            InlineKeyboardButton("Тир 3 (Камень)", callback_data="fight_3"),
            InlineKeyboardButton("Тир 4 (Медь)", callback_data="fight_4"),
        ],
        [
            InlineKeyboardButton("🗡️ Танк", callback_data="fight_type_tank"),
            InlineKeyboardButton("🏃 Слабый", callback_data="fight_type_slaby"),
            InlineKeyboardButton("🔥 Маг", callback_data="fight_type_mag"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Выбери тир и тип моба:", reply_markup=reply_markup)

async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data.startswith("fight_"):
        tir = data.split("_")[1]
        if tir.isdigit():
            context.user_data["fight_tir"] = int(tir)
            await query.edit_message_text(f"✅ Выбран тир {tir}\nТеперь выбери тип моба")
            return

    if data.startswith("fight_type_"):
        mob_type = data.split("_")[2]
        tir = context.user_data.get("fight_tir")
        if not tir:
            await query.edit_message_text("❌ Сначала выбери тир моба!")
            return

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

        context.user_data["fight_tir"] = None
