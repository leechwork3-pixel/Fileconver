# /bot/handlers/settings.py
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.bot_instance import app
from bot.utils.decorators import is_sudo
from database.mongo import db
from config import Config # <-- ADD THIS LINE

@app.on_message(filters.command("settings") & filters.user(Config.SUDO_ADMINS))
@is_sudo
async def settings_command(client: Client, message: Message):
    start_text = await db.get_setting("start_text") or "Not Set"
    start_pic = await db.get_setting("start_pic") or "Not Set"
    
    settings_msg = (
        f"<b>Bot Settings</b>\n\n"
        f"<b>Start Text:</b> <pre>{start_text}</pre>\n"
        f"<b>Start Picture URL/ID:</b> <pre>{start_pic}</pre>\n\n"
        f"Use /set_start_text and /set_start_pic to change these."
    )
    await message.reply_text(settings_msg, parse_mode="html")

@app.on_message(filters.command("set_start_text") & filters.user(Config.SUDO_ADMINS))
@is_sudo
async def set_start_text_command(client: Client, message: Message):
    try:
        new_text = message.text.split(None, 1)[1]
        await db.set_setting("start_text", new_text)
        await message.reply_text("✅ Start text has been updated successfully!")
    except IndexError:
        await message.reply_text("<b>Usage:</b> /set_start_text <your new welcome message>\n\nSupports HTML formatting.")

@app.on_message(filters.command("set_start_pic") & filters.user(Config.SUDO_ADMINS))
@is_sudo
async def set_start_pic_command(client: Client, message: Message):
    if message.reply_to_message and message.reply_to_message.photo:
        file_id = message.reply_to_message.photo.file_id
        await db.set_setting("start_pic", file_id)
        await message.reply_text("✅ Start picture has been updated successfully!")
    else:
        await message.reply_text("Please reply to an image with /set_start_pic to set it as the start picture.")
        
