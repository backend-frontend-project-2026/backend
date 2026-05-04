from app.dependencies.repositories import ChatRepositoryDep
from app.schemas.chats import ChatListResponse, ChatResponse
from app.services.crud import CrudService


class ChatService(CrudService):
    def __init__(self, chat_repository: ChatRepositoryDep):
        super().__init__(chat_repository, ChatResponse, ChatListResponse)
