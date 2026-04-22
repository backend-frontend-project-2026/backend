from typing import Generic, Optional, TypeVar

from pydantic import BaseModel

from app.models.base import BaseModel as DbBaseModel
from app.schemas.base import CommonListFilters, PaginatedResponse
from app.utils.repository import Repository

ModelT = TypeVar('ModelT', bound=DbBaseModel)
CreateT = TypeVar('CreateT', bound=BaseModel)
UpdateT = TypeVar('UpdateT', bound=BaseModel)
ResponseT = TypeVar('ResponseT', bound=BaseModel)
FiltersT = TypeVar('FiltersT', bound=CommonListFilters)


class CrudService(Generic[ModelT, CreateT, UpdateT, ResponseT, FiltersT]):
    def __init__(
        self,
        repository: Repository[ModelT],
        response_type: type[ResponseT],
    ):
        self._repository = repository
        self._response_type = response_type

    def _to_response(self, item: ModelT) -> ResponseT:
        return self._response_type.model_validate(item)

    async def get_list(self, filters: FiltersT) -> PaginatedResponse[ResponseT]:
        items = await self._repository.fetch(
            filters=filters,
            offset=filters.offset,
            limit=filters.limit,
        )
        total = await self._repository.count(filters=filters)
        return PaginatedResponse[ResponseT](
            items=[self._to_response(item) for item in items],
            total=total,
            page=filters.page,
            page_size=filters.page_size,
        )

    async def get_by_id(self, item_id: int) -> Optional[ResponseT]:
        item = await self._repository.get(item_id)
        if item is None:
            return None
        return self._to_response(item)

    async def create(self, payload: CreateT) -> ResponseT:
        item = self._repository.model(**payload.model_dump())
        saved_item = await self._repository.save(item)
        return self._to_response(saved_item)

    async def update(self, item_id: int, payload: UpdateT) -> Optional[ResponseT]:
        item = await self._repository.get(item_id)
        if item is None:
            return None

        for key, value in payload.model_dump(exclude_unset=True).items():
            if hasattr(item, key):
                setattr(item, key, value)

        saved_item = await self._repository.save(item)
        return self._to_response(saved_item)

    async def delete(self, item_id: int) -> Optional[ResponseT]:
        item = await self._repository.delete(item_id)
        if item is None:
            return None
        return self._to_response(item)
