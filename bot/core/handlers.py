import os

from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message
from dotenv import load_dotenv
from main import bot

from core import keyboards, messages
from core.data_fetcher import create_progress, get_description
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
    await message.answer(messages.HELP_MESSAGE,
                         reply_markup=keyboards.get_commands_kb(),
                         parse_mode=ParseMode.HTML)


@router.callback_query(F.data == 'start')
async def cmd_start_callback(callback: CallbackQuery):
    await callback.message.answer(messages.START_MESSAGE,
                                  reply_markup=keyboards.get_langeages_kb())
    await callback.answer()


@router.callback_query(F.data == 'feedback')
async def get_feedback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BotStates.feedback)
    await callback.message.answer('Напиши мне, что думаешь')
    await callback.answer()


@router.message(BotStates.feedback)
async def send_feedback_to_admin(message: Message, state: FSMContext):
    await bot.send_message(chat_id=ADMIN_TG_ID,
                           text=f'пользователь с id={message.from_user.id}'
                                f' написал "{message.text}"')
    await state.clear()
    await message.answer('Спасибо за фидбэк, мы передали его автору')


@router.callback_query(F.data.in_({'python', 'go', 'rust'}))
async def get_info_from_user(callback: CallbackQuery, state: FSMContext):

    language = callback.data

    await state.set_state(BotStates.starting)
    await state.update_data(language=language)

    description = await get_description(language)
    await callback.answer(text=description, show_alert=True)

    tg_user_id = callback.from_user.id
    await state.update_data(tg_user_id=tg_user_id)
    await callback.message.answer(f'Ты изучал ранее {language.title()}?',
                                  reply_markup=keyboards.get_yes_no_kb())
    # await callback.answer()


@router.callback_query(BotStates.starting)
async def get_progress(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    tg_user_id = state_data['tg_user_id']
    language = state_data['language']
    last_completed_lesson = 0

    if callback.data == 'да':
        pass
        # await test_the_user()

    await create_progress(tg_user_id, language, last_completed_lesson)
