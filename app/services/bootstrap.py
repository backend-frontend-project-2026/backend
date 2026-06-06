from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
from app.models.faculties import FacultyModel
from app.models.roles import (
    PermissionModel,
    RoleModel,
    RolePermissionLink,
    UserRoleLink,
)
from app.models.tags import TagCategory, TagModel
from app.models.universities import UniversityModel
from app.models.users import UserModel
from app.utils.hashing import get_password_hash


ROLE_PERMISSIONS = {
    settings.RBAC_PUBLIC_ROLE: [
        'auth:me',
        'profiles:read',
        'profiles:create',
        'profiles:update',
        'chats:read',
        'chats:create',
        'messages:read',
        'messages:create',
        'media:upload',
        'deals:read',
        'deals:create',
        'complaints:create',
        'references:read',
    ],
    settings.RBAC_ADMIN_ROLE: [
        'auth:me',
        'users:read',
        'users:create',
        'users:update',
        'users:delete',
        'profiles:read',
        'profiles:create',
        'profiles:update',
        'profiles:delete',
        'chats:read',
        'chats:create',
        'chats:delete',
        'messages:read',
        'messages:create',
        'messages:update',
        'messages:delete',
        'media:upload',
        'deals:read',
        'deals:create',
        'deals:update',
        'deals:delete',
        'complaints:read',
        'complaints:create',
        'complaints:update',
        'complaints:delete',
        'references:read',
        'references:create',
        'references:update',
        'references:delete',
        'roles:read',
        'roles:create',
        'roles:update',
        'roles:delete',
    ],
}


DEMO_TAGS: list[tuple[TagCategory, str, str]] = [
    (TagCategory.SLEEP_SCHEDULE, 'early_bird', 'Жаворонок'),
    (TagCategory.SLEEP_SCHEDULE, 'night_owl', 'Сова'),
    (TagCategory.SLEEP_SCHEDULE, 'flexible', 'Гибкий график'),

    (TagCategory.CLEANLINESS, 'low', 'Не принципиально'),
    (TagCategory.CLEANLINESS, 'medium', 'Средняя чистота'),
    (TagCategory.CLEANLINESS, 'high', 'Люблю чистоту'),

    (TagCategory.NOISE_LEVEL, 'quiet', 'Тишина'),
    (TagCategory.NOISE_LEVEL, 'moderate', 'Нормальный уровень шума'),
    (TagCategory.NOISE_LEVEL, 'social', 'Активно / шумно'),

    (TagCategory.GUEST_FREQUENCY, 'never', 'Без гостей'),
    (TagCategory.GUEST_FREQUENCY, 'rarely', 'Гости редко'),
    (TagCategory.GUEST_FREQUENCY, 'sometimes', 'Иногда'),
    (TagCategory.GUEST_FREQUENCY, 'often', 'Гости часто'),

    (TagCategory.SMOKING_PREFERENCE, 'no', 'Не курю'),
    (TagCategory.SMOKING_PREFERENCE, 'outside_only', 'Только на улице'),
    (TagCategory.SMOKING_PREFERENCE, 'yes', 'Курение не мешает'),

    (TagCategory.ALCOHOL_PREFERENCE, 'no', 'Не употребляю'),
    (TagCategory.ALCOHOL_PREFERENCE, 'rarely', 'Редко'),
    (TagCategory.ALCOHOL_PREFERENCE, 'socially', 'В компании'),
    (TagCategory.ALCOHOL_PREFERENCE, 'yes', 'Нейтрально / можно'),

    (TagCategory.ROOM_ORDER_PREFERENCE, 'strict', 'Строгий порядок'),
    (TagCategory.ROOM_ORDER_PREFERENCE, 'balanced', 'Баланс'),
    (TagCategory.ROOM_ORDER_PREFERENCE, 'flexible', 'Гибко'),

    (TagCategory.PET_PREFERENCE, 'no_pets', 'Без животных'),
    (TagCategory.PET_PREFERENCE, 'has_pets', 'Есть питомец'),
    (TagCategory.PET_PREFERENCE, 'pet_friendly', 'Можно с питомцами'),

    (TagCategory.INTERESTS, 'Учёба', 'Учёба'),
    (TagCategory.INTERESTS, 'Спорт', 'Спорт'),
    (TagCategory.INTERESTS, 'Кино', 'Кино'),
    (TagCategory.INTERESTS, 'Бег', 'Бег'),
    (TagCategory.INTERESTS, 'Кофе', 'Кофе'),
    (TagCategory.INTERESTS, 'Сериалы', 'Сериалы'),
    (TagCategory.INTERESTS, 'Готовка', 'Готовка'),
    (TagCategory.INTERESTS, 'Книги', 'Книги'),
    (TagCategory.INTERESTS, 'Прогулки', 'Прогулки'),
    (TagCategory.INTERESTS, 'Спортзал', 'Спортзал'),
    (TagCategory.INTERESTS, 'Подкасты', 'Подкасты'),
    (TagCategory.INTERESTS, 'Настолки', 'Настолки'),
    (TagCategory.INTERESTS, 'Музыка', 'Музыка'),
    (TagCategory.INTERESTS, 'Йога', 'Йога'),
    (TagCategory.INTERESTS, 'Кофейни', 'Кофейни'),
    (TagCategory.INTERESTS, 'Фотография', 'Фотография'),
    (TagCategory.INTERESTS, 'IT', 'IT'),
    (TagCategory.INTERESTS, 'Дизайн', 'Дизайн'),
    (TagCategory.INTERESTS, 'Игры', 'Игры'),
    (TagCategory.INTERESTS, 'Путешествия', 'Путешествия'),
]


DEMO_UNIVERSITIES: dict[str, dict[str, object]] = {
    'ИТИС': {
        'city': 'Казань',
        'faculties': [
            'Разработка программного обеспечения',
            'Программная инженерия',
            'Информационные системы и технологии',
        ],
    },
    'КФУ': {
        'city': 'Казань',
        'faculties': [
            'Институт вычислительной математики и информационных технологий',
            'Институт управления, экономики и финансов',
            'Юридический факультет',
        ],
    },
    'КНИТУ-КАИ': {
        'city': 'Казань',
        'faculties': [
            'Институт компьютерных технологий и защиты информации',
            'Институт авиации, наземного транспорта и энергетики',
        ],
    },
}


async def bootstrap_roles_and_permissions(session: AsyncSession) -> None:
    permissions_by_scope = await _ensure_permissions(session)
    roles_by_name = await _ensure_roles(session)

    await _sync_role_permissions(
        session=session,
        roles_by_name=roles_by_name,
        permissions_by_scope=permissions_by_scope,
    )

    await _bootstrap_admin_user(session, roles_by_name)
    await _bootstrap_demo_reference_data(session)

    await session.commit()


async def _ensure_permissions(
    session: AsyncSession,
) -> dict[str, PermissionModel]:
    permissions_by_scope: dict[str, PermissionModel] = {}

    all_scopes = sorted(
        {
            scope
            for scopes in ROLE_PERMISSIONS.values()
            for scope in scopes
        }
    )

    for scope in all_scopes:
        result = await session.execute(
            select(PermissionModel).where(PermissionModel.scope == scope)
        )
        permission = result.scalars().first()

        if permission is None:
            permission = PermissionModel(scope=scope)
            session.add(permission)
            await session.flush()

        permissions_by_scope[scope] = permission

    return permissions_by_scope


async def _ensure_roles(session: AsyncSession) -> dict[str, RoleModel]:
    roles_by_name: dict[str, RoleModel] = {}

    for role_name in ROLE_PERMISSIONS:
        result = await session.execute(
            select(RoleModel).where(RoleModel.name == role_name)
        )
        role = result.scalars().first()

        if role is None:
            role = RoleModel(name=role_name)
            session.add(role)
            await session.flush()

        roles_by_name[role_name] = role

    return roles_by_name


async def _sync_role_permissions(
    session: AsyncSession,
    roles_by_name: dict[str, RoleModel],
    permissions_by_scope: dict[str, PermissionModel],
) -> None:
    for role_name, scopes in ROLE_PERMISSIONS.items():
        role = roles_by_name[role_name]

        await session.execute(
            delete(RolePermissionLink).where(
                RolePermissionLink.role_id == role.id,
            )
        )

        for scope in scopes:
            permission = permissions_by_scope[scope]
            session.add(
                RolePermissionLink(
                    role_id=role.id,
                    permission_id=permission.id,
                )
            )

    await session.flush()


async def _bootstrap_admin_user(
    session: AsyncSession,
    roles_by_name: dict[str, RoleModel],
) -> None:
    result = await session.execute(
        select(UserModel).where(UserModel.email == settings.RBAC_ADMIN_EMAIL)
    )
    admin_user = result.scalars().first()

    admin_role = roles_by_name.get(settings.RBAC_ADMIN_ROLE)
    if admin_role is None:
        return

    if admin_user is None:
        admin_user = UserModel(
            first_name=settings.RBAC_ADMIN_FIRST_NAME,
            last_name=settings.RBAC_ADMIN_LAST_NAME,
            email=settings.RBAC_ADMIN_EMAIL,
            password_hash=get_password_hash(settings.RBAC_ADMIN_PASSWORD),
        )
        session.add(admin_user)
        await session.flush()

    await session.execute(
        delete(UserRoleLink).where(UserRoleLink.user_id == admin_user.id)
    )
    session.add(
        UserRoleLink(
            user_id=admin_user.id,
            role_id=admin_role.id,
        )
    )

    await session.flush()


async def _bootstrap_demo_reference_data(session: AsyncSession) -> None:
    await _bootstrap_tags(session)
    await _bootstrap_universities_and_faculties(session)


async def _bootstrap_tags(session: AsyncSession) -> None:
    for category, value, label in DEMO_TAGS:
        result = await session.execute(
            select(TagModel).where(
                TagModel.category == category,
                TagModel.value == value,
            )
        )
        tag = result.scalars().first()

        if tag is None:
            session.add(
                TagModel(
                    category=category,
                    value=value,
                    label=label,
                )
            )
        elif tag.label != label:
            tag.label = label

    await session.flush()


async def _bootstrap_universities_and_faculties(
    session: AsyncSession,
) -> None:
    for university_name, data in DEMO_UNIVERSITIES.items():
        city = str(data['city'])
        faculty_names = list(data['faculties'])

        result = await session.execute(
            select(UniversityModel)
            .options(selectinload(UniversityModel.faculties))
            .where(UniversityModel.name == university_name)
        )
        university = result.scalars().first()

        if university is None:
            university = UniversityModel(
                name=university_name,
                city=city,
            )
            session.add(university)
            await session.flush()
        elif university.city != city:
            university.city = city

        existing_faculty_names = {
            faculty.name
            for faculty in university.faculties
        }

        for faculty_name in faculty_names:
            if faculty_name not in existing_faculty_names:
                session.add(
                    FacultyModel(
                        uni_id=university.id,
                        name=faculty_name,
                    )
                )

    await session.flush()