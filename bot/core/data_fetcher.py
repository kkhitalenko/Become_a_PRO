import aiohttp

from core import endpoints


async def get_description(language: str):
    """Returns language description."""
    async with aiohttp.ClientSession() as session:
        async with session.get(f'{endpoints.LANGUAGES}{language}/') as resp:
            result = await resp.json()
            return result.get('description')


async def create_progress(tg_user_id: int, language: str,
                          last_completed_lesson: int):
    """Sending Django progress creation request. Returns status code."""
    async with aiohttp.ClientSession() as session:
        payload = {'tg_user_id': tg_user_id, 'language': language,
                   'last_completed_lesson': last_completed_lesson}
        async with session.post(endpoints.PROGRESS, data=payload) as resp:
            return resp.status
