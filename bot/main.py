import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv

from core.commands import set_commands


load_dotenv()
TOKEN = os.getenv('TOKEN')

dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=TOKEN)


async def main():
    from core.handlers import router

    dp.include_router(router)
    await set_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
