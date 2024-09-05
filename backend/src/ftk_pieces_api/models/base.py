from pydantic import BaseModel


class Serializable(BaseModel):
    id: int
