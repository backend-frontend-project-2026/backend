from pathlib import Path
from typing import Any

from fastapi import logger
from fastapi_mail import ConnectionConfig, FastMail, MessageSchema, MessageType
from jinja2 import Environment, FileSystemLoader, select_autoescape
from pydantic import EmailStr

from app.core.settings import settings


class EmailService:
    def __init__(self) -> None:
        template_dir = Path(__file__).resolve().parents[1] / 'templates' / 'emails'

        self._template_env = Environment(
            loader=FileSystemLoader(template_dir),
            autoescape=select_autoescape(['html', 'xml']),
        )

        self._connection_config = ConnectionConfig(
            MAIL_USERNAME=settings.SMTP_USERNAME,
            MAIL_PASSWORD=settings.SMTP_PASSWORD,
            MAIL_FROM=settings.SMTP_FROM_EMAIL,
            MAIL_PORT=settings.SMTP_PORT,
            MAIL_SERVER=settings.SMTP_HOST,
            MAIL_FROM_NAME=settings.SMTP_FROM_NAME,
            MAIL_STARTTLS=settings.SMTP_STARTTLS,
            MAIL_SSL_TLS=settings.SMTP_SSL_TLS,
            USE_CREDENTIALS=True,
            VALIDATE_CERTS=True,
        )

    async def send_template_email(
        self,
        recipient: EmailStr | str,
        subject: str,
        template_name: str,
        context: dict[str, Any],
    ) -> None:
        if not settings.EMAIL_NOTIFICATIONS_ENABLED:
            logger.warning(
                'Email notifications are disabled. Skip sending email: recipient=%s subject=%s',
                recipient,
                subject,
            )
            return

        template = self._template_env.get_template(template_name)
        html_body = template.render(**context)

        message = MessageSchema(
            subject=subject,
            recipients=[str(recipient)],
            body=html_body,
            subtype=MessageType.html,
        )

        fast_mail = FastMail(self._connection_config)
        await fast_mail.send_message(message)

    async def send_account_confirmation_email(
        self,
        recipient: EmailStr | str,
        code: str,
        user_id: int,
    ) -> None:
        confirmation_url = (
            f'{settings.FRONTEND_BASE_URL}/confirm-account'
            f'?user_id={user_id}&code={code}'
        )

        await self.send_template_email(
            recipient=recipient,
            subject='Подтверждение аккаунта Roomie Match',
            template_name='account_confirmation.html',
            context={
                'code': code,
                'confirmation_url': confirmation_url,
            },
        )

    async def send_password_reset_email(
        self,
        recipient: EmailStr | str,
        code: str,
        user_id: int,
    ) -> None:
        reset_url = (
            f'{settings.FRONTEND_BASE_URL}/reset-password'
            f'?user_id={user_id}&code={code}'
        )

        await self.send_template_email(
            recipient=recipient,
            subject='Сброс пароля Roomie Match',
            template_name='password_reset.html',
            context={
                'code': code,
                'reset_url': reset_url,
            },
        )