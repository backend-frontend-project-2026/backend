from typing import Annotated

from fastapi import APIRouter, Depends, Security

from app.dependencies.auth import get_current_user
from app.dependencies.services import TagServiceDep
from app.exceptions.base import NotFoundError
from app.exceptions.responses import common_error_responses, create_error_responses
from app.models.tags import TagCategory, TagCreate, TagUpdate
from app.models.users import UserModel
from app.schemas.tags import (
    TagFilters,
    TagListResponse,
    TagResponse,
)

router = APIRouter(prefix='/tags', tags=['Tags'])

_MOCK_TAGS: list[dict] = [
    # sleep_schedule
    {'id': 1, 'category': TagCategory.SLEEP_SCHEDULE, 'value': 'early_bird', 'label': 'Жаворонок'},
    {'id': 2, 'category': TagCategory.SLEEP_SCHEDULE, 'value': 'night_owl', 'label': 'Сова'},
    {'id': 3, 'category': TagCategory.SLEEP_SCHEDULE, 'value': 'flexible', 'label': 'Гибкий график'},
    # cleanliness
    {'id': 4, 'category': TagCategory.CLEANLINESS, 'value': 'low', 'label': 'Не принципиально'},
    {'id': 5, 'category': TagCategory.CLEANLINESS, 'value': 'medium', 'label': 'Средняя чистота'},
    {'id': 6, 'category': TagCategory.CLEANLINESS, 'value': 'high', 'label': 'Люблю чистоту'},
    # noise_level
    {'id': 7, 'category': TagCategory.NOISE_LEVEL, 'value': 'quiet', 'label': 'Тишина'},
    {'id': 8, 'category': TagCategory.NOISE_LEVEL, 'value': 'moderate', 'label': 'Нормальный уровень шума'},
    {'id': 9, 'category': TagCategory.NOISE_LEVEL, 'value': 'social', 'label': 'Активно / шумно'},
    # guest_frequency
    {'id': 10, 'category': TagCategory.GUEST_FREQUENCY, 'value': 'never', 'label': 'Без гостей'},
    {'id': 11, 'category': TagCategory.GUEST_FREQUENCY, 'value': 'rarely', 'label': 'Гости редко'},
    {'id': 12, 'category': TagCategory.GUEST_FREQUENCY, 'value': 'sometimes', 'label': 'Иногда'},
    {'id': 13, 'category': TagCategory.GUEST_FREQUENCY, 'value': 'often', 'label': 'Гости часто'},
    # smoking_preference
    {'id': 14, 'category': TagCategory.SMOKING_PREFERENCE, 'value': 'no', 'label': 'Не курю'},
    {'id': 15, 'category': TagCategory.SMOKING_PREFERENCE, 'value': 'outside_only', 'label': 'Только на улице'},
    {'id': 16, 'category': TagCategory.SMOKING_PREFERENCE, 'value': 'yes', 'label': 'Курение не мешает'},
    # alcohol_preference
    {'id': 17, 'category': TagCategory.ALCOHOL_PREFERENCE, 'value': 'no', 'label': 'Не употребляю'},
    {'id': 18, 'category': TagCategory.ALCOHOL_PREFERENCE, 'value': 'rarely', 'label': 'Редко'},
    {'id': 19, 'category': TagCategory.ALCOHOL_PREFERENCE, 'value': 'socially', 'label': 'В компании'},
    {'id': 20, 'category': TagCategory.ALCOHOL_PREFERENCE, 'value': 'yes', 'label': 'Нейтрально / можно'},
    # room_order_preference
    {'id': 21, 'category': TagCategory.ROOM_ORDER_PREFERENCE, 'value': 'strict', 'label': 'Строгий порядок'},
    {'id': 22, 'category': TagCategory.ROOM_ORDER_PREFERENCE, 'value': 'balanced', 'label': 'Баланс'},
    {'id': 23, 'category': TagCategory.ROOM_ORDER_PREFERENCE, 'value': 'flexible', 'label': 'Гибко'},
    # pet_preference
    {'id': 24, 'category': TagCategory.PET_PREFERENCE, 'value': 'no_pets', 'label': 'Без животных'},
    {'id': 25, 'category': TagCategory.PET_PREFERENCE, 'value': 'has_pets', 'label': 'Есть питомец'},
    {'id': 26, 'category': TagCategory.PET_PREFERENCE, 'value': 'pet_friendly', 'label': 'Можно с питомцами'},
    # interests (value == label — фронт показывает raw value в summary)
    {'id': 27, 'category': TagCategory.INTERESTS, 'value': 'Учёба', 'label': 'Учёба'},
    {'id': 28, 'category': TagCategory.INTERESTS, 'value': 'Спорт', 'label': 'Спорт'},
    {'id': 29, 'category': TagCategory.INTERESTS, 'value': 'Кино', 'label': 'Кино'},
    {'id': 30, 'category': TagCategory.INTERESTS, 'value': 'Бег', 'label': 'Бег'},
    {'id': 31, 'category': TagCategory.INTERESTS, 'value': 'Кофе', 'label': 'Кофе'},
    {'id': 32, 'category': TagCategory.INTERESTS, 'value': 'Сериалы', 'label': 'Сериалы'},
    {'id': 33, 'category': TagCategory.INTERESTS, 'value': 'Готовка', 'label': 'Готовка'},
    {'id': 34, 'category': TagCategory.INTERESTS, 'value': 'Книги', 'label': 'Книги'},
    {'id': 35, 'category': TagCategory.INTERESTS, 'value': 'Прогулки', 'label': 'Прогулки'},
    {'id': 36, 'category': TagCategory.INTERESTS, 'value': 'Спортзал', 'label': 'Спортзал'},
    {'id': 37, 'category': TagCategory.INTERESTS, 'value': 'Подкасты', 'label': 'Подкасты'},
    {'id': 38, 'category': TagCategory.INTERESTS, 'value': 'Настолки', 'label': 'Настолки'},
    {'id': 39, 'category': TagCategory.INTERESTS, 'value': 'Музыка', 'label': 'Музыка'},
    {'id': 40, 'category': TagCategory.INTERESTS, 'value': 'Йога', 'label': 'Йога'},
    {'id': 41, 'category': TagCategory.INTERESTS, 'value': 'Кофейни', 'label': 'Кофейни'},
    {'id': 42, 'category': TagCategory.INTERESTS, 'value': 'Фотография', 'label': 'Фотография'},
    {'id': 43, 'category': TagCategory.INTERESTS, 'value': 'IT', 'label': 'IT'},
    {'id': 44, 'category': TagCategory.INTERESTS, 'value': 'Дизайн', 'label': 'Дизайн'},
    {'id': 45, 'category': TagCategory.INTERESTS, 'value': 'Игры', 'label': 'Игры'},
    {'id': 46, 'category': TagCategory.INTERESTS, 'value': 'Путешествия', 'label': 'Путешествия'},
]


@router.get(
    '',
    response_model=TagListResponse,
    responses=common_error_responses,
)
async def list_tags(
    filters: Annotated[TagFilters, Depends()],
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['references:read'],
    ),
):
    items = _MOCK_TAGS
    if filters.category is not None:
        items = [t for t in items if t['category'] == filters.category]
    if filters.value is not None:
        items = [t for t in items if t['value'] == filters.value]

    offset = (filters.page - 1) * filters.page_size
    page_items = items[offset: offset + filters.page_size]

    return TagListResponse(
        items=[TagResponse(**t) for t in page_items],
        total=len(items),
        page=filters.page,
        page_size=filters.page_size,
    )


@router.get(
    '/{tag_id}',
    response_model=TagResponse,
    responses=common_error_responses,
)
async def get_tag(
    tag_id: int,
    tag_service: TagServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['references:read'],
    ),
):
    tag = await tag_service.get_by_id(tag_id)
    if tag is None:
        raise NotFoundError('Tag not found')
    return tag


@router.post(
    '',
    response_model=TagResponse,
    responses=create_error_responses,
)
async def create_tag(
    tag_create: TagCreate,
    tag_service: TagServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['references:create'],
    ),
):
    return await tag_service.create(tag_create)


@router.put(
    '/{tag_id}',
    response_model=TagResponse,
    responses=common_error_responses,
)
async def update_tag(
    tag_id: int,
    tag_update: TagUpdate,
    tag_service: TagServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['references:update'],
    ),
):
    tag = await tag_service.update(tag_id, tag_update)
    if tag is None:
        raise NotFoundError('Tag not found')
    return tag


@router.delete(
    '/{tag_id}',
    response_model=TagResponse,
    responses=common_error_responses,
)
async def delete_tag(
    tag_id: int,
    tag_service: TagServiceDep,
    _current_user: UserModel = Security(
        get_current_user,
        scopes=['references:delete'],
    ),
):
    tag = await tag_service.delete(tag_id)
    if tag is None:
        raise NotFoundError('Tag not found')
    return tag