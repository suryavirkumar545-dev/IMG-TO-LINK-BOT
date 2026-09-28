import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_ID = int(os.getenv("API_ID", "0"))
    API_HASH = os.getenv("API_HASH", "0")
    BOT_TOKEN = os.getenv("BOT_TOKEN", "0")
    
    # Database
    MONGO_URL = os.getenv("MONGO_URL", "0")
    
    # Admin
    ADMIN_STR = os.getenv("ADMINS", "0")
    ADMINS = [int(x) for x in ADMIN_STR.split()] if ADMIN_STR else []
    
    # Channel
    FORCE_SUB_CHANNEL = os.getenv("FORCE_SUB_CHANNEL", "-1002425134828") # username or ID
    
    # UI
    START_PIC = os.getenv("START_PIC", "https://ibb.co/XZZhqDs0") # Default image
    
    # Log Channel
    LOG_CHANNEL = os.getenv("LOG_CHANNEL", "0") # Channel ID (e.g. -100xxxx)

