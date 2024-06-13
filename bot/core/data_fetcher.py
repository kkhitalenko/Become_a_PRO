import aiohttp

from core import endpoints


async def get_description(language):
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{endpoints.LANGUAGES}{language}/') as resp:
            result = await resp.json()
            return result.get('description')


async def create_user(user_id, username):
    async with aiohttp.ClientSession() as session:
        payload = {'user_id': user_id, 'username': username}
        async with session.post(endpoints.CREATE_USER, data=payload) as resp:
            return resp.status
