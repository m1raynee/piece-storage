import re

import aiohttp
from aiogram import Router, types, filters
from aiogram.fsm.context import FSMContext

from states import SetActiveStudentState
from keyboards.students import get_kb_set_active_student, get_inline_students


students_router = Router()

stu_regex = re.compile(r"\(STU-(\d+)\)")


@students_router.message(filters.Command("setactive"))
async def set_active_student(message: types.Message, state: FSMContext):
    await state.set_state(SetActiveStudentState.name)
    await message.answer(
        "Пожалуйста, выберите пользователя",
        reply_markup=get_kb_set_active_student(message.from_user),
    )


@students_router.inline_query(SetActiveStudentState.name)
async def inline_student_search(inline_query: types.InlineQuery):
    query = {"name": inline_query.query, "size": "20"}

    async with aiohttp.ClientSession("http://localhost:8000") as session:
        async with session.request("GET", "/students/", params=query) as req:
            req.raise_for_status()
            data = await req.json()

    items = get_inline_students(data["items"])

    await inline_query.answer(items, cache_time=1)


@students_router.message(SetActiveStudentState.name)
async def set_result(message: types.Message, state: FSMContext):
    await state.clear()

    if message.text is None or (m := stu_regex.search(message.text)) is None:
        return await message.answer("Отправьте сообщение из инлайна")
    if message.text.startswith("Нет совпадений"):
        return await message.answer("Таких пользователей нет")

    student_id = m.groups()[0]

    async with aiohttp.ClientSession("http://localhost:8000") as session:
        async with session.get(f"/students/{student_id}/") as req:
            req.raise_for_status()

    await state.update_data({"perform_id": student_id})
    await message.answer(f"Активный пользователь сменён на: {message.text}")
