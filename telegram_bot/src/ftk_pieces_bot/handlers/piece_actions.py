from aiogram import Router
from aiogram.utils.deep_linking import decode_payload
from aiogram.filters import Command, CommandObject
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from states import SetActiveStudentState
from keyboards.students import get_kb_set_active_student

piece_action_router = Router()


@piece_action_router.message(Command("newaction"))
async def handler(message: Message):
    await message.answer(f"Your payload: {args}\nID: {message.from_user.id}")
