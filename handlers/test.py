from telegram import Update
from telegram.ext import ContextTypes
from core.database import load_player, save_player

async def add_pesok(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_player(user_id)
    try:
        amount = int(context.args[0])
        data["chastitsy"]["1"] += amount
        save_player(user_id, data)
        await update.message.reply_text(f"➕ Добавлено {amount} песка")
    except:
        await update.message.reply_text("❌ /add_pesok <число>")

async def add_glina(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_player(user_id)
    try:
        amount = int(context.args[0])
        data["chastitsy"]["2"] += amount
        save_player(user_id, data)
        await update.message.reply_text(f"➕ Добавлено {amount} глины")
    except:
        await update.message.reply_text("❌ /add_glina <число>")

async def add_kamen(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_player(user_id)
    try:
        amount = int(context.args[0])
        data["chastitsy"]["3"] += amount
        save_player(user_id, data)
        await update.message.reply_text(f"➕ Добавлено {amount} камня")
    except:
        await update.message.reply_text("❌ /add_kamen <число>")

async def add_med(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_player(user_id)
    try:
        amount = int(context.args[0])
        data["chastitsy"]["4"] += amount
        save_player(user_id, data)
        await update.message.reply_text(f"➕ Добавлено {amount} меди")
    except:
        await update.message.reply_text("❌ /add_med <число>")
