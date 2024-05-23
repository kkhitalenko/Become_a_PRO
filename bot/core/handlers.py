from aiogram import Router, types
from aiogram.filters.command import Command

from core import keyboards, messages


router = Router()


@router.message(Command('start'))
async def cmd_start(message: types.Message):
    await message.answer(messages.START_MESSAGE,
                         reply_markup=keyboards.languages_builder.as_markup())
