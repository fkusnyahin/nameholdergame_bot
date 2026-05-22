from telegram import Update
from telegram.ext import ContextTypes
from core.database import load_player, save_player

async def upgrade_ku(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_player(user_id)
    current = data["ku"]
    if current >= 4:
        await update.message.reply_text("❌ Вы уже на максимальном тире (Медь)")
        return
    cost_map = {1: 10, 2: 20, 3: 40}
    cost = cost_map[current]
    cost_tier = current + 1
    if data["chastitsy"][str(cost_tier)] >= cost:
        data["chastitsy"][str(cost_tier)] -= cost
        data["ku"] = current + 1
        save_player(user_id, data)
        await update.message.reply_text(f"✅ Корневой узел повышен до тира {current + 1}!")
    else:
        await update.message.reply_text(f"❌ Нужно {cost} частиц тира {cost_tier}")

async def upgrade_telo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_player(user_id)
    current = data["telo"]
    if current >= 4:
        await update.message.reply_text("❌ Тело уже на максимальном тире")
        return
    if current >= data["ku"] + 1:
        await update.message.reply_text(f"❌ Тело не может быть выше КУ+1 (КУ={data['ku']})")
        return
    next_tier = current + 1
    cost = 10 * next_tier
    if data["chastitsy"][str(next_tier)] >= cost:
        data["chastitsy"][str(next_tier)] -= cost
        data["telo"] = next_tier
        save_player(user_id, data)
        await update.message.reply_text(f"✅ Тело повышено до тира {next_tier}!")
    else:
        await update.message.reply_text(f"❌ Нужно {cost} частиц тира {next_tier}")

async def upgrade_mosch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_player(user_id)
    current = data["mosch"]
    if current >= 4:
        await update.message.reply_text("❌ Мощь уже на максимальном тире")
        return
    if current >= data["ku"] + 1:
        await update.message.reply_text(f"❌ Мощь не может быть выше КУ+1 (КУ={data['ku']})")
        return
    next_tier = current + 1
    cost = 5 * next_tier
    if data["chastitsy"][str(next_tier)] >= cost:
        data["chastitsy"][str(next_tier)] -= cost
        data["mosch"] = next_tier
        save_player(user_id, data)
        await update.message.reply_text(f"✅ Мощь повышена до тира {next_tier}!")
    else:
        await update.message.reply_text(f"❌ Нужно {cost} частиц тира {next_tier}")
