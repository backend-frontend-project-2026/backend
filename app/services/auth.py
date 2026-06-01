from datetime import datetime, timezone
from app.exceptions.base import ConflictError, InternalServerError, UnauthorizedError

from app.dependencies.repositories import (
    RefreshSessionRepository,
    RoleRepository,
    UserAuthRepository,
)
from app.core.settings import settings
from app.models.refresh_sessions import RefreshSessionModel
from app.models.users import UserModel
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
        )
        user.roles = [public_role]

        return await user_repository.save(user)

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