from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.database import load_player, save_player
from core.fight import fight

async def fight_command(update, context):
    keyboard = [
        [
            InlineKeyboardButton("Tier 1 (Sand)", callback_data="tier_1"),
            InlineKeyboardButton("Tier 2 (Clay)", callback_data="tier_2"),
            InlineKeyboardButton("Tier 3 (Stone)", callback_data="tier_3"),
            InlineKeyboardButton("Tier 4 (Copper)", callback_data="tier_4"),
        ],
        [InlineKeyboardButton("Back to menu", callback_data="main_menu_back")]
    ]
    if hasattr(update, 'callback_query'):
        await update.callback_query.message.reply_text("Choose mob tier:", reply_markup=InlineKeyboardMarkup(keyboard))
    else:
        await update.message.reply_text("Choose mob tier:", reply_markup=InlineKeyboardMarkup(keyboard))

async def tier_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    tir = int(query.data.split("_")[1])
    context.user_data["fight_tir"] = tir
    keyboard = [
        [
            InlineKeyboardButton("Tank", callback_data=f"select_tank_{tir}"),
            InlineKeyboardButton("Weak", callback_data=f"select_slaby_{tir}"),
            InlineKeyboardButton("Mage", callback_data=f"select_mag_{tir}"),
        ],
        [InlineKeyboardButton("Back to tiers", callback_data="back_to_tiers")],
        [InlineKeyboardButton("Back to menu", callback_data="main_menu_back")]
    ]
    await query.edit_message_text(f"Tier {tir} selected. Choose mob type:", reply_markup=InlineKeyboardMarkup(keyboard))

async def type_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split("_")
    mob_type = parts[1]
    tir = int(parts[2])
    context.user_data["fight_mob_type"] = mob_type
    mob_names = {"tank": "Tank", "slaby": "Weak", "mag": "Mage"}
    mob_name = mob_names.get(mob_type, mob_type)
    keyboard = [
        [InlineKeyboardButton("Start fight", callback_data=f"fight_start_{tir}_{mob_type}")],
        [InlineKeyboardButton("Back to types", callback_data=f"back_to_types_{tir}")],
        [InlineKeyboardButton("Back to menu", callback_data="main_menu_back")]
    ]
    await query.edit_message_text(f"Enemy: Tier {tir} {mob_name}\nPress Start fight", reply_markup=InlineKeyboardMarkup(keyboard))

async def fight_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split("_")
    tir = int(parts[2])
    mob_type = parts[3]
    user_id = update.effective_user.id
    player_data = load_player(user_id)
    await query.edit_message_text(f"Fight with {mob_type} tier {tir} started...")
    victory, log_text, drop = fight(player_data, tir, mob_type)
    if victory:
        player_data["chastitsy"][str(tir)] += drop
        save_player(user_id, player_data)
        await query.message.reply_text(f"WIN!\n\n{log_text}\n\nDrop: +{drop} particles")
    else:
        for key in player_data["chastitsy"]:
            player_data["chastitsy"][key] //= 2
        save_player(user_id, player_data)
        await query.message.reply_text(f"LOSE!\n\n{log_text}\n\nLost 50% particles")
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
