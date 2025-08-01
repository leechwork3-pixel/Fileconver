# /bot/handlers/converter.py
import os
import zipfile
from PIL import Image
import fitz  # PyMuPDF
from bs4 import BeautifulSoup
import ebooklib
from ebooklib import epub
from pyrogram import Client, filters
from pyrogram.types import Message
from bot.bot_instance import app

# --- Helper functions (convert_cbz_to_pdf, convert_epub_to_pdf) remain the same ---
def convert_cbz_to_pdf(cbz_path, pdf_path):
    try:
        # ... (code from previous version)
        img_list = []
        with zipfile.ZipFile(cbz_path, 'r') as z:
            for filename in sorted(z.namelist()):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.gif')):
                    with z.open(filename) as f:
                        img = Image.open(f)
                        img = img.convert("RGB")
                        img_list.append(img)
        if not img_list: return None
        img_list[0].save(pdf_path, save_all=True, append_images=img_list[1:])
        return pdf_path
    except Exception as e:
        print(f"Error converting CBZ to PDF: {e}")
        return None

def convert_epub_to_pdf(epub_path, pdf_path):
    try:
        # ... (code from previous version)
        book = epub.read_epub(epub_path)
        pdf = fitz.open()
        for item in book.get_items_of_type(ebooklib.ITEM_DOCUMENT):
            soup = BeautifulSoup(item.get_content(), 'html.parser')
            text = soup.get_text()
            page = pdf.new_page()
            page.insert_text(fitz.Rect(50, 50, 550, 750), text, fontsize=11)
        pdf.save(pdf_path)
        pdf.close()
        return pdf_path
    except Exception as e:
        print(f"Error converting EPUB to PDF: {e}")
        return None


@app.on_message(filters.document & filters.private)
async def file_converter(client: Client, message: Message):
    doc = message.document
    if not doc.file_name:
        await message.reply_text("This file has no name.")
        return

    # --- ADD FILE SIZE CHECK HERE ---
    # Set a 25 MB file size limit
    if doc.file_size > 25 * 1024 * 1024:
        await message.reply_text("❌ **File is too large!**\n\nThis bot is running on a free server. Please send files smaller than 25 MB to avoid memory issues.")
        return
    
    file_ext = doc.file_name.split('.')[-1].lower()
    msg = await message.reply_text(f"Received `{doc.file_name}`. Downloading...")
    
    file_path = await message.download()
    new_file_path = None
    
    try:
        await msg.edit_text("Converting...")
        output_path = f"{os.path.splitext(file_path)[0]}.pdf"

        if file_ext == "cbz":
            new_file_path = convert_cbz_to_pdf(file_path, output_path)
        elif file_ext in ["epub", "mobi", "azw3", "fb2"]:
            new_file_path = convert_epub_to_pdf(file_path, output_path)
        else:
            await msg.edit_text(f"Sorry, conversion from `{file_ext}` is not fully supported yet.")
            os.remove(file_path)
            return

        if new_file_path:
            await msg.edit_text("Conversion successful! Uploading...")
            await message.reply_document(new_file_path)
        else:
            await msg.edit_text("Sorry, something went wrong during conversion.")
    
    except Exception as e:
        await msg.edit_text(f"An error occurred: {e}")
    
    finally:
        if os.path.exists(file_path):
            os.remove(file_path)
        if new_file_path and os.path.exists(new_file_path):
            os.remove(new_file_path)
        await msg.delete()

