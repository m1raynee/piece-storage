from typing import Any
from pydantic import BaseModel

class PageData(BaseModel):
    items: list[dict[str, Any]]
    total: int
    page: int
    size: int
    pages: int
    endpoint: str | None

def get_paginator(data: PageData)