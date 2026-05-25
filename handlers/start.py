from telegram import Update
from telegram.ext import ContextTypes
from core.database import load_player
from handlers.menu import menu

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    load_player(user_id)
    await menu(update.message, context)
