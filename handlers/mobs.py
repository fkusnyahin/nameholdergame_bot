from telegram import Update
from telegram.ext import ContextTypes
from core.mobs_loader import get_mobs_from_sheets

async def mobs(update: Update, context: ContextTypes.DEFAULT_TYPE):
    mobs = get_mobs_from_sheets()
    if not mobs:
        await update.message.reply_text("❌ Нет данных о мобах")
        return
    text = "📊 Мобы из JSON:\n\n"
    for mob in mobs[:10]:
        text += f"• {mob.get('name')} | {mob.get('role')} | HP: {mob.get('hp')}\n"
    await update.message.reply_text(text, parse_mode="Markdown")
