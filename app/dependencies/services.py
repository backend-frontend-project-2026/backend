from typing import Annotated

from fastapi import Depends

from app.dependencies.repositories import MediaRepositoryDep
from app.services.chats import ChatService
from app.services.complaints import ComplaintService
from app.services.deals import DealService
from app.services.dorms import DormService
from app.services.faculties import FacultyService
from app.services.messages import MessageService
from app.services.neighbourhoods import NeighbourhoodService
from app.services.profiles import ProfileService
from app.services.reactions import ReactionService
from app.services.tags import TagService
from app.services.universities import UniversityService
from app.services.users import UserService
from app.services.email import EmailService
from app.services.media import MediaService


def get_media_service(repository: MediaRepositoryDep) -> MediaService:
    return MediaService(repository)


def get_email_service() -> EmailService:
    return EmailService()


type UserServiceDep = Annotated[UserService, Depends(UserService)]
type ProfileServiceDep = Annotated[ProfileService, Depends(ProfileService)]
type DealServiceDep = Annotated[DealService, Depends(DealService)]
type ComplaintServiceDep = Annotated[ComplaintService, Depends(ComplaintService)]
type ChatServiceDep = Annotated[ChatService, Depends(ChatService)]
type MessageServiceDep = Annotated[MessageService, Depends(MessageService)]
type UniversityServiceDep = Annotated[UniversityService, Depends(UniversityService)]
type FacultyServiceDep = Annotated[FacultyService, Depends(FacultyService)]
type DormServiceDep = Annotated[DormService, Depends(DormService)]
type NeighbourhoodServiceDep = Annotated[
    NeighbourhoodService, Depends(NeighbourhoodService)
]
type TagServiceDep = Annotated[TagService, Depends(TagService)]
type ReactionServiceDep = Annotated[ReactionService, Depends(ReactionService)]
MediaServiceDep = Annotated[MediaService, Depends(get_media_service)]
type EmailServiceType = EmailService

EmailServiceDep = Annotated[
    EmailServiceType,
    Depends(get_email_service),
]