from aiogram import F, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import LANGUAGE_LIST
from core import bot, keyboards, messages
from core.services import (get_progress_list, get_wrong_answered_questions,
                           update_wrong_answered_questions)
from core.states import BotStates


router = Router()


@router.message(Command('repeat'))
async def cmd_repeat(message: Message, state: FSMContext):
    """
    If state exists, gets language, tg_user_id and goes into repeat mode.

    Otherwise check if progress exists in several languages
     - Notify user if progress not found
     - Form data and call repeat() if progress is only one
     - Send keyboard to user for language choice if progress is more than one.
    """

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
    """Gets tg_user_id and language and goes into repeat mode."""

    tg_user_id = callback.from_user.id
    language = callback.data.split('_')[1]

    await callback.message.edit_text(messages.REPEAT)

    await state.set_state(BotStates.repeating)
    await state.update_data(tg_user_id=tg_user_id, language=language)
    await repeat(state)

    await callback.answer()


async def repeat(state: FSMContext):
    """
    Defines wrong answered questions for this user in this language.
    Sends first question and provides with multiple options choice keyboard.
    """

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
        new_question_ids = set()

        await state.update_data(questions=questions,
                                question_number=0,
                                correct_option=correct_option,
                                new_question_ids=new_question_ids)

        await bot.send_message(chat_id=tg_user_id, text=question_text,
                               reply_markup=keyboards.create_kb(options),
                               parse_mode=ParseMode.MARKDOWN)

    else:
        await bot.send_message(chat_id=tg_user_id,
                               text=messages.NOTHING_TO_REPEAT)
        await state.clear()


@router.callback_query(BotStates.repeating)
async def repeat_callback(callback: CallbackQuery, state: FSMContext):
    """
    Compares the received answer with the correct one
    - if they are not equal, notify user
    - otherwise, asks user the next question
    After last question updates the progress.
    """

    state_data = await state.get_data()
    questions = state_data['questions']
    question_number = state_data['question_number']
    correct_option = state_data['correct_option']
    new_question_ids = state_data['new_question_ids']

    if callback.data != correct_option:
        new_question_ids.add(questions[question_number]['id'])
        await callback.answer(text=messages.TRY_AGAIN,
                              show_alert=True)
        await state.update_data(new_question_ids=new_question_ids)

    else:
        question_number += 1
        if question_number < len(questions):
            question = questions[question_number]
            question_text = question.get('text')
            options = [
                question.get('answer1'),
                question.get('answer2'),
                question.get('answer3')
            ]
            correct_option = question.get('correct_answer')
            await state.update_data(correct_option=correct_option,
                                    question_number=question_number)
            await callback.message.answer(
                text=question_text,
                reply_markup=keyboards.create_kb(options),
                parse_mode=ParseMode.MARKDOWN
            )

        else:
            tg_user_id = state_data['tg_user_id']
            language = state_data['language']
            payload = {'tg_user_id': tg_user_id, 'language': language,
                       'wrong_answers': new_question_ids}
            await update_wrong_answered_questions(**payload)
            await repeat(state)

    await callback.answer()
