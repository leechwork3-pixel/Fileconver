# /config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Get variables from environment or use default values
    API_ID = int(os.environ.get("API_ID", 24171111))
    API_HASH = os.environ.get("API_HASH", "c850cb56b64b6c3b10ade9c28ef7966a")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "7804274444:AAESKpYJQVhftykvv5cKZP2uyCYvxlwQvow")
    
    # --- Database ---
    DATABASE_URI = os.environ.get("DATABASE_URI", "mongodb+srv://Furina:furinafile@furinafile.tjrqfwh.mongodb.net/?retryWrites=true&w=majority&appName=Furinafile")
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "Furinafile")
    
    # --- Admins ---
    # User IDs of admins. Can be a single ID or a space-separated list.
    SUDO_ADMINS = [int(admin) for admin in os.environ.get("SUDO_ADMINS", "1335306418").split()]
    
    # --- Channels ---
    # ID of the channel where logs and new user notifications will be sent
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", -1002585029413))

    # --- Telegraph ---
    TELEGRAPH_ACCOUNT_NAME = os.environ.get("TELEGRAPH_ACCOUNT_NAME", "@Element_Network")
    # Add the new token variable
    TELEGRAPH_TOKEN = os.environ.get("TELEGRAPH_TOKEN", None)
    
