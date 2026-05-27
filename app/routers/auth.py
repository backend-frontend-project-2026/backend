from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, HTTPException, Response, Security, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.settings import settings
from app.dependencies.auth import get_current_user
from app.dependencies.repositories import (
    RefreshSessionRepositoryDep,
    UserAuthRepositoryDep,
)
from app.models.users import UserModel, UserPublic
from app.schemas.auth import MessageResponse, RegisterRequest, TokenResponse
from app.services.auth import AuthService

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post('/register', response_model=MessageResponse)
async def register(
    payload: RegisterRequest,
    user_repository: UserAuthRepositoryDep,
) -> MessageResponse:
    await AuthService.register_user(
        user_repository=user_repository,
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=str(payload.email),
        password=payload.password,
    )

    return MessageResponse(message='Registration successful')


@router.post('/login', response_model=TokenResponse)
async def login(
    response: Response,
    user_repository: UserAuthRepositoryDep,
    refresh_session_repository: RefreshSessionRepositoryDep,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> TokenResponse:
    user = await AuthService.authenticate_user(
        user_repository=user_repository,
        email=form_data.username,
        password=form_data.password,
    )

    tokens = await AuthService.create_token_pair(
        refresh_session_repository=refresh_session_repository,
        user=user,
    )

    response.set_cookie(
        key=settings.REFRESH_COOKIE_NAME,
        value=tokens.refresh_token,
        httponly=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_SECONDS,
        samesite='lax',
    )

    return TokenResponse(access_token=tokens.access_token)


@router.get('/me', response_model=UserPublic)
async def get_me(
    current_user: UserModel = Security(get_current_user, scopes=['auth:me']),
) -> UserModel:
    return current_user


@router.post('/refresh', response_model=TokenResponse)
async def refresh(
    response: Response,
    user_repository: UserAuthRepositoryDep,
    refresh_session_repository: RefreshSessionRepositoryDep,
    refresh_token: str | None = Cookie(default=None),
) -> TokenResponse:
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token is missing',
        )

    tokens = await AuthService.refresh_tokens(
        user_repository=user_repository,
        refresh_session_repository=refresh_session_repository,
        refresh_token=refresh_token,
    )

    response.set_cookie(
        key=settings.REFRESH_COOKIE_NAME,
        value=tokens.refresh_token,
        httponly=True,
        max_age=settings.REFRESH_TOKEN_EXPIRE_SECONDS,
        samesite='lax',
    )

    return TokenResponse(access_token=tokens.access_token)


@router.post('/logout', response_model=MessageResponse)
async def logout(
    response: Response,
    refresh_session_repository: RefreshSessionRepositoryDep,
    refresh_token: str | None = Cookie(default=None),
) -> MessageResponse:
    if refresh_token is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail='Refresh token is missing',
        )

    await AuthService.logout(
        refresh_session_repository=refresh_session_repository,
        refresh_token=refresh_token,
    )

    response.delete_cookie(key=settings.REFRESH_COOKIE_NAME)

    return MessageResponse(message='Logout successful')