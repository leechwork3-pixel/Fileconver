# /bot/utils/decorators.py
from functools import wraps
from pyrogram.types import Message
from config import Config

def is_sudo(func):
    @wraps(func)
    async def decorator(client, message: Message):
        if message.from_user.id in Config.SUDO_ADMINS:
            await func(client, message)
        else:
            await message.reply_text("You are not authorized to use this command.")
    return decorator
