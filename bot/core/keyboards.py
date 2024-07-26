from aiogram.filters.callback_data import CallbackData
from aiogram.types import List
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_yes_no_kb():
    """Returns the keyboard with 'yes' and 'no' buttons."""

    kb = InlineKeyboardBuilder()
    kb.button(text='да', callback_data='yes')
    kb.button(text='нет', callback_data='no')
    return kb.as_markup()


def get_continue_repeat_reset_kb():
    """Returns the keyboard with 'continue', 'repeat' and 'reset' buttons."""

    kb = InlineKeyboardBuilder()
    kb.button(text='продолжить', callback_data='continue')
    kb.button(text='повторить', callback_data='repeat')
    kb.button(text='начать заново', callback_data='reset')
    return kb.as_markup()


def create_kb(buttons: List[str]):
    """Receive a list of buttons and returns a keyboard with those buttons."""

    kb = InlineKeyboardBuilder()
    for btn in buttons:
        kb.button(text=btn.title(), callback_data=btn)
    return kb.as_markup()


class LanguagesRepeatCbData(CallbackData, prefix='repeat'):
    language: str


def create_languages_kb(language_list: List[str]):
    """Returns the keyboard with language buttons and prefix='repeat'."""

    kb = InlineKeyboardBuilder()
    for language in language_list:
        cbdata = LanguagesRepeatCbData(language=language)
        kb.button(text=language.title(), callback_data=cbdata.pack())
    return kb.as_markup()
