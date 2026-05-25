from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from core.database import load_player, save_player
from core.formulas import get_player_stats

async def menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Главное меню"""
    keyboard = [
        [
            InlineKeyboardButton("🎮 Бой", callback_data="menu_fight"),
            InlineKeyboardButton("👤 Персонаж", callback_data="menu_character"),
        ],
        [
            InlineKeyboardButton("💎 Частицы", callback_data="menu_particles"),
            InlineKeyboardButton("❓ Помощь", callback_data="menu_help"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    text = "🏠 **Главное меню**\n\nВыбери действие:"
    await update.message.reply_text(text, reply_markup=reply_markup, parse_mode="Markdown")

async def menu_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Обработчик кнопок меню"""
    query = update.callback_query
    await query.answer()
    data = query.data

    if data == "menu_fight":
        keyboard = [
            [
                InlineKeyboardButton("Тир 1 (Песок)", callback_data="tier_1"),
                InlineKeyboardButton("Тир 2 (Глина)", callback_data="tier_2"),
                InlineKeyboardButton("Тир 3 (Камень)", callback_data="tier_3"),
                InlineKeyboardButton("Тир 4 (Медь)", callback_data="tier_4"),
            ],
            [InlineKeyboardButton("⬅️ Назад в меню", callback_data="menu_back")]
        ]
        await query.edit_message_text("Выбери тир моба:", reply_markup=InlineKeyboardMarkup(keyboard))
    elif data == "menu_character":
        await show_character(query, context)
    elif data == "menu_particles":
        await show_particles(query, context)
    elif data == "menu_help":
        await show_help(query)
    elif data == "menu_back":
        await show_main_menu(query)
    elif data.startswith("upgrade_"):
        await handle_upgrade(query, context)
    elif data == "exchange_20_1":
        await exchange_particles(query, context)

async def show_main_menu(query):
    """Показать главное меню"""
    keyboard = [
        [
            InlineKeyboardButton("🎮 Бой", callback_data="menu_fight"),
            InlineKeyboardButton("👤 Персонаж", callback_data="menu_character"),
        ],
        [
            InlineKeyboardButton("💎 Частицы", callback_data="menu_particles"),
            InlineKeyboardButton("❓ Помощь", callback_data="menu_help"),
        ],
    ]
    await query.edit_message_text(
        "🏠 **Главное меню**\n\nВыбери действие:",
        reply_markup=InlineKeyboardMarkup(keyboard),
        parse_mode="Markdown"
    )

async def show_character(query, context):
    user_id = query.from_user.id
    data = load_player(user_id)
    stats = get_player_stats(data)

    text = f"👤 **Персонаж**\n\n"
    text += f"🔹 Корневой узел: тир {data['ku']}\n"
    text += f"🔹 Тело: тир {data['telo']}\n"
    text += f"🔹 Мощь: тир {data['mosch']}\n"
    text += f"⚔️ Урон: {stats['damage']}\n"
    text += f"❤️ Здоровье: {stats['hp_max']}\n"

    keyboard = [
        [
            InlineKeyboardButton("⬆️ КУ", callback_data="upgrade_ku"),
            InlineKeyboardButton("⬆️ Тело", callback_data="upgrade_telo"),
            InlineKeyboardButton("⬆️ Мощь", callback_data="upgrade_mosch"),
        ],
        [InlineKeyboardButton("💎 Частицы", callback_data="menu_particles")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="menu_back")],
    ]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def show_particles(query, context):
    user_id = query.from_user.id
    data = load_player(user_id)

    text = f"💎 **Ваши частицы**\n\n"
    text += f"🟤 Песок: {data['chastitsy']['1']}\n"
    text += f"🟠 Глина: {data['chastitsy']['2']}\n"
    text += f"⚪ Камень: {data['chastitsy']['3']}\n"
    text += f"🟡 Медь: {data['chastitsy']['4']}\n"

    keyboard = [
        [InlineKeyboardButton("🔄 Обмен 20:1", callback_data="exchange_20_1")],
        [InlineKeyboardButton("⬅️ Назад", callback_data="menu_back")],
    ]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def show_help(query):
    text = "❓ **Помощь**\n\n"
    text += "📋 Команды:\n"
    text += "/status — статус персонажа\n"
    text += "/fight — начать бой\n"
    text += "/upgrade_ku — повысить КУ\n"
    text += "/upgrade_telo — повысить Тело\n"
    text += "/upgrade_mosch — повысить Мощь\n"
    text += "/reset — сбросить прогресс\n"
    text += "/menu — открыть меню\n"

    keyboard = [[InlineKeyboardButton("⬅️ Назад", callback_data="menu_back")]]
    await query.edit_message_text(text, reply_markup=InlineKeyboardMarkup(keyboard), parse_mode="Markdown")

async def handle_upgrade(query, context):
    user_id = query.from_user.id
    data = load_player(user_id)
    action = query.data.split("_")[1]

    from handlers.upgrade import upgrade_ku, upgrade_telo, upgrade_mosch
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
    elif action == "mosch":
        await upgrade_mosch(fake, context)

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
            await query.message.reply_text(f"🔄 Обменяно {exchange_count * 20} частиц тира {tier} → {exchange_count} частиц тира {tier + 1}")
            break

    if not exchanged:
        await query.message.reply_text("❌ Нет 20 частиц одного тира для обмена")

    save_player(user_id, data)
    await show_particles(query, context)