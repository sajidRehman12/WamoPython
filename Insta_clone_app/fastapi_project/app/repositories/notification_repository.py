from uuid import UUID

from sqlalchemy.orm import Session
from app.models.tables import User
from app.models.tables import Notification
# from app.models.post import Post
# from app.models.follow import Follow    
# from app.models.user import User
# from app.models.comment import Comment
# from app.models.token import Token
# from app.models.notification import Notification
# from app.models.like import Like 

class NotificationRepository:

    def __init__(self, db: Session):
        self.db = db
    def create(self, notification: Notification):
        self.db.add(notification)
        self.db.commit()
        self.db.refresh(notification)
        return notification
    def get_user_notifications(self, user_id: int):
        notifications=(
            self.db.query(Notification, User.username.label("actor_name"))
            .join(User, Notification.actor_id == User.id)
            .filter(Notification.recipient_id == user_id)
            .order_by(Notification.created_at.desc())
            .all()
        )

        return [
            {
                "id": notification.Notification.id,
                "recipient_id": notification.Notification.recipient_id,
                "actor_id": notification.Notification.actor_id,
                "actor_name": notification.actor_name,
                "type": notification.Notification.type,
                "target_id": notification.Notification.target_id,     
                "target_type": notification.Notification.target_type,
                "is_read": notification.Notification.is_read,
                "created_at": notification.Notification.created_at          
            }
            for notification in notifications
        ]  

        
    def get_unread_notifications(self, user_id: int):
        return (
            self.db.query(Notification)
            .filter(
                Notification.recipient_id == user_id,
                Notification.is_read == False
            )
            .order_by(Notification.created_at.desc())
            .all()
        )
    def get_by_id(self, notification_id: int):
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
    def mark_all_as_read(self, user_id: int):
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

    def unread_count(self, user_id: int):
        return (
            self.db.query(Notification)
            .filter(
                Notification.recipient_id == user_id,
                Notification.is_read == False
            )
            .count()
        )