from app.dependencies.repositories import MessageRepositoryDep
from app.schemas.messages import (
    MessageListResponse,
    MessageResponse,
)
from app.services.crud import CrudService


class MessageService(CrudService):
    def __init__(self, message_repository: MessageRepositoryDep):
        super().__init__(
            message_repository,
            MessageResponse,
            MessageListResponse,
        )
