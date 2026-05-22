from telegram import Update
from telegram.ext import ContextTypes
from core.database import load_player

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    load_player(user_id)
    await update.message.reply_text(
        "🎮 Добро пожаловать в RPG бот!\n\n"
        "📋 Команды:\n"
        "/status — посмотреть своего персонажа\n"
        "/fight — начать бой (с кнопками)\n"
        "/upgrade_ku — повысить Корневой узел\n"
        "/upgrade_telo — повысить Тело\n"
        "/upgrade_mosch — повысить Мощь\n"
        "/reset — сбросить прогресс"
    )
