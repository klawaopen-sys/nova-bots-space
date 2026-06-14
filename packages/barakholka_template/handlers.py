import aiosqlite, logging, emoji, os, requests
from google import genai
from google.genai import types
from datetime import datetime, timedelta
from aiogram import Router, F, Bot, types as tg_types
from aiogram.filters import CommandStart, StateFilter, CommandObject
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import StatesGroup, State
from aiogram.types import FSInputFile, ReplyKeyboardRemove, InputMediaPhoto
from aiogram.exceptions import TelegramBadRequest

import kb
from config import DB_NAME, GEMINI_API_KEY, ADMIN_ID, GROQ_API_KEY, GROQ_MODEL, CITY_NAME
from tools.i18n import t

router = Router()
client = genai.Client(api_key=GEMINI_API_KEY)

AUTO_CATS_LOGIC = ["🚗 Легкові авто", "🏍️ Мототехніка", "🚚 Вантажівки", "🚜 Сільгосптехніка", "🚌 Автобуси"]

class SellState(StatesGroup):
    section, category, title, param, size = State(), State(), State(), State(), State()
    car_brand, car_year, car_mileage, car_trans, car_fuel = State(), State(), State(), State(), State()
    price, exchange, condition, photo, phone, show_phone, confirm = [State() for _ in range(7)]

class EditState(StatesGroup):
    edit_id = State()
    edit_field = State()
    input_text = State()
    input_photo = State()

class CategoryState(StatesGroup):
    input_name = State()
    editing_old_name = State()
    add_new_name = State()
    current_section = State()

async def del_msg(m: tg_types.Message):
    try: await m.delete()
    except: pass

# --- KABINET ---
async def open_kabinet_view(user_id, message_obj):
    lang = message_obj.from_user.language_code
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT bonus_posts, subscription_until FROM users WHERE user_id=?", (user_id,)) as cur:
            row = await cur.fetchone()
        if not row:
            await db.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, message_obj.chat.username or f"id{user_id}"))
            await db.commit()
            bonus_posts, sub_until_str = 0, None
        else:
            bonus_posts, sub_until_str = row
            
        async with db.execute("SELECT id, title, price FROM ads WHERE user_id=?", (user_id,)) as cur:
            ads = await cur.fetchall()
            
    sub_status = "❌ Немає активної підписки"
    if sub_until_str:
        try:
            sub_until = datetime.fromisoformat(sub_until_str)
            if sub_until > datetime.now():
                sub_status = f"✅ Безліміт активний до {sub_until.strftime('%d.%m.%Y %H:%M')}"
        except ValueError:
            pass
            
    local_now = datetime.now()
    monday = local_now - timedelta(days=local_now.weekday())
    monday_start = monday.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
    
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT COUNT(*) FROM ads WHERE user_id=? AND created_at >= ?", (user_id, monday_start)) as cur:
            res = await cur.fetchone()
            posted_this_week = res[0] if res else 0
            
    limit_text = "Безліміт" if "Безліміт" in sub_status else f"{posted_this_week} / {3 + bonus_posts}"
    
    info_text = (
        f"<b>💼 {t('btn_cabinet', lang)}</b>\n\n"
        f"👑 Статус підписки: {sub_status}\n"
        f"📊 Опубліковано цього тижня: <code>{limit_text}</code>\n"
        f"🎁 Накопичено бонусних лімітів: +<code>{bonus_posts}</code> публікацій\n"
    )
    
    if user_id == ADMIN_ID:
        await message_obj.answer("👑 Привіт, Адмін! Ось пульт керування:", reply_markup=tg_types.InlineKeyboardMarkup(inline_keyboard=[
            [tg_types.InlineKeyboardButton(text="📂 Керувати категоріями", callback_data="admin_manage_cats")],
            [tg_types.InlineKeyboardButton(text="🗑 Видалити будь-яке оголошення", callback_data="admin_delete_ads_start")]
        ]))
        
    await message_obj.answer(info_text, reply_markup=kb.cabinet_menu_kb(), parse_mode="HTML")
    
    if ads:
        await message_obj.answer("🗂 <b>Ваші опубліковані оголошення:</b>", parse_mode="HTML")
        for aid, t_item, p in ads:
            await message_obj.answer(f"🔹 {t_item} — {p}", reply_markup=kb.my_ads_actions(aid))

# --- MAIN MENU ---
@router.message(CommandStart(), StateFilter("*"))
async def start_handler(m: tg_types.Message, state: FSMContext, command: CommandObject):
    await state.clear(); await del_msg(m)
    await register_user_if_not_exists(m.from_user.id, m.from_user.username or f"id{m.from_user.id}", command.args, m.bot)
    await show_main_menu(m)

@router.message(F.text == "🔄 Оновити", StateFilter("*"))
@router.message(F.text == "🔙 Назад до меню", StateFilter("*"))
@router.message(F.text == "🔙 Назад в меню", StateFilter("*"))
@router.message(F.text == "🔙 Back to Menu", StateFilter("*"))
async def back_menu_handler(m: tg_types.Message, state: FSMContext):
    await state.clear(); await del_msg(m)
    await register_user_if_not_exists(m.from_user.id, m.from_user.username or f"id{m.from_user.id}", None, m.bot)
    await show_main_menu(m)

async def show_main_menu(m: tg_types.Message):
    lang = m.from_user.language_code
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT 1 FROM ads WHERE user_id=? LIMIT 1", (m.from_user.id,)) as cur:
            has_ads = await cur.fetchone() is not None
    
    welcome_title = t("welcome_title", lang, city=CITY_NAME)
    welcome_body = t("welcome_body", lang)
    welcome_text = f"<b>{welcome_title}</b>\n\n{welcome_body}"
    
    # Render customized menu markup based on language
    builder = tg_types.ReplyKeyboardBuilder()
    builder.row(tg_types.KeyboardButton(text=t("btn_buy", lang)), tg_types.KeyboardButton(text=t("btn_sell", lang)))
    builder.row(tg_types.KeyboardButton(text=t("btn_cabinet", lang)))
    builder.row(tg_types.KeyboardButton(text=t("btn_refresh", lang)))
    custom_menu = builder.as_markup(resize_keyboard=True)
    
    # Try to load welcome photo, fallback to text if missing
    try:
        await m.answer_photo(photo=FSInputFile(".tmp/welcome.png"), caption=welcome_text, reply_markup=custom_menu, parse_mode="HTML")
    except Exception:
        await m.answer(welcome_text, reply_markup=custom_menu, parse_mode="HTML")

# --- CHOOSE SECTION ---
@router.message(F.text.in_({"🛒 Купити", "🛒 Купить", "🛒 Buy", "📦 Продати", "📦 Продать", "📦 Sell"}), StateFilter("*"))
async def select_section(m: tg_types.Message, state: FSMContext):
    lang = m.from_user.language_code
    await state.clear(); await del_msg(m)
    
    is_sell = any(sell_keyword in m.text for sell_keyword in ["Продати", "Продать", "Sell"])
    
    if is_sell:
        allowed, posted, limit = await check_user_limits(m.from_user.id)
        if not allowed:
            limit_msg = t("limit_reached", lang, posted=posted, limit=limit)
            await m.answer(limit_msg, reply_markup=kb.cabinet_menu_kb(), parse_mode="HTML")
            return
        await state.update_data(mode="sell")
    else:
        await state.update_data(mode="buy")
    await m.answer(t("select_section", lang), reply_markup=kb.sections_kb())

# --- CHOOSE CATEGORY ---
@router.callback_query(F.data.startswith("sec_"))
async def show_categories_in_section(c: tg_types.CallbackQuery, state: FSMContext):
    lang = c.from_user.language_code
    section_code = c.data.replace("sec_", "") 
    d = await state.get_data()
    is_sell = d.get("mode") == "sell"
    
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT name FROM categories WHERE section=?", (section_code,)) as cur:
            cats = [row[0] for row in await cur.fetchall()]
        
        async with db.execute("SELECT category, COUNT(*) FROM ads GROUP BY category") as cur:
            counts_data = await cur.fetchall()
            counts_map = {row[0]: row[1] for row in counts_data}
    
    final_cats_for_kb = []
    for cat in cats:
        count = counts_map.get(cat, 0)
        if is_sell:
             display_text = cat 
        else:
             marker = "🟢" if count > 0 else "⚪️"
             display_text = f"{marker} {cat} ({count})"
        final_cats_for_kb.append((display_text, cat))
    
    if is_sell:
        await state.set_state(SellState.category)
        await c.message.edit_text(t("select_category_sell", lang), reply_markup=kb.categories_kb(final_cats_for_kb))
    else:
        await c.message.edit_text(t("select_category_buy", lang), reply_markup=kb.categories_kb(final_cats_for_kb))
    await c.answer()

@router.callback_query(F.data == "back_to_sections")
async def back_sec(c: tg_types.CallbackQuery, state: FSMContext):
    lang = c.from_user.language_code
    await c.message.edit_text(t("select_section", lang), reply_markup=kb.sections_kb())

# --- SELL FLOW START ---
@router.callback_query(SellState.category, F.data.startswith("cat_"))
async def s_cat(c: tg_types.CallbackQuery, state: FSMContext):
    cat = c.data.split("_")[1]; await state.update_data(category=cat)
    
    if any(ac in cat for ac in AUTO_CATS_LOGIC):
        await state.set_state(SellState.car_brand); await c.message.answer("🏎 Марка авто:", reply_markup=kb.back_kb())
    elif "Автозапчастини" in cat:
         await state.set_state(SellState.title); await c.message.answer("✏️ Введіть назву запчастини:", reply_markup=kb.back_kb())
    else:
        await state.set_state(SellState.title); await c.message.answer("✏️ Введіть назву:", reply_markup=kb.back_kb())
    await c.answer()

# --- VEHICLE LOGIC ---
@router.message(SellState.car_brand)
async def s_car_brand(m: tg_types.Message, state: FSMContext):
    await state.update_data(car_brand=m.text, title=m.text); await state.set_state(SellState.car_year)
    await m.answer("📅 Рік випуску:", reply_markup=kb.back_kb())

@router.message(SellState.car_year)
async def s_car_year(m: tg_types.Message, state: FSMContext):
    await state.update_data(car_year=m.text); await state.set_state(SellState.car_mileage)
    await m.answer("🛣 Пробіг (тис. км):", reply_markup=kb.back_kb())

@router.message(SellState.car_mileage)
async def s_car_mileage(m: tg_types.Message, state: FSMContext):
    await state.update_data(car_mileage=m.text); await state.set_state(SellState.car_trans)
    await m.answer("⚙️ КП:", reply_markup=kb.transmission_kb())

@router.callback_query(SellState.car_trans, F.data.startswith("trans_"))
async def s_car_trans(c: tg_types.CallbackQuery, state: FSMContext):
    await state.update_data(car_trans=c.data.split("_")[1]); await state.set_state(SellState.car_fuel)
    await c.message.answer("⛽️ Паливо:", reply_markup=kb.fuel_kb()); await c.answer()

@router.callback_query(SellState.car_fuel, F.data.startswith("fuel_"))
async def s_car_fuel(c: tg_types.CallbackQuery, state: FSMContext):
    await state.update_data(car_fuel=c.data.split("_")[1]); await state.set_state(SellState.param)
    await c.message.answer("ℹ️ Опис авто:", reply_markup=kb.back_kb()); await c.answer()

# --- GOODS & SERVICES LOGIC ---
@router.message(SellState.title)
async def s_title(m: tg_types.Message, state: FSMContext):
    await state.update_data(title=m.text); await state.set_state(SellState.param)
    await m.answer("ℹ️ Опис:", reply_markup=kb.back_kb())

@router.message(SellState.param)
async def s_param(m: tg_types.Message, state: FSMContext):
    await state.update_data(param=m.text)
    await state.set_state(SellState.price)
    await m.answer("💰 Ціна:", reply_markup=kb.price_options_kb())

# --- PRICE & EXCHANGE ---
@router.callback_query(SellState.price, F.data.startswith("pr_"))
async def s_price_btn(c: tg_types.CallbackQuery, state: FSMContext):
    val = c.data.split("_")[1]; await state.update_data(price=val)
    await check_condition_step(c.message, state); await c.answer()

@router.message(SellState.price)
async def s_price_text(m: tg_types.Message, state: FSMContext):
    await state.update_data(price=m.text)
    d = await state.get_data()
    cat = d.get('category', '')
    
    if any(ac in cat for ac in AUTO_CATS_LOGIC):
        await state.set_state(SellState.exchange)
        await m.answer(f"💰 Ціна {m.text} прийнята.\nЧи розглядаєте ви обмін?", reply_markup=kb.exchange_ask_kb())
    else:
        await check_condition_step(m, state)

@router.callback_query(SellState.exchange, F.data.startswith("exch_"))
async def s_exchange_decision(c: tg_types.CallbackQuery, state: FSMContext):
    d = await state.get_data()
    price = d.get('price', '')
    if "yes" in c.data:
        await state.update_data(price=f"{price} (Можливий обмін)")
    await check_condition_step(c.message, state)
    await c.answer()

async def check_condition_step(message_obj, state: FSMContext):
    d = await state.get_data()
    cat = d['category']
    
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT section FROM categories WHERE name=?", (cat,)) as cur:
            res = await cur.fetchone()
            section = res[0] if res else "goods"

    if any(ac in cat for ac in AUTO_CATS_LOGIC) or section == "service":
        await state.update_data(condition="")
        await state.set_state(SellState.photo)
        await message_obj.answer("📸 Фото:", reply_markup=kb.back_kb())
    else:
        if "Автозапчастини" in cat:
             await message_obj.answer("✨ Стан запчастини:", reply_markup=kb.condition_kb())
        else:
             await message_obj.answer("✨ Стан товару:", reply_markup=kb.condition_kb())
        await state.set_state(SellState.condition)

@router.callback_query(SellState.condition, F.data.startswith("cond_"))
async def s_condition(c: tg_types.CallbackQuery, state: FSMContext):
    val = c.data.split("_")[1]; await state.update_data(condition=val)
    await state.set_state(SellState.photo)
    await c.message.answer("📸 Фото товару:", reply_markup=kb.back_kb()); await c.answer()

@router.message(SellState.photo, F.photo)
async def s_photo(m: tg_types.Message, state: FSMContext, bot: Bot):
    d = await state.get_data(); photo = m.photo[-1]; photo_bytes = await bot.download(photo.file_id)
    try:
        res = client.models.generate_content(model="gemini-2.5-flash", contents=[f"Це '{d['title']}'? ТАК/НІ", types.Part.from_bytes(data=photo_bytes.getvalue(), mime_type="image/jpeg")])
        if "НІ" in res.text.upper(): return await m.answer("❌ Модерація: Схоже, це не товар.")
    except: pass
    await state.update_data(photo_id=photo.file_id); await state.set_state(SellState.phone)
    await m.answer("📱 Надішліть свій номер телефону (натисніть кнопку нижче або введіть вручну):", reply_markup=kb.phone_kb())

@router.message(SellState.photo)
async def s_photo_wrong(m: tg_types.Message):
    await m.answer("⚠️ Це не фото! Надішліть зображення 📸")

@router.message(SellState.phone, (F.contact | F.text))
async def s_phone(m: tg_types.Message, state: FSMContext):
    if m.contact: num = m.contact.phone_number
    else: num = m.text.strip()
    if not num.startswith("+"): num = f"+{num}"
    await state.update_data(phone=num); await state.set_state(SellState.show_phone)
    await m.answer("✅ Контакт прийнято.", reply_markup=ReplyKeyboardRemove())
    await m.answer("📞 Показувати номер?", reply_markup=kb.show_phone_kb())

@router.callback_query(SellState.show_phone, F.data.startswith("show_phone_"))
async def s_privacy(c: tg_types.CallbackQuery, state: FSMContext):
    choice = 1 if "yes" in c.data else 0
    await state.update_data(show_phone=choice); await state.set_state(SellState.confirm)
    await c.message.edit_text("🎯 Все готово!", reply_markup=kb.publish_confirm_kb()); await c.answer()

@router.callback_query(SellState.confirm, F.data == "confirm_publish")
async def finish_publish(c: tg_types.CallbackQuery, state: FSMContext):
    lang = c.from_user.language_code
    allowed, posted, limit = await check_user_limits(c.from_user.id)
    if not allowed:
        await c.answer(t("limit_reached", lang, posted=posted, limit=limit), show_alert=True)
        return

    d = await state.get_data(); param = d['param']
    if any(ac in d.get('category','') for ac in AUTO_CATS_LOGIC):
        if 'car_year' in d:
             param = f"📅 Рік: {d['car_year']} р.\n🛣 Пробіг: {d['car_mileage']} тис. км\n⚙️ КП: {d['car_trans']}\n⛽️ Паливо: {d['car_fuel']}\n\n{param}"
    
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("INSERT INTO ads (user_id, username, category, title, param, price, condition, photo_id, phone, show_phone, created_at) VALUES (?,?,?,?,?,?,?,?,?,?,?)", 
            (c.from_user.id, c.from_user.username or f"id{c.from_user.id}", d['category'], d['title'], param, d['price'], d.get('condition', ''), d['photo_id'], d['phone'], d['show_phone'], datetime.now().isoformat()))
        await db.commit()
    await state.clear(); await c.message.answer(t("published_success", lang), reply_markup=kb.main_menu(True)); await c.answer()
    await activate_referral_if_first_ad(c.from_user.id, c.from_user.username or f"id{c.from_user.id}", c.bot)

@router.callback_query(F.data.startswith("cat_"), ~StateFilter(SellState), ~StateFilter(EditState), ~StateFilter(CategoryState))
async def show_ads(c: tg_types.CallbackQuery):
    lang = c.from_user.language_code
    cat = c.data.split("_")[1]
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT id, title, price, param, condition, photo_id, username, phone, show_phone FROM ads WHERE category=?", (cat,)) as cur:
            ads = await cur.fetchall()
    if not ads:
        await c.answer(t("no_ads_category", lang), show_alert=True)
        return
    
    bot_info = await c.bot.get_me()
    aid, t_item, p, par, cond, ph_id, u, phone, show = ads[0]
    contact = f"\n📞 Тел: {phone}" if show == 1 else ""
    cond_text = f"\nСтан: {cond}" if cond else ""
    caption_text = f"<b>{t_item}</b>\n{par}{cond_text}\n💰 Ціна: {p}{contact}\n🤖 <a href='https://t.me/{bot_info.username}'>Барахолка у кишені м. {CITY_NAME}</a>"
    
    is_admin = (c.from_user.id == ADMIN_ID)
    await c.message.answer_photo(photo=ph_id, caption=caption_text, reply_markup=kb.pagination_kb(0, len(ads), u, cat, is_admin=is_admin, ad_id=aid), parse_mode="HTML"); await c.answer()

@router.callback_query(F.data.startswith("pg_"))
async def pagination_handler(c: tg_types.CallbackQuery):
    parts = c.data.split("_"); category, index = parts[1], int(parts[2])
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT id, title, price, param, condition, photo_id, username, phone, show_phone FROM ads WHERE category=?", (category,)) as cur:
            ads = await cur.fetchall()
    bot_info = await c.bot.get_me()
    aid, t_item, p, par, cond, ph_id, u, phone, show = ads[index]
    contact = f"\n📞 Тел: {phone}" if show == 1 else ""
    cond_text = f"\nСтан: {cond}" if cond else ""
    caption_text = f"<b>{t_item}</b>\n{par}{cond_text}\n💰 Ціна: {p}{contact}\n🤖 <a href='https://t.me/{bot_info.username}'>Барахолка у кишені м. {CITY_NAME}</a>"
    
    is_admin = (c.from_user.id == ADMIN_ID)
    try: await c.message.edit_media(media=InputMediaPhoto(media=ph_id, caption=caption_text, parse_mode="HTML"), reply_markup=kb.pagination_kb(index, len(ads), u, category, is_admin=is_admin, ad_id=aid))
    except: pass
    await c.answer()

@router.callback_query(F.data == "back_to_cat_list")
async def back_to_cat_list_handler(c: tg_types.CallbackQuery, state: FSMContext):
    try: await c.message.delete()
    except: pass
    await c.message.answer("📂 Оберіть розділ:", reply_markup=kb.sections_kb())
    await c.answer()

@router.message(F.text.in_({"💼 Кабінет продавця", "💼 Личный кабинет", "💼 User Cabinet"}), StateFilter("*"))
async def kabinet_btn(m: tg_types.Message, state: FSMContext):
    await state.clear(); await del_msg(m)
    await open_kabinet_view(m.from_user.id, m)

@router.callback_query(F.data == "back_to_cabinet", StateFilter("*"))
async def back_to_cab(c: tg_types.CallbackQuery, state: FSMContext):
    await state.clear(); await del_msg(c.message)
    await open_kabinet_view(c.from_user.id, c.message); await c.answer()

# --- EDIT ADS FLOW ---
@router.callback_query(F.data.startswith("edit_"), StateFilter("*"))
async def edit_menu_open(c: tg_types.CallbackQuery):
    ad_id = c.data.split("_")[1]
    try: await c.message.edit_text("⚙️ Що змінити?", reply_markup=kb.edit_options_kb(ad_id))
    except: pass
    await c.answer()

@router.callback_query(F.data.startswith("ed_"), StateFilter("*"))
async def edit_field_select(c: tg_types.CallbackQuery, state: FSMContext):
    parts = c.data.split("_")
    field_map = {"t": "title", "p": "param", "c": "price", "f": "photo_id", "ph": "phone"}
    field = field_map.get(parts[1])
    ad_id = parts[2]
    await state.update_data(edit_id=ad_id, edit_field=field)
    try: await c.message.delete()
    except: pass

    if parts[1] == "f": 
        await state.set_state(EditState.input_photo)
        await c.message.answer("📸 Надішліть НОВЕ фото:", reply_markup=kb.back_kb())
    elif parts[1] == "ph": 
        await state.set_state(EditState.input_text)
        await c.message.answer("📞 Новий номер:", reply_markup=kb.phone_kb())
    else: 
        await state.set_state(EditState.input_text)
        await c.message.answer(f"📝 Введіть нове значення:", reply_markup=kb.back_kb())
    await c.answer()

@router.message(EditState.input_text, (F.text | F.contact))
async def edit_text_finish(m: tg_types.Message, state: FSMContext):
    d = await state.get_data()
    aid, field = d['edit_id'], d['edit_field']
    if m.contact: new_val = m.contact.phone_number
    else:
        new_val = m.text
        if field == "phone" and not new_val.startswith("+"): new_val = f"+{new_val.strip()}"

    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(f"UPDATE ads SET {field}=? WHERE id=?", (new_val, aid))
        await db.commit()
    await state.clear()
    await m.answer("✅ Дані оновлено!", reply_markup=ReplyKeyboardRemove())
    await m.answer("💼 Кабінет:", reply_markup=kb.main_menu(True))
    await open_kabinet_view(m.from_user.id, m)

@router.message(EditState.input_photo, F.photo)
async def edit_photo_finish(m: tg_types.Message, state: FSMContext):
    d = await state.get_data(); aid = d['edit_id']
    new_photo = m.photo[-1].file_id
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE ads SET photo_id=? WHERE id=?", (new_photo, aid))
        await db.commit()
    await state.clear(); await m.answer("📸 Фото оновлено!", reply_markup=kb.main_menu(True))
    await open_kabinet_view(m.from_user.id, m)

@router.callback_query(F.data.startswith("del_"))
async def delete_ad(c: tg_types.CallbackQuery):
    ad_id = c.data.split("_")[1]
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM ads WHERE id=?", (ad_id,)); await db.commit()
    await c.message.edit_text("🗑 Видалено!"); await c.answer()

# --- ADMIN PANEL ---
@router.callback_query(F.data == "admin_manage_cats")
async def admin_cats_root(c: tg_types.CallbackQuery):
    await c.message.answer("📂 Оберіть розділ для редагування:", reply_markup=kb.admin_sections_kb())
    await c.answer()

@router.callback_query(F.data.startswith("adm_sec_"))
async def admin_show_section(c: tg_types.CallbackQuery, state: FSMContext):
    sec_code = c.data.replace("adm_sec_", "")
    await state.update_data(current_section=sec_code)
    
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT name FROM categories WHERE section=?", (sec_code,)) as cur:
            filtered_cats = [row[0] for row in await cur.fetchall()]

    await c.message.answer(f"📂 Категорії у розділі ({sec_code}):", reply_markup=kb.admin_add_kb())
    if not filtered_cats:
        await c.message.answer("Пусто...")
    else:
        for cat in filtered_cats:
            await c.message.answer(f"▫️ {cat}", reply_markup=kb.admin_cat_actions(cat))
    await c.answer()

@router.callback_query(F.data == "adm_add_new")
async def admin_add_start(c: tg_types.CallbackQuery, state: FSMContext):
    await state.set_state(CategoryState.add_new_name)
    await c.message.answer("➕ Введіть назву НОВОЇ категорії:", reply_markup=kb.back_kb())
    await c.answer()

@router.message(CategoryState.add_new_name)
async def admin_add_finish(m: tg_types.Message, state: FSMContext):
    d = await state.get_data()
    current_sec = d.get('current_section', 'goods')
    new_name = emoji.emojize(m.text)
    
    try:
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute("INSERT INTO categories (name, section) VALUES (?, ?)", (new_name, current_sec))
            await db.commit()
        await m.answer(f"✅ Категорію '{new_name}' додано до '{current_sec}'!", reply_markup=kb.main_menu(True))
        await state.clear()
    except aiosqlite.IntegrityError:
        await m.answer(f"❌ Категорія '{new_name}' вже існує!", reply_markup=kb.back_kb())

@router.callback_query(F.data.startswith("adm_edit_"))
async def admin_edit_cat_start(c: tg_types.CallbackQuery, state: FSMContext):
    old_name = c.data.replace("adm_edit_", "")
    await state.set_state(CategoryState.editing_old_name)
    await state.update_data(editing_old_name=old_name)
    await state.set_state(CategoryState.input_name)
    await c.message.answer(f"✏️ Введіть НОВУ назву для категорії '{old_name}':", reply_markup=kb.back_kb())
    await c.answer()

@router.message(CategoryState.input_name)
async def admin_edit_cat_finish(m: tg_types.Message, state: FSMContext):
    d = await state.get_data()
    old_name = d['editing_old_name']
    new_name = emoji.emojize(m.text)
    
    try:
        async with aiosqlite.connect(DB_NAME) as db:
            await db.execute("UPDATE categories SET name=? WHERE name=?", (new_name, old_name))
            await db.execute("UPDATE ads SET category=? WHERE category=?", (new_name, old_name))
            await db.commit()
        await m.answer(f"✅ Перейменовано: '{old_name}' -> '{new_name}'", reply_markup=kb.main_menu(True))
        await state.clear()
    except aiosqlite.IntegrityError:
        await m.answer(f"❌ Назва '{new_name}' вже зайнята!", reply_markup=kb.back_kb())

@router.callback_query(F.data.startswith("adm_del_"))
async def admin_del_cat(c: tg_types.CallbackQuery):
    cat = c.data.replace("adm_del_", "")
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM categories WHERE name=?", (cat,))
        await db.execute("DELETE FROM ads WHERE category=?", (cat,))
        await db.commit()
    await c.message.edit_text(f"🗑 Категорію '{cat}' ВИДАЛЕНО!"); await c.answer()

@router.callback_query(F.data == "admin_delete_ads_start")
async def admin_delete_ads_start(c: tg_types.CallbackQuery):
    if c.from_user.id != ADMIN_ID:
        await c.answer("🚫 Доступ заборонений.", show_alert=True)
        return
    await c.message.answer("📂 Оберіть розділ для перегляду та видалення оголошень:", reply_markup=kb.sections_kb())
    await c.answer()

@router.callback_query(F.data.startswith("adm_delad_"))
async def admin_delete_ad_callback(c: tg_types.CallbackQuery):
    if c.from_user.id != ADMIN_ID:
        await c.answer("🚫 Доступ заборонений.", show_alert=True)
        return
        
    parts = c.data.split("_")
    ad_id = int(parts[2])
    category = parts[3]
    
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("DELETE FROM ads WHERE id=?", (ad_id,))
        await db.commit()
        
    await c.answer("🗑 Оголошення видалено!", show_alert=True)
    
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT id, title, price, param, condition, photo_id, username, phone, show_phone FROM ads WHERE category=?", (category,)) as cur:
            ads = await cur.fetchall()
            
    if not ads:
        try: await c.message.delete()
        except: pass
        await c.message.answer("📂 У цій категорії більше немає оголошень.", reply_markup=kb.sections_kb())
    else:
        bot_info = await c.bot.get_me()
        aid, t_item, p, par, cond, ph_id, u, phone, show = ads[0]
        contact = f"\n📞 Тел: {phone}" if show == 1 else ""
        cond_text = f"\nСтан: {cond}" if cond else ""
        caption_text = f"<b>{t_item}</b>\n{par}{cond_text}\n💰 Ціна: {p}{contact}\n🤖 <a href='https://t.me/{bot_info.username}'>Барахолка у кишені м. {CITY_NAME}</a>"
        
        is_admin = (c.from_user.id == ADMIN_ID)
        try:
            await c.message.edit_media(
                media=InputMediaPhoto(media=ph_id, caption=caption_text, parse_mode="HTML"),
                reply_markup=kb.pagination_kb(0, len(ads), u, category, is_admin=is_admin, ad_id=aid)
            )
        except Exception:
            try: await c.message.delete()
            except: pass
            await c.message.answer_photo(
                photo=ph_id,
                caption=caption_text,
                reply_markup=kb.pagination_kb(0, len(ads), u, category, is_admin=is_admin, ad_id=aid),
                parse_mode="HTML"
            )

# --- VOICE TRANSCRIBER ---
@router.message(F.voice, StateFilter("*"))
async def handle_voice_input(m: tg_types.Message, state: FSMContext, bot: Bot):
    current_state = await state.get_state()
    if not current_state:
        return
    
    destination = f"voice_{m.from_user.id}.ogg"
    try:
        file_id = m.voice.file_id
        file = await bot.get_file(file_id)
        await bot.download_file(file.file_path, destination)
    except Exception as e:
        print(f"❌ Failed to download voice message: {e}")
        await m.answer("⚠️ Не вдалося завантажити голосове повідомлення. Спробуйте надіслати текстове.")
        return
        
    url = "https://api.groq.com/openai/v1/audio/transcriptions"
    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}"
    }
    
    transcribed_text = ""
    try:
        with open(destination, "rb") as f:
            files = {
                "file": (os.path.basename(destination), f, "audio/ogg")
            }
            data = {
                "model": GROQ_MODEL,
                "language": "uk"
            }
            r = requests.post(url, headers=headers, files=files, data=data, timeout=30)
            if r.status_code == 200:
                transcribed_text = r.json().get("text", "").strip()
            else:
                print(f"❌ Groq Transcription API Error: {r.status_code} - {r.text}")
    except Exception as e:
        print(f"❌ Exception during Groq transcription: {e}")
    finally:
        if os.path.exists(destination):
            try: os.remove(destination)
            except Exception: pass
            
    if not transcribed_text:
        await m.answer("🧠 Вибачте, не вдалося розпізнати голосове повідомлення. Спробуйте записати чіткіше.")
        return

    m = m.model_copy(update={"text": transcribed_text})
    await m.answer(f"🎤 <i>Надиктовано: \"{transcribed_text}\"</i>", parse_mode="HTML")
    
    if current_state == SellState.car_brand.state:
        await s_car_brand(m, state)
    elif current_state == SellState.car_year.state:
        await s_car_year(m, state)
    elif current_state == SellState.car_mileage.state:
        await s_car_mileage(m, state)
    elif current_state == SellState.title.state:
        await s_title(m, state)
    elif current_state == SellState.param.state:
        await s_param(m, state)
    elif current_state == SellState.price.state:
        await s_price_text(m, state)
    elif current_state == EditState.input_text.state:
        await edit_text_finish(m, state)
    elif current_state == CategoryState.add_new_name.state:
        await admin_add_finish(m, state)
    elif current_state == CategoryState.input_name.state:
        await admin_edit_cat_finish(m, state)

# --- REFERRALS & PLAN LIMITS ---
async def register_user_if_not_exists(user_id: int, username: str, args: str, bot: Bot):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT 1 FROM users WHERE user_id=?", (user_id,)) as cur:
            exists = await cur.fetchone() is not None
        if not exists:
            referred_by = None
            if args and args.startswith("ref_"):
                try:
                    ref_id = int(args.replace("ref_", ""))
                    if ref_id != user_id:
                        referred_by = ref_id
                except ValueError:
                    pass
            await db.execute("INSERT INTO users (user_id, username, referred_by) VALUES (?, ?, ?)",
                             (user_id, username, referred_by))
            if referred_by:
                await db.execute("INSERT INTO referrals (referrer_id, referred_id, status) VALUES (?, ?, 'pending')",
                                 (referred_by, user_id))
                try:
                    await bot.send_message(
                        chat_id=referred_by,
                        text=f"🔔 За вашим реферальним посиланням зареєструвався новий користувач @{username}!\n"
                             f"Бонус +3 оголошення буде активовано після того, як він опублікує свій перший пост."
                    )
                except Exception as e:
                    print(f"Failed to notify referrer {referred_by}: {e}")
            await db.commit()

async def check_user_limits(user_id: int):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT bonus_posts, subscription_until FROM users WHERE user_id=?", (user_id,)) as cur:
            row = await cur.fetchone()
        if not row:
            await db.execute("INSERT OR IGNORE INTO users (user_id, username) VALUES (?, ?)", (user_id, f"id{user_id}"))
            await db.commit()
            return True, 0, 3
            
        bonus_posts, sub_until_str = row
        
        if sub_until_str:
            try:
                sub_until = datetime.fromisoformat(sub_until_str)
                if sub_until > datetime.now():
                    return True, "безліміт", None
            except ValueError:
                pass
                
        local_now = datetime.now()
        monday = local_now - timedelta(days=local_now.weekday())
        monday_start = monday.replace(hour=0, minute=0, second=0, microsecond=0).isoformat()
        
        async with db.execute("SELECT COUNT(*) FROM ads WHERE user_id=? AND created_at >= ?", (user_id, monday_start)) as cur:
            res = await cur.fetchone()
            posted_count = res[0] if res else 0
            
        total_limit = 3 + bonus_posts
        if posted_count < total_limit:
            return True, posted_count, total_limit
        else:
            return False, posted_count, total_limit

async def activate_referral_if_first_ad(user_id: int, username: str, bot: Bot):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute("SELECT COUNT(*) FROM ads WHERE user_id=?", (user_id,)) as cur:
            res = await cur.fetchone()
            ads_count = res[0] if res else 0
            
        if ads_count == 1:
            async with db.execute("SELECT referrer_id FROM referrals WHERE referred_id=? AND status='pending'", (user_id,)) as cur:
                row = await cur.fetchone()
            if row:
                direct_referrer_id = row[0]
                await db.execute("UPDATE referrals SET status='active' WHERE referred_id=? AND status='pending'", (user_id,))
                
                rewards = [3, 2, 1]
                current_parent_id = direct_referrer_id
                
                for level, reward in enumerate(rewards):
                    await db.execute("UPDATE users SET bonus_posts = bonus_posts + ? WHERE user_id=?", (reward, current_parent_id))
                    try:
                        await bot.send_message(
                            chat_id=current_parent_id,
                            text=f"🎉 **Реферальний бонус!** Користувач з вашої структури @{username} опублікував перше оголошення.\n"
                                 f"Вам нараховано <b>+{reward} додаткових публікацій</b> (Рівень {level + 1})!"
                        )
                    except Exception as e:
                        print(f"Failed to notify level {level+1} parent {current_parent_id}: {e}")
                        
                    async with db.execute("SELECT referred_by FROM users WHERE user_id=?", (current_parent_id,)) as parent_cur:
                        p_row = await parent_cur.fetchone()
                    if p_row and p_row[0]:
                        current_parent_id = p_row[0]
                    else:
                        break
                        
                await db.commit()

# --- TELEGRAM STARS PAYMENTS ---
@router.callback_query(F.data == "buy_stars_weekly")
async def process_buy_stars_weekly(c: tg_types.CallbackQuery, bot: Bot):
    await c.answer()
    await bot.send_invoice(
        chat_id=c.from_user.id,
        title="7 днів безліміту",
        description="Оплата тижневої підписки на безлімітні оголошення у м. " + CITY_NAME,
        payload="weekly_stars_sub",
        provider_token="",  # Empty for Telegram Stars
        currency="XTR",
        prices=[tg_types.LabeledPrice(label="7 днів безліміту", amount=5)]
    )

@router.callback_query(F.data == "buy_stars_monthly")
async def process_buy_stars_monthly(c: tg_types.CallbackQuery, bot: Bot):
    await c.answer()
    await bot.send_invoice(
        chat_id=c.from_user.id,
        title="30 днів безліміту",
        description="Оплата місячної підписки на безлімітні оголошення у м. " + CITY_NAME,
        payload="monthly_stars_sub",
        provider_token="",  # Empty for Telegram Stars
        currency="XTR",
        prices=[tg_types.LabeledPrice(label="30 днів безліміту", amount=15)]
    )

@router.pre_checkout_query()
async def process_pre_checkout(query: tg_types.PreCheckoutQuery):
    await query.answer(ok=True)

@router.message(F.successful_payment)
async def process_successful_payment(m: tg_types.Message):
    payload = m.successful_payment.invoice_payload
    user_id = m.from_user.id
    
    if payload == "weekly_stars_sub":
        days = 7
        title = "7 днів безліміту"
    elif payload == "monthly_stars_sub":
        days = 30
        title = "30 днів безліміту"
    else:
        await m.answer("❌ Невідомий тип платежу.")
        return
        
    until_date = (datetime.now() + timedelta(days=days)).isoformat()
    
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("UPDATE users SET subscription_until=? WHERE user_id=?", (until_date, user_id))
        await db.commit()
        
    await m.answer(
        f"🎉 <b>Оплата пройшла успішно!</b>\n\n"
        f"Вам активовано тариф: <b>{title}</b>.\n"
        f"Він діє до: <code>{(datetime.now() + timedelta(days=days)).strftime('%d.%m.%Y %H:%M')}</code>.",
        parse_mode="HTML"
    )

