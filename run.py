# /run.py
from bot.bot_instance import app
from bot.handlers import admin, core, settings, uploader, converter

import logging

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    logging.info("Starting Bot...")
    app.run()
    logging.info("Bot Stopped.")
