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

# Названия тиров по-русски
TIER_NAMES = {
    1: "Песок",
    2: "Глина",
    3: "Камень",
    4: "Медь",
    5: "Бронза",
    6: "Сталь",
    7: "Титан",
    8: "Вольфрам",
    9: "Звезда"
}

async def fight_command(message, context):
    keyboard = [
        [
            InlineKeyboardButton("Песок", callback_data="tier_1"),
            InlineKeyboardButton("Глина", callback_data="tier_2"),
            InlineKeyboardButton("Камень", callback_data="tier_3"),
            InlineKeyboardButton("Медь", callback_data="tier_4"),
        ],
        [
            InlineKeyboardButton("Бронза", callback_data="tier_5"),
            InlineKeyboardButton("Сталь", callback_data="tier_6"),
            InlineKeyboardButton("Титан", callback_data="tier_7"),
            InlineKeyboardButton("Вольфрам", callback_data="tier_8"),
        ],
        [InlineKeyboardButton("Звезда", callback_data="tier_9")],
        [InlineKeyboardButton("Назад в меню", callback_data="main_menu_back")]
    ]
    await message.reply_text("Выбери тир моба:", reply_markup=InlineKeyboardMarkup(keyboard))

async def tier_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    tir = int(query.data.split("_")[1])
    context.user_data["fight_tir"] = tir
    keyboard = [
        [
            InlineKeyboardButton("Страж", callback_data=f"select_tank_{tir}"),
            InlineKeyboardButton("Бес", callback_data=f"select_slaby_{tir}"),
            InlineKeyboardButton("Шаман", callback_data=f"select_mag_{tir}"),
        ],
        [InlineKeyboardButton("Назад в меню", callback_data="main_menu_back")]
    ]
    await query.edit_message_text(f"Тир {TIER_NAMES[tir]} выбран. Выбери тип моба:", reply_markup=InlineKeyboardMarkup(keyboard))

async def type_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split("_")
    mob_type = parts[1]
    tir = int(parts[2])
    context.user_data["fight_mob_type"] = mob_type
    mob_name = MOB_INFO.get(mob_type, {}).get("name", mob_type.capitalize())
    keyboard = [
        [InlineKeyboardButton("Начать бой", callback_data=f"fight_start_{tir}_{mob_type}")],
        [InlineKeyboardButton("Назад в меню", callback_data="main_menu_back")]
    ]
    await query.edit_message_text(f"Противник: {mob_name} ({TIER_NAMES[tir]})\nНажми «Начать бой»", reply_markup=InlineKeyboardMarkup(keyboard))

async def fight_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    parts = query.data.split("_")
    tir = int(parts[2])
    mob_type = parts[3]
    user_id = update.effective_user.id
    player_data = load_player(user_id)
    
    mob_name = MOB_INFO.get(mob_type, {}).get("name", mob_type.capitalize())
    await query.edit_message_text(f"Бой с {mob_name} ({TIER_NAMES[tir]}) начался...")
    victory, log_text, _ = fight(player_data, tir, mob_type)
    
    if victory:
        dary_level = player_data.get("dary", {}).get(str(tir), 1)
        drop_max = {1:1, 2:2, 3:3, 4:5, 5:8, 6:13, 7:21, 8:34, 9:55, 10:89}.get(dary_level, 1)
        drop_amount = random.randint(1, drop_max)
        player_data["chastitsy"][str(tir)] += drop_amount
        save_player(user_id, player_data)
        await query.message.reply_text(f"ПОБЕДА!\n\n{log_text}\n\nДроп: +{drop_amount} частиц")
    else:
        for key in player_data["chastitsy"]:
            player_data["chastitsy"][key] //= 2
        save_player(user_id, player_data)
        await query.message.reply_text(f"ПОРАЖЕНИЕ!\n\n{log_text}\n\nПотеряно 50% частиц")
    
    context.user_data.pop("fight_tir", None)
    context.user_data.pop("fight_mob_type", None)
    
    keyboard = [
        [InlineKeyboardButton("Бой снова", callback_data="main_menu_fight")],
        [InlineKeyboardButton("Назад в меню", callback_data="main_menu_back")]
    ]
    await query.message.reply_text("Что дальше?", reply_markup=InlineKeyboardMarkup(keyboard))

async def main_menu_back(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    await main_menu(query.message, context)
