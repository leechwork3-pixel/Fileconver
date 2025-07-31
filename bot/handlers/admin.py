# /bot/handlers/admin.py
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.bot_instance import app
from bot.utils.decorators import is_sudo
from database.mongo import db
from config import Config # <-- ADD THIS LINE

@app.on_message(filters.command("addsudo") & filters.user(Config.SUDO_ADMINS))
# ... rest of the file is the same
