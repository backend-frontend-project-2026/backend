from typing import Annotated

from fastapi import Depends

from app.dependencies.session import SessionDep
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
from app.models.users import UserModel
from app.repositories.auth import (
    RefreshSessionRepository,
    RoleRepository,
    UserAuthRepository,
)
from app.utils.repository import Repository
from app.models.roles import RoleModel


def get_user_repository(session: SessionDep) -> Repository[UserModel]:
    return Repository[UserModel](session)


def get_user_auth_repository(session: SessionDep) -> UserAuthRepository:
    return UserAuthRepository(session)


def get_refresh_session_repository(
    session: SessionDep,
) -> RefreshSessionRepository:
    return RefreshSessionRepository(session)


def get_profile_repository(session: SessionDep) -> Repository[ProfileModel]:
    return Repository[ProfileModel](session)


def get_deal_repository(session: SessionDep) -> Repository[DealModel]:
    return Repository[DealModel](session)


def get_complaint_repository(session: SessionDep) -> Repository[ComplaintModel]:
    return Repository[ComplaintModel](session)


def get_chat_repository(session: SessionDep) -> Repository[ChatModel]:
    return Repository[ChatModel](session)


def get_message_repository(session: SessionDep) -> Repository[MessageModel]:
    return Repository[MessageModel](session)


def get_university_repository(session: SessionDep) -> Repository[UniversityModel]:
    return Repository[UniversityModel](session)


def get_faculty_repository(session: SessionDep) -> Repository[FacultyModel]:
    return Repository[FacultyModel](session)


def get_dorm_repository(session: SessionDep) -> Repository[DormModel]:
    return Repository[DormModel](session)


def get_neighbourhood_repository(
    session: SessionDep,
) -> Repository[NeighbourhoodModel]:
    return Repository[NeighbourhoodModel](session)


def get_tag_repository(session: SessionDep) -> Repository[TagModel]:
    return Repository[TagModel](session)


def get_reaction_repository(session: SessionDep) -> Repository[ReactionModel]:
    return Repository[ReactionModel](session)


def get_role_repository(session: SessionDep) -> RoleRepository:
    return RoleRepository(session)


type UserRepository = Repository[UserModel]
type UserAuthRepositoryType = UserAuthRepository
type RefreshSessionRepositoryType = RefreshSessionRepository
type RoleRepositoryType = RoleRepository
type ProfileRepository = Repository[ProfileModel]
type DealRepository = Repository[DealModel]
type ComplaintRepository = Repository[ComplaintModel]
type ChatRepository = Repository[ChatModel]
type MessageRepository = Repository[MessageModel]
type UniversityRepository = Repository[UniversityModel]
type FacultyRepository = Repository[FacultyModel]
type DormRepository = Repository[DormModel]
type NeighbourhoodRepository = Repository[NeighbourhoodModel]
type TagRepository = Repository[TagModel]
type ReactionRepository = Repository[ReactionModel]


UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]
UserAuthRepositoryDep = Annotated[
    UserAuthRepositoryType,
    Depends(get_user_auth_repository),
]
RefreshSessionRepositoryDep = Annotated[
    RefreshSessionRepositoryType,
    Depends(get_refresh_session_repository),
]
RoleRepositoryDep = Annotated[
    RoleRepositoryType,
    Depends(get_role_repository),
]
ProfileRepositoryDep = Annotated[ProfileRepository, Depends(get_profile_repository)]
DealRepositoryDep = Annotated[DealRepository, Depends(get_deal_repository)]
ComplaintRepositoryDep = Annotated[
    ComplaintRepository,
    Depends(get_complaint_repository),
]
ChatRepositoryDep = Annotated[ChatRepository, Depends(get_chat_repository)]
MessageRepositoryDep = Annotated[MessageRepository, Depends(get_message_repository)]
UniversityRepositoryDep = Annotated[
    UniversityRepository,
    Depends(get_university_repository),
]
FacultyRepositoryDep = Annotated[FacultyRepository, Depends(get_faculty_repository)]
DormRepositoryDep = Annotated[DormRepository, Depends(get_dorm_repository)]
NeighbourhoodRepositoryDep = Annotated[
    NeighbourhoodRepository,
    Depends(get_neighbourhood_repository),
]
TagRepositoryDep = Annotated[TagRepository, Depends(get_tag_repository)]
ReactionRepositoryDep = Annotated[ReactionRepository, Depends(get_reaction_repository)]