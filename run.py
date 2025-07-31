# /run.py
from bot.bot_instance import app
from web.server import keep_alive # Import the keep_alive function
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":
    logging.info("Starting web server for health checks...")
    keep_alive() # Start the web server in a background thread

    logging.info("Starting Bot...")
    app.run() # Start the Pyrogram bot
    
    logging.info("Bot Stopped.")
    
