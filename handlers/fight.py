from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.database import load_player, save_player
from core.fight import fight
import random`nfrom handlers.menu import menu

async def fight_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [
            InlineKeyboardButton("Tier 1 (Sand)", callback_data="tier_1"),
            InlineKeyboardButton("Tier 2 (Clay)", callback_data="tier_2"),
            InlineKeyboardButton("Tier 3 (Stone)", callback_data="tier_3"),
            InlineKeyboardButton("Tier 4 (Copper)", callback_data="tier_4"),
        ],
        [InlineKeyboardButton("Back to menu", callback_data="main_menu_back")]
    ]
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
    
    # Бой
    await query.edit_message_text(f"Fight with {mob_type} tier {tir} started...")
    victory, log_text, _ = fight(player_data, tir, mob_type)
    
    if victory:
        # Расчёт дропа с учётом Даров
        dary_level = player_data.get("dary", {}).get(str(tir), 1)
        drop_amount = random.randint(1, {1:1,2:2,3:3,4:5,5:8,6:13,7:21,8:34,9:55,10:89}.get(dary_level, 1))
        player_data["chastitsy"][str(tir)] += drop_amount
        save_player(user_id, player_data)
        await query.message.reply_text(f"WIN!\n\n{log_text}\n\nDrop: +{drop_amount} particles")
    else:
        for key in player_data["chastitsy"]:
            player_data["chastitsy"][key] //= 2
        save_player(user_id, player_data)
        await query.message.reply_text(f"LOSE!\n\n{log_text}\n\nLost 50% particles")
    
    context.user_data.pop("fight_tir", None)
    context.user_data.pop("fight_mob_type", None)
    
    # Показать меню после боя
    keyboard = [
        [InlineKeyboardButton("Fight again", callback_data="menu_fight")],
        [InlineKeyboardButton("Back to menu", callback_data="main_menu_back")]
    ]
    await query.message.reply_text("What now?", reply_markup=InlineKeyboardMarkup(keyboard))

async def main_menu_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await menu(update, context)

