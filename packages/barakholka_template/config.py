import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "YOUR_GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "whisper-large-v3-turbo")

# City configuration
CITY_NAME = os.getenv("CITY_NAME", "Ніжин")
DB_NAME = os.getenv("DB_NAME", f"{CITY_NAME.lower()}_ads.db")

# Default i18n language
DEFAULT_LANG = os.getenv("DEFAULT_LANG", "uk")

# Administrator ID
try:
    ADMIN_ID = int(os.getenv("ADMIN_ID", "0"))
except (TypeError, ValueError):
    ADMIN_ID = 0

# Proxy settings
USE_PROXY = os.getenv("USE_PROXY", "False") == "True"
