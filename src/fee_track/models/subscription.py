import enum
import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class SubscribeStatus(enum.Enum):
    """Статусы подписок"""

    TRIAL = "trial"
    ACTIVE = "active"
    PAST_DUE = "past_due"
    CANCELED = "canceled"
    UNPAID = "unpaid"


class UserSubscription(Base):
    """Подписки пользователей"""

    __tablename__ = "user_subscriptions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)  # pyright: ignore[reportUnknownMemberType, reportInvalidTypeForm, reportGeneralTypeIssues]
    user_id: Mapped[uuid.UUID] = mapped_column(index=True, nullable=False, unique=False)
    status: Mapped[SubscribeStatus] = mapped_column(nullable=False)
    current_period_start: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    current_period_end: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        index=True,
    )
    cancel_at_period_end: Mapped[bool] = mapped_column(default=False)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )
