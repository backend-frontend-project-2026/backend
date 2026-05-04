from app.dependencies.repositories import FacultyRepositoryDep
from app.schemas.faculties import (
    FacultyListResponse,
    FacultyResponse,
)
from app.services.crud import CrudService


class FacultyService(CrudService):
    def __init__(self, faculty_repository: FacultyRepositoryDep):
        super().__init__(
            faculty_repository,
            FacultyResponse,
            FacultyListResponse,
        )
