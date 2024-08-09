from typing import Optional, Set

from config import LANGUAGE_LIST
from core import bot_storage, endpoints


async def get_description(language: str) -> str:
    """Returns language description."""

    async with bot_storage['session'].get(
        f'{endpoints.LANGUAGES}{language}/'
    ) as resp:
        result = await resp.json()
        return result.get('description')


async def create_progress(tg_user_id: int, language: str,
                          last_completed_lesson: int) -> int:
    """Sending Django progress creation request. Returns status code."""

    payload = {'tg_user_id': tg_user_id, 'language': language,
               'last_completed_lesson': last_completed_lesson}
    async with bot_storage['session'].post(
        endpoints.PROGRESS, data=payload
    ) as resp:
        return resp.status


async def get_progress(tg_user_id: int, language: str) -> Optional[int]:
    """Returns lesson number if progress exists. Otherwise returns None."""

    progress_url = f'{endpoints.PROGRESS}{language}_{tg_user_id}/'
    async with bot_storage['session'].get(progress_url) as resp:
        result = await resp.json()
        return result.get('last_completed_lesson')


async def get_progress_list(tg_user_id: int) -> list:
    """Returns list of existing progress."""

    progresses = []
    for language in LANGUAGE_LIST:
        progress = await get_progress(tg_user_id, language)
        if progress is not None:
            progresses.append(language)
    return progresses


async def update_progress(tg_user_id: int, language: str,
                          last_completed_lesson: int,
                          wrong_answers: Optional[Set[int]] = None) -> int:
    """Sending Django progress updating request. Returns status code."""

    progress = f'{language}_{tg_user_id}'
    payload = {'last_completed_lesson': last_completed_lesson}
    if wrong_answers:
        payload['wrong_answers'] = list(wrong_answers)
    async with bot_storage['session'].patch(f'{endpoints.PROGRESS}{progress}/',
                                            data=payload) as resp:
        return resp.status


async def get_lesson(language: str, last_completed_lesson: int):
    """Returns json including theory and list of questions."""

    async with bot_storage['session'].get(
        f'{endpoints.LESSONS}{language}/{last_completed_lesson+1}/',
    ) as resp:
        return await resp.json()


async def get_wrong_answered_questions(tg_user_id: int, language: str):
    """Returns json including wrong answered questions."""

    async with bot_storage['session'].get(
        f'{endpoints.PROGRESS}{language}_{tg_user_id}/'
        f'wrong_answered_questions/',
    ) as resp:
        return await resp.json()


async def update_wrong_answered_questions(tg_user_id: int, language: str,
                                          wrong_answers: Optional[Set[int]]):
    """Sending Django progress updating request. Returns status code."""

    payload = {}
    if wrong_answers:
        payload['wrong_answers'] = list(wrong_answers)

    async with bot_storage['session'].patch(
        f'{endpoints.PROGRESS}{language}_{tg_user_id}/'
        f'wrong_answered_questions/', data=payload
    ) as resp:
        return resp.status
