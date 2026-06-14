"""
main.py
Точка входу для бізнес-шаблону бота «Записуха» (Beauty Booking Bot).
Запускає асинхронний цикл aiogram та підключається до Google Sheets.
"""

import asyncio
import logging
import os
from dotenv import load_dotenv

from aiogram import Bot, Dispatcher
from aiogram.types import BotCommand
from aiogram.client.default import DefaultBotProperties

from handlers.zapisukha_handlers import router as zapisukha_router
from config import BOT_TOKEN

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger(__name__)


async def main():
    logger.info("🚀 Запуск ब्यूटी-бота для запису клієнтів...")

    if not BOT_TOKEN or BOT_TOKEN == "YOUR_TELEGRAM_BOT_TOKEN":
        logger.error("❌ BOT_TOKEN не вказано або встановлено за замовчуванням у .env!")
        return

    # Ініціалізація бота з підтримкою HTML парсингу повідомлень
    bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher()
    dp.include_router(zapisukha_router)

    # Налаштування базових команд меню
    await bot.set_my_commands([
        BotCommand(command="start", description="🏠 Головне меню"),
        BotCommand(command="admin", description="👑 Адмін-панель"),
    ])
    
    # Видаляємо вебхуки для безпечного запуску локального пулінгу
    await bot.delete_webhook(drop_pending_updates=True)

    bot_info = await bot.get_me()
    logger.info(f"✅ Бот успішно активовано: @{bot_info.username} (ID: {bot_info.id})")

    try:
        await dp.start_polling(bot, allowed_updates=dp.resolve_used_update_types())
    finally:
        await bot.session.close()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("🛑 Бот зупинено вручну.")
