# /bot/handlers/uploader.py
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.bot_instance import app
from telegraph import Telegraph, upload_file
from config import Config

# Check if the token is set in your environment variables
if Config.TELEGRAPH_TOKEN:
    telegraph = Telegraph(access_token=Config.TELEGRAPH_TOKEN)
else:
    telegraph = None

@app.on_message(filters.photo & filters.private)
async def telegraph_upload(client: Client, message: Message):
    # Check if the Telegraph client was properly initialized
    if not telegraph:
        await message.reply_text(
            "Telegraph is not configured. The `TELEGRAPH_TOKEN` environment variable is missing."
        )
        return

    msg = await message.reply_text("Uploading to Telegraph...")
    try:
        photo_path = await message.download()
        response = upload_file(photo_path)
        url = f"https://telegra.ph{response[0]}"
        await msg.edit_text(
            f"<b>Image uploaded successfully!</b>\n\n<b>URL:</b> {url}",
            disable_web_page_preview=True
        )
    except Exception as e:
        await msg.edit_text(f"Failed to upload image. Error: {e}")

