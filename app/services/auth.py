from datetime import datetime, timedelta, timezone
from secrets import token_urlsafe

from app.core.settings import settings
from app.dependencies.repositories import (
    EmailNotificationRepository,
    RefreshSessionRepository,
    RoleRepository,
    UserAuthRepository,
)
from app.exceptions.base import (
    BadRequestError,
    ConflictError,
    InternalServerError,
    UnauthorizedError,
)
from app.models.email_notifications import (
    EmailNotificationAction,
    EmailNotificationModel,
)
from app.models.refresh_sessions import RefreshSessionModel
from app.models.users import UserModel, UserStatus
from app.schemas.auth import TokenPair
from app.services.jwt import JWTService, TokenType
from app.utils.hashing import get_password_hash, verify_password


class AuthService:
    @staticmethod
    async def register_user(
            user_repository: UserAuthRepository,
            role_repository: RoleRepository,
            first_name: str,
            last_name: str,
            email: str,
            password: str,
            commit: bool = True,
    ) -> UserModel:
        existing_user = await user_repository.get_by_email(email)

        if existing_user is not None:
            raise ConflictError('User with this email already exists')

        public_role = await role_repository.get_by_name(settings.RBAC_PUBLIC_ROLE)

        if public_role is None:
            raise InternalServerError('Public role is not initialized')

        user = UserModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=get_password_hash(password),
            status=UserStatus.CREATED,
        )
        user.roles = [public_role]

        if commit:
            return await user_repository.save(user)

        return await user_repository.add_without_commit(user)

    @staticmethod
    async def create_email_notification(
            email_notification_repository: EmailNotificationRepository,
            user: UserModel,
            action: EmailNotificationAction,
            expire_minutes: int,
            commit: bool = True,
    ) -> EmailNotificationModel:
        if user.id is None:
            raise InternalServerError('User id is missing')

        notification = EmailNotificationModel(
            user_id=user.id,
            recipient_email=user.email,
            action=action,
            code=token_urlsafe(24),
            expires_at=datetime.now(timezone.utc) + timedelta(minutes=expire_minutes),
        )

        if commit:
            return await email_notification_repository.save(notification)

        return await email_notification_repository.add_without_commit(notification)

    @staticmethod
    async def confirm_account(
        user_repository: UserAuthRepository,
        email_notification_repository: EmailNotificationRepository,
        user_id: int,
        code: str,
    ) -> UserModel:
        notification = (
            await email_notification_repository.get_active_by_user_action_code(
                user_id=user_id,
                action=EmailNotificationAction.CONFIRM_ACCOUNT,
                code=code,
            )
        )

        if notification is None or not notification.is_valid:
            raise UnauthorizedError('Invalid confirmation code')

        user = await user_repository.get(user_id)

        if user is None:
            raise UnauthorizedError('User not found')

        user.status = UserStatus.CONFIRMED

        await email_notification_repository.mark_as_used(notification)
        return await user_repository.save(user)

    @staticmethod
    async def request_password_reset(
            user_repository: UserAuthRepository,
            email_notification_repository: EmailNotificationRepository,
            email: str,
            commit: bool = True,
    ) -> EmailNotificationModel | None:
        user = await user_repository.get_by_email(email)

        if user is None:
            return None

        return await AuthService.create_email_notification(
            email_notification_repository=email_notification_repository,
            user=user,
            action=EmailNotificationAction.RESET_PASSWORD,
            expire_minutes=settings.PASSWORD_RESET_CODE_EXPIRE_MINUTES,
            commit=commit,
        )

    @staticmethod
    async def reset_password(
        user_repository: UserAuthRepository,
        email_notification_repository: EmailNotificationRepository,
        refresh_session_repository: RefreshSessionRepository,
        user_id: int,
        code: str,
        new_password: str,
        new_password_repeat: str,
    ) -> None:
        if new_password != new_password_repeat:
            raise BadRequestError('Passwords do not match')

        notification = (
            await email_notification_repository.get_active_by_user_action_code(
                user_id=user_id,
                action=EmailNotificationAction.RESET_PASSWORD,
                code=code,
            )
        )

        if notification is None or not notification.is_valid:
            raise UnauthorizedError('Invalid password reset code')

        user = await user_repository.get(user_id)

        if user is None:
            raise UnauthorizedError('User not found')

        user.password_hash = get_password_hash(new_password)

        await user_repository.save(user)
        await email_notification_repository.mark_as_used(notification)
        await refresh_session_repository.invalidate_all_by_user_id(user_id)

    @staticmethod
    async def change_password(
        user_repository: UserAuthRepository,
        refresh_session_repository: RefreshSessionRepository,
        user: UserModel,
        old_password: str,
        new_password: str,
        new_password_repeat: str,
    ) -> None:
        if user.id is None:
            raise InternalServerError('User id is missing')

        if new_password != new_password_repeat:
            raise BadRequestError('Passwords do not match')

        if not verify_password(old_password, user.password_hash):
            raise UnauthorizedError('Incorrect old password')

        user.password_hash = get_password_hash(new_password)

        await user_repository.save(user)
        await refresh_session_repository.invalidate_all_by_user_id(user.id)

    @staticmethod
    async def authenticate_user(
        user_repository: UserAuthRepository,
        email: str,
        password: str,
    ) -> UserModel:
        user = await user_repository.get_by_email(email)

        if user is None or not verify_password(password, user.password_hash):
            raise UnauthorizedError('Incorrect email or password')

        return user

    @staticmethod
    async def create_token_pair(
        refresh_session_repository: RefreshSessionRepository,
        user: UserModel,
    ) -> TokenPair:
        if user.id is None:
            raise InternalServerError('User id is missing')

        scopes = AuthService.get_user_scopes(user)

        access_token, access_jti, _ = JWTService.create_access_token(
            user_id=user.id,
            scopes=scopes,
        )

        refresh_token, refresh_jti, refresh_expires_at = (
            JWTService.create_refresh_token(user_id=user.id)
        )

        refresh_session = RefreshSessionModel(
            user_id=user.id,
            access_token_jti=access_jti,
            refresh_token_jti=refresh_jti,
            expires_at=refresh_expires_at,
        )

        await refresh_session_repository.save(refresh_session)

        return TokenPair(
            access_token=access_token,
            refresh_token=refresh_token,
            token_type='bearer',
        )

    @staticmethod
    async def get_user_by_access_token(
        user_repository: UserAuthRepository,
        access_token: str,
    ) -> UserModel:
        payload = JWTService.decode_token(access_token)

        if payload.get('type') != TokenType.ACCESS:
            raise UnauthorizedError('Invalid token type')

        user_id = int(payload['sub'])
        user = await user_repository.get(user_id)

        if user is None:
            raise UnauthorizedError('User not found')

        return user

    @staticmethod
    async def refresh_tokens(
        user_repository: UserAuthRepository,
        refresh_session_repository: RefreshSessionRepository,
        refresh_token: str,
    ) -> TokenPair:
        payload = JWTService.decode_token(refresh_token)

        if payload.get('type') != TokenType.REFRESH:
            raise UnauthorizedError('Invalid refresh session')

        refresh_jti = payload['jti']
        user_id = int(payload['sub'])

        refresh_session = await refresh_session_repository.get_by_refresh_jti(
            refresh_jti
        )

        if refresh_session is None or not refresh_session.is_valid:
            raise UnauthorizedError('Invalid refresh session')

        refresh_session.is_invalidated = True
        refresh_session.invalidated_at = datetime.now(timezone.utc)
        await refresh_session_repository.save(refresh_session)

        user = await user_repository.get(user_id)

        if user is None:
            raise UnauthorizedError('User not found')

        return await AuthService.create_token_pair(
            refresh_session_repository=refresh_session_repository,
            user=user,
        )

    @staticmethod
    async def logout(
        refresh_session_repository: RefreshSessionRepository,
        refresh_token: str,
    ) -> None:
        payload = JWTService.decode_token(refresh_token)

        if payload.get('type') != TokenType.REFRESH:
            raise UnauthorizedError('Invalid token type')

        refresh_jti = payload['jti']

        refresh_session = await refresh_session_repository.get_by_refresh_jti(
            refresh_jti
        )

        if refresh_session is None:
            raise UnauthorizedError('Invalid refresh session')

        refresh_session.is_invalidated = True
        refresh_session.invalidated_at = datetime.now(timezone.utc)
        await refresh_session_repository.save(refresh_session)

    @staticmethod
    def get_user_scopes(user: UserModel) -> list[str]:
        scopes = set()

        for role in user.roles:
            for permission in role.permissions:
                scopes.add(permission.scope)

        return sorted(scopes)