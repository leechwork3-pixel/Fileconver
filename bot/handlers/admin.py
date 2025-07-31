# /bot/handlers/admin.py
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.bot_instance import app
from bot.utils.decorators import is_sudo
from database.mongo import db
from config import Config

@app.on_message(filters.command("addsudo") & filters.user(Config.SUDO_ADMINS))
async def add_sudo_command(client: Client, message: Message):
    try:
        user_id = int(message.text.split(None, 1)[1])
        if user_id in Config.SUDO_ADMINS:
            await message.reply_text("This user is already a Sudo Admin.")
            return
        Config.SUDO_ADMINS.append(user_id)
        await message.reply_text(f"Successfully added `{user_id}` to Sudo Admins.")
    except (IndexError, ValueError):
        await message.reply_text("<b>Usage:</b> /addsudo <user_id>")

@app.on_message(filters.command("rmsudo") & filters.user(Config.SUDO_ADMINS))
async def rm_sudo_command(client: Client, message: Message):
    try:
        user_id = int(message.text.split(None, 1)[1])
        if user_id not in Config.SUDO_ADMINS:
            await message.reply_text("This user is not a Sudo Admin.")
            return
        Config.SUDO_ADMINS.remove(user_id)
        await message.reply_text(f"Successfully removed `{user_id}` from Sudo Admins.")
    except (IndexError, ValueError):
        await message.reply_text("<b>Usage:</b> /rmsudo <user_id>")

@app.on_message(filters.command("ban") & filters.user(Config.SUDO_ADMINS))
async def ban_command(client: Client, message: Message):
    try:
        user_id = int(message.text.split(None, 1)[1])
        await db.ban_user(user_id)
        await message.reply_text(f"User `{user_id}` has been banned.")
    except (IndexError, ValueError):
        await message.reply_text("<b>Usage:</b> /ban <user_id>")

@app.on_message(filters.command("unban") & filters.user(Config.SUDO_ADMINS))
async def unban_command(client: Client, message: Message):
    try:
        user_id = int(message.text.split(None, 1)[1])
        await db.unban_user(user_id)
        await message.reply_text(f"User `{user_id}` has been unbanned.")
    except (IndexError, ValueError):
        await message.reply_text("<b>Usage:</b> /unban <user_id>")

@app.on_message(filters.command("broadcast") & filters.user(Config.SUDO_ADMINS))
async def broadcast_command(client: Client, message: Message):
    if not message.reply_to_message:
        await message.reply_text("Please reply to a message to broadcast it.")
        return

    msg = await message.reply_text("Broadcasting... this may take a while.")
    all_users = await db.get_all_user_ids()
    sent_count = 0
    failed_count = 0

    for user_id in all_users:
        try:
            await message.reply_to_message.copy(user_id)
            sent_count += 1
            await asyncio.sleep(0.1) # Avoid API rate limits
        except Exception:
            failed_count += 1
    
    await msg.edit_text(f"**Broadcast Complete**\n\nSent to: {sent_count} users\nFailed for: {failed_count} users")
