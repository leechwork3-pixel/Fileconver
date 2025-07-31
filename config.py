# /config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Get variables from environment or use default values
    API_ID = int(os.environ.get("API_ID", 0))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    
    # --- Database ---
    DATABASE_URI = os.environ.get("DATABASE_URI", "")
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "telegram_bot")
    
    # --- Admins ---
    # User IDs of admins. Can be a single ID or a space-separated list.
    SUDO_ADMINS = [int(admin) for admin in os.environ.get("SUDO_ADMINS", "").split()]
    
    # --- Channels ---
    # ID of the channel where logs and new user notifications will be sent
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", 0))

    # --- Telegraph ---
    TELEGRAPH_ACCOUNT_NAME = os.environ.get("TELEGRAPH_ACCOUNT_NAME", "ConverterBot")
