from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies.services import TagServiceDep
from app.schemas.tags import (
    TagCreate,
    TagFilters,
    TagListResponse,
    TagResponse,
    TagUpdate,
)

router = APIRouter(prefix='/tags', tags=['Tags'])


@router.get('', response_model=TagListResponse)
async def list_tags(
    tag_service: TagServiceDep,
    filters: Annotated[TagFilters, Depends()],
) -> TagListResponse:
    return await tag_service.get_list(filters)


@router.get('/{tag_id}', response_model=TagResponse)
async def get_tag(
    tag_id: int,
    tag_service: TagServiceDep,
) -> TagResponse:
    tag = await tag_service.get_by_id(tag_id)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return tag


@router.post('', response_model=TagResponse, status_code=status.HTTP_201_CREATED)
async def create_tag(
    tag_create: TagCreate,
    tag_service: TagServiceDep,
) -> TagResponse:
    return await tag_service.create(tag_create)


@router.put('/{tag_id}', response_model=TagResponse)
async def update_tag(
    tag_id: int,
    tag_update: TagUpdate,
    tag_service: TagServiceDep,
) -> TagResponse:
    tag = await tag_service.update(tag_id, tag_update)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return tag


@router.delete('/{tag_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_tag(
    tag_id: int,
    tag_service: TagServiceDep,
) -> Response:
    tag = await tag_service.delete(tag_id)
    if tag is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail='Not found')
    return Response(status_code=status.HTTP_204_NO_CONTENT)
