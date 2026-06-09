from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship, attribute_keyed_dict

from app.db.base import Base
from app.db.models.references.country import Country
from app.db.models.references.currency import Currency

if TYPE_CHECKING:
    from app.db.models.core.organization import Organization
    from app.db.models.core.bank_account_localization import BankAccountLocalization


class BankAccount(Base):
    __tablename__ = "bank_accounts"
    __table_args__ = (
        Index(
            "idx_organization_id",
            "organization_id"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    localizations: Mapped[dict[str, BankAccountLocalization]] = relationship(
        back_populates="bank_account",
        collection_class=attribute_keyed_dict("language_code"),
        cascade="all, delete-orphan",
    )

    country_code: Mapped[str] = mapped_column(
        ForeignKey("countries.code"),
    )

    country: Mapped[Country] = relationship()

    iban: Mapped[str] = mapped_column(
        String(34),
        unique=True
    )

    swift: Mapped[str] = mapped_column(
        String(11),
    )

    currency_code: Mapped[str] = mapped_column(
        ForeignKey("currencies.code"),
    )

    currency: Mapped[Currency] = relationship()

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
    )

    organization: Mapped[Organization] = relationship(
        foreign_keys=[organization_id],
        back_populates="bank_accounts",
    )