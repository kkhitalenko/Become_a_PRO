from aiogram import F, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import LANGUAGE_LIST
from core import keyboards, messages
from core.services import get_progress_list, get_wrong_answered_questions
from core.states import BotStates
from main import bot


router = Router()


@router.message(Command('repeat'))
async def cmd_repeat(message: Message, state: FSMContext):
    state_data = await state.get_data()

    if state_data:
        tg_user_id = state_data['tg_user_id']
        language = state_data['language']
        await state.set_state(BotStates.repeating)
        await state.update_data(tg_user_id=tg_user_id, language=language)
        await repeat(state)

    else:
        tg_user_id = message.from_user.id
        progresses = await get_progress_list(tg_user_id)
        if not progresses:
            await message.answer(
                messages.LETS_START,
                reply_markup=keyboards.create_kb(LANGUAGE_LIST)
            )
        elif len(progresses) == 1:
            language = progresses[0]
            await state.set_state(BotStates.repeating)
            await state.update_data(tg_user_id=tg_user_id, language=language)
            await repeat(state)
        else:
            await message.answer(
                messages.WHICH_LANGUAGE_REPEAT,
                reply_markup=keyboards.create_languages_kb(progresses)
            )


@router.callback_query(F.data.startswith('repeat'))
async def cb_cmd_repeat(callback: CallbackQuery, state: FSMContext):
    tg_user_id = callback.from_user.id
    language = callback.data.split('_')[1]

    await state.set_state(BotStates.repeating)
    await state.update_data(tg_user_id=tg_user_id, language=language)
    await repeat(state)

    await callback.answer()


async def repeat(state: FSMContext):
    state_data = await state.get_data()
    tg_user_id = state_data['tg_user_id']
    language = state_data['language']

    questions = await get_wrong_answered_questions(tg_user_id, language)
    questions = questions.get('wrong_answers')
    if questions:
        first_question = questions[0]
        question_text = first_question.get('text')
        options = [
                first_question.get('answer1'),
                first_question.get('answer2'),
                first_question.get('answer3')
            ]
        correct_option = first_question.get('correct_answer')
        question_ids = [question.get('id') for question in questions]

        await state.update_data(questions=questions, current_question=0,
                                correct_option=correct_option,
                                question_ids=question_ids)

        await bot.send_message(chat_id=tg_user_id, text=question_text,
                               reply_markup=keyboards.create_kb(options),
                               parse_mode=ParseMode.MARKDOWN)

    else:
        await bot.send_message(chat_id=tg_user_id,
                               text=messages.NOTHING_TO_REPEAT)
        await state.clear()


@router.callback_query(BotStates.repeating)
async def repeat_callback(callback: CallbackQuery, state: FSMContext):
    pass
