from datetime import datetime
from pydantic import BaseModel

from ftk_pieces_api.database.models import ActionType
from .base import Serializable


class _PieceActionBase(BaseModel):
    piece_id: int
    performer_id: int
    requester_id: int
    type_id: ActionType
    created_at: datetime
    until: datetime | None
    description: str | None


class In(_PieceActionBase):
    ...


class Out(_PieceActionBase, Serializable):
    ...


class Modify(_PieceActionBase):
    ...
