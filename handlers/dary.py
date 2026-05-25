from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.database import load_player, save_player

async def dary_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
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
    
    text += f"\n*Upgrade cost*: 10 particles of NEXT tier"
    text += f"\n*Max level* = your Core node tier ({ku})"
    
    keyboard = []
    for tier in range(1, 5):
        current = dary.get(str(tier), 0)
        if current < ku:
            keyboard.append([InlineKeyboardButton(f"Upgrade Tier {tier}", callback_data=f"upgrade_dary_{tier}")])
    
    keyboard.append([InlineKeyboardButton("Back to menu", callback_data="menu_back")])
    
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def upgrade_dary(update: Update, context: ContextTypes.DEFAULT_TYPE, tier: int):
    user_id = update.effective_user.id
    data = load_player(user_id)
    
    current_level = data.get("dary", {}).get(str(tier), 0)
    max_level = data.get("ku", 1)
    
    if current_level >= max_level:
        await update.message.reply_text(f"Tier {tier} Gifts already at max level ({max_level})")
        return
    
    cost_tier = tier + 1
    cost = 10
    if cost_tier > 4:
        await update.message.reply_text("Cannot upgrade: no higher tier exists")
        return
    
    if data["chastitsy"][str(cost_tier)] >= cost:
        data["chastitsy"][str(cost_tier)] -= cost
        if "dary" not in data:
            data["dary"] = {"1": 1, "2": 0, "3": 0, "4": 0}
        data["dary"][str(tier)] = current_level + 1
        save_player(user_id, data)
        await update.message.reply_text(f"Tier {tier} Gifts upgraded to level {current_level + 1}!")
    else:
        await update.message.reply_text(f"Need {cost} particles of tier {cost_tier}")

async def upgrade_dary_1(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await upgrade_dary(update, context, 1)

async def upgrade_dary_2(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await upgrade_dary(update, context, 2)

async def upgrade_dary_3(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await upgrade_dary(update, context, 3)

async def upgrade_dary_4(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await upgrade_dary(update, context, 4)
