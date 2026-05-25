from telegram import Update
from telegram.ext import ContextTypes
from core.database import load_player
from core.formulas import get_player_stats

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    data = load_player(user_id)
    stats = get_player_stats(data)

    text = f"Character stats:\n\n"
    text += f"Core node: tier {data['ku']}\n"
    text += f"\n=== Tier 1 nodes ===\n"
    text += f"Body: tier {data['telo']}\n"
    text += f"Head: tier {data['golova']}\n"
    text += f"Spirit: tier {data['duh']}\n"
    text += f"\n=== Tier 2 nodes (Body) ===\n"
    text += f"Power: tier {data['mosch']}\n"
    text += f"Agility: tier {data['lovkost']}\n"
    text += f"Blood: tier {data['krov']}\n"
    text += f"\n=== Tier 2 nodes (Head) ===\n"
    text += f"Mind: tier {data['um']}\n"
    text += f"Eyes: tier {data['glaza']}\n"
    text += f"Will: tier {data['volya']}\n"
    text += f"\n=== Tier 2 nodes (Spirit) ===\n"
    text += f"Life: tier {data['zhizn']}\n"
    text += f"Senses: tier {data['chuvstva']}\n"
    text += f"Energy: tier {data['energiya']}\n"
    text += f"\n=== Combat stats ===\n"
    text += f"Physical damage: {stats['damage']}\n"
    text += f"Magic damage: {stats['magic_damage']}\n"
    text += f"Max HP: {stats['hp_max']}\n"
    text += f"Dodge chance: {int(stats['dodge']*100)}%\n"
    text += f"Attack speed: {stats['attack_speed']:.1f}\n"
    text += f"Mana: {stats['mana_max']}\n"
    text += f"Mana regen: {int(stats['mana_regen']*100)}%/sec\n"
    text += f"\n=== Particles ===\n"
    text += f"Sand: {data['chastitsy']['1']}\n"
    text += f"Clay: {data['chastitsy']['2']}\n"
    text += f"Stone: {data['chastitsy']['3']}\n"
    text += f"Copper: {data['chastitsy']['4']}"

    await update.message.reply_text(text)