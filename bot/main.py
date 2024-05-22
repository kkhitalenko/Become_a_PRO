import asyncio
import logging
import os

from aiogram import Bot, Dispatcher, types
from aiogram.filters.command import CommandStart

from core import keyboards, messages

TOKEN = os.getenv('TOKEN')

dp = Dispatcher()


@dp.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer(messages.START_MESSAGE,
                         reply_markup=keyboards.languages_builder.as_markup())


async def main():
    bot = Bot(token=TOKEN)
    await dp.start_polling(bot)

if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
