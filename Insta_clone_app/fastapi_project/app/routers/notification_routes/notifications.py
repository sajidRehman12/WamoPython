from uuid import UUID

from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status
)
from sqlalchemy.orm import Session

from app.database.database import get_db

from app.repositories.notification_repository import (
    NotificationRepository
)

from app.services.notification_service import (
    NotificationService
)

from app.core.oauth import get_current_user


router = APIRouter(
    prefix="/notifications",
    tags=["Notifications"]
)


def get_notification_service(
    db: Session = Depends(get_db)
):
    return NotificationService(
        NotificationRepository(db)
    )

@router.get("/")
def get_notifications(
    current_user=Depends(get_current_user),
    service: NotificationService = Depends(
        get_notification_service
    )
):
    notifications= service.get_my_notifications(
        current_user.id
    )
    print(notifications)
    return notifications

@router.get("/unread")
def get_unread_notifications(
    current_user=Depends(get_current_user),
    service: NotificationService = Depends(
        get_notification_service
    )
):
    return service.get_my_unread_notifications(
        current_user.id
    )

@router.get("/unread-count")
def unread_count(
    current_user=Depends(get_current_user),
    service: NotificationService = Depends(
        get_notification_service
    )
):
    return service.get_unread_count(
        current_user.id
    )

@router.patch("/{notification_id}/read")
def mark_notification_as_read(
    notification_id: int,
    current_user=Depends(get_current_user),
    service: NotificationService = Depends(
        get_notification_service
    )
):
    try:
        service.mark_notification_as_read(
            notification_id,
            current_user.id
        )
        return "notification marked as read"

    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        )

    except PermissionError as ex:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(ex)
        )
    
@router.patch("/read-all")
def mark_all_notifications_as_read(
    current_user=Depends(get_current_user),
    service: NotificationService = Depends(
        get_notification_service
    )
):
    return service.mark_all_notifications_as_read(
        current_user.id
    )
@router.delete("/{notification_id}")
def delete_notification(
    notification_id: int,
    current_user=Depends(get_current_user),
    service: NotificationService = Depends(
        get_notification_service
    )
):
    try:
        return service.delete_notification(
            notification_id,
            current_user.id

        )

    except ValueError as ex:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=str(ex)
        )

    except PermissionError as ex:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail=str(ex)
        )