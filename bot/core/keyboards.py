from aiogram.types import List
from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_langeages_kb():
    """Returns the keyboard with 'Python', 'Go' and 'Rust' buttons."""

    kb = InlineKeyboardBuilder()
    kb.button(text='Python', callback_data='python')
    kb.button(text='Go', callback_data='go')
    kb.button(text='Rust', callback_data='rust')
    return kb.as_markup()


def get_yes_no_kb():
    """Returns the keyboard with 'yes' and 'no' buttons."""

    kb = InlineKeyboardBuilder()
    kb.button(text='да', callback_data='yes')
    kb.button(text='нет', callback_data='no')
    return kb.as_markup()


def get_continue_or_reset_kb():
    """Returns the keyboard with 'continue' and 'reset' buttons."""

    kb = InlineKeyboardBuilder()
    kb.button(text='продолжить', callback_data='continue')
    kb.button(text='начать заново', callback_data='reset')
    return kb.as_markup()


def create_kb(buttons: List[str]):
    """Receive a list of buttons and returns a keyboard with those buttons."""

    kb = InlineKeyboardBuilder()
    for btn in buttons:
        kb.button(text=btn.title(), callback_data=btn)
    return kb.as_markup()
