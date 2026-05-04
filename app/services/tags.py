from app.dependencies.repositories import TagRepositoryDep
from app.schemas.tags import TagListResponse, TagResponse
from app.services.crud import CrudService


class TagService(CrudService):
    def __init__(self, tag_repository: TagRepositoryDep):
        super().__init__(tag_repository, TagResponse, TagListResponse)
