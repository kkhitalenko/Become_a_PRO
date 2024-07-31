from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import LinkPreviewOptions, Message

from config import ADMIN_TG_ID, LANGUAGE_LIST
from core import keyboards, messages
from core.states import BotStates


router = Router()


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(messages.HELP)


@router.message(Command('github'))
async def cmd_github(message: Message):
    option = LinkPreviewOptions(is_disabled=True)
    await message.answer(messages.GITHUB_URL,
                         link_preview_options=option)


@router.message(Command('feedback'))
async def cmd_feedback(message: Message, state: FSMContext):
    await state.set_state(BotStates.feedback)
    await message.answer(messages.FEEDBACK)


@router.message(BotStates.feedback)
async def send_feedback_to_admin(message: Message, state: FSMContext):
    await message.bot.send_message(
        chat_id=ADMIN_TG_ID,
        text=messages.MESSAGE_TO_ADMIN.format(message.from_user.id,
                                              message.text)
    )
    await state.clear()
    await message.answer(messages.THANKS_FOR_FEEDBACK)


@router.message(Command('switch_language'))
async def cmd_switch_language(message: Message, state: FSMContext):
    state_data = await state.get_data()
    if state_data:
        current_language = state_data.get('language')
        others_languages = LANGUAGE_LIST.copy()
        others_languages.remove(current_language)
        await message.answer(
            messages.WHICH_LANGUAGE_SWITCH,
            reply_markup=keyboards.create_kb(others_languages)
        )
    else:
        await message.answer(messages.WHICH_LANGUAGE_SWITCH,
                             reply_markup=keyboards.create_kb(LANGUAGE_LIST))
