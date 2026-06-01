from typing import Annotated

from fastapi import APIRouter, Depends, Security

from app.dependencies.auth import get_current_user
from app.dependencies.services import DealServiceDep
from app.exceptions.base import NotFoundError
from app.exceptions.responses import common_error_responses, create_error_responses
from app.models.deals import DealCreate
from app.models.users import UserModel
from app.schemas.deals import (
    DealFilters,
    DealListResponse,
    DealResponse,
)

router = APIRouter(prefix='/deals', tags=['Deals'])


@router.get(
    '',
    response_model=DealListResponse,
    responses=common_error_responses,
)
async def list_deals(
    deal_service: DealServiceDep,
    filters: Annotated[DealFilters, Depends()],
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['deals:read'],
    ),
):
    return await deal_service.get_list(filters)


@router.post(
    '',
    response_model=DealResponse,
    responses=create_error_responses,
)
async def create_deal(
    deal_create: DealCreate,
    deal_service: DealServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['deals:create'],
    ),
):
    return await deal_service.create(deal_create)


@router.get(
    '/{deal_id}',
    response_model=DealResponse,
    responses=common_error_responses,
)
async def get_deal(
    deal_id: int,
    deal_service: DealServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['deals:read'],
    ),
):
    deal = await deal_service.get_by_id(deal_id)
    if deal is None:
        raise NotFoundError('Deal not found')
    return deal