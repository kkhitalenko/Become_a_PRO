import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from config import TOKEN
from core.commands import set_commands


dp = Dispatcher(storage=MemoryStorage())
bot = Bot(token=TOKEN)


async def main():
    from core.handlers.studying_handlers import router as studying_router
    from core.handlers.common_handlers import router as common_router

    dp.include_routers(common_router, studying_router)
    await set_commands(bot)
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
