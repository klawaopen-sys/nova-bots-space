"""
tools/zapisukha_db.py
Робота з Google Таблицею бота «Записуха» через gspread.
Конвертовано з логіки оригінального Google Apps Script.
Підтримує локалізовані назви листів та колонок.
"""

import os
import asyncio
import logging
from datetime import datetime, timedelta
from typing import Optional

import gspread
from google.oauth2.service_account import Credentials

from config import (
    GOOGLE_CREDENTIALS_FILE, GOOGLE_SHEETS_ID,
    WORK_HOURS, SERVICES, PRICES, ADDRESS_SALON, ADDRESS_HOME, SHIFT_START_DATE,
    SHEET_NAMES, COLUMN_HEADERS
)

logger = logging.getLogger(__name__)

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

_gc: Optional[gspread.Client] = None
_spreadsheet = None


def _get_client() -> gspread.Client:
    """Ліниве підключення до Google Sheets API."""
    global _gc
    if _gc is None:
        creds = Credentials.from_service_account_file(GOOGLE_CREDENTIALS_FILE, scopes=SCOPES)
        _gc = gspread.authorize(creds)
        logger.info("✅ gspread: підключення встановлено")
    return _gc


def _get_spreadsheet():
    """Повертає об'єкт таблиці Записухи."""
    global _spreadsheet
    if _spreadsheet is None:
        _spreadsheet = _get_client().open_by_key(GOOGLE_SHEETS_ID)
        logger.info(f"✅ gspread: таблиця відкрита ({GOOGLE_SHEETS_ID[:20]}...)")
    return _spreadsheet


def _get_ws(name: str):
    """Повертає конкретний лист таблиці."""
    return _get_spreadsheet().worksheet(name)


# ─── Допоміжні функції ──────────────────────────────────────────────────────

def get_shift_type(date: datetime) -> str:
    """Визначає тип зміни: 'Салон' або 'Дім' за схемою 2/2."""
    delta = (date.replace(hour=0, minute=0, second=0, microsecond=0) -
             SHIFT_START_DATE.replace(hour=0, minute=0, second=0, microsecond=0))
    day_num = delta.days
    cycle_pos = day_num % 4
    if cycle_pos in [0, 1]:
        return "Салон"
    else:
        return "Дім"


def get_shift_address(date: datetime) -> str:
    """Повертає адресу за типом зміни."""
    shift = get_shift_type(date)
    return ADDRESS_SALON if shift == "Салон" else ADDRESS_HOME


def parse_date(date_str: str) -> Optional[datetime]:
    """Парсить рядок дати з таблиці."""
    for fmt in ("%d.%m.%Y", "%Y-%m-%d", "%d/%m/%Y"):
        try:
            return datetime.strptime(date_str.strip(), fmt)
        except ValueError:
            continue
    return None


# ─── Клієнти ────────────────────────────────────────────────────────────────

def find_client_by_id(user_id: int) -> Optional[dict]:
    """Шукає клієнта за Telegram ID у листі Клієнти."""
    try:
        ws = _get_ws(SHEET_NAMES["clients"])
        records = ws.get_all_records()
        for i, row in enumerate(records, start=2):
            if str(row.get(COLUMN_HEADERS["client_id"], "")) == str(user_id):
                # Повертаємо уніфіковані ключі для коду
                return {
                    "row": i,
                    "ID": row.get(COLUMN_HEADERS["client_id"]),
                    "Ім'я": row.get(COLUMN_HEADERS["client_name"]),
                    "Телефон": row.get(COLUMN_HEADERS["client_phone"]),
                    "Username": row.get(COLUMN_HEADERS["client_username"]),
                    "Нотатки": row.get(COLUMN_HEADERS["client_notes"]),
                    "Дата": row.get(COLUMN_HEADERS["client_date"]),
                    "Статус": row.get(COLUMN_HEADERS["client_status"]),
                    "Крок": row.get(COLUMN_HEADERS["client_step"]),
                    "Фото": row.get(COLUMN_HEADERS["client_photo"]),
                    "MsgID": row.get(COLUMN_HEADERS["client_msgid"])
                }
        return None
    except Exception as e:
        logger.error(f"find_client_by_id error: {e}")
        return None


def upsert_client(user_id: int, name: str, phone: str = "", username: str = "",
                  step: str = "", status: str = "") -> int:
    """Оновлює або створює клієнта. Повертає номер рядка."""
    try:
        ws = _get_ws(SHEET_NAMES["clients"])
        records = ws.get_all_records()
        for i, row in enumerate(records, start=2):
            if str(row.get(COLUMN_HEADERS["client_id"], "")) == str(user_id):
                # Оновлюємо існуючого
                ws.update(f"A{i}:J{i}", [[
                    str(user_id), name, phone or row.get(COLUMN_HEADERS["client_phone"], ""),
                    username or row.get(COLUMN_HEADERS["client_username"], ""),
                    row.get(COLUMN_HEADERS["client_notes"], ""),
                    datetime.now().strftime("%d.%m.%Y"),
                    status or row.get(COLUMN_HEADERS["client_status"], ""),
                    step or row.get(COLUMN_HEADERS["client_step"], ""),
                    row.get(COLUMN_HEADERS["client_photo"], ""),
                    row.get(COLUMN_HEADERS["client_msgid"], "")
                ]])
                return i
        # Новий клієнт
        new_row = [str(user_id), name, phone, username, "",
                   datetime.now().strftime("%d.%m.%Y"), status, step, "", ""]
        ws.append_row(new_row, value_input_option="USER_ENTERED")
        return len(records) + 2
    except Exception as e:
        logger.error(f"upsert_client error: {e}")
        return -1


def update_client_step(user_id: int, step: str, extra: dict = None):
    """Оновлює крок FSM клієнта в таблиці."""
    try:
        client = find_client_by_id(user_id)
        if not client:
            upsert_client(user_id, f"user_{user_id}", step=step)
            return
        ws = _get_ws(SHEET_NAMES["clients"])
        row_num = client["row"]
        ws.update_cell(row_num, 8, step)  # Колонка H = Крок (8-ма колонка)
        if extra:
            if "name" in extra:
                ws.update_cell(row_num, 2, extra["name"]) # B = Ім'я
            if "phone" in extra:
                ws.update_cell(row_num, 3, extra["phone"]) # C = Телефон
            if "status" in extra:
                ws.update_cell(row_num, 7, extra["status"]) # G = Статус
    except Exception as e:
        logger.error(f"update_client_step error: {e}")


# ─── Записи (бронювання) ─────────────────────────────────────────────────────

def get_available_slots(date: datetime) -> list[str]:
    """Повертає список вільних годин для дати."""
    try:
        date_str = date.strftime("%d.%m.%Y")

        # Перевіряємо чи не вихідний
        ws_off = _get_ws(SHEET_NAMES["holidays"])
        off_days = [r[0] for r in ws_off.get_all_values() if r]
        if date_str in off_days:
            return []

        # Отримуємо заблоковані часи
        ws_block = _get_ws(SHEET_NAMES["blocked_time"])
        blocked = []
        for row in ws_block.get_all_values():
            if len(row) >= 2 and row[0] == date_str:
                blocked.append(row[1])

        # Отримуємо зайняті записи
        ws_rec = _get_ws(SHEET_NAMES["appointments"])
        booked = []
        for row in ws_rec.get_all_values()[1:]:  # Пропускаємо заголовок
            if len(row) >= 3 and row[1] == date_str:
                status = row[5] if len(row) > 5 else ""
                if status not in ("скасовано", "відмінено", "cancelled"):
                    booked.append(row[2])

        taken = set(blocked + booked)
        return [h for h in WORK_HOURS if h not in taken]
    except Exception as e:
        logger.error(f"get_available_slots error: {e}")
        return WORK_HOURS.copy()


def create_appointment(client_id: int, date: datetime, time_slot: str,
                       service_code: str, wishes: str = "") -> Optional[str]:
    """Створює новий запис. Повертає ID запису або None."""
    try:
        ws = _get_ws(SHEET_NAMES["appointments"])
        records = ws.get_all_values()
        rec_id = f"R{len(records) + 1:04d}"
        date_str = date.strftime("%d.%m.%Y")
        service_name = SERVICES.get(service_code, service_code)
        price = PRICES.get(service_code, 0)

        ws.append_row([
            rec_id, date_str, time_slot, str(client_id),
            service_name, "підтверджено", wishes, str(price)
        ], value_input_option="USER_ENTERED")
        return rec_id
    except Exception as e:
        logger.error(f"create_appointment error: {e}")
        return None


def cancel_appointment(rec_id: str) -> bool:
    """Скасовує запис за ID."""
    try:
        ws = _get_ws(SHEET_NAMES["appointments"])
        records = ws.get_all_values()
        for i, row in enumerate(records, start=1):
            if row and row[0] == rec_id:
                ws.update_cell(i, 6, "скасовано") # Колонка F = Статус (6-та колонка)
                return True
        return False
    except Exception as e:
        logger.error(f"cancel_appointment error: {e}")
        return False


def get_client_appointments(client_id: int, upcoming_only: bool = True) -> list[dict]:
    """Повертає список записів клієнта."""
    try:
        ws = _get_ws(SHEET_NAMES["appointments"])
        records = ws.get_all_values()
        today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
        result = []
        
        # Визначаємо індекси стовпчиків за назвами
        headers = records[0]
        idx_id = headers.index(COLUMN_HEADERS["appointment_id"])
        idx_date = headers.index(COLUMN_HEADERS["appointment_date"])
        idx_time = headers.index(COLUMN_HEADERS["appointment_time"])
        idx_client = headers.index(COLUMN_HEADERS["appointment_client_id"])
        idx_service = headers.index(COLUMN_HEADERS["appointment_service"])
        idx_status = headers.index(COLUMN_HEADERS["appointment_status"])
        idx_wishes = headers.index(COLUMN_HEADERS["appointment_wishes"])
        idx_price = headers.index(COLUMN_HEADERS["appointment_price"])
        
        for row in records[1:]:
            if len(row) > max(idx_client, idx_status) and str(row[idx_client]) == str(client_id):
                status = row[idx_status]
                if status in ("скасовано", "відмінено", "cancelled"):
                    continue
                date = parse_date(row[idx_date])
                if upcoming_only and date and date < today:
                    continue
                result.append({
                    "id": row[idx_id],
                    "date": row[idx_date],
                    "time": row[idx_time],
                    "service": row[idx_service],
                    "status": status,
                    "wishes": row[idx_wishes] if len(row) > idx_wishes else "",
                    "price": row[idx_price] if len(row) > idx_price else ""
                })
        return result
    except Exception as e:
        logger.error(f"get_client_appointments error: {e}")
        return []


def get_price_list() -> list[dict]:
    """Повертає прайс-лист послуг."""
    try:
        ws = _get_ws(SHEET_NAMES["price"])
        records = ws.get_all_values()
        return [{"name": r[0], "price": r[1]} for r in records if len(r) >= 2]
    except Exception as e:
        logger.error(f"get_price_list error: {e}")
        return [{"name": name, "price": f"{price} грн"} for name, price in zip(SERVICES.values(), PRICES.values())]


# ─── Обгортки для asyncio ────────────────────────────────────────────────────

async def async_find_client(user_id: int) -> Optional[dict]:
    return await asyncio.get_event_loop().run_in_executor(None, find_client_by_id, user_id)


async def async_upsert_client(user_id: int, name: str, phone: str = "",
                               username: str = "", step: str = "", status: str = "") -> int:
    return await asyncio.get_event_loop().run_in_executor(
        None, lambda: upsert_client(user_id, name, phone, username, step, status)
    )


async def async_update_step(user_id: int, step: str, extra: dict = None):
    return await asyncio.get_event_loop().run_in_executor(
        None, lambda: update_client_step(user_id, step, extra)
    )


async def async_get_slots(date: datetime) -> list[str]:
    return await asyncio.get_event_loop().run_in_executor(None, get_available_slots, date)


async def async_create_appointment(client_id: int, date: datetime, time_slot: str,
                                    service_code: str, wishes: str = "") -> Optional[str]:
    return await asyncio.get_event_loop().run_in_executor(
        None, lambda: create_appointment(client_id, date, time_slot, service_code, wishes)
    )


async def async_cancel_appointment(rec_id: str) -> bool:
    return await asyncio.get_event_loop().run_in_executor(None, cancel_appointment, rec_id)


async def async_get_client_appointments(client_id: int) -> list[dict]:
    return await asyncio.get_event_loop().run_in_executor(
        None, lambda: get_client_appointments(client_id, upcoming_only=True)
    )


async def async_get_price_list() -> list[dict]:
    return await asyncio.get_event_loop().run_in_executor(None, get_price_list)
