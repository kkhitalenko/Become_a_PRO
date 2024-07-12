from aiogram import Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from config import ADMIN_TG_ID
from core import messages
from core.states import BotStates


router = Router()


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(messages.HELP)


@router.message(Command('github'))
async def cmd_github(message: Message):
    await message.answer(messages.GITHUB_URL)


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
