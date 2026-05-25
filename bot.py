import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import TOKEN
from core.database import init_db
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

from handlers.start import start
from handlers.status import status
from handlers.fight import fight_command, tier_selected, type_selected, fight_start, main_menu_back
from handlers.upgrade import (
    upgrade_ku, upgrade_telo, upgrade_mosch, upgrade_golova, upgrade_duh,
    upgrade_lovkost, upgrade_krov, upgrade_um, upgrade_glaza, upgrade_volya,
    upgrade_zhizn, upgrade_chuvstva, upgrade_energiya
)
from handlers.dary import dary_command, upgrade_dary_1, upgrade_dary_2, upgrade_dary_3, upgrade_dary_4, dary_upgrade_menu, dary_do_upgrade, dary_upgrade_menu, dary_do_upgrade
from handlers.test import add_pesok, add_glina, add_kamen, add_med
from handlers.reset import reset
from handlers.main_menu import main_menu, main_menu_callback

def main():
    init_db()
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("menu", main_menu))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("dary", dary_command))

    app.add_handler(CommandHandler("upgrade_ku", upgrade_ku))
    app.add_handler(CommandHandler("upgrade_telo", upgrade_telo))
    app.add_handler(CommandHandler("upgrade_mosch", upgrade_mosch))
    app.add_handler(CommandHandler("upgrade_golova", upgrade_golova))
    app.add_handler(CommandHandler("upgrade_duh", upgrade_duh))
    app.add_handler(CommandHandler("upgrade_lovkost", upgrade_lovkost))
    app.add_handler(CommandHandler("upgrade_krov", upgrade_krov))
    app.add_handler(CommandHandler("upgrade_um", upgrade_um))
    app.add_handler(CommandHandler("upgrade_glaza", upgrade_glaza))
    app.add_handler(CommandHandler("upgrade_volya", upgrade_volya))
    app.add_handler(CommandHandler("upgrade_zhizn", upgrade_zhizn))
    app.add_handler(CommandHandler("upgrade_chuvstva", upgrade_chuvstva))
    app.add_handler(CommandHandler("upgrade_energiya", upgrade_energiya))

    app.add_handler(CommandHandler("upgrade_dary_1", upgrade_dary_1))
    app.add_handler(CommandHandler("upgrade_dary_2", upgrade_dary_2))
    app.add_handler(CommandHandler("upgrade_dary_3", upgrade_dary_3))
    app.add_handler(CommandHandler("upgrade_dary_4", upgrade_dary_4))

    app.add_handler(CommandHandler("add_pesok", add_pesok))
    app.add_handler(CommandHandler("add_glina", add_glina))
    app.add_handler(CommandHandler("add_kamen", add_kamen))
    app.add_handler(CommandHandler("add_med", add_med))
    app.add_handler(CommandHandler("reset", reset))

    app.add_handler(CallbackQueryHandler(tier_selected, pattern="^tier_"))
    app.add_handler(CallbackQueryHandler(type_selected, pattern="^select_"))
    app.add_handler(CallbackQueryHandler(fight_start, pattern="^fight_start_"))
    app.add_handler(CallbackQueryHandler(main_menu_back, pattern="^main_menu_back$"))
    app.add_handler(CallbackQueryHandler(main_menu_back, pattern="^main_menu_back$"))
    app.add_handler(CallbackQueryHandler(main_menu_callback, pattern="^(main_menu_|upgrade_|exchange_)"))

    print("Bot started!")
    app.run_polling()

if __name__ == "__main__":
    main()





