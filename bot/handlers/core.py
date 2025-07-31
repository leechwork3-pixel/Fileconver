# /bot/handlers/core.py
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.bot_instance import app
from database.mongo import db
from config import Config # <-- ADD THIS LINE

@app.on_message(filters.command("start") & filters.private)
# ... rest of the file is the same
