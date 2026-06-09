from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.references.language import Language

if TYPE_CHECKING:
    from app.db.models.core.bank_account import BankAccount


class BankAccountLocalization(Base):
    __tablename__ = "bank_account_localizations"

    bank_account_id: Mapped[int] = mapped_column(
        ForeignKey("bank_accounts.id"),
        primary_key=True,
    )

    language_code: Mapped[str] = mapped_column(
        ForeignKey("languages.code"),
        primary_key=True,
    )

    bank_account: Mapped[BankAccount] = relationship(
        foreign_keys=[bank_account_id],
        back_populates="localizations",
    )

    language: Mapped[Language] = relationship(
        foreign_keys=[language_code],
    )

    bank_name: Mapped[str] = mapped_column(
        String(255),
    )

    bank_info: Mapped[str] = mapped_column(
        String(255),
    )