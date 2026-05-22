from telegram import Update
from telegram.ext import ContextTypes
import sqlite3
from core.database import DB_PATH

async def reset(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("DELETE FROM players WHERE user_id = ?", (user_id,))
    conn.commit()
    conn.close()
    await update.message.reply_text("🔄 Прогресс сброшен! Используйте /start для начала.")
