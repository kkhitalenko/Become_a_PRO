import asyncio
import logging

import aiohttp

from core import bot, bot_storage, dp
from core.commands import set_commands
from core.handlers import main_router


async def main():
    bot_storage['session'] = aiohttp.ClientSession()
    async with bot_storage['session']:
        dp.include_router(main_router)
        await set_commands(bot)
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(bot)


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())
