from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from app.db.base import Base
from app.db.types import CountryEnum, CurrencyEnum
from app.domain.enums import Country, Currency, Language

if TYPE_CHECKING:
    from app.db.models.organization import Organization
    from app.db.models.bank_account_localization import BankAccountLocalization

class BankAccount(Base):
    __tablename__ = "bank_accounts"
    __table_args__ = (
        Index(
            "idx_organization_id",
            "organization_id"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    localizations: Mapped[dict[Language, BankAccountLocalization]] = relationship(
        back_populates="bank_account",
        collection_class=attribute_mapped_collection("language"),
        cascade="all, delete-orphan",
    )

    country: Mapped[Country] = mapped_column(
        CountryEnum,
    )

    iban: Mapped[str] = mapped_column(
        String(34),
        unique=True
    )

    swift: Mapped[str] = mapped_column(String(11))

    currency: Mapped[Currency] = mapped_column(CurrencyEnum)

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False,
    )

    organization: Mapped[Organization] = relationship(
        back_populates="bank_accounts",
    )