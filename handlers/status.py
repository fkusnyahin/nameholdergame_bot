from telegram import Update
from telegram.ext import ContextTypes
from core.database import load_player
from core.formulas import get_player_stats

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_player(user_id)
    stats = get_player_stats(data)

    text = f"Character stats:\n\nCore node: tier {data['ku']}\nBody: tier {data['telo']}\nPower: tier {data['mosch']}\nDamage: {stats['damage']}\nHP: {stats['hp_max']}\n\nParticles:\nSand: {data['chastitsy']['1']}\nClay: {data['chastitsy']['2']}\nStone: {data['chastitsy']['3']}\nCopper: {data['chastitsy']['4']}"
    await update.message.reply_text(text)
