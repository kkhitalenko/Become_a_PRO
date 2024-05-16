import asyncio
import logging
import os

from aiogram import Bot, Dispatcher
from dotenv import load_dotenv


load_dotenv()

bot = Bot(os.getenv('bot_token'))
dp = Dispatcher()


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s - %(name)s - %(message)s",
    )
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
