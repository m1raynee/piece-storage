import re
from datetime import datetime
from enum import IntEnum
import sqlalchemy as sql
from sqlalchemy import orm

from .base import Base


class ActionType(IntEnum):
    lost = -1
    stored = 0
    taken = 1


class Set(Base):
    name: orm.Mapped[str]
    place_code: orm.Mapped[str | None]

    pieces: orm.Mapped[list["Piece"]] = orm.relationship(back_populates="set")


class Piece(Base):
    article: orm.Mapped[int | None]
    name: orm.Mapped[str]
    description: orm.Mapped[str]
    set_number: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("sets.number"))

    set: orm.Mapped[Set] = orm.relationship(back_populates="pieces")
    actions: orm.Mapped[list["PieceAction"]] = orm.relationship(back_populates="piece")


class PieceAction(Base):
    piece_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("pieces.id"))
    performer_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("students.id"))
    requester_id: orm.Mapped[int] = orm.mapped_column(sql.ForeignKey("students.id"))
    type: orm.Mapped[ActionType]
    created_at: orm.Mapped[datetime] = orm.mapped_column(default=sql.func.now())
    until: orm.Mapped[datetime | None]
    description: orm.Mapped[str | None]

    piece: orm.Mapped[Piece] = orm.relationship(back_populates="actions")
    performer: orm.Mapped["Student"] = orm.relationship(
        back_populates="actions_performed", foreign_keys=[performer_id]
    )
    requester: orm.Mapped["Student"] = orm.relationship(
        back_populates="actions", foreign_keys=[requester_id]
    )


class Student(Base):
    first_name: orm.Mapped[str]
    last_name: orm.Mapped[str]
    middle_name: orm.Mapped[str]

    actions_performed: orm.Mapped[list["PieceAction"]] = orm.relationship(
        back_populates="performer", foreign_keys=[PieceAction.performer_id]
    )
    actions: orm.Mapped[list["PieceAction"]] = orm.relationship(
        back_populates="requester", foreign_keys=[PieceAction.requester_id]
    )
