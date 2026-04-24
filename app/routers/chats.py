from datetime import datetime

from fastapi import APIRouter, HTTPException, Query, Response, status

from app.dependencies.services import ChatServiceDep, MessageServiceDep
from app.schemas.chats import ChatCreate, ChatFilters, ChatListResponse, ChatResponse
from app.schemas.messages import (
    MessageCreate,
    MessageFilters,
    MessageListResponse,
    MessageResponse,
    MessageUpdate,
)

router = APIRouter(prefix='/chats', tags=['Chats'])
message_router = APIRouter(prefix='/chats/{chat_id}/messages', tags=['Messages'])


@router.get('', response_model=ChatListResponse)
async def list_chats(
    chat_service: ChatServiceDep,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1),
    profile_id: int | None = None,
    deal_id: int | None = None,
    created_from: datetime | None = None,
    created_to: datetime | None = None,
) -> ChatListResponse:
    return await chat_service.get_list(
        ChatFilters(
            page=page,
            page_size=page_size,
            profile_id=profile_id,
            deal_id=deal_id,
            created_from=created_from,
            created_to=created_to,
        )
    )


@router.post('', response_model=ChatResponse, status_code=status.HTTP_201_CREATED)
async def create_chat(
    chat_create: ChatCreate,
    chat_service: ChatServiceDep,
) -> ChatResponse:
    return await chat_service.create(chat_create)


@router.get('/{chat_id}', response_model=ChatResponse)
async def get_chat(
    chat_id: int,
    chat_service: ChatServiceDep,
) -> ChatResponse:
    chat = await chat_service.get_by_id(chat_id)
    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Chat not found'
        )
    return chat


@router.delete('/{chat_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_chat(
    chat_id: int,
    chat_service: ChatServiceDep,
) -> Response:
    chat = await chat_service.delete(chat_id)
    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Chat not found'
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@message_router.get('', response_model=MessageListResponse)
async def list_messages(
    chat_id: int,
    message_service: MessageServiceDep,
    page: int = Query(default=1, ge=1),
    page_size: int = Query(default=20, ge=1),
    profile_id: int | None = None,
    sent_from: datetime | None = None,
    sent_to: datetime | None = None,
    is_read: bool | None = None,
) -> MessageListResponse:
    return await message_service.get_list(
        MessageFilters(
            page=page,
            page_size=page_size,
            chat_id=chat_id,
            profile_id=profile_id,
            sent_from=sent_from,
            sent_to=sent_to,
            is_read=is_read,
        )
    )


@message_router.post('', response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
async def create_message(
    chat_id: int,
    message_create: MessageCreate,
    message_service: MessageServiceDep,
) -> MessageResponse:
    return await message_service.create(
        message_create.model_copy(update={'chat_id': chat_id})
    )


@message_router.get('/{message_id}', response_model=MessageResponse)
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


@message_router.put('/{message_id}', response_model=MessageResponse)
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


@message_router.delete('/{message_id}', status_code=status.HTTP_204_NO_CONTENT)
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
