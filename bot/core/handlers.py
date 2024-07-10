from aiogram import F, Router
from aiogram.filters import Command, CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from config import ADMIN_TG_ID, LANGUAGE_LIST
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


@router.message(Command('help'))
async def cmd_help(message: Message):
    await message.answer(messages.HELP)


@router.message(Command('github'))
async def cmd_github(message: Message):
    await message.answer(messages.GITHUB_URL)


@router.message(Command('feedback'))
async def get_feedback(message: Message, state: FSMContext):
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


@router.callback_query(F.data.in_(LANGUAGE_LIST))
async def start_studying(callback: CallbackQuery, state: FSMContext):
    language = callback.data
    tg_user_id = callback.from_user.id

    await state.set_state(BotStates.starting)
    await state.update_data(language=language)
    await state.update_data(tg_user_id=tg_user_id)

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


@router.callback_query(F.data.in_({'yes', 'no'}), BotStates.starting)
async def set_progress(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    tg_user_id = state_data['tg_user_id']
    language = state_data['language']

    if callback.data == 'yes':
        last_completed_lesson = await test_the_user(tg_user_id, language)
    elif callback.data == 'no':
        last_completed_lesson = 0
        description = await get_description(language)
        await callback.answer(text=description, show_alert=True)

    await create_progress(tg_user_id, language, last_completed_lesson)
    await _continue_studying(tg_user_id, language, state)


@router.callback_query(F.data == 'reset', BotStates.starting)
async def reset(callback: CallbackQuery, state: FSMContext):
    state_data = await state.get_data()
    tg_user_id = state_data['tg_user_id']
    language = state_data['language']
    last_completed_lesson = 0
    await update_progress(tg_user_id, language, last_completed_lesson)
    await _continue_studying(tg_user_id, language, state)
    await callback.answer()


async def test_the_user(tg_user_id: int, language: str):
    pass


@router.message(Command('continue'))
async def cmd_continue(message: Message, state: FSMContext):
    """
    Check if progress exists in several languages

     - Notify user if progress not found
     - Form data and call _continue_studying if progress is only one
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
        await _continue_studying(tg_user_id, language, state)
    else:
        await message.answer(messages.WHICH_LANGUAGE,
                             reply_markup=keyboards.create_kb(progresses))


@router.callback_query(F.data == 'continue')
async def callback_continue(callback: CallbackQuery, state: FSMContext):
    """Form data and call _continue_studying."""

    state_data = await state.get_data()
    tg_user_id = state_data['tg_user_id']
    language = state_data['language']
    await _continue_studying(tg_user_id, language, state)
    await callback.answer()


async def _continue_studying(tg_user_id: int, language: str,
                             state: FSMContext):
    """
    Takes an user id and a language as inputs.
    Defines last completed lesson for this user in this language.
    Sends next lesson information, first question and provides with multiple
    options choice keyboard.
    """

    last_completed_lesson = await get_progress(tg_user_id, language)
    lesson = await get_lesson(language, last_completed_lesson)
    if lesson.get('title') is None:
        await bot.send_message(chat_id=tg_user_id,
                               text=messages.FINISH)
        await state.clear()

    else:
        await bot.send_message(chat_id=tg_user_id,
                               text=str(lesson.get('title')))

        questions = lesson.get('questions_of_lesson')
        first_question = questions[0]
        question_text = first_question.get('text')
        options = [
            first_question.get('answer1'),
            first_question.get('answer2'),
            first_question.get('answer3')
        ]
        correct_option = first_question.get('correct_answer')

        await state.set_state(BotStates.studying)
        await state.update_data(tg_user_id=tg_user_id)
        await state.update_data(language=language)
        await state.update_data(last_completed_lesson=last_completed_lesson)
        await state.update_data(questions=questions)
        await state.update_data(current_question=0)
        await state.update_data(correct_option=correct_option)

        await bot.send_message(chat_id=tg_user_id, text=question_text,
                               reply_markup=keyboards.create_kb(options))


@router.callback_query(BotStates.studying)
async def continue_studying_callback(callback: CallbackQuery,
                                     state: FSMContext):
    """
    Send questions to user.
    After last question calls _continue_studying for the next lesson.
    """

    state_data = await state.get_data()
    correct_option = state_data['correct_option']

    if callback.data != correct_option:
        await callback.answer(text=messages.TRY_AGAIN,
                              show_alert=True)
    else:
        current_question_num = state_data['current_question'] + 1
        questions = state_data['questions']

        if current_question_num < len(questions):
            await state.update_data(current_question=current_question_num)
            current_question = questions[current_question_num]
            question_text = current_question.get('text')
            options = [
                current_question.get('answer1'),
                current_question.get('answer2'),
                current_question.get('answer3')
            ]
            correct_option = current_question.get('correct_answer')
            await state.update_data(correct_option=correct_option)
            await state.update_data(current_question=current_question_num)

            await callback.message.answer(
                text=question_text,
                reply_markup=keyboards.create_kb(options)
            )
        else:
            tg_user_id = state_data['tg_user_id']
            language = state_data['language']
            last_completed_lesson = state_data['last_completed_lesson'] + 1

            await update_progress(tg_user_id, language, last_completed_lesson)
            await _continue_studying(tg_user_id, language, state)

    await callback.answer()
