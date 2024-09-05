from pydantic import BaseModel
from .base import Serializable


class _PieceBase(BaseModel):
    article: int | None
    name: str
    description: str
    set_id: int


class In(_PieceBase):
    ...


class Out(_PieceBase, Serializable):
    ...


class Modify(_PieceBase):
    ...
