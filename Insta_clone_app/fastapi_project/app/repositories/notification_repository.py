from uuid import UUID

from sqlalchemy.orm import Session

from app.models.tables import Notification


class NotificationRepository:

    def __init__(self, db: Session):
        self.db = db
    def create(self, notification: Notification):
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification
    def get_user_notifications(self, user_id: UUID):
        return (
            self.db.query(Notification)
            .filter(Notification.recipient_id == user_id)
            .order_by(Notification.created_at.desc())
            .all()
        )
    def get_unread_notifications(self, user_id: UUID):
        return (
            self.db.query(Notification)
            .filter(
                Notification.recipient_id == user_id,
                Notification.is_read == False
            )
            .order_by(Notification.created_at.desc())
            .all()
        )
    def get_by_id(self, notification_id: UUID):
        return (
            self.db.query(Notification)
            .filter(Notification.id == notification_id)
            .first()
        )
    def mark_as_read(self, notification: Notification):
        notification.is_read = True
        self.db.commit()
        self.db.refresh(notification)
        return notification
    def mark_all_as_read(self, user_id: UUID):
        notifications = (
            self.db.query(Notification)
            .filter(
                Notification.recipient_id == user_id,
                Notification.is_read == False
            )
            .all()
        )
        for notification in notifications:
            notification.is_read = True

        self.db.commit()

        return len(notifications)

    def delete(self, notification: Notification):
        self.db.delete(notification)
        self.db.commit()

    def unread_count(self, user_id: UUID):
        return (
            self.db.query(Notification)
            .filter(
                Notification.recipient_id == user_id,
                Notification.is_read == False
            )
            .count()
        )