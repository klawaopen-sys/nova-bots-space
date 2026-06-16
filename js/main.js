// --- Мультимовні сценарії чатів для симулятора Telegram ---
const BOT_SCENARIOS = {
    uk: {
        zapisukha: [
            { sender: 'user', text: '/start' },
            { sender: 'bot', text: '👋 <b>Вітаємо!</b>\nЯ допоможу вам швидко записатися на бьюти-процедури.\n\nОберіть послугу нижче 👇', buttons: ['💅 Манікюр', '🦶 Педикюр', '🧴 Депіляція'] },
            { sender: 'user', text: '💅 Манікюр' },
            { sender: 'bot', text: '💅 <b>Ви обрали Манікюр (580 грн).</b>\n\nОберіть зручний день для візиту:', buttons: ['📅 15.06 (Пн)', '📅 16.06 (Вв)', '📅 17.06 (Ср)'] },
            { sender: 'user', text: '📅 15.06 (Пн)' },
            { sender: 'bot', text: '⏰ <b>Оберіть вільний час:</b>', buttons: ['⏰ 10:00', '⏰ 12:00', '⏰ 14:00'] },
            { sender: 'user', text: '⏰ 12:00' },
            { sender: 'bot', text: '📱 Надішліть ваш номер телефону для підтвердження запису.' },
            { sender: 'user', text: '+380991234567' },
            { sender: 'bot', text: '🎉 <b>Запис підтверджено!</b>\n\n📅 Дата: 15.06.2026\n⏰ Час: 12:00\n💅 Послуга: Манікюр\n📍 Адреса: м. Ніжин, вул. Шевченка 128\n\nЧекаємо на вас! 🌸' }
        ],
        mriya: [
            { sender: 'user', text: '/start' },
            { sender: 'bot', text: '🏠 <b>Вітаємо в CRM нерухомості!</b>\nЯ ваш цифровий асистент.\n\nОберіть дію:', buttons: ['🔎 Пошук об\'єктів', '➕ Додати об\'єкт'] },
            { sender: 'user', text: '➕ Додати об\'єкт' },
            { sender: 'bot', text: '✏️ Оберіть тип угоди:', buttons: ['🏷 Продаж', '🔑 Оренда'] },
            { sender: 'user', text: '🏷 Продаж' },
            { sender: 'bot', text: '📁 Оберіть категорію нерухомості:', buttons: ['🏢 Квартира', '🏡 Будинок', '🌾 Ділянка'] },
            { sender: 'user', text: '🏢 Квартира' },
            { sender: 'bot', text: '📸 Будь ласка, надішліть фотографію об\'єкта.' },
            { sender: 'user', isMedia: true, text: '🖼️ [Фото квартири]' },
            { sender: 'bot', text: '🧠 <b>ШІ-Модерація Gemini:</b> Фото успішно перевірено. Гола стіна/сміття не виявлені.\n\n✏️ Введіть ціну в гривнях:' },
            { sender: 'user', text: '1200000' },
            { sender: 'bot', text: '💵 <b>Автоконвертація по курсу НБУ:</b> $30,000.\n\n🚀 Об\'єкт успішно додано до бази та збережено у Google Таблиці!' }
        ],
        librarian: [
            { sender: 'user', text: '/start book_12' },
            { sender: 'bot', text: '🔒 <b>Доступ обмежено!</b>\n\nЩоб безкоштовно розблокувати цей файл, тобі потрібно підписатися на наші корисні канали.\n\nБудь ласка, підпишись на канали нижче та натисни кнопку перевірки:', buttons: ['📢 Сім сорок | Трейдинг', '🧠 Психологія', '🤖 Те що треба | AI', '🔄 Перевірити підписку', '⭐️ Забрати за 1 Зірку (без підписки)'] },
            { sender: 'user', text: '⭐️ Забрати за 1 Зірку (без підписки)' },
            { sender: 'bot', text: '💳 Бот виставив рахунок: <b>Швидкий доступ до книги</b> за 1 Telegram Star (XTR).\nОчікування оплати...' },
            { sender: 'user', text: '[Оплата успішно проведена 👍]' },
            { sender: 'bot', text: '🎉 <b>Дякуємо за підтримку зірками!</b>\nТвій файл успішно розблоковано:\n\n📚 <i>Книга_Маркетинг_ШИ.pdf (4.8 MB)</i>\n\nПриємного читання! 📖' }
        ]
    },
    ru: {
        zapisukha: [
            { sender: 'user', text: '/start' },
            { sender: 'bot', text: '👋 <b>Добро пожаловать!</b>\nЯ помогу вам быстро записаться на бьюти-процедуры.\n\nВыберите услугу ниже 👇', buttons: ['💅 Маникюр', '🦶 Педикюр', '🧴 Депиляция'] },
            { sender: 'user', text: '💅 Маникюр' },
            { sender: 'bot', text: '💅 <b>Вы выбрали Маникюр (580 грн).</b>\n\nВыберите удобный день для визита:', buttons: ['📅 15.06 (Пн)', '📅 16.06 (Вт)', '📅 17.06 (Ср)'] },
            { sender: 'user', text: '📅 15.06 (Пн)' },
            { sender: 'bot', text: '⏰ <b>Выберите свободное время:</b>', buttons: ['⏰ 10:00', '⏰ 12:00', '⏰ 14:00'] },
            { sender: 'user', text: '⏰ 12:00' },
            { sender: 'bot', text: '📱 Отправьте ваш номер телефона для подтверждения записи.' },
            { sender: 'user', text: '+380991234567' },
            { sender: 'bot', text: '🎉 <b>Запись подтверждена!</b>\n\n📅 Дата: 15.06.2026\n⏰ Время: 12:00\n💅 Услуга: Маникюр\n📍 Адрес: г. Нежин, ул. Шевченко 128\n\nЖдем вас! 🌸' }
        ],
        mriya: [
            { sender: 'user', text: '/start' },
            { sender: 'bot', text: '🏠 <b>Добро пожаловать в CRM недвижимости!</b>\nЯ ваш цифровой ассистент по недвижимости.\n\nВыберите действие:', buttons: ['🔎 Поиск объектов', '➕ Добавить объект'] },
            { sender: 'user', text: '➕ Добавить объект' },
            { sender: 'bot', text: '✏️ Выберите тип сделки:', buttons: ['🏷 Продажа', '🔑 Аренда'] },
            { sender: 'user', text: '🏷 Продажа' },
            { sender: 'bot', text: '📁 Выберите категорию недвижимости:', buttons: ['🏢 Квартира', '🏡 Дом', '🌾 Участок'] },
            { sender: 'user', text: '🏢 Квартира' },
            { sender: 'bot', text: '📸 Пожалуйста, отправьте фотографию объекта.' },
            { sender: 'user', isMedia: true, text: '🖼️ [Фото квартиры]' },
            { sender: 'bot', text: '🧠 <b>ИИ-Модерация Gemini:</b> Фото успешно проверено. Голая стена/мусор не обнаружены.\n\n✏️ Введите цену в гривнах:' },
            { sender: 'user', text: '1200000' },
            { sender: 'bot', text: '💵 <b>Автоконвертация по курсу НБУ:</b> $30,000.\n\n🚀 Объект успешно добавлен в базу и сохранен в Google Таблицу!' }
        ],
        librarian: [
            { sender: 'user', text: '/start book_12' },
            { sender: 'bot', text: '🔒 <b>Доступ ограничен!</b>\n\nЧтобы бесплатно разблокировать этот файл, вам нужно подписаться на наши полезные каналы.\n\nПожалуйста, подпишитесь на каналы ниже и нажмите кнопку проверки:', buttons: ['📢 Семь сорок | Трейдинг', '🧠 Психология', '🤖 Те что надо | AI', '🔄 Проверить подписку', '⭐️ Забрать за 1 Звезду (без подписки)'] },
            { sender: 'user', text: '⭐️ Забрать за 1 Звезду (без подписки)' },
            { sender: 'bot', text: '💳 Бот выставил счет: <b>Быстрый доступ к книге</b> за 1 Telegram Star (XTR).\nОжидание оплаты...' },
            { sender: 'user', text: '[Оплата успешно проведена 👍]' },
            { sender: 'bot', text: '🎉 <b>Спасибо за поддержку звездами!</b>\nТвой файл успешно разблокирован:\n\n📚 <i>Книга_Маркетинг_ШИ.pdf (4.8 MB)</i>\n\nПриятного чтения! 📖' }
        ]
    },
    en: {
        zapisukha: [
            { sender: 'user', text: '/start' },
            { sender: 'bot', text: '👋 <b>Welcome!</b>\nI will help you book beauty appointments quickly.\n\nChoose a service below 👇', buttons: ['💅 Manicure', '🦶 Pedicure', '🧴 Depilation'] },
            { sender: 'user', text: '💅 Manicure' },
            { sender: 'bot', text: '💅 <b>You selected Manicure ($20).</b>\n\nChoose a convenient day for your visit:', buttons: ['📅 15.06 (Mon)', '📅 16.06 (Tue)', '📅 17.06 (Wed)'] },
            { sender: 'user', text: '📅 15.06 (Mon)' },
            { sender: 'bot', text: '⏰ <b>Choose an available time:</b>', buttons: ['⏰ 10:00 AM', '⏰ 12:00 PM', '⏰ 02:00 PM'] },
            { sender: 'user', text: '⏰ 12:00 PM' },
            { sender: 'bot', text: '📱 Send your phone number to confirm the booking.' },
            { sender: 'user', text: '+380991234567' },
            { sender: 'bot', text: '🎉 <b>Booking Confirmed!</b>\n\n📅 Date: 15.06.2026\n⏰ Time: 12:00 PM\n💅 Service: Manicure\n📍 Location: Salon "Beauty", Shevchenko Str. 128\n\nWe look forward to seeing you! 🌸' }
        ],
        mriya: [
            { sender: 'user', text: '/start' },
            { sender: 'bot', text: '🏠 <b>Welcome to Real Estate CRM!</b>\nI am your digital real estate assistant.\n\nChoose an action:', buttons: ['🔎 Search Properties', '➕ Add Property'] },
            { sender: 'user', text: '➕ Add Property' },
            { sender: 'bot', text: '✏️ Select deal type:', buttons: ['🏷 Sale', '🔑 Rent'] },
            { sender: 'user', text: '🏷 Sale' },
            { sender: 'bot', text: '📁 Select property category:', buttons: ['🏢 Apartment', '🏡 House', '🌾 Land Plot'] },
            { sender: 'user', text: '🏢 Apartment' },
            { sender: 'bot', text: '📸 Please send a photo of the property.' },
            { sender: 'user', isMedia: true, text: '🖼️ [Property Photo]' },
            { sender: 'bot', text: '🧠 <b>AI-Moderation Gemini:</b> Photo successfully verified. Clear walls/no debris detected.\n\nEnter price in UAH:' },
            { sender: 'user', text: '1200000' },
            { sender: 'bot', text: '💵 <b>Exchange rate conversion:</b> $30,000.\n\n🚀 Property successfully added to the database and saved to Google Sheets!' }
        ],
        librarian: [
            { sender: 'user', text: '/start book_12' },
            { sender: 'bot', text: '🔒 <b>Access Restricted!</b>\n\nTo unlock this file for free, you must subscribe to our partner channels.\n\nPlease subscribe to the channels below and click verification:', buttons: ['📢 Seven Forty | Trading', '🧠 Psychology', '🤖 Te Shoo Treba | AI', '🔄 Check Subscription', '⭐️ Get for 1 Star (no subscription)'] },
            { sender: 'user', text: '⭐️ Get for 1 Star (no subscription)' },
            { sender: 'bot', text: '💳 Invoice sent: <b>Instant access to book</b> for 1 Telegram Star (XTR).\nWaiting for payment...' },
            { sender: 'user', text: '[Payment Successful 👍]' },
            { sender: 'bot', text: '🎉 <b>Thank you for supporting us with stars!</b>\nYour file has been successfully unlocked:\n\n📚 <i>Book_Marketing_AI.pdf (4.8 MB)</i>\n\nEnjoy reading! 📖' }
        ]
    }
};

// --- Мультимовний інтерфейс посадкової сторінки ---
const PAGE_TRANSLATIONS = {
    uk: {
        "nav_catalog": "Каталог",
        "nav_demo": "Інтерактивне Демо",
        "nav_pricing": "Тарифи",
        "nav_order": "Замовити",
        "btn_order_bot": "Замовити бота",
        "hero_title": "Telegram-боти та ІИ-рішення, які <span class=\"text-gradient\">працюють на ваш бізнес</span>",
        "hero_desc": "Готові шаблони для автоматизації локальних сервісів з підтримкою автовизначення мови (i18n) та моментальним налаштуванням під будь-яке місто. Заощаджуйте тижні розробки.",
        "hero_btn_catalog": "Дивитися каталог",
        "hero_btn_turnkey": "Замовити під ключ",
        
        "catalog_title": "Готові рішення (Шаблони)",
        "catalog_subtitle": "Всі наші боти розроблені на чистому коді Python з вбудованим автовизначенням мов і легкою зміною налаштувань.",
        
        "prod_market_title": "Барахолка (локальний маркетплейс / аналог OLX / Авіто)",
        "prod_market_desc": "Повноцінна доска оголошень для будь-якого міста (Київ, Берлін, Варшава, Ніжин та ін.). Достатньо змінити одну змінну <code>CITY_NAME</code> в файлі <code>.env</code> — і бот самостійно перебудує бази даних, опис, логіку фільтрів та привітання під вказане місто.",
        "prod_booking_title": "Бот запису клієнтів для б'юті-майстрів",
        "prod_booking_desc": "Автоматизований запис клієнтів на процедури для салонів краси чи майстрів. Автоматичний підбір вільних віконців, знижки для лояльних клієнтів та повна інтеграція з Google Таблицями для зручного перегляду записів.",
        "prod_crm_title": "CRM нерухомості для ріелторів",
        "prod_crm_desc": "Потужний помічник для ріелторів. Дозволяє додавати об'єкти нерухомості з телефону, автоматично перевіряє фото через ШІ Gemini на наявність водяних знаків та сміття, конвертує ціни по курсу НБУ та веде клієнтську базу.",
        "prod_lib_title": "Бібліотекар (Digital Delivery)",
        "prod_lib_desc": "Бот-дистриб'ютор цифрових товарів (книг, мануалів, кодів). Надійно блокує контент та видає його тільки за підписку на цільові канали спонсорів (збільшення аудиторії) або при оплаті через Telegram Stars.",
        "prod_voice_title": "Voice Widget (Desktop App)",
        "prod_voice_desc": "Зручний плаваючий віджет для будь-якого комп'ютера (Windows, macOS, Linux). Дозволяє надиктовувати текст голосом у будь-яке активне текстове поле на ПК. Підтримує підключення будь-яких ШІ-моделей розпізнавання мови.<br><br>💡 <b>Як отримати:</b><br>• Придбати окремо за <b>$1</b><br>• Отримати <b>безкоштовно</b> за підписку на наші канали: <a href='https://t.me/cem_copok' class='text-indigo-400 hover:underline' target='_blank'>Сім сорок</a>, <a href='https://t.me/ncux_olo_guY' class='text-indigo-400 hover:underline' target='_blank'>Психологія</a>, <a href='https://t.me/te_shoo_treba' class='text-indigo-400 hover:underline' target='_blank'>Те що треба</a><br>• Отримати <b>в подарунок</b> при замовленні будь-якого бота «Під ключ»!",
        "btn_voice_gift": "Придбати ($1) / Отримати",
        "btn_voice_buy_1": "Придбати за $1",
        "btn_voice_free": "Отримати безкоштовно",
        "btn_buy_template": "Купити шаблон",
        "btn_order_buy_template": "Замовити / Купити шаблон",
        
        "demo_title": "Спробуйте ботів у дії",
        "demo_subtitle": "Клікніть на вкладку справа та протестуйте сценарій реального діалогу в симуляторі смартфона.",
        "demo_booking_tab_desc": "Симуляція запису клієнта на манікюр із підтвердженням за номером телефону та розрахунком ціни.",
        "demo_crm_tab_desc": "Процес додавання квартири продавцем з автоматичною модерацією фото через Gemini та валютною автоконвертацією.",
        "demo_lib_tab_desc": "Воронка підписки на канали спонсорів або миттєва купівля книги за Telegram Stars (зірки).",
        
        "pricing_title": "Гнучкі тарифи під ваші цілі",
        "pricing_subtitle": "Оберіть рівень автоматизації, який найкраще підходить для вашого проекту чи бізнесу.",
        
        "price_self_title": "Тариф «Шаблон»",
        "price_self_desc": "Отримайте чистий вихідний код бота з детальними інструкціями для самостійного налаштування. Підходить для розробників.",
        "price_self_price_val": "$49",
        "price_turnkey_title": "Тариф «Під ключ»",
        "badge_popular": "Популярний",
        "price_turnkey_desc": "Ми повністю налаштуємо бота під ваші вимоги, зареєструємо його на серверах Railway чи VPS, приєднаємо ваші API ключі та Google Таблиці.",
        "price_turnkey_price_val": "$149",
        "price_sub_title": "Тариф «Обслуговування»",
        "price_sub_desc": "Повний супровід вашого бота (хостинг, моніторинг логів, оновлення). Тариф: $15/міс. При передплаті на 3 місяці — $12/міс, на 6 місяців (і більше) — $10/міс.",
        "price_sub_price_val": "$15",
        "price_once": "/ одноразово",
        "price_monthly": "/ місяць",
        "price_turnkey_btn": "Замовити під ключ",
        "price_sub_btn": "Підписатися",
        
        "pricing_li_code": "Повний вихідний код (Clean Python)",
        "pricing_li_db": "Шаблон бази Google Sheets / SQLite",
        "pricing_li_i18n": "Мультиязичність та локалізація",
        "pricing_li_no_setup": "Налаштування API та серверів",
        "pricing_li_all_template": "Усе з тарифу «Шаблон»",
        "pricing_li_deploy": "Деплой бота на сервер хостингу",
        "pricing_li_api": "Приєднання API (Gemini/Groq)",
        "pricing_li_google_api": "Налаштування Google Service Account",
        "pricing_li_voice_gift": "🎁 ПОДАРУНОК: Voice Widget у комплекті!",
        "pricing_li_free_month": "🔥 1-й місяць обслуговування БЕЗКОШТОВНО!",
        "pricing_li_hosting": "Хостинг бота в хмарі включено",
        "pricing_li_updates": "Оновлення коду під зміни API Telegram",
        "pricing_li_monitoring": "Щоденний моніторинг логів та багів",
        "pricing_li_support": "24/7 технічна підтримка",
        
        "contact_title": "Залишити заявку",
        "contact_subtitle": "Заповніть форму, і ми зв'яжемося з вами в Telegram протягом 30 хвилин.",
        "form_name_label": "Ваше ім'я",
        "form_tg_label": "Username у Telegram",
        "form_bot_label": "Який бот вас цікавить?",
        "form_tariff_label": "Оберіть тариф",
        "form_submit": "Надіслати запит",
        
        "form_success": "Дякуємо! Ваша заявка успішно надіслана. Ми зв'яжемося з вами в Telegram найближчим часом.",
        "menu_alert": "Меню розробляється. Використовуйте прокручування сторінки.",
        "footer_copy": "© 2026 Nova Bots. Створено з розумом.",
        "footer_privacy": "Конфіденційність",
        "footer_terms": "Умови",
        "footer_contact": "Контакти",
        "pricing_payment_methods": "Приймаємо до оплати: Visa/Mastercard (через Банку Mono), Криптовалюту (USDT, USDC) та Telegram Stars ⭐️",
        "btn_pay_stars": "Сплатити зірками",
        "btn_pay_card": "Сплатити карткою",
        "btn_pay_crypto": "Сплатити USDT / USDC",
        "pay_modal_title": "Оплата замовлення",
        "pay_modal_subtitle": "Оберіть зручний спосіб оплати нижче. Після транзакції надішліть скріншот підтримці.",
        "pay_order_details": "Обраний тариф",
        "pay_amount": "Сума",
        "pay_method_crypto": "Криптовалюта",
        "pay_method_card": "Банківська карта",
        "pay_wallet_addr": "Адреса гаманця для оплати",
        "pay_copy": "Копіювати",
        "pay_copied": "Скопійовано!",
        "pay_network_warning_both": "Надсилайте ТІЛЬКИ <b>USDT</b> у мережі <b>TRC-20</b> або <b>USDC</b> у мережі <b>ERC-20</b>! Будь-яка інша мережа призведе до безповоротної втрати коштів.",
        "pay_card_num": "Номер картки Банки",
        "pay_card_holder": "Банк / Отримувач",
        "pay_card_holder_val": "Monobank (Банка: Nova Bots | Оплата)",
        "pay_card_direct_btn": "Сплатити онлайн (Apple Pay / Google Pay / Карта)",
        "pay_card_note": "Будь ласка, переказуйте точну суму. Зарахування відбудеться автоматично після підтвердження від менеджера.",
        "pay_confirm_btn": "Я сплатив (Підтвердити в Telegram)"
    },
    ru: {
        "nav_catalog": "Каталог",
        "nav_demo": "Интерактивное Демо",
        "nav_pricing": "Тарифы",
        "nav_order": "Заказать",
        "btn_order_bot": "Заказать бота",
        "hero_title": "Telegram-боты и ИИ-решения, которые <span class=\"text-gradient\">работают на ваш бизнес</span>",
        "hero_desc": "Готовые шаблоны для автоматизации локальных сервисов с поддержкой автоопределения языка (i18n) и моментальной настройкой под любой город. Экономьте недели разработки.",
        "hero_btn_catalog": "Смотреть каталог",
        "hero_btn_turnkey": "Заказать под ключ",
        
        "catalog_title": "Готовые решения (Шаблоны)",
        "catalog_subtitle": "Все наши боты разработаны на чистом коде Python со встроенным автоопределением языков и легкой сменой настроек.",
        
        "prod_market_title": "Барахолка (локальный маркетплейс / аналог OLX / Авито)",
        "prod_market_desc": "Полноценная доска объявлений для любого города (Киев, Берлин, Варшава, Нежин и др.). Достаточно изменить одну переменную <code>CITY_NAME</code> в файле <code>.env</code> — и бот самостоятельно перестроит базы данных, описание, логику фильтров и приветствие под указанный город.",
        "prod_booking_title": "Бот записи клиентов для бьюти-мастеров",
        "prod_booking_desc": "Автоматизированная запись клиентов на процедуры для салонов красоты или мастеров. Автоматический подбор свободных окошек, скидки для лояльных клиентов и полная интеграция с Google Таблицами для удобного просмотра записей.",
        "prod_crm_title": "CRM недвижимости для риелторов",
        "prod_crm_desc": "Мощный помощник для риелторов. Позволяет добавлять объекты недвижимости с телефона, автоматически проверяет фото через ИИ Gemini на наличие водяных знаков и мусора, конвертирует цены по курсу НБУ и ведет клиентскую базу.",
        "prod_lib_title": "Библиотекарь (Digital Delivery)",
        "prod_lib_desc": "Бот-дистрибьютор цифровых товаров (книг, мануалов, кодов). Надежно блокирует контент и выдает его только за подписку на целевые каналы спонсоров (увеличение аудитории) или при оплате через Telegram Stars.",
        "prod_voice_title": "Voice Widget (Desktop App)",
        "prod_voice_desc": "Удобный плавающий виджет для любого компьютера (Windows, macOS, Linux). Позволяет надиктовывать текст голосом в любое активное текстовое поле на ПК. Поддерживает подключение любых ИИ-моделей распознавания речи.<br><br>💡 <b>Как получить:</b><br>• Купить отдельно за <b>$1</b><br>• Получить <b>бесплатно</b> за подписку на наши каналы: <a href='https://t.me/cem_copok' class='text-indigo-400 hover:underline' target='_blank'>Семь сорок</a>, <a href='https://t.me/ncux_olo_guY' class='text-indigo-400 hover:underline' target='_blank'>Психология</a>, <a href='https://t.me/te_shoo_treba' class='text-indigo-400 hover:underline' target='_blank'>Те что надо</a><br>• Получить <b>в подарок</b> при заказе любого бота «Под ключ»!",
        "btn_voice_gift": "Купить ($1) / Получить",
        "btn_voice_buy_1": "Купить за $1",
        "btn_voice_free": "Получить бесплатно",
        "btn_buy_template": "Купить шаблон",
        "btn_order_buy_template": "Заказать / Купить шаблон",
        
        "demo_title": "Попробуйте ботов в действии",
        "demo_subtitle": "Кликните на вкладку справа и протестируйте сценарий реального диалога в симуляторе смартфона.",
        "demo_booking_tab_desc": "Симуляция записи клиента на маникюр с подтверждением по номеру телефона и расчетом цены.",
        "demo_crm_tab_desc": "Процесс добавления квартиры продавцом с автоматической модерацией фото через Gemini и валютной автоконвертацией.",
        "demo_lib_tab_desc": "Воронка подписки на каналы спонсоров или моментальная покупка книги за Telegram Stars (звезды).",
        
        "pricing_title": "Гибкие тарифы под ваши цели",
        "pricing_subtitle": "Выберите подходящий уровень автоматизации для вашего проекта или бизнеса.",
        
        "price_self_title": "Тариф «Шаблон»",
        "price_self_desc": "Получите чистый исходный код бота с подробными инструкциями для самостоятельной настройки. Подходит для разработчиков.",
        "price_self_price_val": "$49",
        "price_turnkey_title": "Тариф «Под ключ»",
        "badge_popular": "Популярный",
        "price_turnkey_desc": "Мы полностью настроем бота под ваши требования, зарегистрируем его на серверах Railway или VPS, подключим ваши API ключи и Google Таблицы.",
        "price_turnkey_price_val": "$149",
        "price_sub_title": "Тариф «Обслуживание»",
        "price_sub_desc": "Полное сопровождение вашего бота (хостинг, мониторинг логов, обновления). Тариф: $15/мес. При подписке на 3 месяца — $12/мес, на 6 месяцев (и более) — $10/мес.",
        "price_sub_price_val": "$15",
        "price_once": "/ единоразово",
        "price_monthly": "/ месяц",
        "price_turnkey_btn": "Заказать под ключ",
        "price_sub_btn": "Подписаться",
        
        "pricing_li_code": "Полный исходный код (Clean Python)",
        "pricing_li_db": "Шаблон базы Google Sheets / SQLite",
        "pricing_li_i18n": "Мультиязычность и локализация",
        "pricing_li_no_setup": "Настройка API и серверов",
        "pricing_li_all_template": "Всё из тарифа «Шаблон»",
        "pricing_li_deploy": "Деплой бота на сервер хостинга",
        "pricing_li_api": "Подключение API (Gemini/Groq)",
        "pricing_li_google_api": "Настройка Google Service Account",
        "pricing_li_voice_gift": "🎁 ПОДАРОК: Voice Widget в комплекте!",
        "pricing_li_free_month": "🔥 1-й месяц обслуживания БЕСПЛАТНО!",
        "pricing_li_hosting": "Hosting бота в облаке включен",
        "pricing_li_updates": "Обновление кода под изменения API Telegram",
        "pricing_li_monitoring": "Ежедневный мониторинг логов и багов",
        "pricing_li_support": "24/7 техническая поддержка",
        
        "contact_title": "Оставить заявку",
        "contact_subtitle": "Заполните форму, и мы свяжемся с вами в Telegram в течение 30 минут.",
        "form_name_label": "Ваше имя",
        "form_tg_label": "Username в Telegram",
        "form_bot_label": "Какой бот вас интересует?",
        "form_tariff_label": "Выберите тариф",
        "form_submit": "Отправить запрос",
        
        "form_success": "Спасибо! Ваша заявка успешно отправлена. Мы свяжемся с вами в Telegram в ближайшее время.",
        "menu_alert": "Меню разрабатывается. Используйте прокрутку страницы.",
        "footer_copy": "© 2026 Nova Bots. Создано с умом.",
        "footer_privacy": "Конфиденциальность",
        "footer_terms": "Условия",
        "footer_contact": "Контакты",
        "pricing_payment_methods": "Принимаем к оплате: Visa/Mastercard (через Банку Mono), Криптовалюту (USDT, USDC) и Telegram Stars ⭐️",
        "btn_pay_stars": "Оплатить звездами",
        "btn_pay_card": "Оплатить картой",
        "btn_pay_crypto": "Оплатить USDT / USDC",
        "pay_modal_title": "Оплата заказа",
        "pay_modal_subtitle": "Выберите удобный способ оплаты ниже. После транзакции отправьте скриншот поддержке.",
        "pay_order_details": "Выбранный тариф",
        "pay_amount": "Сумма",
        "pay_method_crypto": "Криптовалюта",
        "pay_method_card": "Банковская карта",
        "pay_wallet_addr": "Адрес кошелька для оплаты",
        "pay_copy": "Копировать",
        "pay_copied": "Скопировано!",
        "pay_network_warning_both": "Отправляйте ТОЛЬКО <b>USDT</b> в сети <b>TRC-20</b> или <b>USDC</b> в сети <b>ERC-20</b>! Любая другая сеть приведет к безвозвратной потере средств.",
        "pay_card_num": "Номер карты Банки",
        "pay_card_holder": "Банк / Получатель",
        "pay_card_holder_val": "Monobank (Банка: Nova Bots | Оплата)",
        "pay_card_direct_btn": "Оплатить онлайн (Apple Pay / Google Pay / Карта)",
        "pay_card_note": "Пожалуйста, переводите точную сумму. Зачисление произойдет автоматически после подтверждения менеджером.",
        "pay_confirm_btn": "Я оплатил (Подтвердить в Telegram)"
    },
    en: {
        "nav_catalog": "Catalog",
        "nav_demo": "Interactive Demo",
        "nav_pricing": "Pricing",
        "nav_order": "Order",
        "btn_order_bot": "Order Bot",
        "hero_title": "Telegram bots and AI solutions that <span class=\"text-gradient\">work for your business</span>",
        "hero_desc": "Ready-to-use templates for automation of local services with built-in language detection (i18n) and instant white-label customisation. Save weeks of development.",
        "hero_btn_catalog": "Browse Catalog",
        "hero_btn_turnkey": "Turnkey Installation",
        
        "catalog_title": "Ready Solutions (Templates)",
        "catalog_subtitle": "All our bots are written in clean Python, featuring automatic language detection and easy customisation.",
        
        "prod_market_title": "Flea Market (local marketplace / OLX or Craigslist analog)",
        "prod_market_desc": "Fully autonomous classifieds board for any city. AI image moderation via Google Gemini, voice message transcription via Groq Whisper, weekly listing limits, multi-level referrals, and unlimited posting plans purchased via Telegram Stars.",
        "prod_booking_title": "Beauty Appointment Booking Bot",
        "prod_booking_desc": "A complete booking assistant for beauty salons and individual masters. Two-week calendar shift selection (Salon/Home 2/2 cycle), real-time free time slot picker, automatic discount promos for returning users, and active Google Sheets sync.",
        "prod_crm_title": "Real Estate CRM for Brokers",
        "prod_crm_desc": "Automated property listing upload (apartments, houses, land plots) directly from sellers. AI photo moderation, automatic currency exchange conversion (UAH/USD), and active database export directly to Google Sheets for managers.",
        "prod_lib_title": "Librarian (Digital Product File Delivery Bot)",
        "prod_lib_desc": "Lead generation bot and sales funnel. Protects digital download links for books or files. Users get the file for free after subscribing to partner sponsor channels or can purchase it instantly via 1-2 Telegram Stars.",
        "prod_voice_title": "Voice Widget (Desktop App)",
        "prod_voice_desc": "Convenient floating widget for any desktop system (Windows, macOS, Linux). Dictate text with your voice into any active text field on your computer. Supports integration with any speech-to-text models.<br><br>💡 <b>How to get:</b><br>• Purchase separately for <b>$1</b><br>• Get for <b>free</b> by subscribing to our channels: <a href='https://t.me/cem_copok' class='text-indigo-400 hover:underline' target='_blank'>Seven Forty</a>, <a href='https://t.me/ncux_olo_guY' class='text-indigo-400 hover:underline' target='_blank'>Psychology</a>, <a href='https://t.me/te_shoo_treba' class='text-indigo-400 hover:underline' target='_blank'>Te Shoo Treba</a><br>• Get as a <b>gift</b> when ordering any 'Turnkey' bot!",
        "btn_voice_gift": "Buy ($1) / Get Free",
        "btn_voice_buy_1": "Buy for $1",
        "btn_voice_free": "Get for Free",
        "btn_buy_template": "Buy Template",
        "btn_order_buy_template": "Buy / Order Template",
        
        "demo_title": "Try Bots In Action",
        "demo_subtitle": "Click a tab on the right and test the interactive chat simulator inside the smartphone mockup.",
        "demo_booking_tab_desc": "Simulation of beauty appointment slot booking, with phone validation and receipt calculation.",
        "demo_crm_tab_desc": "Property upload scenario featuring Gemini image validation and exchange rate calculations.",
        "demo_lib_tab_desc": "Funnel showing channel subscription verification and instant file delivery via Telegram Stars.",
        
        "pricing_title": "Flexible Plans For Your Needs",
        "pricing_subtitle": "Choose the most suitable launch and customization option for your project.",
        
        "price_self_title": "Template License",
        "price_self_desc": "Get clean Python source code, table schemas, and deployment checklists. Best for developers.",
        "price_self_price_val": "$49",
        "price_turnkey_title": "Turnkey Launch",
        "badge_popular": "Popular",
        "price_turnkey_desc": "We configure databases, register Google API service keys, set up config parameters, and deploy to Railway/VPS.",
        "price_turnkey_price_val": "$149",
        "price_sub_title": "Active Maintenance",
        "price_sub_desc": "Complete maintenance of your bot (hosting, log monitoring, and updates). Plan: $15/mo. Save with 3 months — $12/mo, or 6+ months — $10/mo.",
        "price_sub_price_val": "$15",
        "price_once": "/ one-time",
        "price_monthly": "/ month",
        "price_turnkey_btn": "Order Turnkey Setup",
        "price_sub_btn": "Subscribe Now",
        
        "pricing_li_code": "Full clean Python source code",
        "pricing_li_db": "Google Sheets / SQLite schemas",
        "pricing_li_i18n": "Multilingual UI out-of-the-box",
        "pricing_li_no_setup": "Manual API & server deployment",
        "pricing_li_all_template": "Everything from 'Template' plan",
        "pricing_li_deploy": "Active deployment to cloud server",
        "pricing_li_api": "Gemini & Groq API key bindings",
        "pricing_li_google_api": "Google Cloud Service Account setup",
        "pricing_li_voice_gift": "🎁 GIFT: Voice Widget included!",
        "pricing_li_free_month": "🔥 1st month of maintenance for FREE!",
        "pricing_li_hosting": "Cloud hosting costs included",
        "pricing_li_updates": "Proactive API adaptation updates",
        "pricing_li_monitoring": "Daily log monitoring & bugfixes",
        "pricing_li_support": "24/7 dedicated support desk",
        
        "contact_title": "Request Setup",
        "contact_subtitle": "Fill out the questionnaire and our team will get in touch in Telegram within 30 minutes.",
        "form_name_label": "Your Name",
        "form_tg_label": "Telegram @username",
        "form_bot_label": "Choose Bot Solution",
        "form_tariff_label": "Choose Deployment Plan",
        "form_submit": "Submit Order",
        
        "form_success": "Thank you! Your request has been successfully submitted. We will contact you in Telegram shortly.",
        "menu_alert": "Menu is under construction. Please scroll the page.",
        "footer_copy": "© 2026 Nova Bots. Built with intelligence.",
        "footer_privacy": "Privacy Policy",
        "footer_terms": "Terms & Conditions",
        "footer_contact": "Contacts",
        "pricing_payment_methods": "We accept: Visa/Mastercard (via Mono Jar), Cryptocurrencies (USDT, USDC) & Telegram Stars ⭐️",
        "btn_pay_stars": "Pay with Stars",
        "btn_pay_card": "Pay by Card",
        "btn_pay_crypto": "Pay with USDT / USDC",
        "pay_modal_title": "Order Payment",
        "pay_modal_subtitle": "Choose a convenient payment method below. Send a screenshot to support after transaction.",
        "pay_order_details": "Selected Plan",
        "pay_amount": "Amount",
        "pay_method_crypto": "Cryptocurrency",
        "pay_method_card": "Credit Card",
        "pay_wallet_addr": "Wallet Address for Payment",
        "pay_copy": "Copy",
        "pay_copied": "Copied!",
        "pay_network_warning_both": "Send ONLY <b>USDT</b> on <b>TRC-20</b> network or <b>USDC</b> on <b>ERC-20</b> network! Any other network will result in permanent loss of funds.",
        "pay_card_num": "Jar Card Number",
        "pay_card_holder": "Bank / Recipient",
        "pay_card_holder_val": "Monobank (Jar: Nova Bots | Payment)",
        "pay_card_direct_btn": "Pay Online (Apple Pay / Google Pay / Card)",
        "pay_card_note": "Please transfer the exact amount. Verification will complete automatically once approved by our manager.",
        "pay_confirm_btn": "I have paid (Confirm in Telegram)"
    }
};

// --- Simulator Session State variables for dynamic interactive branching ---
let currentLang = 'uk';
let currentBot = 'zapisukha';
let currentStep = 0;
let isAnimating = false;

// Dynamic selection session choices
let bookingService = 'manicure'; // manicure, pedicure, depilation
let bookingDay = '';
let bookingTime = '';
let realEstateType = 'sale';     // sale, rent
let propertyCategory = 'apartment'; // apartment, house, land

function getLocalizedServiceName(service, lang) {
    const data = {
        manicure: { uk: 'Манікюр', ru: 'Маникюр', en: 'Manicure' },
        pedicure: { uk: 'Педикюр', ru: 'Педикюр', en: 'Pedicure' },
        depilation: { uk: 'Депіляція', ru: 'Депиляция', en: 'Depilation' }
    };
    return data[service] ? data[service][lang] : '';
}

function getLocalizedServicePrice(service, lang) {
    const data = {
        manicure: { uk: '580 грн', ru: '580 грн', en: '$20' },
        pedicure: { uk: '550 грн', ru: '550 грн', en: '$18' },
        depilation: { uk: '200 грн', ru: '200 грн', en: '$8' }
    };
    return data[service] ? data[service][lang] : '';
}

function getLocalizedServiceIcon(service) {
    const data = {
        manicure: '💅',
        pedicure: '🦶',
        depilation: '🧴'
    };
    return data[service] || '💅';
}

function formatSimulatorMessage(text) {
    if (!text) return text;
    
    // Day and time defaults
    const displayDay = bookingDay || (currentLang === 'en' ? '15.06 (Mon)' : '15.06 (Пн)');
    const displayTime = bookingTime || (currentLang === 'en' ? '12:00 PM' : '12:00');
    
    // Zapisukha replacement logic
    if (currentBot === 'zapisukha') {
        const serviceName = getLocalizedServiceName(bookingService, currentLang);
        const servicePrice = getLocalizedServicePrice(bookingService, currentLang);
        const serviceIcon = getLocalizedServiceIcon(bookingService);
        
        text = text.replace(/Манікюр/g, serviceName)
                   .replace(/Маникюр/g, serviceName)
                   .replace(/Manicure/g, serviceName)
                   .replace(/580 грн/g, servicePrice)
                   .replace(/\$20/g, servicePrice)
                   .replace(/💅/g, serviceIcon)
                   .replace(/15\.06 \(Пн\)/g, displayDay)
                   .replace(/15\.06 \(Mon\)/g, displayDay)
                   .replace(/12:00/g, displayTime)
                   .replace(/12:00 PM/g, displayTime);
    }
    
    // Mriya CRM replacement logic
    if (currentBot === 'mriya') {
        const typeName = realEstateType === 'rent'
            ? (currentLang === 'uk' ? 'Оренда' : currentLang === 'ru' ? 'Аренда' : 'Rent')
            : (currentLang === 'uk' ? 'Продаж' : currentLang === 'ru' ? 'Продажа' : 'Sale');
            
        const catName = propertyCategory === 'house'
            ? (currentLang === 'uk' ? 'Будинок' : currentLang === 'ru' ? 'Дом' : 'House')
            : propertyCategory === 'land'
            ? (currentLang === 'uk' ? 'Земельну ділянку' : currentLang === 'ru' ? 'Земельный участок' : 'Land Plot')
            : (currentLang === 'uk' ? 'Квартира' : currentLang === 'ru' ? 'Квартиру' : 'Apartment');

        const catNameNominative = propertyCategory === 'house'
            ? (currentLang === 'uk' ? 'Будинок' : currentLang === 'ru' ? 'Дом' : 'House')
            : propertyCategory === 'land'
            ? (currentLang === 'uk' ? 'Ділянка' : currentLang === 'ru' ? 'Участок' : 'Land Plot')
            : (currentLang === 'uk' ? 'Квартира' : currentLang === 'ru' ? 'Квартира' : 'Apartment');

        const displayPrice = realEstateType === 'rent'
            ? '12000'
            : '1200000';
            
        const displayUSD = realEstateType === 'rent'
            ? (currentLang === 'uk' ? '$300/міс.' : currentLang === 'ru' ? '$300/мес.' : '$300/mo.')
            : (currentLang === 'uk' ? '$30,000' : currentLang === 'ru' ? '$30,000' : '$30,000');

        text = text.replace(/Продаж/g, typeName)
                   .replace(/Продажа/g, typeName)
                   .replace(/Sale/g, typeName)
                   .replace(/Квартира/g, catName)
                   .replace(/Квартиру/g, catName)
                   .replace(/Apartment/g, catName)
                   .replace(/квартира/gi, catName.toLowerCase())
                   .replace(/квартиру/gi, catName.toLowerCase())
                   .replace(/apartment/gi, catName.toLowerCase())
                   .replace(/\[Фото квартири\]/g, `[Фото ${catNameNominative.toLowerCase()}]`)
                   .replace(/\[Фото квартиры\]/g, `[Фото ${catNameNominative.toLowerCase()}]`)
                   .replace(/\[Property Photo\]/g, `[${catNameNominative} Photo]`)
                   .replace(/1200000/g, displayPrice)
                   .replace(/\$30,000/g, displayUSD);

        // Adjust conversion message
        if (text.includes('Автоконвертація по курсу НБУ') || text.includes('Автоконвертация по курсу НБУ') || text.includes('Exchange rate conversion')) {
            text = currentLang === 'uk'
                ? `💵 <b>Автоконвертація по курсу НБУ:</b> ${displayUSD}.\n\n🚀 Об'єкт успішно додано до бази та збережено у Google Таблиці!`
                : currentLang === 'ru'
                ? `💵 <b>Автоконвертация по курсу НБУ:</b> ${displayUSD}.\n\n🚀 Объект успешно добавлен в базу и сохранен в Google Таблицу!`
                : `💵 <b>Exchange rate conversion:</b> ${displayUSD}.\n\n🚀 Property successfully added to the database and saved to Google Sheets!`;
        }

        // Adjust Gemini AI moderation message
        if (text.includes('Gemini:')) {
            text = currentLang === 'uk'
                ? `🧠 <b>ШІ-Модерація Gemini:</b> Фото успішно перевірено. Гола стіна/сміття не виявлені. Бот розпізнав об'єкт як <b>${catNameNominative}</b>.\n\n✏️ Введіть ціну в гривнях:`
                : currentLang === 'ru'
                ? `🧠 <b>ИИ-Модерация Gemini:</b> Фото успешно проверено. Голая стена/мусор не обнаружены. Бот распознал объект как <b>${catNameNominative}</b>.\n\n✏️ Введите цену в гривнах:`
                : `🧠 <b>AI-Moderation Gemini:</b> Photo successfully verified. Clear walls/no debris detected. Bot recognized the property as <b>${catNameNominative}</b>.\n\nEnter price in UAH:`;
        }
    }
    return text;
}

function renderMessage(msg) {
    const chatContainer = document.getElementById('chat-container');
    const msgElement = document.createElement('div');
    
    msgElement.className = `flex flex-col mb-3 animate-[fadeIn_0.3s_ease-out] ${msg.sender === 'user' ? 'items-end' : 'items-start'}`;
    
    // Formatted message content using dynamic choices
    let displayTemplate = formatSimulatorMessage(msg.text);
    
    let contentHtml = '';
    if (msg.isMedia) {
        contentHtml = `
            <div class="bg-zinc-800 rounded-2xl p-2 max-w-[80%] border border-zinc-700">
                <div class="w-48 h-32 bg-zinc-700 rounded-xl flex items-center justify-center text-zinc-500 mb-1">
                    <span class="material-symbols-outlined text-4xl">image</span>
                </div>
                <span class="text-xs text-zinc-400 block px-1">${displayTemplate}</span>
            </div>
        `;
    } else {
        const bgClass = msg.sender === 'user' 
            ? 'bg-gradient-to-r from-indigo-500 to-violet-500 text-white rounded-2xl rounded-tr-sm' 
            : 'bg-zinc-800 text-zinc-200 rounded-2xl rounded-tl-sm border border-zinc-700';
        contentHtml = `
            <div class="${bgClass} px-4 py-2.5 max-w-[85%] text-sm shadow-md leading-relaxed">
                ${displayTemplate}
            </div>
        `;
    }
    
    msgElement.innerHTML = contentHtml;
    chatContainer.appendChild(msgElement);
    
    // Render Keyboard buttons if present
    const keyboardContainer = document.getElementById('chat-keyboard');
    keyboardContainer.innerHTML = '';
    
    if (msg.buttons && msg.buttons.length > 0) {
        const gridClass = msg.buttons.length > 2 ? 'grid-cols-2' : 'grid-cols-1';
        const kbElement = document.createElement('div');
        kbElement.className = `grid ${gridClass} gap-2 w-full mt-2 animate-[fadeIn_0.4s_ease-out]`;
        
        msg.buttons.forEach(btnText => {
            const btn = document.createElement('button');
            btn.className = "bg-zinc-800 hover:bg-zinc-700 text-zinc-200 border border-zinc-700 py-2.5 px-4 rounded-xl text-xs font-medium transition-all text-center truncate shadow-sm active:scale-95";
            btn.innerHTML = btnText;
            btn.onclick = () => {
                if (isAnimating) return;
                
                // Track user selection choices dynamically to handle branches
                const lowerText = btnText.toLowerCase();
                if (lowerText.includes('педикюр') || lowerText.includes('pedicure')) {
                    bookingService = 'pedicure';
                } else if (lowerText.includes('депіляція') || lowerText.includes('depilation') || lowerText.includes('депиляция')) {
                    bookingService = 'depilation';
                } else if (lowerText.includes('манікюр') || lowerText.includes('manicure') || lowerText.includes('маникюр')) {
                    bookingService = 'manicure';
                } else if (lowerText.includes('оренда') || lowerText.includes('rent') || lowerText.includes('аренда')) {
                    realEstateType = 'rent';
                } else if (lowerText.includes('продаж') || lowerText.includes('sale') || lowerText.includes('продажа')) {
                    realEstateType = 'sale';
                } else if (lowerText.includes('будинок') || lowerText.includes('house') || lowerText.includes('дом')) {
                    propertyCategory = 'house';
                } else if (lowerText.includes('ділянка') || lowerText.includes('land') || lowerText.includes('участок')) {
                    propertyCategory = 'land';
                } else if (lowerText.includes('квартира') || lowerText.includes('apartment')) {
                    propertyCategory = 'apartment';
                }
                
                // Capture day selection
                if (btnText.includes('📅')) {
                    bookingDay = btnText.replace('📅', '').trim();
                }
                // Capture time selection
                if (btnText.includes('⏰')) {
                    bookingTime = btnText.replace('⏰', '').trim();
                }
                
                simulateNextStep(btnText);
            };
            kbElement.appendChild(btn);
        });
        keyboardContainer.appendChild(kbElement);
    }
    
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

function simulateNextStep(clickedText) {
    const scenario = BOT_SCENARIOS[currentLang][currentBot];
    if (currentStep >= scenario.length || isAnimating) return;
    
    isAnimating = true;
    
    // 1. Render user message (displaying clicked button text if available)
    const userMsg = Object.assign({}, scenario[currentStep]);
    if (clickedText) {
        userMsg.text = clickedText;
    }
    renderMessage(userMsg);
    currentStep++;
    
    // 2. Render bot reply after delay
    setTimeout(() => {
        if (currentStep < scenario.length) {
            const botMsg = Object.assign({}, scenario[currentStep]);
            
            // Show typing indicator
            const chatContainer = document.getElementById('chat-container');
            const typingIndicator = document.createElement('div');
            typingIndicator.id = 'typing-indicator';
            typingIndicator.className = 'flex items-center gap-1 bg-zinc-800 border border-zinc-700 px-4 py-3 rounded-2xl rounded-tl-sm w-16 mb-3 self-start animate-pulse';
            typingIndicator.innerHTML = '<span class="w-1.5 h-1.5 bg-zinc-500 rounded-full animate-bounce"></span><span class="w-1.5 h-1.5 bg-zinc-500 rounded-full animate-bounce" style="animation-delay:0.2s"></span><span class="w-1.5 h-1.5 bg-zinc-500 rounded-full animate-bounce" style="animation-delay:0.4s"></span>';
            chatContainer.appendChild(typingIndicator);
            chatContainer.scrollTop = chatContainer.scrollHeight;
            
            setTimeout(() => {
                const indicator = document.getElementById('typing-indicator');
                if (indicator) indicator.remove();
                
                renderMessage(botMsg);
                currentStep++;
                isAnimating = false;
                
                // If the next step doesn't require button input, auto-trigger it after 1.5s
                if (currentStep < scenario.length && scenario[currentStep].sender === 'user' && !botMsg.buttons) {
                    setTimeout(simulateNextStep, 1500);
                }
            }, 1200);
        } else {
            isAnimating = false;
        }
    }, 800);
}

function startScenario(botName) {
    currentBot = botName;
    currentStep = 0;
    isAnimating = false;
    
    // Reset session choices
    bookingService = 'manicure';
    bookingDay = '';
    bookingTime = '';
    realEstateType = 'sale';
    propertyCategory = 'apartment';
    
    // Update Header UI based on currentBot and currentLang
    const headerTitle = document.getElementById('phone-header-title');
    const headerStatus = document.getElementById('phone-header-status');
    const names = {
        uk: {
            zapisukha: { title: 'Бот запису 💅', status: 'бот автозапису' },
            mriya: { title: 'CRM нерухомості 🏠', status: 'для ріелторів' },
            librarian: { title: 'Бібліотекар 📚', status: 'видача файлів' }
        },
        ru: {
            zapisukha: { title: 'Бот записи 💅', status: 'бот автозаписи' },
            mriya: { title: 'CRM недвижимости 🏠', status: 'для риелторов' },
            librarian: { title: 'Библиотекарь 📚', status: 'выдача файлов' }
        },
        en: {
            zapisukha: { title: 'Booking Bot 💅', status: 'beauty masters' },
            mriya: { title: 'Real Estate CRM 🏠', status: 'for brokers' },
            librarian: { title: 'Librarian 📚', status: 'file delivery' }
        }
    };
    
    headerTitle.innerText = names[currentLang][botName].title;
    headerStatus.innerText = names[currentLang][botName].status;
    
    // Clear chat
    document.getElementById('chat-container').innerHTML = '';
    document.getElementById('chat-keyboard').innerHTML = '';
    
    // Update Tabs UI
    document.querySelectorAll('.demo-tab').forEach(tab => {
        if (tab.dataset.bot === botName) {
            tab.classList.add('border-indigo-500', 'text-white', 'bg-indigo-500/10');
            tab.classList.remove('border-zinc-800', 'text-zinc-400');
        } else {
            tab.classList.remove('border-indigo-500', 'text-white', 'bg-indigo-500/10');
            tab.classList.add('border-zinc-800', 'text-zinc-400');
        }
    });
    
    // Run first step (user /start)
    simulateNextStep();
}

// Translate landing page UI text components
function updatePageTranslations(langCode) {
    const texts = PAGE_TRANSLATIONS[langCode];
    if (!texts) return;
    
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        const translation = texts[key];
        if (translation) {
            if (el.tagName === 'INPUT' || el.tagName === 'TEXTAREA') {
                el.placeholder = translation;
            } else if (el.tagName === 'SELECT') {
                // Ignore select tag text directly
            } else {
                el.innerHTML = translation;
            }
        }
    });
}

function setLanguage(langCode) {
    if (currentLang === langCode) return;
    
    currentLang = langCode;
    
    // Update dropdown button text
    const langBtnText = document.querySelector('header button span.font-label-sm');
    if (langBtnText) {
        langBtnText.innerText = langCode.toUpperCase();
    }
    
    // Update Landing page interface texts
    updatePageTranslations(langCode);
    
    // Reload active scenario in new language
    startScenario(currentBot);
}

// Global initialization
document.addEventListener('DOMContentLoaded', () => {
    // Connect selector tabs
    document.querySelectorAll('.demo-tab').forEach(tab => {
        tab.onclick = () => {
            if (isAnimating) return;
            startScenario(tab.dataset.bot);
        };
    });
    
    // Connect language selectors
    document.querySelectorAll('.lang-select').forEach(link => {
        link.onclick = (e) => {
            e.preventDefault();
            const langCode = link.dataset.lang;
            setLanguage(langCode);
            
            // Visual highlight of active lang in dropdown
            document.querySelectorAll('.lang-select').forEach(el => {
                el.className = "flex items-center px-4 py-2 text-xs text-zinc-400 hover:text-white hover:bg-white/5 transition-colors lang-select";
            });
            link.className = "flex items-center px-4 py-2 text-xs text-white bg-indigo-500/20 hover:bg-indigo-500/30 transition-colors lang-select";
        };
    });
    
    // Start default scenario
    startScenario('zapisukha');

    const clientBotSelect = document.getElementById('client-bot');
    const clientTierSelect = document.getElementById('client-tier');
    const btnPayStars = document.getElementById('btn-pay-stars');
    const labelPayStars = document.getElementById('label-pay-stars');

    const botNamesTrans = {
        barakholka: { uk: 'Барахолка', ru: 'Барахолка', en: 'Flea Market' },
        zapisukha: { uk: 'Бот запису для б\'юті', ru: 'Бот записи для бьюти', en: 'Beauty Booking Bot' },
        mriya: { uk: 'CRM нерухомості', ru: 'CRM недвижимости', en: 'Real Estate CRM' },
        librarian: { uk: 'Бібліотекар', ru: 'Библиотекарь', en: 'Librarian' },
        voice: { uk: 'Voice Widget', ru: 'Voice Widget', en: 'Voice Widget' },
        custom: { uk: 'Кастомний бот', ru: 'Кастомный бот', en: 'Custom Bot' }
    };

    const botMsgIds = {
        zapisukha: 'zapisukha_34',
        voice: 'voice_widget_35',
        mriya: 'mriya_36',
        barakholka: 'barakholka_37',
        librarian: 'librarian_38'
    };

    function getStarsPrice(bot, tier) {
        if (bot === 'voice') {
            return 50;
        }
        if (tier === 'template') return 2500;
        if (tier === 'sync_template') return 4000;
        return 0; // Для інших тарифів Stars недоступні
    }

    function updatePaymentOptions() {
        if (!clientBotSelect || !clientTierSelect || !btnPayStars) return;
        const bot = clientBotSelect.value;
        
        // Для Voice Widget доступний тільки шаблон за $1 / 50 Stars
        if (bot === 'voice') {
            clientTierSelect.value = 'template';
            for (let i = 1; i < clientTierSelect.options.length; i++) {
                clientTierSelect.options[i].disabled = true;
            }
        } else {
            for (let i = 0; i < clientTierSelect.options.length; i++) {
                clientTierSelect.options[i].disabled = false;
            }
        }

        const currentBot = clientBotSelect.value;
        const currentTier = clientTierSelect.value;
        const starsPrice = getStarsPrice(currentBot, currentTier);
        const isStarsAvailable = starsPrice > 0 && botMsgIds[currentBot];

        if (isStarsAvailable) {
            btnPayStars.disabled = false;
            btnPayStars.classList.remove('opacity-50', 'cursor-not-allowed');
            if (labelPayStars) {
                labelPayStars.innerText = (PAGE_TRANSLATIONS[currentLang]['btn_pay_stars'] || 'Сплатити зірками') + ` (${starsPrice} ⭐️)`;
            }
        } else {
            btnPayStars.disabled = true;
            btnPayStars.classList.add('opacity-50', 'cursor-not-allowed');
            if (labelPayStars) {
                labelPayStars.innerText = PAGE_TRANSLATIONS[currentLang]['btn_pay_stars'] || 'Сплатити зірками';
            }
        }
    }

    if (clientBotSelect && clientTierSelect) {
        clientBotSelect.onchange = updatePaymentOptions;
        clientTierSelect.onchange = updatePaymentOptions;
    }

    document.querySelectorAll('.btn-order').forEach(btn => {
        btn.addEventListener('click', (e) => {
            const botKey = btn.dataset.bot;
            if (botKey && clientBotSelect) {
                // Встановлюємо значення
                clientBotSelect.value = botKey;
                
                // Приховуємо вибір бота, якщо це конкретний бот (не custom)
                const divClientBot = document.getElementById('div-client-bot');
                if (divClientBot) {
                    if (botKey === 'custom') {
                        divClientBot.classList.remove('hidden');
                    } else {
                        divClientBot.classList.add('hidden');
                    }
                }

                // Зміна заголовка форми замовлення
                const contactTitle = document.getElementById('contact-form-title');
                if (contactTitle) {
                    const botName = botNamesTrans[botKey][currentLang] || botKey;
                    contactTitle.innerText = `${PAGE_TRANSLATIONS[currentLang]['contact_title'] || 'Залишити заявку'}: ${botName}`;
                }

                updatePaymentOptions();
            }
        });
    });

    // Перевірка імені та телеграму
    function validateClientData() {
        const clientNameElement = document.getElementById('client-name');
        const clientTgElement = document.getElementById('client-username');
        if (!clientNameElement || !clientTgElement) return null;

        const clientName = clientNameElement.value.trim();
        const clientTg = clientTgElement.value.trim();
        if (!clientName || !clientTg) {
            alert(currentLang === 'uk' ? 'Будь ласка, заповніть Ваше ім\'я та Username у Telegram!' : 
                  currentLang === 'ru' ? 'Пожалуйста, заполните Ваше имя и Username в Telegram!' :
                  'Please fill in your Name and Telegram Username!');
            return null;
        }
        return { name: clientName, tg: clientTg };
    }

    function getPriceUSD(bot, tier) {
        if (bot === 'voice') return '\u00241';
        if (tier === 'template') return '\u002449';
        if (tier === 'turnkey') return '\u0024149';
        if (tier === 'maintenance') return '\u002415';
        if (tier === 'sync_template') return '\u002479';
        if (tier === 'sync_turnkey') return '\u0024249';
        return '\u002449';
    }

    // Кнопка оплати зірками Stars
    if (btnPayStars) {
        btnPayStars.onclick = () => {
            if (!clientBotSelect) return;
            const bot = clientBotSelect.value;
            const startParam = botMsgIds[bot];
            if (startParam) {
                window.open(`https://t.me/librar_ian_bot?start=${startParam}`, '_blank');
            }
        };
    }

    // Відкриття модалки оплати
    function openPaymentModal(method) {
        const clientData = validateClientData();
        if (!clientData) return;

        if (!clientBotSelect || !clientTierSelect) return;
        const bot = clientBotSelect.value;
        const tier = clientTierSelect.value;
        const botName = botNamesTrans[bot][currentLang] || bot;
        const tierText = clientTierSelect.options[clientTierSelect.selectedIndex].text;
        const price = getPriceUSD(bot, tier);

        document.getElementById('payment-selected-tariff').innerText = `${botName} (${tierText})`;
        document.getElementById('payment-selected-price').innerText = price;

        const modal = document.getElementById('payment-modal');
        modal.classList.remove('hidden');

        // Перемикання на вкладку
        if (method === 'card') {
            const tabCardElement = document.getElementById('tab-card');
            if (tabCardElement) tabCardElement.click();
        } else {
            const tabCryptoElement = document.getElementById('tab-crypto');
            if (tabCryptoElement) tabCryptoElement.click();
        }
    }

    const btnPayCard = document.getElementById('btn-pay-card');
    if (btnPayCard) btnPayCard.onclick = () => openPaymentModal('card');

    const btnPayCrypto = document.getElementById('btn-pay-crypto');
    if (btnPayCrypto) btnPayCrypto.onclick = () => openPaymentModal('crypto');

    // Modal Close
    const closeModal = document.getElementById('close-payment-modal');
    if (closeModal) {
        closeModal.onclick = () => {
            document.getElementById('payment-modal').classList.add('hidden');
        };
    }

    // Tabs
    const tabCrypto = document.getElementById('tab-crypto');
    const tabCard = document.getElementById('tab-card');
    const panelCrypto = document.getElementById('panel-crypto');
    const panelCard = document.getElementById('panel-card');
    
    if (tabCrypto && tabCard && panelCrypto && panelCard) {
        tabCrypto.onclick = () => {
            tabCrypto.className = "py-2.5 rounded-lg text-xs font-semibold bg-indigo-500/20 text-white border border-indigo-500/30 transition-all flex items-center justify-center gap-1.5";
            tabCard.className = "py-2.5 rounded-lg text-xs font-semibold text-zinc-400 hover:text-white transition-all flex items-center justify-center gap-1.5";
            panelCrypto.classList.remove('hidden');
            panelCard.classList.add('hidden');
        };
        
        tabCard.onclick = () => {
            tabCard.className = "py-2.5 rounded-lg text-xs font-semibold bg-indigo-500/20 text-white border border-indigo-500/30 transition-all flex items-center justify-center gap-1.5";
            tabCrypto.className = "py-2.5 rounded-lg text-xs font-semibold text-zinc-400 hover:text-white transition-all flex items-center justify-center gap-1.5";
            panelCard.classList.remove('hidden');
            panelCrypto.classList.add('hidden');
        };
    }

    // Copy handlers
    function setupCopyButton(btnId, inputId) {
        const btn = document.getElementById(btnId);
        const input = document.getElementById(inputId);
        if (btn && input) {
            btn.onclick = () => {
                input.select();
                navigator.clipboard.writeText(input.value).then(() => {
                    const originalHtml = btn.innerHTML;
                    const copiedText = PAGE_TRANSLATIONS[currentLang]['pay_copied'] || 'Copied!';
                    
                    const hasText = btn.innerText.trim().length > 0;
                    if (hasText) {
                        btn.innerHTML = `<span class="material-symbols-outlined text-[14px]">check</span><span>${copiedText}</span>`;
                    } else {
                        btn.innerHTML = `<span class="material-symbols-outlined text-[13px]">check</span>`;
                    }
                    
                    btn.classList.add('bg-emerald-600', 'border-emerald-500');
                    setTimeout(() => {
                        btn.innerHTML = originalHtml;
                        btn.classList.remove('bg-emerald-600', 'border-emerald-500');
                    }, 2000);
                });
            };
        }
    }
    setupCopyButton('copy-wallet-btn-usdt', 'payment-wallet-address-usdt');
    setupCopyButton('copy-wallet-btn-usdc', 'payment-wallet-address-usdc');
    setupCopyButton('copy-card-btn', 'payment-card-number');

    // Voice Widget direct buy button
    const btnBuyVoice = document.getElementById('btn-buy-voice');
    if (btnBuyVoice) {
        btnBuyVoice.onclick = () => {
            let widgetName = 'Voice Widget (Desktop App)';
            if (currentLang === 'uk') widgetName = 'Voice Widget (Десктопний віджет)';
            else if (currentLang === 'ru') widgetName = 'Voice Widget (Десктопный виджет)';
            
            document.getElementById('payment-selected-tariff').innerText = widgetName;
            document.getElementById('payment-selected-price').innerText = '$1';
            
            const modal = document.getElementById('payment-modal');
            if (modal) modal.classList.remove('hidden');
        };
    }

    // Confirm logic
    const btnConfirm = document.getElementById('btn-confirm-payment');
    if (btnConfirm) {
        btnConfirm.onclick = () => {
            const plan = document.getElementById('payment-selected-tariff').innerText;
            const price = document.getElementById('payment-selected-price').innerText;
            const message = encodeURIComponent(`Привіт! Я оплатив замовлення:\nТариф: ${plan}\nСума: ${price}`);
            window.open(`https://t.me/nova_bots_support?text=${message}`, '_blank');
            document.getElementById('payment-modal').classList.add('hidden');
        };
    }
    
    // Initial call to set active styles & disabled states
    updatePaymentOptions();
});
