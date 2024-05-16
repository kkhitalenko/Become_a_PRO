import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import Command
from dotenv import load_dotenv

import bot.messages
from bot.keyboards import languages_builder

logging.basicConfig(level=logging.INFO)

load_dotenv()
tg_bot = Bot(os.getenv('token'))
dp = Dispatcher()


@dp.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(bot.messages.START_MESSAGE,
                         reply_markup=languages_builder.as_markup())


async def main():
    await dp.start_polling(tg_bot)

if __name__ == '__main__':
    asyncio.run(main())
