import re

import aiohttp
from aiogram import Router, types, filters
from aiogram.fsm.context import FSMContext

from states import InlinePieceSearch
from keyboards.pieces import (
    get_kb_piece_attributes,
    piece_fields,
    kb_inliner,
    inline_query_search_empty,
    get_inline_pieces,
)

pieces_router = Router()
pce_regex = re.compile(r"\(PCE-(\d+)\)")


@pieces_router.message(filters.Command("pieces"))
async def pieces_list(message: types.Message, state: FSMContext):
    await state.set_state(InlinePieceSearch.type_choosing)
    await message.answer(
        "Как будем искать деталь?", reply_markup=get_kb_piece_attributes()
    )


@pieces_router.message(
    lambda message: message.text[3:] in piece_fields, InlinePieceSearch.type_choosing
)
async def piece_list_type_chosen(message: types.Message, state: FSMContext):
    assert message.text is not None

    await state.set_state(InlinePieceSearch.search)
    await state.set_data({"piece_search": message.text[3:]})
    await message.answer(f"Ищем деталь по {message.text[3:]}", reply_markup=kb_inliner)


@pieces_router.inline_query(InlinePieceSearch.search)
async def piece_list_inline_query(inline_query: types.InlineQuery, state: FSMContext):
    if not inline_query.query:
        return await inline_query.answer(inline_query_search_empty, cache_time=1)

    field = (await state.get_data())["piece_search"]

    params = {field: inline_query.query, "size": 10}

    async with aiohttp.ClientSession("http://localhost:8000") as session:
        async with session.request("GET", "/pieces", params=params) as req:
            req.raise_for_status()
            data = await req.json()

    await inline_query.answer(get_inline_pieces(data["items"]))


@pieces_router.message(InlinePieceSearch.search)
async def inline_query_serch_final(message: types.Message, state: FSMContext):
    await state.set_state()
    if message.text in ("Нет совпадений", "Отмена"):
        return await message.answer("Поиск детали отменён")
    if message.text is None or (m := pce_regex.search(message.text)) is None:
        return await message.answer("Отправьте сообщение из инлайна")

    piece_id = m.groups()[0]

    async with aiohttp.ClientSession("http://localhost:8000") as session:
        async with session.get(f"/pieces/{piece_id}") as req:
            req.raise_for_status()
            data = await req.json()

    await message.answer(str(data))

