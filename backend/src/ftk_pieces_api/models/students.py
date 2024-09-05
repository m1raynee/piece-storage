from pydantic import BaseModel
from .base import Serializable


class _StudentBase(BaseModel):
    first_name: str
    middle_name: str
    last_name: str


class In(_StudentBase):
    ...


class Out(_StudentBase, Serializable):
    ...


class Modify(_StudentBase):
    ...
