import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from config import TOKEN
from core.database import init_db
from telegram.ext import Application, CommandHandler, CallbackQueryHandler

# Импорты команд
from handlers.start import start
from handlers.status import status
from handlers.fight import fight_command, button_callback
from handlers.upgrade import upgrade_ku, upgrade_telo, upgrade_mosch
from handlers.test import add_pesok, add_glina, add_kamen, add_med
from handlers.reset import reset

def main():
    init_db()
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("fight", fight_command))
    app.add_handler(CallbackQueryHandler(button_callback))
    app.add_handler(CommandHandler("upgrade_ku", upgrade_ku))
    app.add_handler(CommandHandler("upgrade_telo", upgrade_telo))
    app.add_handler(CommandHandler("upgrade_mosch", upgrade_mosch))
    app.add_handler(CommandHandler("add_pesok", add_pesok))
    app.add_handler(CommandHandler("add_glina", add_glina))
    app.add_handler(CommandHandler("add_kamen", add_kamen))
    app.add_handler(CommandHandler("add_med", add_med))
    app.add_handler(CommandHandler("reset", reset))

    print("🚀 Бот запущен!")
    app.run_polling()

if __name__ == "__main__":
    main()
