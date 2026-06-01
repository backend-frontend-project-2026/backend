from typing import Annotated

from fastapi import APIRouter, Depends, Security

from app.dependencies.auth import get_current_user
from app.dependencies.services import TagServiceDep
from app.exceptions.base import NotFoundError
from app.exceptions.responses import common_error_responses, create_error_responses
from app.models.tags import TagCreate, TagUpdate
from app.models.users import UserModel
from app.schemas.tags import (
    TagFilters,
    TagListResponse,
    TagResponse,
)

router = APIRouter(prefix='/tags', tags=['Tags'])


@router.get(
    '',
    response_model=TagListResponse,
    responses=common_error_responses,
)
async def list_tags(
    tag_service: TagServiceDep,
    filters: Annotated[TagFilters, Depends()],
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['references:read'],
    ),
):
    return await tag_service.get_list(filters)


@router.get(
    '/{tag_id}',
    response_model=TagResponse,
    responses=common_error_responses,
)
async def get_tag(
    tag_id: int,
    tag_service: TagServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['references:read'],
    ),
):
    tag = await tag_service.get_by_id(tag_id)
    if tag is None:
        raise NotFoundError('Tag not found')
    return tag


@router.post(
    '',
    response_model=TagResponse,
    responses=create_error_responses,
)
async def create_tag(
    tag_create: TagCreate,
    tag_service: TagServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['references:create'],
    ),
):
    return await tag_service.create(tag_create)


@router.put(
    '/{tag_id}',
    response_model=TagResponse,
    responses=common_error_responses,
)
async def update_tag(
    tag_id: int,
    tag_update: TagUpdate,
    tag_service: TagServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['references:update'],
    ),
):
    tag = await tag_service.update(tag_id, tag_update)
    if tag is None:
        raise NotFoundError('Tag not found')
    return tag


@router.delete(
    '/{tag_id}',
    response_model=TagResponse,
    responses=common_error_responses,
)
async def delete_tag(
    tag_id: int,
    tag_service: TagServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['references:delete'],
    ),
):
    tag = await tag_service.delete(tag_id)
    if tag is None:
        raise NotFoundError('Tag not found')
    return tag