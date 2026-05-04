from app.dependencies.repositories import UniversityRepositoryDep
from app.schemas.universities import (
    UniversityListResponse,
    UniversityResponse,
)
from app.services.crud import CrudService


class UniversityService(CrudService):
    def __init__(self, university_repository: UniversityRepositoryDep):
        super().__init__(
            university_repository,
            UniversityResponse,
            UniversityListResponse,
        )
