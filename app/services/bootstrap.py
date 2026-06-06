from sqlalchemy import delete, select
from sqlalchemy.orm import selectinload
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.settings import settings
from app.models.dorms import DormModel
from app.models.faculties import FacultyModel
from app.models.neighbourhoods import NeighbourhoodModel
from app.models.profiles import ProfileModel, ProfileSex
from app.models.roles import (
    PermissionModel,
    RoleModel,
    RolePermissionLink,
    UserRoleLink,
)
from app.models.tags import TagCategory, TagModel
from app.models.universities import UniversityModel
from app.models.users import UserModel, UserStatus
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
            'Институт ИТИС',
            'Институт вычислительной математики и информационных технологий',
            'Институт управления, экономики и финансов',
            'Юридический факультет',
        ],
    },
    'КНИТУ-КАИ': {
        'city': 'Казань',
        'faculties': [
            'Институт радиоэлектроники и телекоммуникаций',
            'Институт компьютерных технологий и защиты информации',
            'Институт авиации, наземного транспорта и энергетики',
        ],
    },
    'КГЭУ': {
        'city': 'Казань',
        'faculties': [
            'Институт электроэнергетики и электроники',
        ],
    },
    'КНИТУ': {
        'city': 'Казань',
        'faculties': [
            'Факультет информационных технологий',
        ],
    },
}


DEMO_NEIGHBOURHOODS: list[tuple[str, str]] = [
    ('Казань', 'Приволжский район'),
    ('Казань', 'Советский район'),
    ('Казань', 'Вахитовский район'),
    ('Казань', 'Ново-Савиновский район'),
]


DEMO_DORMS: list[dict[str, str]] = [
    {
        'university': 'КФУ',
        'name': 'Деревня Универсиады, корпус 3',
        'city': 'Казань',
        'address': 'Деревня Универсиады, корпус 3',
    },
    {
        'university': 'КГЭУ',
        'name': 'Общежитие КГЭУ №2',
        'city': 'Казань',
        'address': 'Общежитие КГЭУ №2',
    },
]


DEMO_PROFILES: list[dict[str, object]] = [
    {
        'email': 'katya.demo@roomie.local',
        'first_name': 'Катя',
        'last_name': 'Демо',
        'name': 'Катя',
        'age': 20,
        'sex': ProfileSex.FEMALE,
        'university': 'КФУ',
        'faculty': 'Институт ИТИС',
        'course': 2,
        'city': 'Казань',
        'neighbourhood': 'Приволжский район',
        'housing_type': 'dormitory',
        'location': 'Деревня Универсиады, корпус 3',
        'interests': ['Учёба', 'Спорт', 'Кино'],
        'sleep_schedule': 'early_bird',
        'cleanliness': 'high',
        'noise_level': 'quiet',
        'guest_frequency': 'rarely',
        'pet_preference': 'no_pets',
        'smoking_preference': 'no',
        'alcohol_preference': 'no',
        'room_order_preference': 'strict',
        'has_quiet_hours': True,
        'quiet_from': '23:00',
        'quiet_to': '08:00',
        'budget_min': 20,
        'budget_max': 35,
        'stay_duration': '6-12 months',
        'profile_description': 'Спокойная, аккуратная, люблю учёбу и кино.',
        'compatibility_note': 'Подойдёт тем, кто ценит тишину и порядок.',
    },
    {
        'email': 'danil.demo@roomie.local',
        'first_name': 'Данил',
        'last_name': 'Демо',
        'name': 'Данил',
        'age': 22,
        'sex': ProfileSex.MALE,
        'university': 'КНИТУ-КАИ',
        'faculty': 'Институт радиоэлектроники и телекоммуникаций',
        'course': 4,
        'city': 'Казань',
        'neighbourhood': 'Советский район',
        'housing_type': 'rental',
        'location': 'Съём у Аметьево',
        'interests': ['Бег', 'Кофе', 'Сериалы'],
        'sleep_schedule': 'flexible',
        'cleanliness': 'medium',
        'noise_level': 'moderate',
        'guest_frequency': 'sometimes',
        'pet_preference': 'no_pets',
        'smoking_preference': 'outside_only',
        'alcohol_preference': 'socially',
        'room_order_preference': 'balanced',
        'budget_min': 24,
        'budget_max': 38,
        'stay_duration': '12+ months',
        'profile_description': 'Ищу соседа для спокойного совместного проживания.',
        'compatibility_note': 'Гибкий график, нормально отношусь к гостям иногда.',
    },
    {
        'email': 'mila.demo@roomie.local',
        'first_name': 'Мила',
        'last_name': 'Демо',
        'name': 'Мила',
        'age': 21,
        'sex': ProfileSex.FEMALE,
        'university': 'КГЭУ',
        'faculty': 'Институт электроэнергетики и электроники',
        'course': 3,
        'city': 'Казань',
        'neighbourhood': 'Вахитовский район',
        'housing_type': 'dormitory',
        'location': 'Общежитие КГЭУ №2',
        'interests': ['Готовка', 'Книги', 'Прогулки'],
        'sleep_schedule': 'early_bird',
        'cleanliness': 'high',
        'noise_level': 'quiet',
        'guest_frequency': 'never',
        'pet_preference': 'has_pets',
        'smoking_preference': 'no',
        'alcohol_preference': 'rarely',
        'room_order_preference': 'strict',
        'has_quiet_hours': True,
        'quiet_from': '23:00',
        'quiet_to': '07:30',
        'budget_min': 22,
        'budget_max': 32,
        'stay_duration': '6-12 months',
        'profile_description': 'Люблю уют, книги и готовку.',
        'compatibility_note': 'Комфортно жить с аккуратными и спокойными соседями.',
    },
    {
        'email': 'lev.demo@roomie.local',
        'first_name': 'Лев',
        'last_name': 'Демо',
        'name': 'Лев',
        'age': 23,
        'sex': ProfileSex.MALE,
        'university': 'КНИТУ',
        'faculty': 'Факультет информационных технологий',
        'course': 4,
        'city': 'Казань',
        'neighbourhood': 'Ново-Савиновский район',
        'housing_type': 'rental',
        'location': 'Съём у Козьей Слободы',
        'interests': ['Спортзал', 'Подкасты', 'Настолки'],
        'sleep_schedule': 'night_owl',
        'cleanliness': 'medium',
        'noise_level': 'social',
        'guest_frequency': 'often',
        'pet_preference': 'pet_friendly',
        'smoking_preference': 'outside_only',
        'alcohol_preference': 'yes',
        'room_order_preference': 'flexible',
        'budget_min': 28,
        'budget_max': 45,
        'stay_duration': '3-6 months',
        'profile_description': 'Общительный, люблю спорт и настолки.',
        'compatibility_note': 'Подойдёт тем, кому не мешает активный режим.',
    },
]


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
    await _bootstrap_demo_users_and_profiles(session, roles_by_name)

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
            status=UserStatus.CONFIRMED,
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
    await _bootstrap_neighbourhoods(session)
    await _bootstrap_dorms(session)


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


async def _bootstrap_neighbourhoods(session: AsyncSession) -> None:
    for city, district_name in DEMO_NEIGHBOURHOODS:
        result = await session.execute(
            select(NeighbourhoodModel).where(
                NeighbourhoodModel.city == city,
                NeighbourhoodModel.district_name == district_name,
            )
        )
        neighbourhood = result.scalars().first()

        if neighbourhood is None:
            session.add(
                NeighbourhoodModel(
                    city=city,
                    district_name=district_name,
                )
            )

    await session.flush()


async def _bootstrap_dorms(session: AsyncSession) -> None:
    for dorm_data in DEMO_DORMS:
        university = await _get_university_by_name(
            session,
            str(dorm_data['university']),
        )
        if university is None:
            continue

        result = await session.execute(
            select(DormModel).where(
                DormModel.uni_id == university.id,
                DormModel.name == dorm_data['name'],
            )
        )
        dorm = result.scalars().first()

        if dorm is None:
            session.add(
                DormModel(
                    uni_id=university.id,
                    name=dorm_data['name'],
                    city=dorm_data['city'],
                    address=dorm_data['address'],
                )
            )
        else:
            dorm.city = dorm_data['city']
            dorm.address = dorm_data['address']

    await session.flush()


async def _bootstrap_demo_users_and_profiles(
    session: AsyncSession,
    roles_by_name: dict[str, RoleModel],
) -> None:
    public_role = roles_by_name.get(settings.RBAC_PUBLIC_ROLE)

    for profile_data in DEMO_PROFILES:
        email = str(profile_data['email'])

        user_result = await session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user = user_result.scalars().first()

        if user is None:
            user = UserModel(
                first_name=str(profile_data['first_name']),
                last_name=str(profile_data['last_name']),
                email=email,
                password_hash=get_password_hash('DemoPassword123'),
                status=UserStatus.CONFIRMED,
            )
            session.add(user)
            await session.flush()
        else:
            user.first_name = str(profile_data['first_name'])
            user.last_name = str(profile_data['last_name'])
            user.status = UserStatus.CONFIRMED

        if public_role is not None:
            await _ensure_user_role(session, user.id, public_role.id)

        await _upsert_demo_profile(session, user.id, profile_data)

    await session.flush()


async def _upsert_demo_profile(
    session: AsyncSession,
    user_id: int,
    profile_data: dict[str, object],
) -> None:
    university = await _get_university_by_name(
        session,
        str(profile_data['university']),
    )
    if university is None:
        return

    faculty = await _get_faculty_by_name(
        session,
        university.id,
        str(profile_data['faculty']),
    )

    neighbourhood = await _get_neighbourhood_by_name(
        session,
        str(profile_data['city']),
        str(profile_data['neighbourhood']),
    )

    result = await session.execute(
        select(ProfileModel).where(ProfileModel.user_id == user_id)
    )
    profile = result.scalars().first()

    profile_values = {
        'user_id': user_id,
        'uni_id': university.id,
        'faculty_id': faculty.id if faculty else None,
        'neighbourhood_id': neighbourhood.id if neighbourhood else None,
        'name': str(profile_data['name']),
        'sex': profile_data['sex'],
        'age': int(profile_data['age']),
        'course': int(profile_data['course']),
        'city': str(profile_data['city']),
        'profile_description': str(profile_data['profile_description']),
        'sleep_schedule': str(profile_data['sleep_schedule']),
        'cleanliness': str(profile_data['cleanliness']),
        'noise_level': str(profile_data['noise_level']),
        'guest_frequency': str(profile_data['guest_frequency']),
        'smoking_preference': str(profile_data['smoking_preference']),
        'alcohol_preference': str(profile_data['alcohol_preference']),
        'room_order_preference': str(profile_data['room_order_preference']),
        'pet_preference': str(profile_data['pet_preference']),
        'has_quiet_hours': bool(profile_data.get('has_quiet_hours', False)),
        'quiet_from': profile_data.get('quiet_from'),
        'quiet_to': profile_data.get('quiet_to'),
        'is_smoking_allowed': profile_data['smoking_preference'] != 'no',
        'has_pets': profile_data['pet_preference'] == 'has_pets',
        'budget_min': int(profile_data['budget_min']),
        'budget_max': int(profile_data['budget_max']),
        'stay_duration': str(profile_data['stay_duration']),
        'housing_type': str(profile_data['housing_type']),
        'living_notes': str(profile_data['location']),
        'ideal_roommate_description': str(profile_data['compatibility_note']),
        'rental_criteria': str(profile_data['location']),
        'interests': list(profile_data['interests']),
        'compatibility_note': str(profile_data['compatibility_note']),
        'photo_urls': [],
    }

    if profile is None:
        session.add(ProfileModel(**profile_values))
    else:
        for field_name, value in profile_values.items():
            setattr(profile, field_name, value)

    await session.flush()


async def _ensure_user_role(
    session: AsyncSession,
    user_id: int,
    role_id: int,
) -> None:
    result = await session.execute(
        select(UserRoleLink).where(
            UserRoleLink.user_id == user_id,
            UserRoleLink.role_id == role_id,
        )
    )
    existing_link = result.scalars().first()

    if existing_link is None:
        session.add(
            UserRoleLink(
                user_id=user_id,
                role_id=role_id,
            )
        )


async def _get_university_by_name(
    session: AsyncSession,
    name: str,
) -> UniversityModel | None:
    result = await session.execute(
        select(UniversityModel).where(UniversityModel.name == name)
    )
    return result.scalars().first()


async def _get_faculty_by_name(
    session: AsyncSession,
    university_id: int,
    name: str,
) -> FacultyModel | None:
    result = await session.execute(
        select(FacultyModel).where(
            FacultyModel.uni_id == university_id,
            FacultyModel.name == name,
        )
    )
    return result.scalars().first()


async def _get_neighbourhood_by_name(
    session: AsyncSession,
    city: str,
    district_name: str,
) -> NeighbourhoodModel | None:
    result = await session.execute(
        select(NeighbourhoodModel).where(
            NeighbourhoodModel.city == city,
            NeighbourhoodModel.district_name == district_name,
        )
    )
    return result.scalars().first()