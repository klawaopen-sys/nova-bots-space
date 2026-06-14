import asyncio
import logging
from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties

from handlers import router
from database import init_db
from config import BOT_TOKEN, USE_PROXY

async def main():
    logging.basicConfig(level=logging.INFO)
    
    # Check proxy configuration
    if USE_PROXY:
        session = AiohttpSession(proxy="http://proxy.server:3128")
        bot = Bot(token=BOT_TOKEN, session=session, default=DefaultBotProperties(parse_mode="HTML"))
    else:
        bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    
    dp = Dispatcher()
    dp.include_router(router)
    
    # Initialize SQLite database schema
    await init_db()
    
    # Register commands in the user menu
    await bot.set_my_commands([
        BotCommand(command="start", description="🏠 Головне меню")
    ])
    
    await bot.delete_webhook(drop_pending_updates=True)
    print("🤖 Бот успішно запущено!")
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("🛑 Бот зупинений.")
