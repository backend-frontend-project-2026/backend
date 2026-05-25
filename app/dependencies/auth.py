from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from app.dependencies.session import SessionDep
from app.models.users import UserModel
from app.services.auth import AuthService

bearer_scheme = HTTPBearer(auto_error=False)


async def get_current_user(
    session: SessionDep,
    credentials: HTTPAuthorizationCredentials | None = Depends(bearer_scheme),
) -> UserModel:
    if credentials is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Not authenticated',
        )

    return await AuthService.get_user_by_access_token(
        session=session,
        access_token=credentials.credentials,
    )