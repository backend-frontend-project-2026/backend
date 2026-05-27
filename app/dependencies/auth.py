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