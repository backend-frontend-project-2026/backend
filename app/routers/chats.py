from typing import Annotated

from fastapi import APIRouter, Depends, Security

from app.dependencies.auth import get_current_user
from app.dependencies.services import ChatServiceDep
from app.exceptions.base import NotFoundError
from app.exceptions.responses import common_error_responses, create_error_responses
from app.models.chats import ChatCreate, ChatPublic
from app.models.users import UserModel
from app.schemas.chats import ChatFilters, ChatListResponse

router = APIRouter(prefix='/chats', tags=['Chats'])


@router.get(
    '',
    response_model=ChatListResponse,
    responses=common_error_responses,
)
async def list_chats(
    chat_service: ChatServiceDep,
    filters: Annotated[ChatFilters, Depends()],
    _current_user: UserModel = Security(get_current_user, scopes=['chats:read']),
):
    return await chat_service.get_list(filters)


@router.post(
    '',
    response_model=ChatPublic,
    responses=create_error_responses,
)
async def create_chat(
    chat_create: ChatCreate,
    chat_service: ChatServiceDep,
    _current_user: UserModel = Security(get_current_user, scopes=['chats:create']),
):
    return await chat_service.create(chat_create)


@router.get(
    '/{chat_id}',
    response_model=ChatPublic,
    responses=common_error_responses,
)
async def get_chat(
    chat_id: int,
    chat_service: ChatServiceDep,
    _current_user: UserModel = Security(get_current_user, scopes=['chats:read']),
):
    chat = await chat_service.get_by_id(chat_id)
    if chat is None:
        raise NotFoundError('Chat not found')
    return chat


@router.delete(
    '/{chat_id}',
    response_model=ChatPublic,
    responses=common_error_responses,
)
async def delete_chat(
    chat_id: int,
    chat_service: ChatServiceDep,
    _current_user: UserModel = Security(get_current_user, scopes=['chats:delete']),
):
    chat = await chat_service.delete(chat_id)
    if chat is None:
        raise NotFoundError('Chat not found')
    return chat