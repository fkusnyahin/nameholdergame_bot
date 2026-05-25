import random
import json
import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.database import load_player, save_player
from core.fight import fight
from handlers.main_menu import main_menu

def load_mob_info():
    path = os.path.join(os.path.dirname(__file__), '..', 'mobs_info.json')
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

MOB_INFO = load_mob_info()

async def fight_command(message, context):
    keyboard = [
        [
            InlineKeyboardButton("Tier 1 (Sand)", callback_data="tier_1"),
            InlineKeyboardButton("Tier 2 (Clay)", callback_data="tier_2"),
            InlineKeyboardButton("Tier 3 (Stone)", callback_data="tier_3"),
            InlineKeyboardButton("Tier 4 (Copper)", callback_data="tier_4"),
        ],
        [
            InlineKeyboardButton("Tier 5 (Bronze)", callback_data="tier_5"),
            InlineKeyboardButton("Tier 6 (Steel)", callback_data="tier_6"),
            InlineKeyboardButton("Tier 7 (Titan)", callback_data="tier_7"),
            InlineKeyboardButton("Tier 8 (Wolfram)", callback_data="tier_8"),
        ],
        [InlineKeyboardButton("Tier 9 (Star)", callback_data="tier_9")],
        [InlineKeyboardButton("Back to menu", callback_data="main_menu_back")]
    ]
    await message.reply_text("Choose mob tier:", reply_markup=InlineKeyboardMarkup(keyboard))

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
    # Читаем имя из JSON
    mob_name = MOB_INFO.get(mob_type, {}).get("name", mob_type.capitalize())
    keyboard = [
        [InlineKeyboardButton("Start fight", callback_data=f"fight_start_{tir}_{mob_type}")],
        [InlineKeyboardButton("Back to menu", callback_data="main_menu_back")]
    ]
    await query.edit_message_text(f"Enemy: {mob_name} (Tier {tir})\nPress Start fight", reply_markup=InlineKeyboardMarkup(keyboard))

async def fight_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split("_")
    tir = int(parts[2])
    mob_type = parts[3]
    user_id = update.effective_user.id
    player_data = load_player(user_id)
    
    await query.edit_message_text(f"Fight with {mob_type} tier {tir} started...")
    victory, log_text, _ = fight(player_data, tir, mob_type)
    
    if victory:
        dary_level = player_data.get("dary", {}).get(str(tir), 1)
        drop_max = {1:1, 2:2, 3:3, 4:5, 5:8, 6:13, 7:21, 8:34, 9:55, 10:89}.get(dary_level, 1)
        drop_amount = random.randint(1, drop_max)
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
    
    keyboard = [
        [InlineKeyboardButton("Fight again", callback_data="main_menu_fight")],
        [InlineKeyboardButton("Back to menu", callback_data="main_menu_back")]
    ]
    await query.message.reply_text("What now?", reply_markup=InlineKeyboardMarkup(keyboard))

async def main_menu_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await main_menu(query.message, context)
