from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.references.language import Language

if TYPE_CHECKING:
    from app.db.models.snapshots.snap_bank_account import SnapBankAccount


class SnapBankAccountLocalization(Base):
    __tablename__ = "snap_bank_account_localizations"

    bank_account_id: Mapped[int] = mapped_column(
        ForeignKey("snap_bank_accounts.id"),
        primary_key=True,
    )

    language_code: Mapped[str] = mapped_column(
        ForeignKey("languages.code"),
        primary_key=True,
    )

    bank_account: Mapped[SnapBankAccount] = relationship(
        foreign_keys=[bank_account_id],
        back_populates="localizations",
    )

    language: Mapped[Language] = relationship(
        foreign_keys=[language_code],
    )

    bank_name: Mapped[str] = mapped_column(String(120))

    bank_info: Mapped[str | None] = mapped_column(
        String(255),
    )