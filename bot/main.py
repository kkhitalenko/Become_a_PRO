import asyncio
import logging
import os

from aiogram import Bot, Dispatcher

from core.handlers import router

TOKEN = os.getenv('TOKEN')

dp = Dispatcher()
dp.include_router(router)


async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
