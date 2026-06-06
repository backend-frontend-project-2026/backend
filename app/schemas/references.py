from pydantic import BaseModel


class ReferenceOption(BaseModel):
    value: str
    label: str


class ReferenceListResponse(BaseModel):
    items: list[ReferenceOption]
