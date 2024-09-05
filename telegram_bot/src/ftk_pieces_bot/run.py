import os
import logging

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from handlers.start import start_router
from handlers.piece_actions import piece_action_router
from handlers.students import students_router
from handlers.pieces import pieces_router

print(os.environ)
bot = Bot(os.getenv("BOT_TOKEN"))

dp = Dispatcher(storage=MemoryStorage())
dp.include_router(start_router)
# dp.include_router(piece_action_router)
dp.include_router(students_router)
dp.include_router(pieces_router)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    dp.run_polling(bot, allowed_updates=[])
