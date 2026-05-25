from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.database import load_player, save_player

DROP_MAX = {1: 1, 2: 2, 3: 3, 4: 5, 5: 8, 6: 13, 7: 21, 8: 34, 9: 55, 10: 89}

async def dary_command(message, context):
    user_id = message.chat.id
    data = load_player(user_id)
    dary = data.get("dary", {"1": 1, "2": 0, "3": 0, "4": 0})
    ku = data.get("ku", 1)
    
    text = "*Gifts of the Higher (drop bonus)*\n\n"
    text += "Each level increases maximum drop from mobs:\n"
    text += "Lv1: 1 | Lv2: 1-2 | Lv3: 1-3 | Lv4: 1-5 | Lv5: 1-8\n\n"
    
    for tier in range(1, 5):
        level = dary.get(str(tier), 0)
        max_level = ku
        status = f"level {level}" if level > 0 else "not unlocked"
        if level >= max_level:
            status += " (MAX)"
        text += f"*Tier {tier}*: {status}\n"
    
    text += f"\nUpgrade cost: 10 particles of NEXT tier"
    text += f"\nMax level = your Core node tier ({ku})"
    
    keyboard = []
    for tier in range(1, 5):
        current = dary.get(str(tier), 0)
        if current < ku:
            cb = f"dary_upgrade_{tier}"
            print(f"DEBUG: creating button for tier {tier} with callback_data={cb}")
            keyboard.append([InlineKeyboardButton(f"Upgrade Tier {tier}", callback_data=cb)])
    
    keyboard.append([InlineKeyboardButton("Back to menu", callback_data="main_menu_back")])
    
    await message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def dary_upgrade_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    tier = int(query.data.split("_")[2])
    
    user_id = query.from_user.id
    data = load_player(user_id)
    current_level = data.get("dary", {}).get(str(tier), 0)
    max_level = data.get("ku", 1)
    next_level = current_level + 1 if current_level < max_level else current_level
    
    cost_tier = tier + 1
    cost = 10
    cost_names = ["", "Sand", "Clay", "Stone", "Copper", "Bronze", "Steel", "Titan", "Wolfram", "Star"]
    cost_name = cost_names[cost_tier] if cost_tier < len(cost_names) else "?"
    
    text = f"*Upgrade Tier {tier} Gifts*\n\n"
    text += f"Current level: {current_level}\n"
    if current_level < max_level:
        text += f"Next level: {next_level}\n"
        text += f"Current max drop: 1-{DROP_MAX.get(current_level, 1)}\n"
        text += f"Next max drop: 1-{DROP_MAX.get(next_level, 1)}\n\n"
        text += f"Cost: {cost} {cost_name} particles\n"
    else:
        text += f"MAX level reached ({max_level})\n"
    
    keyboard = []
    if current_level < max_level:
        keyboard.append([InlineKeyboardButton(f"Upgrade (cost: {cost} {cost_name})", callback_data=f"dary_do_upgrade_{tier}")])
    keyboard.append([InlineKeyboardButton("Back to Gifts", callback_data="main_menu_gifts")])
    keyboard.append([InlineKeyboardButton("Back to menu", callback_data="main_menu_back")])
    
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def dary_do_upgrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    tier = int(query.data.split("_")[3])
    
    user_id = query.from_user.id
    data = load_player(user_id)
    
    current_level = data.get("dary", {}).get(str(tier), 0)
    max_level = data.get("ku", 1)
    
    if current_level >= max_level:
        await query.message.reply_text(f"Tier {tier} Gifts already at max level ({max_level})")
        return
    
    cost_tier = tier + 1
    cost = 10
    if cost_tier > 4:
        await query.message.reply_text("Cannot upgrade: no higher tier exists")
        return
    
    if data["chastitsy"][str(cost_tier)] >= cost:
        data["chastitsy"][str(cost_tier)] -= cost
        if "dary" not in data:
            data["dary"] = {"1": 1, "2": 0, "3": 0, "4": 0}
        data["dary"][str(tier)] = current_level + 1
        save_player(user_id, data)
        await query.message.reply_text(f"✅ Tier {tier} Gifts upgraded to level {current_level + 1}!")
        await dary_command(query.message, context)
    else:
        await query.message.reply_text(f"❌ Need {cost} particles of tier {cost_tier}")

async def upgrade_dary_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await dary_upgrade_menu(update, context)

async def upgrade_dary_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await dary_upgrade_menu(update, context)

async def upgrade_dary_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await dary_upgrade_menu(update, context)

async def upgrade_dary_4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await dary_upgrade_menu(update, context)
