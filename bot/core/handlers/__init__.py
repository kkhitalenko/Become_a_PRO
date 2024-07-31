from aiogram import Router

from core.handlers.common_handlers import router as common_router
from core.handlers.repeating_handlers import router as repeat_router
from core.handlers.studying_handlers import router as study_router


main_router = Router()
main_router.include_routers(common_router, study_router, repeat_router)
