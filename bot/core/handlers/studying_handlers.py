from aiogram import F, Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import LANGUAGE_LIST
from core import keyboards, messages
from core.services import (create_progress, get_description, get_lesson,
                           get_progress, update_progress)
from core.states import BotStates
from main import bot


router = Router()


@router.message(CommandStart())
async def cmd_start(message: Message):
    await message.answer(messages.START,
                         reply_markup=keyboards.get_langeages_kb())


@router.message(Command('switch_language'))
async def cmd_switch_language(message: Message, state: FSMContext):
    state_data = await state.get_data()
    if state_data:
        current_language = state_data.get('language')
        others_languages = LANGUAGE_LIST.copy()
        others_languages.remove(current_language)
        await message.answer(messages.WHICH_LANGUAGE_SWITCH,
                             reply_markup=keyboards.create_kb(others_languages))
    else:
        await message.answer(messages.WHICH_LANGUAGE_SWITCH,
                             reply_markup=keyboards.get_langeages_kb())



@router.callback_query(F.data.in_(LANGUAGE_LIST))
async def prepare_data_for_study(callback: CallbackQuery, state: FSMContext):
    tg_user_id = callback.from_user.id
    language = callback.data

    await state.set_state(BotStates.studying)
    await state.update_data(tg_user_id=tg_user_id, language=language)

    progress = await get_progress(tg_user_id, language)
    if progress:
        await callback.message.answer(
            messages.ALREADY_LEARNED.format(language.title()),
            reply_markup=keyboards.get_continue_or_reset_kb()
        )
    else:
        await callback.message.answer(
            messages.HAVE_YOU_ALREADY_LEARNED.format(language.title()),
            reply_markup=keyboards.get_yes_no_kb()
        )
    await callback.answer()


@router.callback_query(F.data.in_({'yes', 'no', 'reset'}), BotStates.studying)
async def set_progress(callback: CallbackQuery, state: FSMContext):
    """
    Sets the initial progress if user has not studied the language before
    or if user wants to reset the progress.
    Otherwise goes into testing mode.
    Eventually goes into study mode.
    """

    state_data = await state.get_data()
    tg_user_id = state_data['tg_user_id']
    language = state_data['language']

    if callback.data == 'yes':
        last_completed_lesson = await test_the_user(tg_user_id, language)
        await create_progress(tg_user_id, language, last_completed_lesson)
    elif callback.data == 'no':
        last_completed_lesson = 0
        description = await get_description(language)
        await callback.message.answer(description)
        await create_progress(tg_user_id, language, last_completed_lesson)
    elif callback.data == 'reset':
        last_completed_lesson = 0
        await update_progress(tg_user_id, language, last_completed_lesson)

    await study(state)
    await callback.answer()


async def test_the_user(tg_user_id: int, language: str):
    pass


@router.message(Command('continue'))
async def cmd_continue(message: Message, state: FSMContext):
    """
    Check if progress exists in several languages

     - Notify user if progress not found
     - Form data and call study() if progress is only one
     - Send keyboard to user for language choice if progress is more than one.
    """

    tg_user_id = message.from_user.id

    progresses = []
    for language in LANGUAGE_LIST:
        progress = await get_progress(tg_user_id, language)
        if progress is not None:
            progresses.append(language)

    if not progresses:
        await message.answer(messages.LETS_START,
                             reply_markup=keyboards.get_langeages_kb())
    elif len(progresses) == 1:
        language = progresses[0]
        await state.set_state(BotStates.studying)
        await state.update_data(tg_user_id=tg_user_id, language=language)
        await study(state)
    else:
        await message.answer(messages.WHICH_LANGUAGE_CONTINUE,
                             reply_markup=keyboards.create_kb(progresses))


@router.callback_query(F.data == 'continue')
async def callback_continue(callback: CallbackQuery, state: FSMContext):
    await study(state)
    await callback.answer()


async def study(state: FSMContext):
    """
    Defines last completed lesson for this user in this language.
    Sends next lesson information, first question and provides with multiple
    options choice keyboard.
    """

    state_data = await state.get_data()
    tg_user_id = state_data['tg_user_id']
    language = state_data['language']

    last_completed_lesson = await get_progress(tg_user_id, language)
    lesson = await get_lesson(language, last_completed_lesson)
    if lesson.get('title') is None:
        await bot.send_message(chat_id=tg_user_id,
                               text=messages.FINISH)
        await state.clear()

    else:
        lesson_title = lesson.get('title')
        await bot.send_message(chat_id=tg_user_id,
                               text=messages.LESSON.format(lesson_title),
                               parse_mode=ParseMode.HTML)
        await bot.send_message(chat_id=tg_user_id,
                               text=lesson.get('theory'))

        questions = lesson.get('questions_of_lesson')
        first_question = questions[0]
        question_text = first_question.get('text')
        options = [
            first_question.get('answer1'),
            first_question.get('answer2'),
            first_question.get('answer3')
        ]
        correct_option = first_question.get('correct_answer')
        wrong_answers = set()

        await state.update_data(last_completed_lesson=last_completed_lesson,
                                questions=questions, current_question=0,
                                correct_option=correct_option,
                                wrong_answers=wrong_answers)

        await bot.send_message(chat_id=tg_user_id, text=question_text,
                               reply_markup=keyboards.create_kb(options),
                               parse_mode=ParseMode.MARKDOWN)


@router.callback_query(BotStates.studying)
async def study_callback(callback: CallbackQuery,
                         state: FSMContext):
    """
    Send questions to user.
    After last question calls study() for the next lesson.
    """

    state_data = await state.get_data()
    correct_option = state_data['correct_option']
    question_number = state_data['current_question']
    wrong_answers = state_data['wrong_answers']

    if callback.data != correct_option:
        await callback.answer(text=messages.TRY_AGAIN,
                              show_alert=True)
        wrong_answers.add(question_number+1)
        await state.update_data(wrong_answers=wrong_answers)

    else:
        question_number += 1
        questions = state_data['questions']
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
                                    current_question=question_number)

            await callback.message.answer(
                text=question_text,
                reply_markup=keyboards.create_kb(options),
                parse_mode=ParseMode.MARKDOWN
            )
        else:
            tg_user_id = state_data['tg_user_id']
            language = state_data['language']
            last_completed_lesson = state_data['last_completed_lesson'] + 1

            payload = {'tg_user_id': tg_user_id, 'language': language,
                       'last_completed_lesson': last_completed_lesson}
            if wrong_answers:
                payload['wrong_answers'] = wrong_answers
            await update_progress(**payload)

            await study(state)

    await callback.answer()
