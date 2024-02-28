
import asyncio
import logging

from aiogram import Bot, Dispatcher
from settings import config

bot = Bot(token=config.bot_token.get_secret_value())
dp = Dispatcher(token=bot)


async def main():
    logging.basicConfig(
        level=logging.INFO,
        format="%(levelname)s - %(name)s - %(message)s",
    )
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())
