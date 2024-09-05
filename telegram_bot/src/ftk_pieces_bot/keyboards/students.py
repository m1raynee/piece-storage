from typing import Callable
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import (
    User,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    InlineQueryResultArticle,
    InputTextMessageContent,
)


def get_kb_set_active_student(user: User | None) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="Выбрать пользователя",
                switch_inline_query_current_chat=(
                    "" if user is None else user.first_name
                ),
            )
        ]]
    )


def get_inline_students(students: list[dict]) -> list[InlineQueryResultArticle]:
    items = []
    if not students:
        items = [
            InlineQueryResultArticle(
                id="-1",
                title="Нет совпадений...",
                input_message_content=InputTextMessageContent(
                    message_text=f"Нет совпадений",
                ),
                description="Попробуйте найти ещё раз или создайте нового пользователя",
            )
        ]

    for item in students:
        items.append(
            InlineQueryResultArticle(
                id=f"STU-{item['id']}",
                title=item["name"],
                input_message_content=InputTextMessageContent(
                    message_text=f"{item['name']} (STU-{item['id']})",
                ),
                description=f"(STU-{item['id']})",
            )
        )

    return items
