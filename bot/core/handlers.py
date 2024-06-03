from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.types import CallbackQuery, Message

from core import keyboards, messages
from core.data_fetcher import get_description


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(messages.START_MESSAGE,
                         reply_markup=keyboards.languages_builder.as_markup())


@router.callback_query(F.data.in_({'Python', 'Go', 'Rust'}))
async def get_language(callback: CallbackQuery):
    language = callback.data
    await callback.answer(f'{language} - мой любимый язык')
    res = await get_description(language.lower())
    await callback.message.answer(res)
