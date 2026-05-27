from app.dependencies.repositories import ChatRepositoryDep
from app.models.chats import ChatPublic
from app.schemas.chats import ChatListResponse
from app.services.crud import CrudService


class ChatService(CrudService):
    def __init__(self, chat_repository: ChatRepositoryDep):
        super().__init__(chat_repository, ChatPublic, ChatListResponse)
