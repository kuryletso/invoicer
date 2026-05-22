from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.types import LanguageEnum
from app.domain.enums import Language

if TYPE_CHECKING:
    from app.db.models.snap_bank_account import SnapBankAccount

class SnapBankAccountLocalization(Base):
    __tablename__ = "snap_bank_account_localizations"

    bank_account_id: Mapped[int] = mapped_column(
        ForeignKey("snap_bank_accounts.id"),
        primary_key=True,
    )

    language: Mapped[Language] = mapped_column(
        LanguageEnum,
        primary_key=True,
    )

    bank_account: Mapped[SnapBankAccount] = relationship(
        back_populates="localizations",
    )

    bank_name: Mapped[str] = mapped_column(String(120))

    bank_info: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )