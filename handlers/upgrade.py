from telegram import Update
from telegram.ext import ContextTypes
from core.database import load_player, save_player

async def upgrade_ku(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_player(user_id)
    current = data["ku"]
    if current >= 4:
        await update.message.reply_text("Core node already at max tier (Copper)")
        return
    cost_map = {1: 10, 2: 20, 3: 40}
    cost = cost_map[current]
    cost_tier = current + 1
    if data["chastitsy"][str(cost_tier)] >= cost:
        data["chastitsy"][str(cost_tier)] -= cost
        data["ku"] = current + 1
        save_player(user_id, data)
        await update.message.reply_text(f"Core node upgraded to tier {current + 1}!")
    else:
        await update.message.reply_text(f"Need {cost} particles of tier {cost_tier}")

async def upgrade_telo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_player(user_id)
    current = data["telo"]
    if current >= 4:
        await update.message.reply_text("Body already at max tier")
        return
    if current >= data["ku"] + 1:
        await update.message.reply_text(f"Body cannot be higher than KU+1 (KU={data['ku']})")
        return
    next_tier = current + 1
    cost = 10 * next_tier
    if data["chastitsy"][str(next_tier)] >= cost:
        data["chastitsy"][str(next_tier)] -= cost
        data["telo"] = next_tier
        save_player(user_id, data)
        await update.message.reply_text(f"Body upgraded to tier {next_tier}!")
    else:
        await update.message.reply_text(f"Need {cost} particles of tier {next_tier}")

async def upgrade_mosch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_player(user_id)
    current = data["mosch"]
    if current >= 4:
        await update.message.reply_text("Power already at max tier")
        return
    if current >= data["ku"] + 1:
        await update.message.reply_text(f"Power cannot be higher than KU+1 (KU={data['ku']})")
        return
    next_tier = current + 1
    cost = 5 * next_tier
    if data["chastitsy"][str(next_tier)] >= cost:
        data["chastitsy"][str(next_tier)] -= cost
        data["mosch"] = next_tier
        save_player(user_id, data)
        await update.message.reply_text(f"Power upgraded to tier {next_tier}!")
    else:
        await update.message.reply_text(f"Need {cost} particles of tier {next_tier}")
