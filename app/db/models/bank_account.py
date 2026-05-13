from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.organization import Organization

from sqlalchemy import Enum as SQLEnum, String, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from app.db.base import Base
from app.db.models.bank_account_localization import BankAccountLocalization
from app.domain.enums import Country, Currency, Language

class BankAccount(Base):
    __tablename__ = "bank_accounts"
    __table_args__ = (
        Index(
            "idx_organization_id",
            "organization_id"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False
    )

    organization: Mapped[Organization] = relationship(
        back_populates="bank_accounts"
    )

    country: Mapped[Country] = mapped_column(
        SQLEnum(Country, name="country_enum")
    )

    iban: Mapped[str] = mapped_column(
        String(34),
        unique=True
    )

    swift: Mapped[str] = mapped_column(String(11))

    currency: Mapped[Currency] = mapped_column(
        SQLEnum(Currency, name="currency_enum")
    )

    bank_account_localizations: Mapped[dict[Language, BankAccountLocalization]] = relationship(
        BankAccountLocalization,
        collection_class=attribute_mapped_collection("language"),
        cascade="all, delete-orphan"
    )