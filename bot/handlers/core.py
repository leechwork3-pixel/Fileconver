# /bot/handlers/core.py

from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode # <-- 1. IMPORT THIS
from bot.bot_instance import app
from database.mongo import db
from config import Config

@app.on_message(filters.command("start") & filters.private)
async def start_command(client: Client, message: Message):
    is_new_user = await db.add_user(message.from_user.id)
    if is_new_user and Config.LOG_CHANNEL != 0:
        try:
            await client.send_message(
                Config.LOG_CHANNEL,
                f"**New User Started Bot!**\n\n"
                f"**User:** {message.from_user.mention}\n"
                f"**ID:** `{message.from_user.id}`"
            )
        except Exception as e:
            print(f"Error sending new user notification: {e}")

    start_text = await db.get_setting("start_text") or "Welcome! I can convert files and upload images to Telegraph."
    start_pic = await db.get_setting("start_pic")

    if start_pic:
        await message.reply_photo(
            photo=start_pic, 
            caption=start_text, 
            parse_mode=ParseMode.HTML  # <-- 2. CORRECT THIS
        )
    else:
        await message.reply_text(
            start_text,
            parse_mode=ParseMode.HTML  # <-- 3. CORRECT THIS
        )

@app.on_message(filters.command("help") & filters.private)
async def help_command(client: Client, message: Message):
    help_text = """
    <b>Here are the available commands:</b>

    /start - Start the bot
    /help - Show this message
    
    <b>File Conversion:</b>
    Simply send me a file (EPUB, MOBI, AZW3, FB2, CBZ, PDF) and I will try to convert it.
    
    <b>Image Uploader:</b>
    Send me an image and I will upload it to Telegraph and give you the link.
    
    <b>Admin Commands:</b>
    /settings - View current settings
    /set_start_text - Set the welcome message
    /set_start_pic - Set the welcome image (reply to an image)
    /ban <user_id> - Ban a user
    /unban <user_id> - Unban a user
    /broadcast - Send a message to all users (reply to a message)
    /addsudo <user_id> - Add a Sudo Admin
    /rmsudo <user_id> - Remove a Sudo Admin
    """
    await message.reply_text(
        help_text,
        parse_mode=ParseMode.HTML  # <-- 4. CORRECT THIS
    )
    
