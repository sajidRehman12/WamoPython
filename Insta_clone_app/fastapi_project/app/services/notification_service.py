from uuid import UUID

from app.models.tables import Notification
from app.repositories.notification_repository import NotificationRepository


class NotificationService:

    def __init__(
        self,
        notification_repo: NotificationRepository
    ):
        self.notification_repo = notification_repo

    def create_notification(
        self,
        recipient_id: UUID,
        actor_id: UUID,
        notification_type: str,
        target_id: UUID | None = None,
        target_type: str | None = None
    ):
        notification = Notification(
            recipient_id=recipient_id,
            actor_id=actor_id,
            type=notification_type,
            target_id=target_id,
            target_type=target_type
        )
        
        return self.notification_repo.create(notification)

    def get_my_notifications(
        self,
        user_id: UUID
    ):
        return self.notification_repo.get_user_notifications(user_id)

    def get_my_unread_notifications(
        self,
        user_id: UUID
    ):
        return self.notification_repo.get_unread_notifications(user_id)

    def get_unread_count(
        self,
        user_id: UUID
    ):
        return {
            "unread_count":
                self.notification_repo.unread_count(user_id)
        }

    def mark_notification_as_read(
        self,
        notification_id: UUID,
        user_id: UUID
    ):
        notification = self.notification_repo.get_by_id(
            notification_id
        )

        if not notification:
            raise ValueError("Notification not found")

        if notification.recipient_id != user_id:
            raise PermissionError(
                "You cannot access this notification"
            )

        return self.notification_repo.mark_as_read(
            notification
        )

    def mark_all_notifications_as_read(
        self,
        user_id: UUID
    ):
        count = self.notification_repo.mark_all_as_read(
            user_id
        )

        return {
            "message":
                f"{count} notifications marked as read"
        }

    def delete_notification(
        self,
        notification_id: UUID,
        user_id: UUID
    ):
        notification = self.notification_repo.get_by_id(
            notification_id
        )

        if not notification:
            raise ValueError("Notification not found")

        if notification.recipient_id != user_id:
            raise PermissionError(
                "You cannot delete this notification"
            )

        self.notification_repo.delete(notification)

        return {
            "message":
                "Notification deleted successfully"
        }