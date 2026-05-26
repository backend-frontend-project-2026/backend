from fastapi import Depends, HTTPException, Security, status
from fastapi.security import OAuth2PasswordBearer, SecurityScopes

from app.dependencies.session import SessionDep
from app.models.users import UserModel
from app.services.auth import AuthService
from app.services.jwt import JWTService

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl='/api/v1/auth/login',
    scopes={
        'auth:me': 'Read current user',
        'profiles:read': 'Read profiles',
        'profiles:update': 'Update own profile',
        'users:manage': 'Manage users',
        'complaints:manage': 'Manage complaints',
        'references:manage': 'Manage references',
    },
)


async def get_current_user(
    security_scopes: SecurityScopes,
    session: SessionDep,
    token: str = Depends(oauth2_scheme),
) -> UserModel:
    payload = JWTService.decode_token(token)
    token_scopes = payload.get('scope', '').split()

    for scope in security_scopes.scopes:
        if scope not in token_scopes:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail='Not enough permissions',
            )

    return await AuthService.get_user_by_access_token(
        session=session,
        access_token=token,
    )


def require_scopes(scopes: list[str]):
    async def dependency(
        current_user: UserModel = Security(get_current_user, scopes=scopes),
    ) -> UserModel:
        return current_user

    return dependency