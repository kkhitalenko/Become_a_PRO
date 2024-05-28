from aiogram.types import InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder


languages_builder = InlineKeyboardBuilder()
languages_builder.add(InlineKeyboardButton(text='Python',
                                           callback_data='Python'))
languages_builder.add(InlineKeyboardButton(text='Go', callback_data='Go'))
languages_builder.add(InlineKeyboardButton(text='Rust', callback_data='Rust'))
