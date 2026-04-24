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
from app.models.chats import ChatModel
from app.models.complaints import ComplaintModel
from app.models.deals import DealModel
from app.models.dorms import DormModel
from app.models.faculties import FacultyModel
from app.models.messages import MessageModel
from app.models.neighbourhoods import NeighbourhoodModel
from app.models.profiles import ProfileModel
from app.models.reactions import ReactionModel
from app.models.tags import TagModel
from app.models.universities import UniversityModel
from app.schemas.chats import ChatCreate, ChatFilters, ChatResponse, ChatUpdate
from app.schemas.complaints import (
    ComplaintCreate,
    ComplaintFilters,
    ComplaintResponse,
    ComplaintUpdate,
)
from app.schemas.deals import DealCreate, DealFilters, DealResponse, DealUpdate
from app.schemas.dorms import DormCreate, DormFilters, DormResponse, DormUpdate
from app.schemas.faculties import (
    FacultyCreate,
    FacultyFilters,
    FacultyResponse,
    FacultyUpdate,
)
from app.schemas.messages import (
    MessageCreate,
    MessageFilters,
    MessageResponse,
    MessageUpdate,
)
from app.schemas.neighbourhoods import (
    NeighbourhoodCreate,
    NeighbourhoodFilters,
    NeighbourhoodResponse,
    NeighbourhoodUpdate,
)
from app.schemas.profiles import (
    ProfileCreate,
    ProfileFilters,
    ProfileResponse,
    ProfileUpdate,
)
from app.schemas.reactions import ReactionCreate, ReactionFilters, ReactionResponse
from app.schemas.tags import TagCreate, TagFilters, TagResponse, TagUpdate
from app.schemas.universities import (
    UniversityCreate,
    UniversityFilters,
    UniversityResponse,
    UniversityUpdate,
)
from app.schemas.users import UserFilters, UserResponse, UserUpdate
from app.services.crud import CrudService
from app.services.profiles import ProfileService
from app.services.reactions import ReactionService
from app.services.users import UserService


def get_user_service(user_repository: UserRepositoryDep) -> UserService:
    return UserService(user_repository)


def get_profile_service(profile_repository: ProfileRepositoryDep) -> ProfileService:
    return ProfileService(profile_repository)


def get_deal_service(
    deal_repository: DealRepositoryDep,
) -> CrudService[DealModel, DealCreate, DealUpdate, DealResponse, DealFilters]:
    return CrudService(deal_repository, DealResponse)


def get_complaint_service(
    complaint_repository: ComplaintRepositoryDep,
) -> CrudService[
    ComplaintModel,
    ComplaintCreate,
    ComplaintUpdate,
    ComplaintResponse,
    ComplaintFilters,
]:
    return CrudService(complaint_repository, ComplaintResponse)


def get_chat_service(
    chat_repository: ChatRepositoryDep,
) -> CrudService[ChatModel, ChatCreate, ChatUpdate, ChatResponse, ChatFilters]:
    return CrudService(chat_repository, ChatResponse)


def get_message_service(
    message_repository: MessageRepositoryDep,
) -> CrudService[
    MessageModel,
    MessageCreate,
    MessageUpdate,
    MessageResponse,
    MessageFilters,
]:
    return CrudService(message_repository, MessageResponse)


def get_university_service(
    university_repository: UniversityRepositoryDep,
) -> CrudService[
    UniversityModel,
    UniversityCreate,
    UniversityUpdate,
    UniversityResponse,
    UniversityFilters,
]:
    return CrudService(university_repository, UniversityResponse)


def get_faculty_service(
    faculty_repository: FacultyRepositoryDep,
) -> CrudService[
    FacultyModel, FacultyCreate, FacultyUpdate, FacultyResponse, FacultyFilters
]:
    return CrudService(faculty_repository, FacultyResponse)


def get_dorm_service(
    dorm_repository: DormRepositoryDep,
) -> CrudService[DormModel, DormCreate, DormUpdate, DormResponse, DormFilters]:
    return CrudService(dorm_repository, DormResponse)


def get_neighbourhood_service(
    neighbourhood_repository: NeighbourhoodRepositoryDep,
) -> CrudService[
    NeighbourhoodModel,
    NeighbourhoodCreate,
    NeighbourhoodUpdate,
    NeighbourhoodResponse,
    NeighbourhoodFilters,
]:
    return CrudService(neighbourhood_repository, NeighbourhoodResponse)


def get_tag_service(
    tag_repository: TagRepositoryDep,
) -> CrudService[TagModel, TagCreate, TagUpdate, TagResponse, TagFilters]:
    return CrudService(tag_repository, TagResponse)


def get_reaction_service(reaction_repository: ReactionRepositoryDep) -> ReactionService:
    return ReactionService(reaction_repository)


type UserServiceDep = Annotated[UserService, Depends(get_user_service)]
type ProfileServiceDep = Annotated[ProfileService, Depends(get_profile_service)]
type DealServiceDep = Annotated[
    CrudService[DealModel, DealCreate, DealUpdate, DealResponse, DealFilters],
    Depends(get_deal_service),
]
type ComplaintServiceDep = Annotated[
    CrudService[
        ComplaintModel,
        ComplaintCreate,
        ComplaintUpdate,
        ComplaintResponse,
        ComplaintFilters,
    ],
    Depends(get_complaint_service),
]
type ChatServiceDep = Annotated[
    CrudService[ChatModel, ChatCreate, ChatUpdate, ChatResponse, ChatFilters],
    Depends(get_chat_service),
]
type MessageServiceDep = Annotated[
    CrudService[
        MessageModel, MessageCreate, MessageUpdate, MessageResponse, MessageFilters
    ],
    Depends(get_message_service),
]
type UniversityServiceDep = Annotated[
    CrudService[
        UniversityModel,
        UniversityCreate,
        UniversityUpdate,
        UniversityResponse,
        UniversityFilters,
    ],
    Depends(get_university_service),
]
type FacultyServiceDep = Annotated[
    CrudService[
        FacultyModel, FacultyCreate, FacultyUpdate, FacultyResponse, FacultyFilters
    ],
    Depends(get_faculty_service),
]
type DormServiceDep = Annotated[
    CrudService[DormModel, DormCreate, DormUpdate, DormResponse, DormFilters],
    Depends(get_dorm_service),
]
type NeighbourhoodServiceDep = Annotated[
    CrudService[
        NeighbourhoodModel,
        NeighbourhoodCreate,
        NeighbourhoodUpdate,
        NeighbourhoodResponse,
        NeighbourhoodFilters,
    ],
    Depends(get_neighbourhood_service),
]
type TagServiceDep = Annotated[
    CrudService[TagModel, TagCreate, TagUpdate, TagResponse, TagFilters],
    Depends(get_tag_service),
]
type ReactionServiceDep = Annotated[ReactionService, Depends(get_reaction_service)]
