from aiogram.utils.keyboard import InlineKeyboardBuilder


def get_commands_kb():
    """Returns the keyboard with existing commands."""

    commands = InlineKeyboardBuilder()
    BOT_COMMANDS = ['start', 'continue', 'reset', 'switch_mode',
                    'switch_language', 'feedback']
    for command in BOT_COMMANDS:
        commands.button(text=command, callback_data=command)
    commands.button(text='github',
                    url='https://github.com/kkhitalenko/Become_a_PRO')
    commands.adjust(3, 2, 2)
    return commands.as_markup()


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
