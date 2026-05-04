from app.dependencies.repositories import DormRepositoryDep
from app.schemas.dorms import DormListResponse, DormResponse
from app.services.crud import CrudService


class DormService(CrudService):
    def __init__(self, dorm_repository: DormRepositoryDep):
        super().__init__(dorm_repository, DormResponse, DormListResponse)
