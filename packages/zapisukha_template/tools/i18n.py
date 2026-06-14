import os

DEFAULT_LANG = os.getenv("DEFAULT_LANG", "uk")

TRANSLATIONS = {
    "welcome_new": {
        "uk": "✍️ <b>Вітаємо у «Записусі»! 💅</b>\n\nЯ ваш особистий асистент для запису в салон краси.\nЯк вас звати? Введіть своє ім'я:",
        "ru": "✍️ <b>Добро пожаловать в «Записуху»! 💅</b>\n\nЯ ваш личный ассистент для записи в салон красоты.\nКак вас зовут? Введите свое имя:",
        "en": "✍️ <b>Welcome to \"Zapisukha\"! 💅</b>\n\nI am your personal booking assistant for the beauty salon.\nWhat is your name? Please enter your name:"
    },
    "welcome_returning": {
        "uk": "✍️ <b>Вітаємо, {name}!</b> 💅\n\nСьогодні наша майстриня у: {addr}\n\nОберіть дію:",
        "ru": "✍️ <b>Рады видеть вас, {name}!</b> 💅\n\nСегодня наш мастер принимает в: {addr}\n\nВыберите действие:",
        "en": "✍️ <b>Welcome back, {name}!</b> 💅\n\nToday our master works at: {addr}\n\nChoose an action:"
    },
    "enter_name_error": {
        "uk": "⚠️ Введіть ваше ім'я (мінімум 2 символи):",
        "ru": "⚠️ Введите ваше имя (минимум 2 символа):",
        "en": "⚠️ Please enter your name (minimum 2 characters):"
    },
    "enter_phone": {
        "uk": "📞 Введіть ваш номер телефону або натисніть кнопку:",
        "ru": "📞 Введите ваш номер телефона или нажмите кнопку:",
        "en": "📞 Enter your phone number or click the button below:"
    },
    "share_contact_btn": {
        "uk": "📱 Поділитися контактом",
        "ru": "📱 Поделиться контактом",
        "en": "📱 Share Contact"
    },
    "registered_success": {
        "uk": "✅ <b>Чудово, {name}!</b>\nВас зареєстровано. Тепер можете записатись 💅\n\nСьогодні майстриня: {addr}",
        "ru": "✅ <b>Отлично, {name}!</b>\nВы успешно зарегистрированы. Теперь можно записаться 💅\n\nСегодня мастер принимает в: {addr}",
        "en": "✅ <b>Awesome, {name}!</b>\nYou have registered. Now you can book an appointment 💅\n\nToday the master works at: {addr}"
    },
    "select_date": {
        "uk": "📅 <b>Виберіть зручну дату для запису:</b>\n\n🏛 = Салон\n🏠 = Вдома\n\nСьогодні майстриня: {today_addr}",
        "ru": "📅 <b>Выберите удобную дату для записи:</b>\n\n🏛 = Салон\n🏠 = Дома\n\nСегодня мастер принимает в: {today_addr}",
        "en": "📅 <b>Select a convenient date for booking:</b>\n\n🏛 = Salon\n🏠 = Home\n\nToday the master works at: {today_addr}"
    },
    "select_time": {
        "uk": "📅 <b>{date_str}</b> — {addr}\n\n🕐 Оберіть вільний час:",
        "ru": "📅 <b>{date_str}</b> — {addr}\n\n🕐 Выберите свободное время:",
        "en": "📅 <b>{date_str}</b> — {addr}\n\n🕐 Select an available time slot:"
    },
    "select_service": {
        "uk": "🕐 Час: <b>{time_slot}</b>\n\n💅 Оберіть послугу:",
        "ru": "🕐 Время: <b>{time_slot}</b>\n\n💅 Выберите услугу:",
        "en": "🕐 Time: <b>{time_slot}</b>\n\n💅 Choose service:"
    },
    "enter_wishes": {
        "uk": "✅ Послуга: <b>{srv_name}</b> — {price} {currency}\n\n💬 Введіть побажання або опис (або напишіть <code>-</code> якщо немає):",
        "ru": "✅ Услуга: <b>{srv_name}</b> — {price} {currency}\n\n💬 Введите пожелания или описание (или напишите <code>-</code> если нет):",
        "en": "✅ Service: <b>{srv_name}</b> — {price} {currency}\n\n💬 Enter comments or wishes (or type <code>-</code> if none):"
    },
    "confirm_title": {
        "uk": "📋 <b>Підтвердіть запис:</b>\n\n",
        "ru": "📋 <b>Подтвердите запись:</b>\n\n",
        "en": "📋 <b>Confirm your appointment:</b>\n\n"
    },
    "confirm_date": {
        "uk": "📅 Дата: <b>{date}</b>\n",
        "ru": "📅 Дата: <b>{date}</b>\n",
        "en": "📅 Date: <b>{date}</b>\n"
    },
    "confirm_time": {
        "uk": "🕐 Час: <b>{time}</b>\n",
        "ru": "🕐 Время: <b>{time}</b>\n",
        "en": "🕐 Time: <b>{time}</b>\n"
    },
    "confirm_service": {
        "uk": "💅 Послуга: <b>{service}</b>\n",
        "ru": "💅 Услуга: <b>{service}</b>\n",
        "en": "💅 Service: <b>{service}</b>\n"
    },
    "confirm_price": {
        "uk": "💰 Вартість: <b>{price} {currency}</b>{discount_text}\n",
        "ru": "💰 Стоимость: <b>{price} {currency}</b>{discount_text}\n",
        "en": "💰 Price: <b>{price} {currency}</b>{discount_text}\n"
    },
    "confirm_place": {
        "uk": "📍 Місце: {addr}\n",
        "ru": "📍 Место: {addr}\n",
        "en": "📍 Location: {addr}\n"
    },
    "confirm_wishes": {
        "uk": "💬 Побажання: {wishes}\n",
        "ru": "💬 Пожелания: {wishes}\n",
        "en": "💬 Comments: {wishes}\n"
    },
    "discount_text": {
        "uk": "\n🔥 <b>Акція!</b> Знижка 10% = -{discount} {currency} (давно не були!)",
        "ru": "\n🔥 <b>Акция!</b> Скидка 10% = -{discount} {currency} (давно не были!)",
        "en": "\n🔥 <b>Special Offer!</b> 10% discount = -{discount} {currency} (we haven't seen you for a while!)"
    },
    "booking_success": {
        "uk": "✅ <b>Ви успішно записані!</b>\n\n📅 {date} о {time}\n💅 {service} — {price} {currency}\n📍 {addr}\n\n🔔 Нагадаємо за день до запису!\n<i>ID запису: {rec_id}</i>",
        "ru": "✅ <b>Вы успешно записаны!</b>\n\n📅 {date} в {time}\n💅 {service} — {price} {currency}\n📍 {addr}\n\n🔔 Напомним за день до записи!\n<i>ID записи: {rec_id}</i>",
        "en": "✅ <b>You have successfully booked!</b>\n\n📅 {date} at {time}\n💅 {service} — {price} {currency}\n📍 {addr}\n\n🔔 We will remind you a day before the booking!\n<i>Record ID: {rec_id}</i>"
    },
    "booking_error": {
        "uk": "❌ Помилка запису. Спробуйте ще раз.",
        "ru": "❌ Ошибка записи. Попробуйте еще раз.",
        "en": "❌ Booking error. Please try again."
    },
    "btn_book": {
        "uk": "📅 Записатись",
        "ru": "📅 Записаться",
        "en": "📅 Book Appointment"
    },
    "btn_my_records": {
        "uk": "📋 Мої записи",
        "ru": "📋 Мои записи",
        "en": "📋 My Bookings"
    },
    "btn_price": {
        "uk": "💰 Прайс",
        "ru": "💰 Прайс",
        "en": "💰 Price List"
    },
    "btn_admin": {
        "uk": "👑 Адмін-панель",
        "ru": "👑 Admin-панель",
        "en": "👑 Admin Panel"
    },
    "btn_cancel": {
        "uk": "❌ Скасувати",
        "ru": "❌ Отмена",
        "en": "❌ Cancel"
    },
    "btn_back": {
        "uk": "⬅️ Назад",
        "ru": "⬅️ Назад",
        "en": "⬅️ Back"
    },
    "btn_menu": {
        "uk": "🔙 Меню",
        "ru": "🔙 Меню",
        "en": "🔙 Menu"
    },
    "btn_confirm": {
        "uk": "✅ Підтвердити запис",
        "ru": "✅ Подтвердить запись",
        "en": "✅ Confirm Appointment"
    },
    "no_available_dates": {
        "uk": "❌ На жаль, немає доступних дат. Спробуйте пізніше.",
        "ru": "❌ К сожалению, нет свободных дат. Попробуйте позже.",
        "en": "❌ Unfortunately, no dates are available. Please try again later."
    },
    "no_available_slots": {
        "uk": "❌ На цю дату немає вільних годин. Оберіть іншу.",
        "ru": "❌ На эту дату нет свободного времени. Выберите другую.",
        "en": "❌ No free time slots for this date. Please select another date."
    },
    "my_records_empty": {
        "uk": "📋 <b>У вас немає активних записів.</b>\n\nЗапишіться на прийом через «📅 Записатись»!",
        "ru": "📋 <b>У вас нет активных записей.</b>\n\nЗапишитесь на прием через кнопку «📅 Записаться»!",
        "en": "📋 <b>You have no active bookings.</b>\n\nBook an appointment using the \"📅 Book Appointment\" button!"
    },
    "my_records_list": {
        "uk": "📋 <b>Ваші активні записи:</b>\n\n",
        "ru": "📋 <b>Ваши активные записи:</b>\n\n",
        "en": "📋 <b>Your active bookings:</b>\n\n"
    },
    "cancel_record_btn": {
        "uk": "❌ Відмінити {date} {time} — {service}",
        "ru": "❌ Отменить {date} {time} — {service}",
        "en": "❌ Cancel {date} {time} — {service}"
    },
    "record_cancelled": {
        "uk": "🗑 Запис <code>{rec_id}</code> скасовано.",
        "ru": "🗑 Запись <code>{rec_id}</code> отменена.",
        "en": "🗑 Booking <code>{rec_id}</code> has been cancelled."
    },
    "record_not_found": {
        "uk": "❌ Запис не знайдено або вже скасовано.",
        "ru": "❌ Запись не найдена или уже отменена.",
        "en": "❌ Booking not found or already cancelled."
    },
    "price_title": {
        "uk": "💅 <b>Прайс-лист послуг:</b>\n\n",
        "ru": "💅 <b>Прайс-лист услуг:</b>\n\n",
        "en": "💅 <b>Price list of services:</b>\n\n"
    },
    "cancel_record_notify_admin": {
        "uk": "⚠️ Клієнт скасував запис <code>{rec_id}</code> (tg_id: {user_id})",
        "ru": "⚠️ Клиент отменил запись <code>{rec_id}</code> (tg_id: {user_id})",
        "en": "⚠️ Client cancelled booking <code>{rec_id}</code> (tg_id: {user_id})"
    },
    "new_booking_notify_admin": {
        "uk": "📬 <b>Новий запис!</b>\n\n👤 Клієнт: {client_name} ({client_phone})\n📅 {date} о {time}\n💅 {service}\n📍 {addr}\n<i>ID: {rec_id}</i>",
        "ru": "📬 <b>Новая запись!</b>\n\n👤 Клиент: {client_name} ({client_phone})\n📅 {date} в {time}\n💅 {service}\n📍 {addr}\n<i>ID: {rec_id}</i>",
        "en": "📬 <b>New Booking!</b>\n\n👤 Client: {client_name} ({client_phone})\n📅 {date} at {time}\n💅 {service}\n📍 {addr}\n<i>ID: {rec_id}</i>"
    },
    "currency": {
        "uk": "грн",
        "ru": "грн",
        "en": "UAH"
    },
    "srv_m": {
        "uk": "💅 Манікюр",
        "ru": "💅 Маникюр",
        "en": "💅 Manicure"
    },
    "srv_p": {
        "uk": "🦶 Педикюр",
        "ru": "🦶 Педикюр",
        "en": "🦶 Pedicure"
    },
    "srv_d": {
        "uk": "🧴 Депіляція",
        "ru": "🧴 Депиляция",
        "en": "🧴 Depilation"
    }
}

def t(key, lang=None, **kwargs):
    if not lang:
        lang = DEFAULT_LANG
    lang = lang.split('-')[0].lower()
    if lang not in ["uk", "ru", "en"]:
        lang = "en"
    text_dict = TRANSLATIONS.get(key, {})
    text = text_dict.get(lang, text_dict.get(DEFAULT_LANG, key))
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
