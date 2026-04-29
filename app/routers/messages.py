from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies.services import MessageServiceDep
from app.schemas.messages import (
    MessageCreate,
    MessageFilters,
    MessageListResponse,
    MessageResponse,
    MessageUpdate,
)

router = APIRouter(prefix='/chats/{chat_id}/messages', tags=['Messages'])


@router.get('')
async def list_messages(
    message_service: MessageServiceDep,
    filters: Annotated[MessageFilters, Depends()],
) -> MessageListResponse:
    return await message_service.get_list(filters)


@router.post('', status_code=status.HTTP_201_CREATED)
async def create_message(
    chat_id: int,
    message_create: MessageCreate,
    message_service: MessageServiceDep,
) -> MessageResponse:
    return await message_service.create(message_create, chat_id=chat_id)


@router.get('/{message_id}')
async def get_message(
    chat_id: int,
    message_id: int,
    message_service: MessageServiceDep,
) -> MessageResponse:
    message = await message_service.get_by_id(message_id)
    if message is None or message.chat_id != chat_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Message not found'
        )
    return message


@router.put('/{message_id}')
async def update_message(
    chat_id: int,
    message_id: int,
    message_update: MessageUpdate,
    message_service: MessageServiceDep,
) -> MessageResponse:
    existing_message = await message_service.get_by_id(message_id)
    if existing_message is None or existing_message.chat_id != chat_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Message not found'
        )
    message = await message_service.update(message_id, message_update)
    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Message not found'
        )
    return message


@router.delete('/{message_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_message(
    chat_id: int,
    message_id: int,
    message_service: MessageServiceDep,
) -> Response:
    existing_message = await message_service.get_by_id(message_id)
    if existing_message is None or existing_message.chat_id != chat_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Message not found'
        )
    message = await message_service.delete(message_id)
    if message is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Message not found'
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
