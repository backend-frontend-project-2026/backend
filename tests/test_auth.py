import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.email_notifications import (
    EmailNotificationAction,
    EmailNotificationModel,
)


async def _register(
    client: AsyncClient,
    email: str = 'user@test.com',
    password: str = 'password123',
) -> None:
    await client.post(
        '/api/v1/auth/register',
        json={
            'first_name': 'Test',
            'last_name': 'User',
            'email': email,
            'password': password,
        },
    )


async def _get_confirm_notification(
    db_session: AsyncSession, email: str
) -> EmailNotificationModel:
    result = await db_session.execute(
        select(EmailNotificationModel)
        .where(
            EmailNotificationModel.recipient_email == email,
            EmailNotificationModel.action == EmailNotificationAction.CONFIRM_ACCOUNT,
        )
        .order_by(EmailNotificationModel.id.desc())
    )
    return result.scalars().first()


async def _confirm(client: AsyncClient, user_id: int, code: str) -> None:
    await client.post(
        '/api/v1/auth/confirm-account',
        json={'user_id': user_id, 'code': code},
    )


async def _login(
    client: AsyncClient, email: str, password: str = 'password123'
) -> dict:
    response = await client.post(
        '/api/v1/auth/login',
        json={'email': email, 'password': password},
    )
    return response


class TestRegister:
    async def test_register_returns_200(self, client):
        response = await client.post(
            '/api/v1/auth/register',
            json={
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'new@test.com',
                'password': 'password123',
            },
        )
        assert response.status_code == 200
        assert response.json()['message'] == 'Registration successful'

    async def test_register_duplicate_email_returns_409(self, client):
        await _register(client, 'dup@test.com')
        response = await client.post(
            '/api/v1/auth/register',
            json={
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'dup@test.com',
                'password': 'password123',
            },
        )
        assert response.status_code == 409

    async def test_register_invalid_email_returns_422(self, client):
        response = await client.post(
            '/api/v1/auth/register',
            json={
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'not-an-email',
                'password': 'password123',
            },
        )
        assert response.status_code == 422

    async def test_register_short_password_returns_422(self, client):
        response = await client.post(
            '/api/v1/auth/register',
            json={
                'first_name': 'Test',
                'last_name': 'User',
                'email': 'short@test.com',
                'password': 'short',
            },
        )
        assert response.status_code == 422


class TestLogin:
    async def test_login_wrong_password_returns_401(self, client):
        await _register(client, 'login@test.com')
        response = await _login(client, 'login@test.com', 'wrongpassword')
        assert response.status_code == 401

    async def test_login_nonexistent_user_returns_401(self, client):
        response = await _login(client, 'nobody@test.com')
        assert response.status_code == 401


class TestRegistrationAndLoginFlow:
    async def test_register_confirm_login(self, client, db_session):
        email = 'flow@test.com'
        password = 'password123'

        reg_response = await client.post(
            '/api/v1/auth/register',
            json={
                'first_name': 'Flow',
                'last_name': 'User',
                'email': email,
                'password': password,
            },
        )
        assert reg_response.status_code == 200

        notification = await _get_confirm_notification(db_session, email)
        assert notification is not None

        confirm_response = await client.post(
            '/api/v1/auth/confirm-account',
            json={'user_id': notification.user_id, 'code': notification.code},
        )
        assert confirm_response.status_code == 200

        login_response = await _login(client, email, password)
        assert login_response.status_code == 200
        data = login_response.json()
        assert 'access_token' in data
        assert data['token_type'] == 'bearer'

    async def test_get_me_returns_current_user(self, client, db_session):
        email = 'me@test.com'
        password = 'password123'

        await _register(client, email, password)
        notification = await _get_confirm_notification(db_session, email)
        await _confirm(client, notification.user_id, notification.code)

        login_response = await _login(client, email, password)
        access_token = login_response.json()['access_token']

        me_response = await client.get(
            '/api/v1/auth/me',
            headers={'Authorization': f'Bearer {access_token}'},
        )
        assert me_response.status_code == 200
        data = me_response.json()
        assert data['email'] == email
        assert 'public' in data['roles']

    async def test_invalid_confirmation_code_returns_401(self, client, db_session):
        email = 'badcode@test.com'
        await _register(client, email)
        notification = await _get_confirm_notification(db_session, email)

        response = await client.post(
            '/api/v1/auth/confirm-account',
            json={'user_id': notification.user_id, 'code': 'wrong-code'},
        )
        assert response.status_code == 401

    async def test_logout_invalidates_refresh_token(self, client, db_session):
        email = 'logout@test.com'
        password = 'password123'

        await _register(client, email, password)
        notification = await _get_confirm_notification(db_session, email)
        await _confirm(client, notification.user_id, notification.code)

        login_response = await _login(client, email, password)
        access_token = login_response.json()['access_token']

        logout_response = await client.post(
            '/api/v1/auth/logout',
            headers={'Authorization': f'Bearer {access_token}'},
        )
        assert logout_response.status_code == 200

        # Refresh must fail because the session was invalidated
        refresh_response = await client.post('/api/v1/auth/refresh')
        assert refresh_response.status_code == 401
