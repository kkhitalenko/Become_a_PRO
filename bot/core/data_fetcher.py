import aiohttp

from core import endpoints


async def get_description(language):
    async with aiohttp.ClientSession() as session:
        async with session.get(endpoints.LANGUAGES+language+'/') as response:
            res = await response.json()
            return res.get('description')
