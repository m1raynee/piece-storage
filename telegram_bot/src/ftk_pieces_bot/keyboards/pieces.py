from typing import Callable
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder
from aiogram.types import (
    User,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    ReplyKeyboardMarkup,
    InlineQueryResultArticle,
    InputTextMessageContent,
)

piece_fields = ("name", "article", "alt_name", "box__name")


def get_kb_piece_attributes() -> ReplyKeyboardMarkup:
    builder = ReplyKeyboardBuilder()

    for field in piece_fields:
        builder.button(text=f"По {field}")
    return builder.adjust(2).as_markup(is_persistent=True, resize_keyboard=True, one_time_keyboard=True)  # type: ignore


kb_inliner = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Выбрать пользователя",
                switch_inline_query_current_chat="",
            )
        ]
    ]
)

inline_query_search_empty = [
    InlineQueryResultArticle(
        id="-1",
        title="Введите запрос...",
        description='Попробуйте "штифт" или "балка". Чтобы отменить, выберите этот пункт.',
        input_message_content=InputTextMessageContent(message_text="Отмена"),
    )
]


def get_inline_pieces(pieces: list[dict]) -> list[InlineQueryResultArticle]:
    if not pieces:
        return [
            InlineQueryResultArticle(
                id="-1",
                title="Нет совпадений...",
                input_message_content=InputTextMessageContent(
                    message_text=f"Нет совпадений",
                ),
                description="Измените запрос или создайте новую деталь",
            )
        ]

    items = []
    for item in pieces:
        items.append(
            InlineQueryResultArticle(
                id=f"PCE-{item['id']}",
                title=item["name"],
                input_message_content=InputTextMessageContent(
                    message_text=f"{item['name']} (PCE-{item['id']})",
                ),
                description=f"(PCE-{item['id']}) всего: {item['amount']} в BOX-{item['box_id']}",
            )
        )

    return items
