from aiogram.filters.callback_data import CallbackData
from aiogram.types import List
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_continue_repeat_reset_kb(language: str):
    """Returns the keyboard with 'continue', 'repeat' and 'reset' buttons."""

    kb = InlineKeyboardBuilder()
    kb.button(text='продолжить', callback_data=f'continue_{language}')
    kb.button(text='повторить', callback_data=f'repeat_{language}')
    kb.button(text='начать заново', callback_data=f'reset_{language}')
    return kb.as_markup()


def create_kb(buttons: List[str]):
    """Receive a list of buttons and returns a keyboard with those buttons."""

    kb = InlineKeyboardBuilder()
    for btn in buttons:
        kb.button(text=btn.title(), callback_data=btn)
    return kb.as_markup()


class LanguagesRepeatCbData(CallbackData, prefix='repeat', sep='_'):
    language: str


def create_languages_kb(language_list: List[str]):
    """Returns the keyboard with language buttons and prefix='repeat'."""

    kb = InlineKeyboardBuilder()
    for language in language_list:
        cbdata = LanguagesRepeatCbData(language=language)
        kb.button(text=language.title(), callback_data=cbdata.pack())
    return kb.as_markup()
