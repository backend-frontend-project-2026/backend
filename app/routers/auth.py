from typing import Annotated

from fastapi import APIRouter, Cookie, Depends, Request, Response, Security
from fastapi.security import OAuth2PasswordRequestForm

from app.core.logging import logger
from app.core.rate_limit import limiter
from app.core.settings import settings
from app.dependencies.auth import get_current_user
from app.dependencies.repositories import (
    EmailNotificationRepositoryDep,
    RefreshSessionRepositoryDep,
    RoleRepositoryDep,
    UserAuthRepositoryDep,
)
from app.dependencies.services import EmailServiceDep
from app.exceptions.base import InternalServerError, UnauthorizedError
from app.exceptions.responses import auth_responses
from app.models.email_notifications import EmailNotificationAction
from app.models.users import UserModel, UserPublic
from app.schemas.auth import (
    ChangePasswordRequest,
    ConfirmAccountRequest,
    MessageResponse,
    RegisterRequest,
    RequestPasswordResetRequest,
    ResetPasswordRequest,
    TokenResponse,
)
from app.services.auth import AuthService

router = APIRouter(prefix='/auth', tags=['Auth'])


@router.post(
    '/register',
    response_model=MessageResponse,
    responses=auth_responses,
)
@limiter.limit(settings.RATE_LIMIT_AUTH)
async def register(
    request: Request,
    payload: RegisterRequest,
    user_repository: UserAuthRepositoryDep,
    role_repository: RoleRepositoryDep,
    email_notification_repository: EmailNotificationRepositoryDep,
    email_service: EmailServiceDep,
) -> MessageResponse:
    user = await AuthService.register_user(
        user_repository=user_repository,
        role_repository=role_repository,
        first_name=payload.first_name,
        last_name=payload.last_name,
        email=str(payload.email),
        password=payload.password,
        commit=False,
    )

    notification = await AuthService.create_email_notification(
        email_notification_repository=email_notification_repository,
        user=user,
        action=EmailNotificationAction.CONFIRM_ACCOUNT,
        expire_minutes=settings.EMAIL_CONFIRMATION_CODE_EXPIRE_MINUTES,
        commit=False,
    )

    try:
        await email_service.send_account_confirmation_email(
            recipient=user.email,
            code=notification.code,
            user_id=user.id,
        )
    except Exception as exc:
        await user_repository.rollback()
        logger.exception(
            'Failed to send confirmation email: recipient=%s',
            user.email,
        )
        raise InternalServerError('Failed to send confirmation email') from exc

    await user_repository.commit()

    return MessageResponse(message='Registration successful')


@router.post(
    '/confirm-account',
    response_model=MessageResponse,
    responses=auth_responses,
)
@limiter.limit(settings.RATE_LIMIT_AUTH)
async def confirm_account(
    request: Request,
    payload: ConfirmAccountRequest,
    user_repository: UserAuthRepositoryDep,
    email_notification_repository: EmailNotificationRepositoryDep,
) -> MessageResponse:
    await AuthService.confirm_account(
        user_repository=user_repository,
        email_notification_repository=email_notification_repository,
        user_id=payload.user_id,
        code=payload.code,
    )

    return MessageResponse(message='Account confirmed successfully')


@router.post(
    '/login',
    response_model=TokenResponse,
    responses=auth_responses,
)
@limiter.limit(settings.RATE_LIMIT_AUTH)
async def login(
    request: Request,
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


@router.get(
    '/me',
    response_model=UserPublic,
    responses=auth_responses,
)
async def get_me(
    current_user: UserModel = Security(get_current_user, scopes=['auth:me']),
) -> UserPublic:
    return UserPublic(
        id=current_user.id,
        created_at=current_user.created_at,
        first_name=current_user.first_name,
        last_name=current_user.last_name,
        email=current_user.email,
        status=current_user.status,
        roles=[role.name for role in current_user.roles],
    )


@router.post(
    '/refresh',
    response_model=TokenResponse,
    responses=auth_responses,
)
@limiter.limit(settings.RATE_LIMIT_AUTH)
async def refresh(
    request: Request,
    response: Response,
    user_repository: UserAuthRepositoryDep,
    refresh_session_repository: RefreshSessionRepositoryDep,
    refresh_token: str | None = Cookie(default=None),
) -> TokenResponse:
    if refresh_token is None:
        raise UnauthorizedError('Refresh token is missing')

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


@router.post(
    '/logout',
    response_model=MessageResponse,
    responses=auth_responses,
)
@limiter.limit(settings.RATE_LIMIT_AUTH)
async def logout(
    request: Request,
    response: Response,
    refresh_session_repository: RefreshSessionRepositoryDep,
    refresh_token: str | None = Cookie(default=None),
) -> MessageResponse:
    if refresh_token is None:
        raise UnauthorizedError('Refresh token is missing')

    await AuthService.logout(
        refresh_session_repository=refresh_session_repository,
        refresh_token=refresh_token,
    )

    response.delete_cookie(key=settings.REFRESH_COOKIE_NAME)

    return MessageResponse(message='Logout successful')


@router.post(
    '/request-password-reset',
    response_model=MessageResponse,
    responses=auth_responses,
)
@limiter.limit(settings.RATE_LIMIT_AUTH)
async def request_password_reset(
    request: Request,
    payload: RequestPasswordResetRequest,
    user_repository: UserAuthRepositoryDep,
    email_notification_repository: EmailNotificationRepositoryDep,
    email_service: EmailServiceDep,
) -> MessageResponse:
    notification = await AuthService.request_password_reset(
        user_repository=user_repository,
        email_notification_repository=email_notification_repository,
        email=str(payload.email),
        commit=False,
    )

    if notification is None:
        return MessageResponse(
            message='If user exists, password reset email will be sent'
        )

    try:
        await email_service.send_password_reset_email(
            recipient=notification.recipient_email,
            code=notification.code,
            user_id=notification.user_id,
        )
    except Exception as exc:
        await email_notification_repository.rollback()
        logger.exception(
            'Failed to send password reset email: recipient=%s',
            notification.recipient_email,
        )
        raise InternalServerError('Failed to send password reset email') from exc

    await email_notification_repository.commit()

    return MessageResponse(
        message='If user exists, password reset email will be sent'
    )


@router.post(
    '/reset-password',
    response_model=MessageResponse,
    responses=auth_responses,
)
@limiter.limit(settings.RATE_LIMIT_AUTH)
async def reset_password(
    request: Request,
    payload: ResetPasswordRequest,
    user_repository: UserAuthRepositoryDep,
    email_notification_repository: EmailNotificationRepositoryDep,
    refresh_session_repository: RefreshSessionRepositoryDep,
) -> MessageResponse:
    await AuthService.reset_password(
        user_repository=user_repository,
        email_notification_repository=email_notification_repository,
        refresh_session_repository=refresh_session_repository,
        user_id=payload.user_id,
        code=payload.code,
        new_password=payload.new_password,
        new_password_repeat=payload.new_password_repeat,
    )

    return MessageResponse(message='Password reset successfully')


@router.post(
    '/change-password',
    response_model=MessageResponse,
    responses=auth_responses,
)
@limiter.limit(settings.RATE_LIMIT_AUTH)
async def change_password(
    request: Request,
    payload: ChangePasswordRequest,
    user_repository: UserAuthRepositoryDep,
    refresh_session_repository: RefreshSessionRepositoryDep,
    current_user: UserModel = Security(get_current_user, scopes=['auth:me']),
) -> MessageResponse:
    await AuthService.change_password(
        user_repository=user_repository,
        refresh_session_repository=refresh_session_repository,
        user=current_user,
        old_password=payload.old_password,
        new_password=payload.new_password,
        new_password_repeat=payload.new_password_repeat,
    )

    return MessageResponse(message='Password changed successfully')