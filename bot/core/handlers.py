import os

from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from dotenv import load_dotenv

from core import keyboards, messages
from core.data_fetcher import (check_progress, create_progress,
                               get_description, update_progress)
from core.states import BotStates


router = Router()

load_dotenv()
ADMIN_TG_ID = os.getenv('ADMIN_TG_ID')


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(messages.START_MESSAGE,
                         reply_markup=keyboards.get_langeages_kb())


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(messages.HELP_MESSAGE)


@router.message(Command('github'))
async def cmd_github(message: Message):
    await message.answer(messages.GITHUB_URL_MESSAGE)


@router.message(Command('feedback'))
async def get_feedback(message: Message, state: FSMContext):
    await state.set_state(BotStates.feedback)
    await message.answer(messages.FEEDBACK_MESSAGE)


@router.message(BotStates.feedback)
async def send_feedback_to_admin(message: Message, state: FSMContext):
    await message.bot.send_message(
        chat_id=ADMIN_TG_ID,
        text=f'пользователь id={message.from_user.id} написал "{message.text}"'
    )
    await state.clear()
    await message.answer(messages.THANKS_FOR_FEEDBACK_MESSAGE)


@router.callback_query(F.data.in_({'python', 'go', 'rust'}))
async def start_studying(callback: CallbackQuery, state: FSMContext):

    language = callback.data
    tg_user_id = callback.from_user.id

    await state.set_state(BotStates.starting)
    await state.update_data(language=language)
    await state.update_data(tg_user_id=tg_user_id)

    progress = await check_progress(tg_user_id, language)
    if progress:
        await callback.message.answer(
            f'Ты уже начал учить {language.title()}, что ты хочешь?',
            reply_markup=keyboards.get_continue_or_reset_kb()
        )
    else:
        await callback.message.answer(
            f'Ты изучал ранее {language.title()}?',
            reply_markup=keyboards.get_yes_no_kb()
        )
    await callback.answer()


@router.callback_query(F.data.in_({'да', 'нет'}), BotStates.starting)
async def set_progress(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    tg_user_id = state_data['tg_user_id']
    language = state_data['language']

    if callback.data == 'да':
        last_completed_lesson = await test_the_user(tg_user_id, language)
    elif callback.data == 'нет':
        last_completed_lesson = 0
        description = await get_description(language)
        await callback.answer(text=description, show_alert=True)

    await create_progress(tg_user_id, language, last_completed_lesson)
    await continue_studying(tg_user_id, language, last_completed_lesson,
                            callback)


@router.callback_query(F.data == 'reset', BotStates.starting)
async def reset(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    tg_user_id = state_data['tg_user_id']
    language = state_data['language']
    last_completed_lesson = 0
    await update_progress(tg_user_id, language, last_completed_lesson)
    await continue_studying(tg_user_id, language, last_completed_lesson,
                            callback)
    await callback.answer()


async def test_the_user(tg_user_id: int, language: str):
    pass


async def continue_studying(tg_user_id: int, language: str,
                            last_completed_lesson: int,
                            callback: CallbackQuery):
    pass
