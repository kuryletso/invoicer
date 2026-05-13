from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.snap_representative import SnapRepresentative
    from app.db.models.snap_bank_account import SnapBankAccount


from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class Party(Base):
    __tablename__ = "parties"

    id: Mapped[int] = mapped_column(primary_key=True)

    legal_name: Mapped[str] = mapped_column(String(100))

    email: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    phone: Mapped[Optional[str]] = mapped_column(
        String(18),
        nullable=True
    )

    address: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    tax_id: Mapped[str] = mapped_column(String(100))

    snap_representative: Mapped[SnapRepresentative] = relationship(
        back_populates="party"
    )

    snap_bank_account: Mapped[SnapBankAccount] = relationship(
        back_populates="party"
    )