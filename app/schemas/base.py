from typing import Any, Generic, TypeVar

from pydantic import BaseModel, ConfigDict, Field

ItemT = TypeVar('ItemT')


class CommonListFilters(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1)

    @property
    def offset(self) -> int:
        return (self.page - 1) * self.page_size

    @property
    def limit(self) -> int:
        return self.page_size


def _strip_required(schema: dict[str, Any]) -> None:
    schema.pop('required', None)


class ApiResponseModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        json_schema_extra=_strip_required,
    )


class PaginatedResponse(ApiResponseModel, Generic[ItemT]):
    items: list[ItemT]
    total: int
    page: int
    page_size: int
