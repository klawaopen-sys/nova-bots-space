import os

DEFAULT_LANG = os.getenv("DEFAULT_LANG", "uk")

TRANSLATIONS = {
    "welcome_title": {
        "uk": "👋 Вітаємо у \"Барахолка у кишені м. {city}\"",
        "ru": "👋 Добро пожаловать в \"Барахолка в кармане г. {city}\"",
        "en": "👋 Welcome to \"Pocket Marketplace, {city}\""
    },
    "welcome_body": {
        "uk": "Тут ви можете швидко та зручно:\n🛒 <b>Купувати</b> — знаходьте потрібні речі та послуги у своєму місті.\n📦 <b>Продавати</b> — розміщуйте оголошення без зайвих зусиль.\n\n<b>Оберіть дію в меню нижче 👇</b>",
        "ru": "Здесь вы можете быстро и удобно:\n🛒 <b>Покупать</b> — находите нужные вещи и услуги в своем городе.\n📦 <b>Продавать</b> — размещайте объявления без лишних усилий.\n\n<b>Выберите действие в меню ниже 👇</b>",
        "en": "Here you can quickly and conveniently:\n🛒 <b>Buy</b> — find items and services in your city.\n📦 <b>Sell</b> — post classified ads with ease.\n\n<b>Choose an action in the menu below 👇</b>"
    },
    "btn_buy": {
        "uk": "🛒 Купити",
        "ru": "🛒 Купить",
        "en": "🛒 Buy"
    },
    "btn_sell": {
        "uk": "📦 Продати",
        "ru": "📦 Продать",
        "en": "📦 Sell"
    },
    "btn_cabinet": {
        "uk": "💼 Кабінет продавця",
        "ru": "💼 Личный кабинет",
        "en": "💼 User Cabinet"
    },
    "btn_refresh": {
        "uk": "🔄 Оновити",
        "ru": "🔄 Обновить",
        "en": "🔄 Refresh"
    },
    "btn_back": {
        "uk": "🔙 Назад до меню",
        "ru": "🔙 Назад в меню",
        "en": "🔙 Back to Menu"
    },
    "select_section": {
        "uk": "📂 Оберіть розділ:",
        "ru": "📂 Выберите раздел:",
        "en": "📂 Choose section:"
    },
    "select_category_sell": {
        "uk": "📂 Оберіть категорію для продажу:",
        "ru": "📂 Выберите категорию для продажи:",
        "en": "📂 Choose category for sale:"
    },
    "select_category_buy": {
        "uk": "🔎 Що шукаєте?",
        "ru": "🔎 Что ищете?",
        "en": "🔎 What are you looking for?"
    },
    "limit_reached": {
        "uk": "❌ <b>Ліміт публікацій вичерпано!</b>\n\nЦього тижня ви вже опублікували <b>{posted}</b> оголошень (ваш тижневий ліміт: <b>{limit}</b>).\n\n📊 Щоб отримати більше лімітів:\n1. 👤 Запросіть друзів.\n2. 🌟 Придбайте безліміт.",
        "ru": "❌ <b>Лимит публикаций исчерпан!</b>\n\nНа этой неделе вы уже опубликовали <b>{posted}</b> объявлений (ваш лимит: <b>{limit}</b>).\n\n📊 Чтобы получить больше лимитов:\n1. 👤 Пригласите друзей.\n2. 🌟 Приобретите безлимит.",
        "en": "❌ <b>Post limit reached!</b>\n\nYou have already posted <b>{posted}</b> ads this week (your limit: <b>{limit}</b>).\n\n📊 To get more limits:\n1. 👤 Invite friends.\n2. 🌟 Purchase unlimited plan."
    },
    "published_success": {
        "uk": "🚀 Опубліковано!",
        "ru": "🚀 Опубликовано!",
        "en": "🚀 Successfully Published!"
    },
    "no_ads_category": {
        "uk": "❌ У цій категорії ще немає оголошень!",
        "ru": "❌ В этой категории еще нет объявлений!",
        "en": "❌ No ads in this category yet!"
    }
}

def t(key, lang=None, **kwargs):
    if not lang:
        lang = DEFAULT_LANG
    
    # Normalize language codes (e.g. 'uk-UA' or 'uk' -> 'uk')
    lang = lang.split('-')[0].lower()
    if lang not in ["uk", "ru", "en"]:
        lang = "en"  # default fallback for global users

    text_dict = TRANSLATIONS.get(key, {})
    text = text_dict.get(lang, text_dict.get(DEFAULT_LANG, key))
    
    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text
