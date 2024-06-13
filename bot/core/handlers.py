from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from core import keyboards, messages
from core.data_fetcher import get_description, create_user
from core.states import BotStates


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(messages.START_MESSAGE,
                         reply_markup=keyboards.get_langeages_kb())


@router.callback_query(F.data.in_({'Python', 'Go', 'Rust'}))
async def get_info_from_user(callback: CallbackQuery, state: FSMContext):

    language = callback.data

    await state.set_state(BotStates.starting)
    await state.update_data(language=language)

    description = await get_description(language.lower())
    await callback.answer(text=description, show_alert=True)

    user_id = callback.from_user.id
    username = callback.from_user.username
    await create_user(user_id, username)

    await callback.message.answer(f'Ты изучал ранее {language}?',
                                  reply_markup=keyboards.get_yes_no_kb())


@router.callback_query(BotStates.starting)
async def clarify_state(callback: CallbackQuery, state: FSMContext):
    pass
