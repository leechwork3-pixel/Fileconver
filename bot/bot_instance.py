# /bot/bot_instance.py
from pyrogram import Client
from config import Config

app = Client(
    "ConverterBot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN,
    plugins=dict(root="bot/handlers") # Automatically loads all handlers
)
