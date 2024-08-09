from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN


bot_storage = {}
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
