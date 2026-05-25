from datetime import datetime, timedelta, timezone

from fastapi import HTTPException, status
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.models.refresh_sessions import RefreshSessionModel
from app.models.users import UserModel
from app.services.hasher import Hasher
from app.services.jwt import JWTService, TokenType


class AuthService:
    @staticmethod
    async def register_user(
        session: AsyncSession,
        first_name: str,
        last_name: str,
        email: str,
        password: str,
    ) -> UserModel:
        result = await session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        existing_user = result.scalars().first()

        if existing_user:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail='User with this email already exists',
            )

        user = UserModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password_hash=Hasher.get_password_hash(password),
        )

        session.add(user)
        await session.commit()
        await session.refresh(user)

        return user

    @staticmethod
    async def authenticate_user(
        session: AsyncSession,
        email: str,
        password: str,
    ) -> UserModel:
        result = await session.execute(
            select(UserModel).where(UserModel.email == email)
        )
        user = result.scalars().first()

        if user is None or not Hasher.verify_password(password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Incorrect email or password',
            )

        return user

    @staticmethod
    async def create_token_pair(
        session: AsyncSession,
        user: UserModel,
    ) -> dict[str, str]:
        access_token, access_jti, _ = JWTService.create_token(
            user_id=user.id,
            expires_delta=timedelta(seconds=settings.ACCESS_TOKEN_EXPIRE_SECONDS),
            token_type=TokenType.ACCESS,
        )

        refresh_token, refresh_jti, refresh_expires_at = JWTService.create_token(
            user_id=user.id,
            expires_delta=timedelta(seconds=settings.REFRESH_TOKEN_EXPIRE_SECONDS),
            token_type=TokenType.REFRESH,
        )

        refresh_session = RefreshSessionModel(
            user_id=user.id,
            access_token_jti=access_jti,
            refresh_token_jti=refresh_jti,
            expires_at=refresh_expires_at,
        )

        session.add(refresh_session)
        await session.commit()

        return {
            'access_token': access_token,
            'refresh_token': refresh_token,
            'token_type': 'bearer',
        }

    @staticmethod
    async def get_user_by_access_token(
        session: AsyncSession,
        access_token: str,
    ) -> UserModel:
        payload = JWTService.decode_token(access_token)

        if payload.get('type') != TokenType.ACCESS:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token type',
            )

        user_id = int(payload['sub'])

        user = await session.get(UserModel, user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='User not found',
            )

        return user

    @staticmethod
    async def refresh_tokens(
        session: AsyncSession,
        refresh_token: str,
    ) -> dict[str, str]:
        payload = JWTService.decode_token(refresh_token)

        if payload.get('type') != TokenType.REFRESH:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid token type',
            )

        refresh_jti = payload['jti']
        user_id = int(payload['sub'])

        result = await session.execute(
            select(RefreshSessionModel).where(
                RefreshSessionModel.refresh_token_jti == refresh_jti,
            )
        )
        refresh_session = result.scalars().first()

        if refresh_session is None or not refresh_session.is_valid:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='Invalid refresh session',
            )

        refresh_session.is_invalidated = True
        refresh_session.invalidated_at = datetime.now(timezone.utc)
        session.add(refresh_session)

        user = await session.get(UserModel, user_id)
        if user is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail='User not found',
            )

        return await AuthService.create_token_pair(session, user)

    @staticmethod
    async def logout(
        session: AsyncSession,
        refresh_token: str,
    ) -> None:
        payload = JWTService.decode_token(refresh_token)

        if payload.get('type') != TokenType.REFRESH:
            return

        refresh_jti = payload['jti']

        result = await session.execute(
            select(RefreshSessionModel).where(
                RefreshSessionModel.refresh_token_jti == refresh_jti,
            )
        )
        refresh_session = result.scalars().first()

        if refresh_session:
            refresh_session.is_invalidated = True
            refresh_session.invalidated_at = datetime.now(timezone.utc)
            session.add(refresh_session)
            await session.commit()