from aiogram import Dispatcher


from core.handlers.chats import router as chats_router


def register_routers(dp: Dispatcher):
    dp.include_router(chats_router)
