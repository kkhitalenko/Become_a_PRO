from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder


languages_builder = InlineKeyboardBuilder()
languages_builder.row(types.InlineKeyboardButton(
    text='Python', url='http://127.0.0.1:8000/api/v1/topics/'
))
languages_builder.row(types.InlineKeyboardButton(
    text='Go', url='http://127.0.0.1:8000/api/v1/topics/'
))
languages_builder.row(types.InlineKeyboardButton(
    text='Rust', url='http://127.0.0.1:8000/api/v1/topics/'
))
