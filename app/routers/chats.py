from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status

from app.dependencies.services import ChatServiceDep
from app.models.chats import ChatCreate
from app.schemas.chats import ChatFilters, ChatListResponse, ChatResponse

router = APIRouter(prefix='/chats', tags=['Chats'])


@router.get('', response_model=ChatListResponse)
async def list_chats(
    chat_service: ChatServiceDep,
    filters: Annotated[ChatFilters, Depends()],
):
    return await chat_service.get_list(filters)


@router.post('', response_model=ChatResponse)
async def create_chat(
    chat_create: ChatCreate,
    chat_service: ChatServiceDep,
):
    return await chat_service.create(chat_create)


@router.get('/{chat_id}', response_model=ChatResponse)
async def get_chat(
    chat_id: int,
    chat_service: ChatServiceDep,
):
    chat = await chat_service.get_by_id(chat_id)
    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Chat not found'
        )
    return chat


@router.delete('/{chat_id}', response_model=ChatResponse)
async def delete_chat(
    chat_id: int,
    chat_service: ChatServiceDep,
):
    chat = await chat_service.delete(chat_id)
    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail='Chat not found'
        )
    return chat
