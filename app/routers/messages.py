from typing import Annotated

from fastapi import APIRouter, Depends, Security

from app.dependencies.auth import get_current_user
from app.dependencies.services import MessageServiceDep
from app.exceptions.base import NotFoundError
from app.exceptions.responses import common_error_responses, create_error_responses
from app.models.messages import MessageCreate, MessageUpdate
from app.models.users import UserModel
from app.schemas.messages import (
    MessageFilters,
    MessageListResponse,
    MessageResponse,
)

router = APIRouter(prefix='/chats/{chat_id}/messages', tags=['Messages'])


@router.get(
    '',
    response_model=MessageListResponse,
    responses=common_error_responses,
)
async def list_messages(
    message_service: MessageServiceDep,
    filters: Annotated[MessageFilters, Depends()],
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['messages:read'],
    ),
) -> MessageListResponse:
    return await message_service.get_list(filters)


@router.post(
    '',
    response_model=MessageResponse,
    responses=create_error_responses,
)
async def create_message(
    chat_id: int,
    message_create: MessageCreate,
    message_service: MessageServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['messages:create'],
    ),
):
    return await message_service.create(message_create, chat_id=chat_id)


@router.get(
    '/{message_id}',
    response_model=MessageResponse,
    responses=common_error_responses,
)
async def get_message(
    chat_id: int,
    message_id: int,
    message_service: MessageServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['messages:read'],
    ),
):
    message = await message_service.get_by_id(message_id)
    if message is None or message.chat_id != chat_id:
        raise NotFoundError('Message not found')
    return message


@router.put(
    '/{message_id}',
    response_model=MessageResponse,
    responses=common_error_responses,
)
async def update_message(
    chat_id: int,
    message_id: int,
    message_update: MessageUpdate,
    message_service: MessageServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['messages:update'],
    ),
):
    existing_message = await message_service.get_by_id(message_id)
    if existing_message is None or existing_message.chat_id != chat_id:
        raise NotFoundError('Message not found')

    message = await message_service.update(message_id, message_update)
    if message is None:
        raise NotFoundError('Message not found')
    return message


@router.delete(
    '/{message_id}',
    response_model=MessageResponse,
    responses=common_error_responses,
)
async def delete_message(
    chat_id: int,
    message_id: int,
    message_service: MessageServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['messages:delete'],
    ),
):
    existing_message = await message_service.get_by_id(message_id)
    if existing_message is None or existing_message.chat_id != chat_id:
        raise NotFoundError('Message not found')

    message = await message_service.delete(message_id)
    if message is None:
        raise NotFoundError('Message not found')
    return message