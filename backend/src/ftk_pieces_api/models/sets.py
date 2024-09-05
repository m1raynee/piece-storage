from pydantic import BaseModel
from .base import Serializable


class _SetBase(BaseModel):
    name: str
    code: int | None
    place_code: str | None


class In(_SetBase):
    ...


class Out(_SetBase, Serializable):
    ...


class Modify(_SetBase):
    ...
