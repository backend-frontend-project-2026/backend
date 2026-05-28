from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from jwt import PyJWTError

from app.dependencies.repositories import UserAuthRepositoryDep
from app.models.users import UserModel
from app.services.auth import AuthService
from app.services.jwt import JWTService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/api/v1/auth/login',
    scopes={
        'auth:me': 'Read current user',

        'users:read': 'Read users',
        'users:create': 'Create users',
        'users:update': 'Update users',
        'users:delete': 'Delete users',

        'profiles:read': 'Read profiles',
        'profiles:create': 'Create profiles',
        'profiles:update': 'Update profiles',
        'profiles:delete': 'Delete profiles',

        'chats:read': 'Read chats',
        'chats:create': 'Create chats',
        'chats:delete': 'Delete chats',

        'messages:read': 'Read messages',
        'messages:create': 'Create messages',
        'messages:update': 'Update messages',
        'messages:delete': 'Delete messages',

        'deals:read': 'Read deals',
        'deals:create': 'Create deals',
        'deals:update': 'Update deals',
        'deals:delete': 'Delete deals',

        'complaints:read': 'Read complaints',
        'complaints:create': 'Create complaints',
        'complaints:update': 'Update complaints',
        'complaints:delete': 'Delete complaints',

        'references:read': 'Read reference data',
        'references:create': 'Create reference data',
        'references:update': 'Update reference data',
        'references:delete': 'Delete reference data',
    },
)


async def get_current_user(
    security_scopes: SecurityScopes,
    user_repository: UserAuthRepositoryDep,
    token: str = Depends(oauth2_scheme),
) -> UserModel:
    try:
        payload = JWTService.decode_token(token)
    except PyJWTError as error:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Invalid token',
        ) from error

    token_scopes = payload.get('scope', '').split()

    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Not enough permissions',
            )

    return await AuthService.get_user_by_access_token(
        user_repository=user_repository,
        access_token=token,
    )


def require_scopes(scopes: list[str]):
    async def dependency(
        current_user: UserModel = Security(get_current_user, scopes=scopes),
    ) -> UserModel:
        return current_user

    return dependency