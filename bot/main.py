import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

from core.commands import set_commands
from core.handlers import router


load_dotenv()


TOKEN = os.getenv('TOKEN')

dp = Dispatcher()
dp.include_router(router)


async def main():
    bot = Bot(token=TOKEN)
    await set_commands(bot)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
