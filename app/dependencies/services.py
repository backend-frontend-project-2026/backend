from typing import Annotated

from fastapi import Depends

from app.dependencies.repositories import (
    ChatRepositoryDep,
    ComplaintRepositoryDep,
    DealRepositoryDep,
    DormRepositoryDep,
    FacultyRepositoryDep,
    MessageRepositoryDep,
    NeighbourhoodRepositoryDep,
    ProfileRepositoryDep,
    ReactionRepositoryDep,
    TagRepositoryDep,
    UniversityRepositoryDep,
    UserRepositoryDep,
)
from app.schemas.chats import ChatListResponse, ChatResponse
from app.schemas.complaints import (
    ComplaintListResponse,
    ComplaintResponse,
)
from app.schemas.deals import DealListResponse, DealResponse
from app.schemas.dorms import DormListResponse, DormResponse
from app.schemas.faculties import (
    FacultyListResponse,
    FacultyResponse,
)
from app.schemas.messages import (
    MessageListResponse,
    MessageResponse,
)
from app.schemas.neighbourhoods import (
    NeighbourhoodListResponse,
    NeighbourhoodResponse,
)
from app.schemas.tags import TagListResponse, TagResponse
from app.schemas.universities import (
    UniversityListResponse,
    UniversityResponse,
)
from app.services.crud import CrudService
from app.services.profiles import ProfileService
from app.services.reactions import ReactionService
from app.services.users import UserService

type DealService = CrudService
type ComplaintService = CrudService
type ChatService = CrudService
type MessageService = CrudService
type UniversityService = CrudService
type FacultyService = CrudService
type DormService = CrudService
type NeighbourhoodService = CrudService
type TagService = CrudService


def get_user_service(user_repository: UserRepositoryDep) -> UserService:
    return UserService(user_repository)


def get_profile_service(profile_repository: ProfileRepositoryDep) -> ProfileService:
    return ProfileService(profile_repository)


def get_deal_service(deal_repository: DealRepositoryDep) -> DealService:
    return CrudService(deal_repository, DealResponse, DealListResponse)


def get_complaint_service(
    complaint_repository: ComplaintRepositoryDep,
) -> ComplaintService:
    return CrudService(
        complaint_repository,
        ComplaintResponse,
        ComplaintListResponse,
    )


def get_chat_service(chat_repository: ChatRepositoryDep) -> ChatService:
    return CrudService(chat_repository, ChatResponse, ChatListResponse)


def get_message_service(message_repository: MessageRepositoryDep) -> MessageService:
    return CrudService(message_repository, MessageResponse, MessageListResponse)


def get_university_service(
    university_repository: UniversityRepositoryDep,
) -> UniversityService:
    return CrudService(
        university_repository,
        UniversityResponse,
        UniversityListResponse,
    )


def get_faculty_service(faculty_repository: FacultyRepositoryDep) -> FacultyService:
    return CrudService(faculty_repository, FacultyResponse, FacultyListResponse)


def get_dorm_service(dorm_repository: DormRepositoryDep) -> DormService:
    return CrudService(dorm_repository, DormResponse, DormListResponse)


def get_neighbourhood_service(
    neighbourhood_repository: NeighbourhoodRepositoryDep,
) -> NeighbourhoodService:
    return CrudService(
        neighbourhood_repository,
        NeighbourhoodResponse,
        NeighbourhoodListResponse,
    )


def get_tag_service(tag_repository: TagRepositoryDep) -> TagService:
    return CrudService(tag_repository, TagResponse, TagListResponse)


def get_reaction_service(reaction_repository: ReactionRepositoryDep) -> ReactionService:
    return ReactionService(reaction_repository)


type UserServiceDep = Annotated[UserService, Depends(get_user_service)]
type ProfileServiceDep = Annotated[ProfileService, Depends(get_profile_service)]
type DealServiceDep = Annotated[DealService, Depends(get_deal_service)]
type ComplaintServiceDep = Annotated[
    ComplaintService, Depends(get_complaint_service)
]
type ChatServiceDep = Annotated[ChatService, Depends(get_chat_service)]
type MessageServiceDep = Annotated[MessageService, Depends(get_message_service)]
type UniversityServiceDep = Annotated[
    UniversityService, Depends(get_university_service)
]
type FacultyServiceDep = Annotated[FacultyService, Depends(get_faculty_service)]
type DormServiceDep = Annotated[DormService, Depends(get_dorm_service)]
type NeighbourhoodServiceDep = Annotated[
    NeighbourhoodService, Depends(get_neighbourhood_service)
]
type TagServiceDep = Annotated[TagService, Depends(get_tag_service)]
type ReactionServiceDep = Annotated[ReactionService, Depends(get_reaction_service)]
