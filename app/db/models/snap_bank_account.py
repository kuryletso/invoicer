from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.db.models.party import Party

from sqlalchemy import String, Enum as SQLEnum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.domain.enums import Currency

class SnapBankAccount(Base):
    __tablename__ = "snap_bank_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)

    bank_name: Mapped[str] = mapped_column(String(120))

    bank_info: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    iban: Mapped[str] = mapped_column(
        String(34)
    )

    swift: Mapped[Optional[str]] = mapped_column(
        String(11),
        nullable=True
    )

    currency: Mapped[Currency] = mapped_column(
        SQLEnum(Currency, name="currency_enum")
    )

    party_id: Mapped[int] = mapped_column(
        ForeignKey("parties.id"),
        nullable=False
    )

    party: Mapped[Party] = relationship(
        back_populates="snap_bank_account"
    )