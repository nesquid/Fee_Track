import uuid
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class PaymentMethod(Base):
    """Способы оплаты пользователей"""

    __tablename__ = "payment_methods"

    id: Mapped[uuid.UUID] = mapped_column(primary_key=True, default=uuid.uuid4)

    user_id: Mapped[uuid.UUID] = mapped_column(index=True, nullable=False)

    yookassa_payment_method_id: Mapped[str] = mapped_column(unique=True, nullable=False)

    is_main: Mapped[bool] = mapped_column(default=True, nullable=False)

    card_type: Mapped[str | None] = mapped_column(nullable=True)
    last4: Mapped[str | None] = mapped_column(nullable=True)

    expiry_month: Mapped[int | None] = mapped_column(nullable=True)
    expiry_year: Mapped[int | None] = mapped_column(nullable=True)

    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
    )
