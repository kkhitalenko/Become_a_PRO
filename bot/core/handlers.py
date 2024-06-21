from aiogram import F, Router
from aiogram.enums import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from core import keyboards, messages
from core.data_fetcher import create_progress, get_description
from core.states import BotStates


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(messages.START_MESSAGE,
                         reply_markup=keyboards.get_langeages_kb())


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(messages.HELP_MESSAGE,
                         reply_markup=keyboards.get_commands_kb(),
                         parse_mode=ParseMode.HTML)


@router.callback_query(F.data.in_({'Python', 'Go', 'Rust'}))
async def get_info_from_user(callback: CallbackQuery, state: FSMContext):

    language = callback.data

    await state.set_state(BotStates.starting)
    await state.update_data(language=language)

    description = await get_description(language.lower())
    await callback.answer(text=description, show_alert=True)

    tg_user_id = callback.from_user.id
    await state.update_data(tg_user_id=tg_user_id)
    await callback.message.answer(f'Ты изучал ранее {language}?',
                                  reply_markup=keyboards.get_yes_no_kb())


@router.callback_query(BotStates.starting)
async def get_progress(callback: CallbackQuery, state: FSMContext):
    # пока так
    ZERO_LESSON_ID = {'Python': 2, 'Go': 2, 'Rust': 1}
    state_data = await state.get_data()
    tg_user_id = state_data['tg_user_id']
    language = state_data['language']
    last_completed_lesson = ZERO_LESSON_ID.get(language)
    if callback.data == 'да':
        pass
        # await test_the_user()
    await create_progress(tg_user_id, language.lower(), last_completed_lesson)
