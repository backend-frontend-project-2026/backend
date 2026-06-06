from collections.abc import Mapping
from typing import Any, Optional, Sequence

from generics import get_filled_type
from pydantic import BaseModel as PydanticBaseModel
from sqlalchemy import func
from sqlalchemy.sql._typing import (
    _ColumnExpressionArgument,
)
from sqlmodel import and_, select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.dependencies.session import SessionDep
from app.models.base import BaseModel

type FilterType = _ColumnExpressionArgument[bool] | bool


class Repository[Model: BaseModel]:
    _model: type[Model] | None = None
    _session: AsyncSession

    @property
    def model(self) -> type[Model]:
        if self._model is None:
            self._model = get_filled_type(self, Repository, 0)
        return self._model

    @property
    def session(self) -> AsyncSession:
        return self._session

    def __init__(self, session: SessionDep):
        self._session = session

    async def get(self, pk: int) -> Optional[Model]:
        return await self._session.get(self.model, pk)

    def _build_filter_statement(
        self, filters: Optional[PydanticBaseModel] = None
    ) -> FilterType:
        filter_statement: FilterType = and_(True)
        if filters is None:
            return filter_statement

        filters_dict = filters.model_dump(exclude_none=True)

        for key, value in filters_dict.items():
            if key.endswith('_min'):
                column_name = key.removesuffix('_min')
                if hasattr(self.model, column_name):
                    filter_statement = and_(
                        filter_statement,
                        getattr(self.model, column_name) >= value,
                    )
                continue

            if key.endswith('_max'):
                column_name = key.removesuffix('_max')
                if hasattr(self.model, column_name):
                    filter_statement = and_(
                        filter_statement,
                        getattr(self.model, column_name) <= value,
                    )
                continue

            if key.endswith('_from'):
                column_name = f'{key.removesuffix("_from")}_at'
                if hasattr(self.model, column_name):
                    filter_statement = and_(
                        filter_statement,
                        getattr(self.model, column_name) >= value,
                    )
                continue

            if key.endswith('_to'):
                column_name = f'{key.removesuffix("_to")}_at'
                if hasattr(self.model, column_name):
                    filter_statement = and_(
                        filter_statement,
                        getattr(self.model, column_name) <= value,
                    )
                continue

            if hasattr(self.model, key):
                filter_statement = and_(
                    filter_statement,
                    getattr(self.model, key) == value,
                )

        return filter_statement

    async def fetch(
        self,
        filters: Optional[PydanticBaseModel] = None,
        offset: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> Sequence[Model]:
        select_statement = select(self.model)

        if filters is not None:
            select_statement = select_statement.where(
                self._build_filter_statement(filters)
            )

        if offset is not None:
            select_statement = select_statement.offset(offset)

        if limit is not None:
            select_statement = select_statement.limit(limit)

        entities = await self._session.execute(select_statement)
        return entities.scalars().all()

    async def count(self, filters: Optional[PydanticBaseModel] = None) -> int:
        select_statement = select(func.count()).select_from(self.model)

        if filters is not None:
            select_statement = select_statement.where(
                self._build_filter_statement(filters)
            )

        result = await self._session.execute(select_statement)
        return result.scalar_one()

    async def save(self, instance: Model) -> Model:
        self._session.add(instance)
        await self._session.commit()
        await self._session.refresh(instance)
        return instance

    async def save_all(self, instances: list[Model]) -> list[Model]:
        self._session.add_all(instances)
        await self._session.commit()

        for instance in instances:
            await self._session.refresh(instance)

        return instances

    async def delete(self, pk: int) -> Optional[Model]:
        instance = await self.get(pk)

        if instance is None:
            return instance

        await self._session.delete(instance)
        await self._session.commit()

        return instance

    async def update(
        self,
        pk: int,
        updates: PydanticBaseModel | Mapping[str, Any],
    ) -> Optional[Model]:
        instance = await self.get(pk)

        if instance is None:
            return None

        if isinstance(updates, PydanticBaseModel):
            instance_update_dump = updates.model_dump(exclude_unset=True)
        else:
            instance_update_dump = dict(updates)

        for key, value in instance_update_dump.items():
            if hasattr(instance, key):
                setattr(instance, key, value)

        await self.save(instance)
        return instance

    async def add_without_commit(self, item: Model) -> Model:
        self._session.add(item)
        await self._session.flush()
        await self._session.refresh(item)
        return item

    async def commit(self) -> None:
        await self._session.commit()

    async def rollback(self) -> None:
        await self._session.rollback()
