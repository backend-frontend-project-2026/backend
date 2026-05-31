from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Security, status

from app.dependencies.auth import get_current_user
from app.dependencies.services import ChatServiceDep
from app.models.chats import ChatCreate, ChatPublic
from app.models.users import UserModel
from app.schemas.chats import ChatFilters, ChatListResponse

router = APIRouter(prefix='/chats', tags=['Chats'])


@router.get('', response_model=ChatListResponse)
async def list_chats(
    chat_service: ChatServiceDep,
    filters: Annotated[ChatFilters, Depends()],
    _current_user: UserModel = Security(get_current_user, scopes=['chats:read']),
):
    return await chat_service.get_list(filters)


@router.post('', response_model=ChatPublic)
async def create_chat(
    chat_create: ChatCreate,
    chat_service: ChatServiceDep,
    _current_user: UserModel = Security(get_current_user, scopes=['chats:create']),
):
    return await chat_service.create(chat_create)


@router.get('/{chat_id}', response_model=ChatPublic)
async def get_chat(
    chat_id: int,
    chat_service: ChatServiceDep,
    _current_user: UserModel = Security(get_current_user, scopes=['chats:read']),
):
    chat = await chat_service.get_by_id(chat_id)
    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Chat not found',
        )
    return chat


@router.delete('/{chat_id}', response_model=ChatPublic)
async def delete_chat(
    chat_id: int,
    chat_service: ChatServiceDep,
    _current_user: UserModel = Security(get_current_user, scopes=['chats:delete']),
):
    chat = await chat_service.delete(chat_id)
    if chat is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail='Chat not found',
        )
    return chat