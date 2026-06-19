import enum
import uuid
from datetime import datetime
from decimal import Decimal

from sqlalchemy import DateTime, ForeignKey, Numeric, String, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class TransactionStatus(enum.Enum):
    """Статус транзации"""

    PENDING = "pending"
    WAITING_FOR_CAPTURE = "waiting_for_capture"
    SUCCEED = "succeed"
    CANCELED = "canceled"


class Transaction(Base):
    """Финансовый лог"""

    __tablename__ = "transactions"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    subscription_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user_subscriptions.id", ondelete="CASCADE"),
        index=True,
        nullable=False,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(index=True, nullable=False)

    yookassa_payment_id: Mapped[str] = mapped_column(
        unique=True, index=True, nullable=False
    )

    amount: Mapped[Decimal] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), default="RUB", nullable=False)

    status: Mapped[TransactionStatus] = mapped_column(
        default=TransactionStatus.PENDING,
        nullable=False,
    )

    error_code: Mapped[str | None] = mapped_column(nullable=True)
    error_description: Mapped[str | None] = mapped_column(nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        onupdate=func.now(),
    )
