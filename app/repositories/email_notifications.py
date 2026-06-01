from datetime import datetime, timezone

from sqlmodel import select

from app.models.email_notifications import (
    EmailNotificationAction,
    EmailNotificationModel,
)
from app.utils.repository import Repository


class EmailNotificationRepository(Repository[EmailNotificationModel]):
    async def get_active_by_user_action_code(
        self,
        user_id: int,
        action: EmailNotificationAction,
        code: str,
    ) -> EmailNotificationModel | None:
        result = await self._session.execute(
            select(EmailNotificationModel).where(
                EmailNotificationModel.user_id == user_id,
                EmailNotificationModel.action == action,
                EmailNotificationModel.code == code,
                EmailNotificationModel.is_used.is_(False),
            )
        )
        return result.scalars().first()

    async def mark_as_used(
        self,
        notification: EmailNotificationModel,
    ) -> EmailNotificationModel:
        notification.is_used = True
        notification.used_at = datetime.now(timezone.utc)
        return await self.save(notification)