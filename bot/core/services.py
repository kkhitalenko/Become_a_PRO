from typing import Optional, Set

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


async def get_progress(tg_user_id: int, language: str) -> Optional[int]:
    """Returns lesson number if progress exists. Otherwise returns None."""

    async with aiohttp.ClientSession() as session:
        progress_url = f'{endpoints.PROGRESS}{language}_{tg_user_id}/'
        async with session.get(progress_url) as resp:
            result = await resp.json()
            return result.get('last_completed_lesson')


async def update_progress(tg_user_id: int, language: str,
                          last_completed_lesson: int,
                          wrong_answers: Optional[Set[int]] = None) -> int:
    """Sending Django progress updating request. Returns status code."""

    async with aiohttp.ClientSession() as session:
        progress = f'{language}_{tg_user_id}'
        payload = {'last_completed_lesson': last_completed_lesson}
        if wrong_answers:
            payload['wrong_answers'] = list(wrong_answers)
        async with session.patch(f'{endpoints.PROGRESS}{progress}/',
                                 data=payload) as resp:
            return resp.status


async def get_lesson(language: str, last_completed_lesson: int):
    """Returns json including theory and list of questions."""

    async with aiohttp.ClientSession() as session:
        async with session.get(
            f'{endpoints.LESSONS}{language}/{last_completed_lesson+1}/',
        ) as resp:
            return await resp.json()
