from app.dependencies.repositories import DealRepositoryDep
from app.schemas.deals import DealListResponse, DealResponse
from app.services.crud import CrudService


class DealService(CrudService):
    def __init__(self, deal_repository: DealRepositoryDep):
        super().__init__(deal_repository, DealResponse, DealListResponse)
