from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_langeages_kb():
    """Returns the keyboard with 'Python', 'Go' and 'Rust' buttons."""

    languages = InlineKeyboardBuilder()
    languages.button(text='Python', callback_data='python')
    languages.button(text='Go', callback_data='go')
    languages.button(text='Rust', callback_data='rust')
    return languages.as_markup()


def get_yes_no_kb():
    """Returns the keyboard with 'yes' and 'no' buttons."""

    yes_no = InlineKeyboardBuilder()
    yes_no.button(text='да', callback_data='да')
    yes_no.button(text='нет', callback_data='нет')
    return yes_no.as_markup()


def get_continue_or_reset_kb():
    """Returns the keyboard with 'continue' and 'reset' buttons."""

    yes_no = InlineKeyboardBuilder()
    yes_no.button(text='продолжить', callback_data='continue')
    yes_no.button(text='начать заново', callback_data='reset')
    return yes_no.as_markup()
