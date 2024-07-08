import aiohttp

from core import endpoints


async def get_description(language: str) -> str:
    """Returns language description."""

    async with aiohttp.ClientSession() as session:
        async with session.get(f'{endpoints.LANGUAGES}{language}/') as resp:
            result = await resp.json()
            return result.get('description')


async def create_progress(tg_user_id: int, language: str,
                          last_completed_lesson: int) -> int:
    """Sending Django progress creation request. Returns status code."""

    async with aiohttp.ClientSession() as session:
        payload = {'tg_user_id': tg_user_id, 'language': language,
                   'last_completed_lesson': last_completed_lesson}
        async with session.post(endpoints.PROGRESS, data=payload) as resp:
            return resp.status


async def check_progress(tg_user_id: int, language: str) -> bool:
    """Returns True if progress exists. Otherwise returns False."""

    async with aiohttp.ClientSession() as session:
        progress_url = f'{endpoints.PROGRESS}{language}_{tg_user_id}/'
        async with session.get(progress_url) as resp:
            if resp.status == 200:
                return True
            elif resp.status == 404:
                return False


async def update_progress(tg_user_id: int, language: str,
                          last_completed_lesson: int) -> int:
    """Sending Django progress updating request. Returns status code."""

    async with aiohttp.ClientSession() as session:
        progress = f'{language}_{tg_user_id}'
        payload = {'last_completed_lesson': last_completed_lesson}
        async with session.patch(f'{endpoints.PROGRESS}{progress}/',
                                 data=payload) as resp:
            return resp.status
