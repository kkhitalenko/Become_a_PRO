from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


languages = InlineKeyboardBuilder()
languages.add(InlineKeyboardButton(text='Python', callback_data='Python'))
languages.add(InlineKeyboardButton(text='Go', callback_data='Go'))
languages.add(InlineKeyboardButton(text='Rust', callback_data='Rust'))

yes_no = InlineKeyboardBuilder()
yes_no.add(InlineKeyboardButton(text='да', callback_data='да'))
yes_no.add(InlineKeyboardButton(text='нет', callback_data='нет'))
