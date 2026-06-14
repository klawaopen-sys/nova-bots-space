from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import InlineKeyboardButton, KeyboardButton

def main_menu(has_ads=False):
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="🛒 Купити"), KeyboardButton(text="📦 Продати"))
    builder.row(KeyboardButton(text="💼 Кабінет продавця"))
    builder.row(KeyboardButton(text="🔄 Оновити"))
    return builder.as_markup(resize_keyboard=True)

def sections_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🚗 Транспорт", callback_data="sec_auto"))
    builder.row(InlineKeyboardButton(text="🛍️ Товари", callback_data="sec_goods"))
    builder.row(InlineKeyboardButton(text="🛠️ Послуги", callback_data="sec_service"))
    return builder.as_markup()

# --- ADMIN SECTIONS ---
def admin_sections_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🚗 Транспорт", callback_data="adm_sec_auto"))
    builder.row(InlineKeyboardButton(text="🛍️ Товари", callback_data="adm_sec_goods"))
    builder.row(InlineKeyboardButton(text="🛠️ Послуги", callback_data="adm_sec_service"))
    return builder.as_markup()

def categories_kb(cats_data):
    builder = InlineKeyboardBuilder()
    for i in range(0, len(cats_data), 2):
        row_btns = []
        text1, data1 = cats_data[i]
        row_btns.append(InlineKeyboardButton(text=text1, callback_data=f"cat_{data1}"))
        if i + 1 < len(cats_data):
            text2, data2 = cats_data[i+1]
            row_btns.append(InlineKeyboardButton(text=text2, callback_data=f"cat_{data2}"))
        builder.row(*row_btns)
    builder.row(InlineKeyboardButton(text="🔙 Назад до розділів", callback_data="back_to_sections"))
    return builder.as_markup()

def condition_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✨ Нове", callback_data="cond_Нове"),
                InlineKeyboardButton(text="🛠 Вживане", callback_data="cond_Вживане"))
    return builder.as_markup()

def price_options_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🤝 Договірна", callback_data="pr_Договірна"),
                InlineKeyboardButton(text="🎁 Безкоштовно", callback_data="pr_Безкоштовно"))
    return builder.as_markup()

def exchange_ask_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🔄 Так, можливий обмін", callback_data="exch_yes"))
    builder.row(InlineKeyboardButton(text="➡️ Ні, тільки продаж", callback_data="exch_no"))
    return builder.as_markup()

def transmission_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="⚙️ Механіка", callback_data="trans_Механіка"),
                InlineKeyboardButton(text="🕹 Автомат", callback_data="trans_Автомат"))
    return builder.as_markup()

def fuel_kb():
    builder = InlineKeyboardBuilder()
    for f in ["Бензин", "Дизель", "Газ/Бензин", "Електро"]:
        builder.row(InlineKeyboardButton(text=f, callback_data=f"fuel_{f}"))
    return builder.as_markup()

def phone_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="📱 Поділитися контактом", request_contact=True))
    return builder.as_markup(resize_keyboard=True)

def show_phone_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✅ Так", callback_data="show_phone_yes"),
                InlineKeyboardButton(text="❌ Ні", callback_data="show_phone_no"))
    return builder.as_markup()

def publish_confirm_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🚀 Опублікувати!", callback_data="confirm_publish"))
    builder.row(InlineKeyboardButton(text="🔙 Скасувати", callback_data="cancel_publish"))
    return builder.as_markup()

def edit_options_kb(ad_id):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✏️ Назва", callback_data=f"ed_t_{ad_id}"))
    builder.row(InlineKeyboardButton(text="ℹ️ Опис", callback_data=f"ed_p_{ad_id}"))
    builder.row(InlineKeyboardButton(text="💰 Ціна", callback_data=f"ed_c_{ad_id}"))
    builder.row(InlineKeyboardButton(text="🖼 Фото", callback_data=f"ed_f_{ad_id}"))
    builder.row(InlineKeyboardButton(text="📞 Телефон", callback_data=f"ed_ph_{ad_id}"))
    builder.row(InlineKeyboardButton(text="🔙 Назад у Кабінет", callback_data="back_to_cabinet"))
    return builder.as_markup()

def pagination_kb(current_index, total_count, username, category, is_admin=False, ad_id=None):
    builder = InlineKeyboardBuilder()
    if username and not username.startswith("id"):
        builder.row(InlineKeyboardButton(text="💬 Написати продавцю", url=f"https://t.me/{username}"))
    
    nav_btns = []
    if current_index > 0: 
        nav_btns.append(InlineKeyboardButton(text="⬅️ Попередній", callback_data=f"pg_{category}_{current_index-1}"))
    if current_index < total_count - 1: 
        nav_btns.append(InlineKeyboardButton(text="Наступний ➡️", callback_data=f"pg_{category}_{current_index+1}"))
    builder.row(*nav_btns)
    
    if is_admin and ad_id is not None:
        builder.row(InlineKeyboardButton(text="🗑 Видалити (Адмін)", callback_data=f"adm_delad_{ad_id}_{category}"))
        
    builder.row(InlineKeyboardButton(text="🔙 До списку категорій", callback_data="back_to_cat_list"))
    return builder.as_markup()

def my_ads_actions(ad_id):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="📝 Редагувати", callback_data=f"edit_{ad_id}"),
                InlineKeyboardButton(text="🗑 Видалити", callback_data=f"del_{ad_id}"))
    return builder.as_markup()

def admin_cat_actions(cat_name):
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="✏️ Змінити назву", callback_data=f"adm_edit_{cat_name}"))
    builder.row(InlineKeyboardButton(text="🗑 Видалити категорію", callback_data=f"adm_del_{cat_name}"))
    return builder.as_markup()

def admin_add_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="➕ Додати нову категорію", callback_data="adm_add_new"))
    builder.row(InlineKeyboardButton(text="🔙 Назад до розділів", callback_data="admin_manage_cats")) 
    return builder.as_markup()

def back_kb():
    builder = ReplyKeyboardBuilder()
    builder.row(KeyboardButton(text="🔙 Назад до меню"))
    return builder.as_markup(resize_keyboard=True)

def cabinet_menu_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="👤 Реферальна програма", callback_data="ref_cabinet"))
    builder.row(InlineKeyboardButton(text="🌟 Купити безліміт", callback_data="stars_buy_menu"))
    return builder.as_markup()

def back_to_cabinet_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="💼 Назад до Кабінету", callback_data="back_to_cabinet"))
    return builder.as_markup()

def stars_tariffs_kb():
    builder = InlineKeyboardBuilder()
    builder.row(InlineKeyboardButton(text="🌟 7 днів безліміту (5 Stars)", callback_data="buy_stars_weekly"))
    builder.row(InlineKeyboardButton(text="🌟 30 днів безліміту (15 Stars)", callback_data="buy_stars_monthly"))
    builder.row(InlineKeyboardButton(text="💼 Назад до Кабінету", callback_data="back_to_cabinet"))
    return builder.as_markup()
