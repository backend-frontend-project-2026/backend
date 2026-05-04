from app.dependencies.repositories import NeighbourhoodRepositoryDep
from app.schemas.neighbourhoods import (
    NeighbourhoodListResponse,
    NeighbourhoodResponse,
)
from app.services.crud import CrudService


class NeighbourhoodService(CrudService):
    def __init__(self, neighbourhood_repository: NeighbourhoodRepositoryDep):
        super().__init__(
            neighbourhood_repository,
            NeighbourhoodResponse,
            NeighbourhoodListResponse,
        )
