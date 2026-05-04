from app.dependencies.repositories import ComplaintRepositoryDep
from app.schemas.complaints import (
    ComplaintListResponse,
    ComplaintResponse,
)
from app.services.crud import CrudService


class ComplaintService(CrudService):
    def __init__(self, complaint_repository: ComplaintRepositoryDep):
        super().__init__(
            complaint_repository,
            ComplaintResponse,
            ComplaintListResponse,
        )
