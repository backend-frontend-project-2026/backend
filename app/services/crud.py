from typing import Any, Generic, Optional, TypeVar

from pydantic import BaseModel

from app.models.base import BaseModel as DbBaseModel
from app.schemas.base import CommonListFilters
from app.utils.repository import Repository

ModelT = TypeVar('ModelT', bound=DbBaseModel)
CreateT = TypeVar('CreateT', bound=BaseModel)
UpdateT = TypeVar('UpdateT', bound=BaseModel)
ResponseT = TypeVar('ResponseT', bound=BaseModel)
ListResponseT = TypeVar('ListResponseT', bound=BaseModel)
FiltersT = TypeVar('FiltersT', bound=CommonListFilters)


class CrudService(
    Generic[ModelT, CreateT, UpdateT, ResponseT, ListResponseT, FiltersT]
):
    def __init__(
        self,
        repository: Repository[ModelT],
        response_type: type[ResponseT],
        list_response_type: type[ListResponseT],
    ):
        self._repository = repository
        self._response_type = response_type
        self._list_response_type = list_response_type

    def _to_response(self, item: ModelT) -> ResponseT:
        return self._response_type.model_validate(item)

    def _prepare_create_data(
        self, payload: CreateT, **extra_data: Any
    ) -> dict[str, Any]:
        return {**payload.model_dump(), **extra_data}

    def _prepare_update_data(self, payload: UpdateT) -> dict[str, Any]:
        return payload.model_dump(exclude_unset=True)

    async def get_list(self, filters: FiltersT) -> ListResponseT:
        items = await self._repository.fetch(
            filters=filters,
            offset=filters.offset,
            limit=filters.limit,
        )
        total = await self._repository.count(filters=filters)
        return self._list_response_type(
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

    async def create(self, payload: CreateT, **extra_data: Any) -> ResponseT:
        item = self._repository.model(
            **self._prepare_create_data(payload, **extra_data)
        )
        saved_item = await self._repository.save(item)
        return self._to_response(saved_item)

    async def update(self, item_id: int, payload: UpdateT) -> Optional[ResponseT]:
        updated_item = await self._repository.update(
            item_id, self._prepare_update_data(payload)
        )
        if updated_item is None:
            return None
        return self._to_response(updated_item)

    async def delete(self, item_id: int) -> Optional[ResponseT]:
        item = await self._repository.delete(item_id)
        if item is None:
            return None
        return self._to_response(item)
