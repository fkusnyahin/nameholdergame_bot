from telegram import Update
from telegram.ext import ContextTypes
from core.database import load_player
from core.formulas import get_player_stats

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_player(user_id)
    stats = get_player_stats(data)

    text = f"📊 **Статус персонажа**\n\n"
    text += f"🔹 Корневой узел: тир {data['ku']}\n"
    text += f"🔹 Тело: тир {data['telo']}\n"
    text += f"🔹 Мощь: тир {data['mosch']}\n"
    text += f"⚔️ Урон: {stats['damage']}\n"
    text += f"❤️ Здоровье: {stats['hp_max']}\n\n"
    text += f"💎 **Частицы:**\n"
    text += f"  🟤 Песок: {data['chastitsy']['1']}\n"
    text += f"  🟠 Глина: {data['chastitsy']['2']}\n"
    text += f"  ⚪ Камень: {data['chastitsy']['3']}\n"
    text += f"  🟡 Медь: {data['chastitsy']['4']}"

    await update.message.reply_text(text, parse_mode="Markdown")
