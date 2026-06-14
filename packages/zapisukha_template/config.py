import os
from datetime import datetime
from dotenv import load_dotenv

load_dotenv()

# Proxy settings
USE_PROXY = os.getenv("USE_PROXY", "False") == "True"

# Google Sheets localization maps based on DEFAULT_LANG
SHEET_NAMES_MAP = {
    "uk": {
        "clients": "Клієнти",
        "appointments": "Записи",
        "holidays": "Вихідні",
        "blocked_time": "БлокЧас",
        "price": "Прайс"
    },
    "ru": {
        "clients": "Клиенты",
        "appointments": "Записи",
        "holidays": "Выходные",
        "blocked_time": "БлокВремя",
        "price": "Прайс"
    },
    "en": {
        "clients": "Clients",
        "appointments": "Appointments",
        "holidays": "Holidays",
        "blocked_time": "BlockedTime",
        "price": "Prices"
    }
}

COLUMN_HEADERS_MAP = {
    "uk": {
        "client_id": "ID",
        "client_name": "Ім'я",
        "client_phone": "Телефон",
        "client_username": "Username",
        "client_notes": "Нотатки",
        "client_date": "Дата",
        "client_status": "Статус",
        "client_step": "Крок",
        "client_photo": "Фото",
        "client_msgid": "MsgID",
        
        "appointment_id": "ID",
        "appointment_date": "Дата",
        "appointment_time": "Час",
        "appointment_client_id": "КлієнтID",
        "appointment_service": "Послуга",
        "appointment_status": "Статус",
        "appointment_wishes": "Побажання",
        "appointment_price": "Ціна"
    },
    "ru": {
        "client_id": "ID",
        "client_name": "Имя",
        "client_phone": "Телефон",
        "client_username": "Username",
        "client_notes": "Заметки",
        "client_date": "Дата",
        "client_status": "Статус",
        "client_step": "Шаг",
        "client_photo": "Фото",
        "client_msgid": "MsgID",
        
        "appointment_id": "ID",
        "appointment_date": "Дата",
        "appointment_time": "Время",
        "appointment_client_id": "КлиентID",
        "appointment_service": "Услуга",
        "appointment_status": "Статус",
        "appointment_wishes": "Пожелания",
        "appointment_price": "Цена"
    },
    "en": {
        "client_id": "ID",
        "client_name": "Name",
        "client_phone": "Phone",
        "client_username": "Username",
        "client_notes": "Notes",
        "client_date": "Date",
        "client_status": "Status",
        "client_step": "Step",
        "client_photo": "Photo",
        "client_msgid": "MsgID",
        
        "appointment_id": "ID",
        "appointment_date": "Date",
        "appointment_time": "Time",
        "appointment_client_id": "ClientID",
        "appointment_service": "Service",
        "appointment_status": "Status",
        "appointment_wishes": "Wishes",
        "appointment_price": "Price"
    }
}

BOT_TOKEN = os.getenv("BOT_TOKEN", "YOUR_TELEGRAM_BOT_TOKEN")
GOOGLE_CREDENTIALS_FILE = os.getenv("GOOGLE_CREDENTIALS_FILE", "credentials.json")
GOOGLE_SHEETS_ID = os.getenv("GOOGLE_SHEETS_ID", "YOUR_GOOGLE_SHEETS_ID")

# Administrator ID(s)
ADMIN_IDS_STR = os.getenv("ADMIN_IDS", "")
ADMIN_IDS = [int(x.strip()) for x in ADMIN_IDS_STR.split(",") if x.strip().isdigit()]

# Default i18n language
DEFAULT_LANG = os.getenv("DEFAULT_LANG", "uk")

# Addresses
ADDRESS_SALON = os.getenv("ADDRESS_SALON", "📍 вул. Шевченка 128 (Салон)")
ADDRESS_HOME = os.getenv("ADDRESS_HOME", "🏠 вул. Сонячна 15 (Дім)")

# Work Schedule Shift Start (2/2 cycle: Salon/Home)
SHIFT_START_STR = os.getenv("SHIFT_START_DATE", "2026-04-21")
try:
    SHIFT_START_DATE = datetime.strptime(SHIFT_START_STR, "%Y-%m-%d")
except Exception:
    SHIFT_START_DATE = datetime(2026, 4, 21)

# Working hours
WORK_HOURS_STR = os.getenv("WORK_HOURS", "10:00,12:00,14:00,16:00")
WORK_HOURS = [x.strip() for x in WORK_HOURS_STR.split(",")]

# Services & Default Prices
# These can be customized, but we provide standard defaults
SERVICES = {
    "m": "💅 Манікюр",
    "p": "🦶 Педикюр",
    "d": "🧴 Депіляція"
}
PRICES = {
    "m": 580,
    "p": 550,
    "d": 200
}

SHEET_NAMES = SHEET_NAMES_MAP.get(DEFAULT_LANG, SHEET_NAMES_MAP["uk"])
COLUMN_HEADERS = COLUMN_HEADERS_MAP.get(DEFAULT_LANG, COLUMN_HEADERS_MAP["uk"])

