import aiosqlite
from config import DB_NAME

async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:
        # 1. Ads table
        await db.execute('''CREATE TABLE IF NOT EXISTS ads (
            id INTEGER PRIMARY KEY AUTOINCREMENT, user_id INTEGER, username TEXT, 
            category TEXT, title TEXT, param TEXT, price TEXT, condition TEXT,
            photo_id TEXT, phone TEXT, show_phone INTEGER)''')
            
        # Migration: add created_at if it does not exist
        async with db.execute("PRAGMA table_info(ads)") as cursor:
            columns = [row[1] for row in await cursor.fetchall()]
        if 'created_at' not in columns:
            await db.execute("ALTER TABLE ads ADD COLUMN created_at TEXT DEFAULT '2026-06-08T00:00:00'")
            
        # 2. Users table
        await db.execute('''CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY,
            username TEXT,
            referred_by INTEGER,
            bonus_posts INTEGER DEFAULT 0,
            subscription_until TIMESTAMP,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            
        # 3. Referrals table
        await db.execute('''CREATE TABLE IF NOT EXISTS referrals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            referrer_id INTEGER,
            referred_id INTEGER,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
            
        # 4. Categories table
        await db.execute('''CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT, 
            name TEXT UNIQUE, 
            section TEXT
        )''')
        
        # Default categorized sections
        default_cats = [
            # Transport (auto)
            ('🚗 Легкові авто', 'auto'), ('🏍️ Мототехніка', 'auto'), ('🚚 Вантажівки', 'auto'), 
            ('🚜 Сільгосптехніка', 'auto'), ('🚌 Автобуси', 'auto'), ('🔩 Автозапчастини', 'auto'),
            
            # Goods (goods)
            ('📱 Телефони та Гаджети', 'goods'), ('💻 Комп\'ютери', 'goods'), ('👕 Одяг та Взуття', 'goods'), 
            ('🧸 Дитячий світ', 'goods'), ('🏠 Дім та Сад', 'goods'), ('🏠 Нерухомість', 'goods'), ('⚽ Спорт та Хобі', 'goods'), 
            ('🐶 Тварини', 'goods'), ('📦 Інше (Товари)', 'goods'),
            
            # Services (service)
            ('💅 Краса та Здоров\'я', 'service'), ('🏗️ Будівництво та Ремонт', 'service'), ('🚚 Перевезення', 'service'), 
            ('🧹 Клінінг', 'service'), ('🎓 Навчання', 'service'), ('💼 Робота', 'service'), 
            ('🔮 Езотерика та Астрологія', 'service'), ('🛠️ Інше (Послуги)', 'service')
        ]
        
        # Seed default categories
        await db.executemany("INSERT OR IGNORE INTO categories (name, section) VALUES (?, ?)", default_cats)
        await db.commit()
