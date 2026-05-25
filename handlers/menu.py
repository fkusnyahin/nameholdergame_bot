from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.database import load_player, save_player
from core.formulas import get_player_stats

async def menu(message, context):
    keyboard = [
        [InlineKeyboardButton("Fight", callback_data="menu_fight")],
        [InlineKeyboardButton("Character", callback_data="menu_character")],
        [InlineKeyboardButton("Particles", callback_data="menu_particles")],
        [InlineKeyboardButton("Gifts", callback_data="menu_gifts")],
        [InlineKeyboardButton("Help", callback_data="menu_help")],
    ]
    await message.reply_text("Main menu:", reply_markup=InlineKeyboardMarkup(keyboard))

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu_fight":
        from handlers.fight import fight_command
        await fight_command(query.message, context)
    elif data == "menu_character":
        await show_character(query, context)
    elif data == "menu_particles":
        await show_particles(query, context)
    elif data == "menu_gifts":
        from handlers.dary import dary_command
        await dary_command(update, context)
    elif data == "menu_help":
        await show_help(query)
    elif data == "menu_back":
        await show_main_menu(query)
    elif data.startswith("upgrade_"):
        await handle_upgrade(query, context)
    elif data == "exchange_20_1":
        await exchange_particles(query, context)

async def show_main_menu(query):
    keyboard = [
        [InlineKeyboardButton("Fight", callback_data="menu_fight")],
        [InlineKeyboardButton("Character", callback_data="menu_character")],
        [InlineKeyboardButton("Particles", callback_data="menu_particles")],
        [InlineKeyboardButton("Gifts", callback_data="menu_gifts")],
        [InlineKeyboardButton("Help", callback_data="menu_help")],
    ]
    await query.edit_message_text("Main menu:", reply_markup=InlineKeyboardMarkup(keyboard))

async def show_character(query, context):
    user_id = query.from_user.id
    data = load_player(user_id)
    stats = get_player_stats(data)

    text = f"Character\n\n"
    text += f"Core node: tier {data['ku']}\n\n"
    text += f"=== Tier 1 ===\n"
    text += f"Body: {data['telo']} | Head: {data['golova']} | Spirit: {data['duh']}\n\n"
    text += f"=== Tier 2 (Body) ===\n"
    text += f"Power: {data['mosch']} | Agility: {data['lovkost']} | Blood: {data['krov']}\n"
    text += f"=== Tier 2 (Head) ===\n"
    text += f"Mind: {data['um']} | Eyes: {data['glaza']} | Will: {data['volya']}\n"
    text += f"=== Tier 2 (Spirit) ===\n"
    text += f"Life: {data['zhizn']} | Senses: {data['chuvstva']} | Energy: {data['energiya']}\n\n"
    text += f"Damage: {stats['damage']} | HP: {stats['hp_max']} | Dodge: {int(stats['dodge']*100)}%"

    keyboard = [
        [InlineKeyboardButton("Upgrade KU", callback_data="upgrade_ku")],
        [InlineKeyboardButton("Upgrade Body", callback_data="upgrade_telo")],
        [InlineKeyboardButton("Upgrade Head", callback_data="upgrade_golova")],
        [InlineKeyboardButton("Upgrade Spirit", callback_data="upgrade_duh")],
        [InlineKeyboardButton("Back", callback_data="menu_back")],
    ]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def show_particles(query, context):
    user_id = query.from_user.id
    data = load_player(user_id)
    text = f"Particles\nSand: {data['chastitsy']['1']}\nClay: {data['chastitsy']['2']}\nStone: {data['chastitsy']['3']}\nCopper: {data['chastitsy']['4']}"
    keyboard = [
        [InlineKeyboardButton("Exchange 20:1", callback_data="exchange_20_1")],
        [InlineKeyboardButton("Back", callback_data="menu_back")],
    ]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def show_help(query):
    text = "Commands:\n/status - character stats\n/upgrade_ku - upgrade core node\n/upgrade_telo - upgrade body\n/upgrade_golova - upgrade head\n/upgrade_duh - upgrade spirit\n/dary - manage Gifts\n/reset - reset progress\n/menu - open menu"
    keyboard = [[InlineKeyboardButton("Back", callback_data="menu_back")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard))

async def handle_upgrade(query, context):
    user_id = query.from_user.id
    action = query.data.split("_")[1]
    from handlers.upgrade import (
        upgrade_ku, upgrade_telo, upgrade_golova, upgrade_duh,
        upgrade_mosch, upgrade_lovkost, upgrade_krov,
        upgrade_um, upgrade_glaza, upgrade_volya,
        upgrade_zhizn, upgrade_chuvstva, upgrade_energiya
    )
    from telegram import Update
    class FakeUpdate:
        def __init__(self, user_id, query):
            self.effective_user = type('obj', (object,), {'id': user_id})()
            self.message = type('obj', (object,), {'reply_text': query.message.reply_text})()
    fake = FakeUpdate(user_id, query)
    if action == "ku":
        await upgrade_ku(fake, context)
    elif action == "telo":
        await upgrade_telo(fake, context)
    elif action == "golova":
        await upgrade_golova(fake, context)
    elif action == "duh":
        await upgrade_duh(fake, context)
    elif action == "mosch":
        await upgrade_mosch(fake, context)
    elif action == "lovkost":
        await upgrade_lovkost(fake, context)
    elif action == "krov":
        await upgrade_krov(fake, context)
    elif action == "um":
        await upgrade_um(fake, context)
    elif action == "glaza":
        await upgrade_glaza(fake, context)
    elif action == "volya":
        await upgrade_volya(fake, context)
    elif action == "zhizn":
        await upgrade_zhizn(fake, context)
    elif action == "chuvstva":
        await upgrade_chuvstva(fake, context)
    elif action == "energiya":
        await upgrade_energiya(fake, context)
    await show_character(query, context)

async def exchange_particles(query, context):
    user_id = query.from_user.id
    data = load_player(user_id)
    exchanged = False
    for tier in range(1, 4):
        amount = data["chastitsy"][str(tier)]
        if amount >= 20:
            exchange_count = amount // 20
            data["chastitsy"][str(tier)] -= exchange_count * 20
            data["chastitsy"][str(tier + 1)] += exchange_count
            exchanged = True
            await query.message.reply_text(f"Exchanged {exchange_count * 20} particles tier {tier} -> {exchange_count} particles tier {tier + 1}")
            break
    if not exchanged:
        await query.message.reply_text("Not enough particles (need 20 of one tier)")
    save_player(user_id, data)
    await show_particles(query, context)
