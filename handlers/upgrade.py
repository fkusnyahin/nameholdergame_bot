from telegram import Update
from telegram.ext import ContextTypes
from core.database import load_player, save_player

# Общая функция для прокачки любого узла
async def upgrade_node(update: Update, context: ContextTypes.DEFAULT_TYPE, node_name: str, max_tier: int = 4):
    user_id = update.effective_user.id
    data = load_player(user_id)
    current = data[node_name]
    if current >= max_tier:
        await update.message.reply_text(f"{node_name} already at max tier")
        return
    if node_name in ["telo", "mosch", "golova", "duh"]:
        if current >= data["ku"] + 1:
            await update.message.reply_text(f"{node_name} cannot be higher than KU+1 (KU={data['ku']})")
            return
    next_tier = current + 1
    # Стоимость: для У1 — 10×тир, для У2 — 5×тир
    if node_name in ["telo", "mosch", "golova", "duh"]:
        cost = 10 * next_tier
    else:
        cost = 5 * next_tier
    if data["chastitsy"][str(next_tier)] >= cost:
        data["chastitsy"][str(next_tier)] -= cost
        data[node_name] = next_tier
        save_player(user_id, data)
        await update.message.reply_text(f"{node_name} upgraded to tier {next_tier}!")
    else:
        await update.message.reply_text(f"Need {cost} particles of tier {next_tier}")

# Команды для каждого узла
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
    await upgrade_node(update, context, "telo")

async def upgrade_mosch(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await upgrade_node(update, context, "mosch")

async def upgrade_golova(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await upgrade_node(update, context, "golova")

async def upgrade_duh(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await upgrade_node(update, context, "duh")

async def upgrade_lovkost(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await upgrade_node(update, context, "lovkost")

async def upgrade_krov(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await upgrade_node(update, context, "krov")

async def upgrade_um(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await upgrade_node(update, context, "um")

async def upgrade_glaza(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await upgrade_node(update, context, "glaza")

async def upgrade_volya(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await upgrade_node(update, context, "volya")

async def upgrade_zhizn(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await upgrade_node(update, context, "zhizn")

async def upgrade_chuvstva(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await upgrade_node(update, context, "chuvstva")

async def upgrade_energiya(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await upgrade_node(update, context, "energiya")