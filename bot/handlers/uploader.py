# /bot/handlers/uploader.py
import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message
from pyrogram.enums import ParseMode
from bot.bot_instance import app
from telegraph import upload_file

@app.on_message(filters.photo & filters.private)
async def telegraph_upload(client: Client, message: Message):
    # Give feedback to the user
    msg = await message.reply_text("`Downloading your image...`")
    
    photo_path = None  # Initialize variable to ensure it exists for the finally block
    try:
        photo_path = await message.download()

        await msg.edit_text("`Uploading to Telegraph...`")
        response = upload_file(photo_path)

        # Add a check for a valid API response
        if not isinstance(response, list) or not response:
            logging.error(f"Telegraph API returned an invalid response: {response}")
            await msg.edit_text("Sorry, there was an unexpected issue with the Telegraph API.")
            return

        url = "https://telegra.ph" + response[0]
        
        await msg.edit_text(
            text=f"<b>Image uploaded successfully!</b>\n\n<b>URL:</b> <a href='{url}'>{url}</a>",
            parse_mode=ParseMode.HTML,
            disable_web_page_preview=True
        )

    except Exception as e:
        # Log the full error for debugging and show a clean message to the user
        logging.error(f"Telegraph upload failed: {e}", exc_info=True)
        await msg.edit_text(
            text=f"<b>Failed to upload image.</b>\n\n<b>Error:</b> <pre>{e}</pre>",
            parse_mode=ParseMode.HTML
        )

    finally:
        # Ensure the downloaded temporary file is always removed
        if photo_path and os.path.exists(photo_path):
            os.remove(photo_path)
            
