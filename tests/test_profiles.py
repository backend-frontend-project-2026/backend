"""
Critical scenario: full user journey — registration → confirmation → login → profile creation.

This flow validates that a new user can register, confirm their account,
log in, and create their roommate profile — the core value path of the app.
"""

from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.core.settings import settings
from app.models.email_notifications import (
    EmailNotificationAction,
    EmailNotificationModel,
)


async def _get_admin_token(client: AsyncClient) -> str:
    response = await client.post(
        '/api/v1/auth/login',
        json={
            'email': settings.RBAC_ADMIN_EMAIL,
            'password': settings.RBAC_ADMIN_PASSWORD,
        },
    )
    assert response.status_code == 200, f'Admin login failed: {response.text}'
    return response.json()['access_token']


class TestProfileCreationFlow:
    async def test_full_profile_creation_journey(self, client, db_session: AsyncSession):
        # Step 1: admin creates a university (reference data)
        admin_token = await _get_admin_token(client)
        uni_response = await client.post(
            '/api/v1/universities',
            json={'name': 'Test University', 'city': 'Almaty'},
            headers={'Authorization': f'Bearer {admin_token}'},
        )
        assert uni_response.status_code == 200
        uni_id = uni_response.json()['id']

        # Step 2: new user registers
        email = 'profile_user@test.com'
        password = 'password123'
        reg_response = await client.post(
            '/api/v1/auth/register',
            json={
                'first_name': 'Profile',
                'last_name': 'User',
                'email': email,
                'password': password,
            },
        )
        assert reg_response.status_code == 200

        # Step 3: confirm account via code from DB (email sending is disabled in tests)
        result = await db_session.execute(
            select(EmailNotificationModel)
            .where(
                EmailNotificationModel.recipient_email == email,
                EmailNotificationModel.action == EmailNotificationAction.CONFIRM_ACCOUNT,
            )
            .order_by(EmailNotificationModel.id.desc())
        )
        notification = result.scalars().first()
        assert notification is not None

        confirm_response = await client.post(
            '/api/v1/auth/confirm-account',
            json={'user_id': notification.user_id, 'code': notification.code},
        )
        assert confirm_response.status_code == 200

        # Step 4: user logs in
        login_response = await client.post(
            '/api/v1/auth/login',
            json={'email': email, 'password': password},
        )
        assert login_response.status_code == 200
        user_token = login_response.json()['access_token']
        user_id = notification.user_id

        # Step 5: user creates their profile
        create_response = await client.post(
            f'/api/v1/users/{user_id}/profile',
            json={
                'user_id': user_id,
                'uni_id': uni_id,
                'name': 'Profile User',
                'sex': 'male',
                'age': 21,
            },
            headers={'Authorization': f'Bearer {user_token}'},
        )
        assert create_response.status_code == 200
        profile_data = create_response.json()
        assert profile_data['name'] == 'Profile User'
        assert profile_data['age'] == 21
        assert profile_data['uni_id'] == uni_id

        # Step 6: profile is retrievable
        get_response = await client.get(
            f'/api/v1/users/{user_id}/profile',
            headers={'Authorization': f'Bearer {user_token}'},
        )
        assert get_response.status_code == 200
        assert get_response.json()['id'] == profile_data['id']

    async def test_duplicate_profile_returns_409(self, client, db_session: AsyncSession):
        admin_token = await _get_admin_token(client)
        uni_response = await client.post(
            '/api/v1/universities',
            json={'name': 'Another University', 'city': 'Astana'},
            headers={'Authorization': f'Bearer {admin_token}'},
        )
        uni_id = uni_response.json()['id']

        email = 'dup_profile@test.com'
        await client.post(
            '/api/v1/auth/register',
            json={
                'first_name': 'Dup',
                'last_name': 'User',
                'email': email,
                'password': 'password123',
            },
        )

        result = await db_session.execute(
            select(EmailNotificationModel)
            .where(
                EmailNotificationModel.recipient_email == email,
                EmailNotificationModel.action == EmailNotificationAction.CONFIRM_ACCOUNT,
            )
        )
        notification = result.scalars().first()
        await client.post(
            '/api/v1/auth/confirm-account',
            json={'user_id': notification.user_id, 'code': notification.code},
        )

        login_response = await client.post(
            '/api/v1/auth/login',
            json={'email': email, 'password': 'password123'},
        )
        user_token = login_response.json()['access_token']
        user_id = notification.user_id

        profile_payload = {
            'user_id': user_id,
            'uni_id': uni_id,
            'name': 'Dup User',
            'sex': 'female',
            'age': 22,
        }
        headers = {'Authorization': f'Bearer {user_token}'}

        first = await client.post(
            f'/api/v1/users/{user_id}/profile',
            json=profile_payload,
            headers=headers,
        )
        assert first.status_code == 200

        second = await client.post(
            f'/api/v1/users/{user_id}/profile',
            json=profile_payload,
            headers=headers,
        )
        assert second.status_code == 409
