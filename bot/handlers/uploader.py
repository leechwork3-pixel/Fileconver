# /bot/handlers/uploader.py
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.bot_instance import app
from telegraph import Telegraph, upload_file
from config import Config

telegraph = Telegraph(account=Config.TELEGRAPH_ACCOUNT_NAME)

@app.on_message(filters.photo & filters.private)
async def telegraph_upload(client: Client, message: Message):
    msg = await message.reply_text("Uploading to Telegraph...")
    try:
        photo_path = await message.download()
        response = upload_file(photo_path)
        url = f"https://telegra.ph{response[0]}"
        await msg.edit_text(f"<b>Image uploaded successfully!</b>\n\n<b>URL:</b> {url}")
    except Exception as e:
        await msg.edit_text(f"Failed to upload image. Error: {e}")

