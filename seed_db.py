import argparse
import asyncio
from collections.abc import Sequence

from sqlalchemy import func, select, text
from sqlmodel.ext.asyncio.session import AsyncSession

import app.models  # noqa: F401
from app.db.engine import async_session_maker
from app.models.chats import ChatModel
from app.models.complaints import (
    ComplaintModel,
    ComplaintReason,
    ComplaintStatus,
)
from app.models.deals import DealModel, DealType
from app.models.dorms import DormModel
from app.models.faculties import FacultyModel
from app.models.messages import MessageModel
from app.models.neighbourhoods import NeighbourhoodModel
from app.models.profiles import ProfileModel, ProfileSex
from app.models.reactions import ReactionModel, ReactionType
from app.models.tags import ProfileTagLink, TagCategory, TagModel
from app.models.universities import UniversityModel
from app.models.users import UserModel, UserRole, UserStatus
from app.utils.hashing import get_password_hash

TRUNCATE_TABLES: Sequence[str] = (
    'messages',
    'reactions',
    'chats',
    'profile_tag_links',
    'deals',
    'profiles',
    'faculties',
    'dorms',
    'complaints',
    'users',
    'universities',
    'tags',
    'neighbourhoods',
)


async def _count_rows(session: AsyncSession, model: type) -> int:
    result = await session.execute(select(func.count()).select_from(model))
    return int(result.scalar_one())


async def _reset_data(session: AsyncSession) -> None:
    await session.execute(
        text(
            'TRUNCATE TABLE '
            + ', '.join(TRUNCATE_TABLES)
            + ' RESTART IDENTITY CASCADE'
        )
    )


async def _ensure_seedable(session: AsyncSession, reset: bool) -> None:
    if reset:
        await _reset_data(session)
        return

    models_to_check = (
        UniversityModel,
        NeighbourhoodModel,
        TagModel,
        UserModel,
        ProfileModel,
        DealModel,
        ChatModel,
        ComplaintModel,
    )
    non_empty = []
    for model in models_to_check:
        row_count = await _count_rows(session, model)
        if row_count:
            non_empty.append(f'{model.__tablename__}: {row_count}')

    if non_empty:
        raise RuntimeError(
            'Database already contains data. '
            'Run the script with --reset to reseed it from scratch.\n'
            + '\n'.join(non_empty)
        )


async def seed_database(reset: bool = False) -> None:
    password_hash = get_password_hash('password123')

    async with async_session_maker() as session:
        await _ensure_seedable(session, reset)

        universities = [
            UniversityModel(name='ITIS', city='Kazan'),
            UniversityModel(name='KFU', city='Kazan'),
            UniversityModel(name='MIPT', city='Moscow'),
        ]
        session.add_all(universities)
        await session.flush()

        faculties = [
            FacultyModel(uni_id=universities[0].id, name='Software Engineering'),
            FacultyModel(uni_id=universities[0].id, name='Data Science'),
            FacultyModel(uni_id=universities[1].id, name='Economics'),
            FacultyModel(uni_id=universities[1].id, name='Philology'),
            FacultyModel(uni_id=universities[2].id, name='Applied Mathematics'),
            FacultyModel(uni_id=universities[2].id, name='Physics'),
        ]
        session.add_all(faculties)

        dorms = [
            DormModel(
                uni_id=universities[0].id,
                name='ITIS Dorm A',
                city='Kazan',
                address='Profsoyuznaya 10',
            ),
            DormModel(
                uni_id=universities[0].id,
                name='ITIS Dorm B',
                city='Kazan',
                address='Pushkina 4',
            ),
            DormModel(
                uni_id=universities[1].id,
                name='KFU Dorm 5',
                city='Kazan',
                address='Kremlevskaya 18',
            ),
            DormModel(
                uni_id=universities[2].id,
                name='MIPT Campus North',
                city='Moscow',
                address='Institutskiy 9',
            ),
        ]
        session.add_all(dorms)

        neighbourhoods = [
            NeighbourhoodModel(city='Kazan', district_name='Vakhitovsky'),
            NeighbourhoodModel(city='Kazan', district_name='Novo-Savinovsky'),
            NeighbourhoodModel(city='Kazan', district_name='Privolzhsky'),
            NeighbourhoodModel(city='Moscow', district_name='Dolgoprudny'),
            NeighbourhoodModel(city='Moscow', district_name='Savelovsky'),
        ]
        session.add_all(neighbourhoods)

        tags = [
            TagModel(category=TagCategory.NOISE, value='Люблю тишину'),
            TagModel(category=TagCategory.NOISE, value='Нормально отношусь к шуму'),
            TagModel(category=TagCategory.BAD_HABITS, value='Не курю'),
            TagModel(category=TagCategory.BAD_HABITS, value='Ок к курению на улице'),
            TagModel(category=TagCategory.GUESTS, value='Гостей редко'),
            TagModel(category=TagCategory.GUESTS, value='Иногда зову друзей'),
            TagModel(category=TagCategory.CLEANLINESS, value='Убираюсь по графику'),
            TagModel(category=TagCategory.ROOM_ORDER, value='Люблю порядок'),
            TagModel(category=TagCategory.SLEEP_SCHEDULE, value='Рано ложусь'),
            TagModel(category=TagCategory.SLEEP_SCHEDULE, value='Сова'),
        ]
        session.add_all(tags)
        await session.flush()

        users = [
            UserModel(
                first_name='Amina',
                last_name='Karimova',
                email='amina@example.com',
                role=UserRole.USER,
                status=UserStatus.CONFIRMED,
                password_hash=password_hash,
            ),
            UserModel(
                first_name='Ilya',
                last_name='Petrov',
                email='ilya@example.com',
                role=UserRole.USER,
                status=UserStatus.CONFIRMED,
                password_hash=password_hash,
            ),
            UserModel(
                first_name='Sofia',
                last_name='Volkova',
                email='sofia@example.com',
                role=UserRole.USER,
                status=UserStatus.CONFIRMED,
                password_hash=password_hash,
            ),
            UserModel(
                first_name='Nikita',
                last_name='Smirnov',
                email='nikita@example.com',
                role=UserRole.USER,
                status=UserStatus.CONFIRMED,
                password_hash=password_hash,
            ),
            UserModel(
                first_name='Alina',
                last_name='Ivanova',
                email='alina@example.com',
                role=UserRole.USER,
                status=UserStatus.CREATED,
                password_hash=password_hash,
            ),
            UserModel(
                first_name='Timur',
                last_name='Safiullin',
                email='timur@example.com',
                role=UserRole.USER,
                status=UserStatus.CONFIRMED,
                password_hash=password_hash,
            ),
            UserModel(
                first_name='Maria',
                last_name='Egorova',
                email='maria@example.com',
                role=UserRole.USER,
                status=UserStatus.CONFIRMED,
                password_hash=password_hash,
            ),
            UserModel(
                first_name='Admin',
                last_name='Root',
                email='admin@example.com',
                role=UserRole.ADMIN,
                status=UserStatus.CONFIRMED,
                password_hash=password_hash,
            ),
        ]
        session.add_all(users)
        await session.flush()

        profiles = [
            ProfileModel(
                user_id=users[0].id,
                uni_id=universities[0].id,
                faculty_id=faculties[0].id,
                name='Амина',
                sex=ProfileSex.FEMALE,
                age=20,
                profile_description='Ищу соседку в спокойную квартиру рядом с центром.',
                course=3,
                city='Kazan',
                neighbourhood_id=neighbourhoods[0].id,
            ),
            ProfileModel(
                user_id=users[1].id,
                uni_id=universities[0].id,
                faculty_id=faculties[1].id,
                name='Илья',
                sex=ProfileSex.MALE,
                age=21,
                profile_description='Учусь на DS, предпочитаю тишину по вечерам.',
                course=4,
                city='Kazan',
                neighbourhood_id=neighbourhoods[1].id,
            ),
            ProfileModel(
                user_id=users[2].id,
                uni_id=universities[1].id,
                faculty_id=faculties[2].id,
                name='София',
                sex=ProfileSex.FEMALE,
                age=19,
                profile_description='Ищу место в общаге или совместную аренду.',
                course=2,
                city='Kazan',
                neighbourhood_id=neighbourhoods[2].id,
            ),
            ProfileModel(
                user_id=users[3].id,
                uni_id=universities[1].id,
                faculty_id=faculties[3].id,
                name='Никита',
                sex=ProfileSex.MALE,
                age=22,
                profile_description='Нужна комната на учебный год.',
                course=4,
                city='Kazan',
                neighbourhood_id=neighbourhoods[0].id,
            ),
            ProfileModel(
                user_id=users[4].id,
                uni_id=universities[2].id,
                faculty_id=faculties[4].id,
                name='Алина',
                sex=ProfileSex.FEMALE,
                age=18,
                profile_description='Первый курс, ищу аккуратную соседку.',
                course=1,
                city='Moscow',
                neighbourhood_id=neighbourhoods[3].id,
            ),
            ProfileModel(
                user_id=users[5].id,
                uni_id=universities[2].id,
                faculty_id=faculties[5].id,
                name='Тимур',
                sex=ProfileSex.MALE,
                age=23,
                profile_description='Рассматриваю комнату рядом с МФТИ.',
                course=5,
                city='Moscow',
                neighbourhood_id=neighbourhoods[4].id,
            ),
            ProfileModel(
                user_id=users[6].id,
                uni_id=universities[0].id,
                faculty_id=faculties[0].id,
                name='Мария',
                sex=ProfileSex.FEMALE,
                age=20,
                profile_description='Люблю чистоту и ранний режим.',
                course=3,
                city='Kazan',
                neighbourhood_id=neighbourhoods[1].id,
            ),
        ]
        session.add_all(profiles)
        await session.flush()

        profile_tag_links = [
            ProfileTagLink(profile_id=profiles[0].id, tag_id=tags[0].id),
            ProfileTagLink(profile_id=profiles[0].id, tag_id=tags[2].id),
            ProfileTagLink(profile_id=profiles[0].id, tag_id=tags[6].id),
            ProfileTagLink(profile_id=profiles[1].id, tag_id=tags[1].id),
            ProfileTagLink(profile_id=profiles[1].id, tag_id=tags[3].id),
            ProfileTagLink(profile_id=profiles[2].id, tag_id=tags[4].id),
            ProfileTagLink(profile_id=profiles[2].id, tag_id=tags[9].id),
            ProfileTagLink(profile_id=profiles[3].id, tag_id=tags[5].id),
            ProfileTagLink(profile_id=profiles[3].id, tag_id=tags[7].id),
            ProfileTagLink(profile_id=profiles[4].id, tag_id=tags[8].id),
            ProfileTagLink(profile_id=profiles[5].id, tag_id=tags[9].id),
            ProfileTagLink(profile_id=profiles[6].id, tag_id=tags[0].id),
            ProfileTagLink(profile_id=profiles[6].id, tag_id=tags[7].id),
            ProfileTagLink(profile_id=profiles[6].id, tag_id=tags[8].id),
        ]
        session.add_all(profile_tag_links)

        deals = [
            DealModel(
                owner_profile_id=profiles[0].id,
                title='Ищу соседку в двушку у центра',
                deal_type=DealType.RENT,
                city='Kazan',
                neighbourhood_id=neighbourhoods[0].id,
                dorm_id=None,
                budget_min=18000,
                budget_max=25000,
                people_amount=2,
            ),
            DealModel(
                owner_profile_id=profiles[1].id,
                title='Комната рядом с ITIS',
                deal_type=DealType.RENT,
                city='Kazan',
                neighbourhood_id=neighbourhoods[1].id,
                dorm_id=None,
                budget_min=15000,
                budget_max=22000,
                people_amount=2,
            ),
            DealModel(
                owner_profile_id=profiles[2].id,
                title='Подселение в общежитие КФУ',
                deal_type=DealType.DORM,
                city='Kazan',
                neighbourhood_id=None,
                dorm_id=dorms[2].id,
                budget_min=None,
                budget_max=9000,
                people_amount=2,
            ),
            DealModel(
                owner_profile_id=profiles[4].id,
                title='Ищу соседку в кампусе МФТИ',
                deal_type=DealType.DORM,
                city='Moscow',
                neighbourhood_id=None,
                dorm_id=dorms[3].id,
                budget_min=None,
                budget_max=12000,
                people_amount=2,
            ),
            DealModel(
                owner_profile_id=profiles[5].id,
                title='Комната в Долгопрудном',
                deal_type=DealType.RENT,
                city='Moscow',
                neighbourhood_id=neighbourhoods[3].id,
                dorm_id=None,
                budget_min=20000,
                budget_max=30000,
                people_amount=2,
            ),
        ]
        session.add_all(deals)
        await session.flush()

        reactions = [
            ReactionModel(
                profile_id=profiles[6].id,
                deal_id=deals[0].id,
                reaction_type=ReactionType.LIKE,
            ),
            ReactionModel(
                profile_id=profiles[2].id,
                deal_id=deals[0].id,
                reaction_type=ReactionType.LIKE,
            ),
            ReactionModel(
                profile_id=profiles[0].id,
                deal_id=deals[1].id,
                reaction_type=ReactionType.LIKE,
            ),
            ReactionModel(
                profile_id=profiles[3].id,
                deal_id=deals[2].id,
                reaction_type=ReactionType.DISLIKE,
            ),
            ReactionModel(
                profile_id=profiles[5].id,
                deal_id=deals[3].id,
                reaction_type=ReactionType.LIKE,
            ),
            ReactionModel(
                profile_id=profiles[4].id,
                deal_id=deals[4].id,
                reaction_type=ReactionType.LIKE,
            ),
        ]
        session.add_all(reactions)

        chats = [
            ChatModel(profile_id=profiles[6].id, deal_id=deals[0].id),
            ChatModel(profile_id=profiles[0].id, deal_id=deals[1].id),
            ChatModel(profile_id=profiles[5].id, deal_id=deals[3].id),
        ]
        session.add_all(chats)
        await session.flush()

        messages = [
            MessageModel(
                chat_id=chats[0].id,
                profile_id=profiles[6].id,
                content='Привет! Комната ещё актуальна?',
                is_read=True,
            ),
            MessageModel(
                chat_id=chats[0].id,
                profile_id=profiles[0].id,
                content='Да, актуальна. Хочешь созвониться вечером?',
                is_read=True,
            ),
            MessageModel(
                chat_id=chats[0].id,
                profile_id=profiles[6].id,
                content='Да, давай после 19:00.',
                is_read=False,
            ),
            MessageModel(
                chat_id=chats[1].id,
                profile_id=profiles[0].id,
                content='Привет, смотрю комнату рядом с ITIS.',
                is_read=True,
            ),
            MessageModel(
                chat_id=chats[1].id,
                profile_id=profiles[1].id,
                content='Привет! Могу отправить фото и условия.',
                is_read=False,
            ),
            MessageModel(
                chat_id=chats[2].id,
                profile_id=profiles[5].id,
                content='Привет! По общежитию МФТИ ещё ищешь соседку?',
                is_read=True,
            ),
            MessageModel(
                chat_id=chats[2].id,
                profile_id=profiles[4].id,
                content='Да, ищу. Напиши пару слов о себе.',
                is_read=False,
            ),
        ]
        session.add_all(messages)

        complaints = [
            ComplaintModel(
                complainant_id=users[0].id,
                reported_user_id=users[3].id,
                reason=ComplaintReason.SPAM,
                screenshots='https://example.com/reports/spam-thread-1.png',
                status=ComplaintStatus.NEW,
            ),
            ComplaintModel(
                complainant_id=users[2].id,
                reported_user_id=users[1].id,
                reason=ComplaintReason.OTHER,
                screenshots='https://example.com/reports/report-2.png',
                status=ComplaintStatus.IN_PROGRESS,
            ),
            ComplaintModel(
                complainant_id=users[6].id,
                reported_user_id=users[5].id,
                reason=ComplaintReason.INAPPROPRIATE_CONTENT,
                screenshots=None,
                status=ComplaintStatus.RESOLVED,
            ),
        ]
        session.add_all(complaints)

        await session.commit()

        summary = {
            'universities': len(universities),
            'faculties': len(faculties),
            'dorms': len(dorms),
            'neighbourhoods': len(neighbourhoods),
            'tags': len(tags),
            'users': len(users),
            'profiles': len(profiles),
            'profile_tag_links': len(profile_tag_links),
            'deals': len(deals),
            'reactions': len(reactions),
            'chats': len(chats),
            'messages': len(messages),
            'complaints': len(complaints),
        }
        print('Seed completed successfully:')
        for table_name, row_count in summary.items():
            print(f'  {table_name}: {row_count}')
        print('Default test password for all users: password123')


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description='Seed the database with deterministic test data.'
    )
    parser.add_argument(
        '--reset',
        action='store_true',
        help='truncate existing data before seeding',
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    asyncio.run(seed_database(reset=args.reset))


if __name__ == '__main__':
    main()
