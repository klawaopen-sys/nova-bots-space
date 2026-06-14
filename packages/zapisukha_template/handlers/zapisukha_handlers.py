"""
handlers/zapisukha_handlers.py
Обробники бота «Записуха» для aiogram 3.x.
Конвертовано з Google Apps Script та повністю локалізовано (i18n).

FSM Flow (клієнт):
  START → (нова людина) → ввід імені → ввід телефону → MENU
  MENU: [Записатись, Мої записи, Прайс]
  BOOKING: вибір дати → вибір часу → вибір послуги → підтвердження → ЗАПИС

Адмін-команди:
  /admin — панель адміна (список записів на сьогодні, завтра, відмінити)
"""

import os
import logging
from datetime import datetime, timedelta

from aiogram import Router, F, Bot, types as tg_types
from aiogram.filters import CommandStart, Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton, ReplyKeyboardRemove

from config import ADMIN_IDS, SERVICES, PRICES, ADDRESS_SALON, ADDRESS_HOME
from tools.i18n import t
from tools.zapisukha_db import (
    get_shift_type, get_shift_address, WORK_HOURS,
    async_find_client, async_upsert_client, async_update_step,
    async_get_slots, async_create_appointment, async_cancel_appointment,
    async_get_client_appointments, async_get_price_list
)

logger = logging.getLogger(__name__)

router = Router()


# ─── FSM ─────────────────────────────────────────────────────────────────────
class RegState(StatesGroup):
    wait_name = State()
    wait_phone = State()


class BookingState(StatesGroup):
    select_date = State()
    select_time = State()
    select_service = State()
    enter_wishes = State()
    confirm = State()


# ─── Клавіатури ──────────────────────────────────────────────────────────────
def _main_menu_kb(is_admin: bool = False, lang: str = None):
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=t("btn_book", lang)))
    builder.row(KeyboardButton(text=t("btn_my_records", lang)), KeyboardButton(text=t("btn_price", lang)))
    if is_admin:
        builder.row(KeyboardButton(text=t("btn_admin", lang)))
    return builder.as_markup(resize_keyboard=True)


def _dates_kb(available_dates: list[datetime], lang: str = None) -> tg_types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for d in available_dates:
        shift = get_shift_type(d)
        emoji = "🏛" if shift == "Салон" else "🏠"
        
        days_of_week = {
            "uk": ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Нд"],
            "ru": ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"],
            "en": ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
        }
        norm_lang = (lang or "uk").split('-')[0].lower()
        if norm_lang not in days_of_week:
            norm_lang = "en"
        day_name = days_of_week[norm_lang][d.weekday()]
        
        btn_text = f"{emoji} {d.strftime('%d.%m')} ({day_name})"
        builder.row(InlineKeyboardButton(text=btn_text, callback_data=f"z_date_{d.strftime('%d.%m.%Y')}"))
    builder.row(InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="z_cancel"))
    return builder.as_markup()


def _times_kb(slots: list[str], date_str: str, lang: str = None) -> tg_types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    row = []
    for slot in slots:
        row.append(InlineKeyboardButton(text=f"🕐 {slot}", callback_data=f"z_time_{slot}"))
    for i in range(0, len(row), 2):
        builder.row(*row[i:i + 2])
    builder.row(InlineKeyboardButton(text=t("btn_back", lang), callback_data="z_back_dates"))
    builder.row(InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="z_cancel"))
    return builder.as_markup()


def _services_kb(lang: str = None) -> tg_types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for code, name in SERVICES.items():
        price = PRICES.get(code, "?")
        currency = t("currency", lang)
        builder.row(InlineKeyboardButton(text=f"{t(f'srv_{code}', lang)} — {price} {currency}", callback_data=f"z_srv_{code}"))
    builder.row(InlineKeyboardButton(text=t("btn_back", lang), callback_data="z_back_times"))
    builder.row(InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="z_cancel"))
    return builder.as_markup()


def _confirm_kb(lang: str = None) -> tg_types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.row(
        InlineKeyboardButton(text=t("btn_confirm", lang), callback_data="z_confirm"),
        InlineKeyboardButton(text=t("btn_cancel", lang), callback_data="z_cancel")
    )
    return builder.as_markup()


def _my_records_kb(records: list[dict], lang: str = None) -> tg_types.InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for rec in records:
        btn_text = t("cancel_record_btn", lang, date=rec['date'], time=rec['time'], service=rec['service'])
        builder.row(InlineKeyboardButton(text=btn_text, callback_data=f"z_cancelrec_{rec['id']}"))
    builder.row(InlineKeyboardButton(text=t("btn_menu", lang), callback_data="z_main_menu"))
    return builder.as_markup()


def _get_next_14_days() -> list[datetime]:
    """Генерує список наступних 14 робочих дат (де є зміни)."""
    result = []
    today = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    for i in range(1, 21):  # +20 днів вперед, беремо перші 14 робочих
        d = today + timedelta(days=i)
        if d.weekday() < 7:
            result.append(d)
        if len(result) >= 14:
            break
    return result


# ─── /start ──────────────────────────────────────────────────────────────────
@router.message(CommandStart(), StateFilter("*"))
async def z_start(m: tg_types.Message, state: FSMContext):
    await state.clear()
    user_id = m.from_user.id
    username = m.from_user.username or f"id{user_id}"
    is_admin = user_id in ADMIN_IDS
    lang = m.from_user.language_code

    client = await async_find_client(user_id)

    if not client or not client.get("Ім'я"):
        # Нова людина — реєстрація
        await m.answer(
            t("welcome_new", lang),
            parse_mode="HTML"
        )
        await state.set_state(RegState.wait_name)
        return

    name = client.get("Ім'я", username)
    addr = get_shift_address(datetime.now())

    await m.answer(
        t("welcome_returning", lang, name=name, addr=addr),
        reply_markup=_main_menu_kb(is_admin, lang), parse_mode="HTML"
    )


@router.message(RegState.wait_name)
async def z_reg_name(m: tg_types.Message, state: FSMContext):
    lang = m.from_user.language_code
    if not m.text or len(m.text.strip()) < 2:
        await m.answer(t("enter_name_error", lang))
        return
    await state.update_data(reg_name=m.text.strip())
    await state.set_state(RegState.wait_phone)
    
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text=t("share_contact_btn", lang), request_contact=True))
    await m.answer(
        t("enter_phone", lang),
        reply_markup=builder.as_markup(resize_keyboard=True)
    )


@router.message(RegState.wait_phone, (F.contact | F.text))
async def z_reg_phone(m: tg_types.Message, state: FSMContext):
    lang = m.from_user.language_code
    if m.contact:
        phone = m.contact.phone_number
    else:
        phone = m.text.strip()
    if not phone.startswith("+"):
        phone = f"+{phone}"

    d = await state.get_data()
    name = d.get("reg_name", m.from_user.first_name or "Client")
    user_id = m.from_user.id
    username = m.from_user.username or f"id{user_id}"
    is_admin = user_id in ADMIN_IDS

    await async_upsert_client(user_id, name, phone, username, step="MAIN", status="new")
    await state.clear()

    addr = get_shift_address(datetime.now())
    await m.answer(
        t("registered_success", lang, name=name, addr=addr),
        reply_markup=_main_menu_kb(is_admin, lang), parse_mode="HTML"
    )


# ─── Головне меню (текстові кнопки) ─────────────────────────────────────────
@router.message(F.text.in_({"📅 Записатись", "📅 Записаться", "📅 Book Appointment"}), StateFilter("*"))
async def z_start_booking(m: tg_types.Message, state: FSMContext):
    await state.clear()
    await state.set_state(BookingState.select_date)
    lang = m.from_user.language_code

    dates = _get_next_14_days()
    if not dates:
        await m.answer(t("no_available_dates", lang))
        return

    today_addr = get_shift_address(datetime.now())
    await m.answer(
        t("select_date", lang, salon_addr=ADDRESS_SALON, home_addr=ADDRESS_HOME, today_addr=today_addr),
        reply_markup=_dates_kb(dates, lang), parse_mode="HTML"
    )


@router.callback_query(BookingState.select_date, F.data.startswith("z_date_"))
async def z_select_date(c: tg_types.CallbackQuery, state: FSMContext):
    lang = c.from_user.language_code
    date_str = c.data.replace("z_date_", "")
    await state.update_data(booking_date=date_str)

    date = datetime.strptime(date_str, "%d.%m.%Y")
    slots = await async_get_slots(date)

    if not slots:
        await c.answer(t("no_available_slots", lang), show_alert=True)
        return

    addr = get_shift_address(date)
    await c.message.edit_text(
        t("select_time", lang, date_str=date_str, addr=addr),
        reply_markup=_times_kb(slots, date_str, lang), parse_mode="HTML"
    )
    await state.set_state(BookingState.select_time)
    await c.answer()


@router.callback_query(BookingState.select_time, F.data.startswith("z_time_"))
async def z_select_time(c: tg_types.CallbackQuery, state: FSMContext):
    lang = c.from_user.language_code
    time_slot = c.data.replace("z_time_", "")
    await state.update_data(booking_time=time_slot)
    
    await c.message.edit_text(
        t("select_service", lang, time_slot=time_slot),
        reply_markup=_services_kb(lang), parse_mode="HTML"
    )
    await state.set_state(BookingState.select_service)
    await c.answer()


@router.callback_query(BookingState.select_service, F.data.startswith("z_srv_"))
async def z_select_service(c: tg_types.CallbackQuery, state: FSMContext):
    lang = c.from_user.language_code
    srv_code = c.data.replace("z_srv_", "")
    srv_name = t(f"srv_{srv_code}", lang)
    srv_price = PRICES.get(srv_code, 0)
    
    await state.update_data(booking_service=srv_code, booking_service_name=srv_name, booking_price=srv_price)
    await state.set_state(BookingState.enter_wishes)
    
    await c.message.edit_text(
        t("enter_wishes", lang, srv_name=srv_name, price=srv_price, currency=t("currency", lang)),
        parse_mode="HTML"
    )
    await c.answer()


@router.message(BookingState.enter_wishes, F.text)
async def z_enter_wishes(m: tg_types.Message, state: FSMContext):
    lang = m.from_user.language_code
    wishes = m.text.strip() if m.text.strip() != "-" else ""
    await state.update_data(booking_wishes=wishes)
    d = await state.get_data()

    date = datetime.strptime(d["booking_date"], "%d.%m.%Y")
    addr = get_shift_address(date)

    # Знижка за давній візит (> 21 день)
    client = await async_find_client(m.from_user.id)
    discount_text = ""
    if client:
        last_visit_str = client.get("Дата", "")
        if last_visit_str:
            try:
                last_visit = datetime.strptime(last_visit_str, "%d.%m.%Y")
                days_since = (datetime.now() - last_visit).days
                if days_since > 21:
                    discount = int(d["booking_price"] * 0.1)
                    discount_text = t("discount_text", lang, discount=discount, currency=t("currency", lang))
            except Exception:
                pass

    confirm_text = (
        t("confirm_title", lang) +
        t("confirm_date", lang, date=d['booking_date']) +
        t("confirm_time", lang, time=d['booking_time']) +
        t("confirm_service", lang, service=d['booking_service_name']) +
        t("confirm_price", lang, price=d['booking_price'], currency=t("currency", lang), discount_text=discount_text) +
        t("confirm_place", lang, addr=addr)
    )
    if wishes:
        confirm_text += t("confirm_wishes", lang, wishes=wishes)

    await state.set_state(BookingState.confirm)
    await m.answer(confirm_text, reply_markup=_confirm_kb(lang), parse_mode="HTML")


@router.callback_query(BookingState.confirm, F.data == "z_confirm")
async def z_confirm_booking(c: tg_types.CallbackQuery, state: FSMContext):
    lang = c.from_user.language_code
    d = await state.get_data()
    user_id = c.from_user.id

    date = datetime.strptime(d["booking_date"], "%d.%m.%Y")
    rec_id = await async_create_appointment(
        user_id, date, d["booking_time"], d["booking_service"], d.get("booking_wishes", "")
    )

    if not rec_id:
        await c.answer(t("booking_error", lang), show_alert=True)
        await state.clear()
        return

    addr = get_shift_address(date)
    await state.clear()

    is_admin = user_id in ADMIN_IDS
    await c.message.edit_text(
        t("booking_success", lang, date=d['booking_date'], time=d['booking_time'], service=d['booking_service_name'], price=d['booking_price'], currency=t("currency", lang), addr=addr, rec_id=rec_id),
        parse_mode="HTML"
    )
    await c.message.answer(t("btn_menu", lang) + ":", reply_markup=_main_menu_kb(is_admin, lang))
    await c.answer()

    # Сповіщення адмінів (використовує шаблон нової заявки)
    client = await async_find_client(user_id)
    client_name = client.get("Ім'я", f"id{user_id}") if client else f"id{user_id}"
    client_phone = client.get("Телефон", "—") if client else "—"
    
    admin_notify_text = t("new_booking_notify_admin", "uk", client_name=client_name, client_phone=client_phone, date=d['booking_date'], time=d['booking_time'], service=d['booking_service_name'], addr=addr, rec_id=rec_id)
    
    for admin_id in ADMIN_IDS:
        try:
            await c.bot.send_message(
                chat_id=admin_id,
                text=admin_notify_text,
                parse_mode="HTML"
            )
        except Exception as e:
            logger.warning(f"Failed to notify admin {admin_id}: {e}")


# ─── Мої записи ──────────────────────────────────────────────────────────────
@router.message(F.text.in_({"📋 Мої записи", "📋 Мои записи", "📋 My Bookings"}), StateFilter("*"))
async def z_my_records(m: tg_types.Message, state: FSMContext):
    await state.clear()
    lang = m.from_user.language_code
    records = await async_get_client_appointments(m.from_user.id)
    if not records:
        await m.answer(
            t("my_records_empty", lang),
            parse_mode="HTML"
        )
        return
    text = t("my_records_list", lang)
    for rec in records:
        text += f"• {rec['date']} {rec['time']} — {rec['service']} ({rec['price']} {t('currency', lang)})\n"
    await m.answer(text, reply_markup=_my_records_kb(records, lang), parse_mode="HTML")


@router.callback_query(F.data.startswith("z_cancelrec_"))
async def z_cancel_record(c: tg_types.CallbackQuery):
    lang = c.from_user.language_code
    rec_id = c.data.replace("z_cancelrec_", "")
    ok = await async_cancel_appointment(rec_id)
    if ok:
        await c.answer(t("record_cancelled", lang).replace("<code>", "").replace("</code>", ""), show_alert=True)
        await c.message.edit_text(t("record_cancelled", lang), parse_mode="HTML")
        
        # Сповіщення адмінів
        admin_notify_cancel = t("cancel_record_notify_admin", "uk", rec_id=rec_id, user_id=c.from_user.id)
        for admin_id in ADMIN_IDS:
            try:
                await c.bot.send_message(
                    admin_id,
                    admin_notify_cancel,
                    parse_mode="HTML"
                )
            except Exception:
                pass
    else:
        await c.answer(t("record_not_found", lang), show_alert=True)


# ─── Прайс ───────────────────────────────────────────────────────────────────
@router.message(F.text.in_({"💰 Прайс", "💰 Стоимость", "💰 Price List"}), StateFilter("*"))
async def z_price_list(m: tg_types.Message, state: FSMContext):
    await state.clear()
    lang = m.from_user.language_code
    prices = await async_get_price_list()
    text = t("price_title", lang)
    for item in prices:
        text += f"• {item['name']} — <b>{item['price']}</b>\n"
    text += f"\n📍 {ADDRESS_SALON}\n🏠 {ADDRESS_HOME}"
    await m.answer(text, parse_mode="HTML")


# ─── Зворотні кнопки навігації ────────────────────────────────────────────────
@router.callback_query(F.data == "z_back_dates")
async def z_back_to_dates(c: tg_types.CallbackQuery, state: FSMContext):
    lang = c.from_user.language_code
    dates = _get_next_14_days()
    await c.message.edit_text(
        "📅 <b>" + t("select_date", lang).split("</b>")[0].replace("📅 <b>", "") + "</b>",
        reply_markup=_dates_kb(dates, lang), parse_mode="HTML"
    )
    await state.set_state(BookingState.select_date)
    await c.answer()


@router.callback_query(F.data == "z_back_times")
async def z_back_to_times(c: tg_types.CallbackQuery, state: FSMContext):
    lang = c.from_user.language_code
    d = await state.get_data()
    date_str = d.get("booking_date", "")
    if not date_str:
        await c.answer("❌ Error. Restart booking.", show_alert=True)
        return
    date = datetime.strptime(date_str, "%d.%m.%Y")
    slots = await async_get_slots(date)
    addr = get_shift_address(date)
    await c.message.edit_text(
        t("select_time", lang, date_str=date_str, addr=addr),
        reply_markup=_times_kb(slots, date_str, lang), parse_mode="HTML"
    )
    await state.set_state(BookingState.select_time)
    await c.answer()


@router.callback_query(F.data == "z_cancel")
async def z_cancel_booking(c: tg_types.CallbackQuery, state: FSMContext):
    lang = c.from_user.language_code
    await state.clear()
    await c.message.edit_text("❌ " + t("btn_cancel", lang))
    await c.answer()


@router.callback_query(F.data == "z_main_menu")
async def z_back_main_menu(c: tg_types.CallbackQuery, state: FSMContext):
    lang = c.from_user.language_code
    await state.clear()
    is_admin = c.from_user.id in ADMIN_IDS
    await c.message.edit_text("📋 Menu")
    await c.message.answer(t("btn_menu", lang) + ":", reply_markup=_main_menu_kb(is_admin, lang))
    await c.answer()


# ─── Адмін-панель ────────────────────────────────────────────────────────────
@router.message(F.text.in_({"👑 Адмін-панель", "👑 Админ-панель", "👑 Admin Panel"}), StateFilter("*"))
@router.message(Command("admin"))
async def z_admin_panel(m: tg_types.Message, state: FSMContext):
    if m.from_user.id not in ADMIN_IDS:
        await m.answer("🚫 Access denied.")
        return
    await state.clear()

    today = datetime.now().strftime("%d.%m.%Y")
    tomorrow = (datetime.now() + timedelta(days=1)).strftime("%d.%m.%Y")

    today_addr = get_shift_address(datetime.now())
    tomorrow_addr = get_shift_address(datetime.now() + timedelta(days=1))

    admin_text = (
        f"👑 <b>Адмін-панель «Записуха»</b>\n\n"
        f"📅 <b>Сьогодні</b> ({today}) — {today_addr}\n"
        f"📅 <b>Завтра</b> ({tomorrow}) — {tomorrow_addr}\n\n"
        f"Оберіть дію:"
    )

    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text=f"📋 Записи сьогодні", callback_data=f"z_adm_recs_{today}"))
    builder.row(InlineKeyboardButton(text=f"📋 Записи завтра", callback_data=f"z_adm_recs_{tomorrow}"))

    await m.answer(admin_text, reply_markup=builder.as_markup(), parse_mode="HTML")


@router.callback_query(F.data.startswith("z_adm_recs_"))
async def z_admin_show_recs(c: tg_types.CallbackQuery):
    if c.from_user.id not in ADMIN_IDS:
        await c.answer("🚫 Access denied.", show_alert=True)
        return
    date_str = c.data.replace("z_adm_recs_", "")

    try:
        from tools.zapisukha_db import _get_ws
        import asyncio
        ws = await asyncio.get_event_loop().run_in_executor(None, _get_ws, "Записи")
        all_recs = await asyncio.get_event_loop().run_in_executor(None, ws.get_all_values)
        today_recs = [r for r in all_recs[1:] if len(r) >= 3 and r[1] == date_str and r[5] not in ("скасовано", "відмінено")]
    except Exception as e:
        await c.answer(f"❌ Error reading table: {e}", show_alert=True)
        return

    if not today_recs:
        await c.message.edit_text(f"📋 На {date_str} записів немає.")
        await c.answer()
        return

    text = f"📋 <b>Записи на {date_str}:</b>\n\n"
    for rec in sorted(today_recs, key=lambda x: x[2]):
        rec_id = rec[0]
        time = rec[2]
        client_id = rec[3]
        service = rec[4]
        status = rec[5]
        wishes = rec[6] if len(rec) > 6 else ""
        price = rec[7] if len(rec) > 7 else ""
        text += f"🕐 <b>{time}</b> — {service} ({price} грн)\n"
        text += f"   Клієнт ID: {client_id}"
        if wishes:
            text += f"\n   💬 {wishes}"
        text += f"\n   Статус: {status}\n\n"

    await c.message.edit_text(text, parse_mode="HTML")
    await c.answer()
