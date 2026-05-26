from datetime import datetime, timedelta, timezone
from uuid import uuid4

import jwt

from app.core.settings import settings


class TokenType:
    ACCESS = 'access'
    REFRESH = 'refresh'


class JWTService:
    @staticmethod
    def create_token(
            user_id: int,
            expires_delta: timedelta,
            token_type: str,
            scopes: list[str] | None = None,
    ) -> tuple[str, str, datetime]:
        now = datetime.now(timezone.utc)
        expires_at = now + expires_delta
        jti = str(uuid4())

        payload = {
            'iat': int(now.timestamp()),
            'exp': int(expires_at.timestamp()),
            'sub': str(user_id),
            'jti': jti,
            'type': token_type,
            'scope': ' '.join(scopes or []),
        }

        token = jwt.encode(
            payload,
            settings.JWT_SECRET_KEY,
            algorithm=settings.JWT_ALGORITHM,
        )

        return token, jti, expires_at

    @staticmethod
    def decode_token(token: str) -> dict:
        return jwt.decode(
            token,
            settings.JWT_SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM],
        )