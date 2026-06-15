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
        recipient_id: int,
        actor_id: int,
        notification_type: str,
        target_id: int | None = None,
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
        user_id: int
    ):
        return self.notification_repo.get_user_notifications(user_id)

    def get_my_unread_notifications(
        self,
        user_id: int
    ):
        return self.notification_repo.get_unread_notifications(user_id)

    def get_unread_count(
        self,
        user_id: int
    ):
        return {
            "unread_count":
                self.notification_repo.unread_count(user_id)
        }

    def mark_notification_as_read(
        self,
        notification_id: int,
        user_id: int
    ):
        notification = self.notification_repo.get_by_id(
            notification_id
        )

        if not notification:
            raise ValueError("Notification not found")

        if notification.recipient_id == user_id:
            return self.notification_repo.mark_as_read(
                notification
        
            )
            
        raise PermissionError(
               f"You cannot access this notification {notification.recipient_id}  {user_id}"

            )


    def mark_all_notifications_as_read(
        self,
        user_id: int
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
        notification_id: int,
        user_id: int
    ):
        notification = self.notification_repo.get_by_id(
            notification_id
        )

        if not notification:
            raise ValueError("Notification not found")

        if notification.recipient_id != user_id:
            raise PermissionError(
                f"You cannot delete this notification {user_id}  {notification.recipient_id}"
            )

        self.notification_repo.delete(notification)

        return {
            "message":
                "Notification deleted successfully"
        }