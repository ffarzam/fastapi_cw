from pydantic import BaseModel


class BookInput(BaseModel):
    name: str
    price: float


class BookOutput(BookInput):
    id: str


