from app.schemas.base import ApiResponseModel, CommonListFilters, PaginatedResponse


class CityItem(ApiResponseModel):
    id: int
    name: str


class CityFilters(CommonListFilters):
    name: str | None = None


CityListResponse = PaginatedResponse[CityItem]
