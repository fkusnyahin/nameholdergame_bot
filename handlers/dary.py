from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.database import load_player, save_player

async def dary_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_player(user_id)
    dary = data.get("dary", {"1": 1, "2": 0, "3": 0, "4": 0})
    
    text = "Gifts of the Higher (drop chance increase):\n\n"
    text += f"Tier 1 (Sand): level {dary.get('1', 0)}\n"
    text += f"Tier 2 (Clay): level {dary.get('2', 0)}\n"
    text += f"Tier 3 (Stone): level {dary.get('3', 0)}\n"
    text += f"Tier 4 (Copper): level {dary.get('4', 0)}\n\n"
    text += "Upgrade costs: 10 particles of NEXT tier"
    
    keyboard = [
        [InlineKeyboardButton("Upgrade Sand", callback_data="upgrade_dary_1")],
        [InlineKeyboardButton("Upgrade Clay", callback_data="upgrade_dary_2")],
        [InlineKeyboardButton("Upgrade Stone", callback_data="upgrade_dary_3")],
        [InlineKeyboardButton("Upgrade Copper", callback_data="upgrade_dary_4")],
        [InlineKeyboardButton("Back to menu", callback_data="menu_back")],
    ]
    await update.message.reply_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def upgrade_dary(update: Update, context: ContextTypes.DEFAULT_TYPE, tier: int):
    user_id = update.effective_user.id
    data = load_player(user_id)
    
    current_level = data.get("dary", {}).get(str(tier), 0)
    max_level = data.get("ku", 1)
    
    if current_level >= max_level:
        await update.message.reply_text(f"Cannot upgrade: your KU level is {max_level}")
        return
    
    cost_tier = tier + 1
    cost = 10
    if cost_tier > 4:
        await update.message.reply_text("Max tier reached for upgrades")
        return
    
    if data["chastitsy"][str(cost_tier)] >= cost:
        data["chastitsy"][str(cost_tier)] -= cost
        if "dary" not in data:
            data["dary"] = {"1": 1, "2": 0, "3": 0, "4": 0}
        data["dary"][str(tier)] = current_level + 1
        save_player(user_id, data)
        await update.message.reply_text(f"Dary for tier {tier} upgraded to level {current_level + 1}!")
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
