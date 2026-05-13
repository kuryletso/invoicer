from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.organization import Organization

from sqlalchemy import Enum as SQLEnum, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from app.db.base import Base
from app.db.models.bank_account_localization import BankAccountLocalization
from app.domain.enums import Country, Currency, Language

class BankAccount(Base):
    __tablename__ = "bank_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)

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

    bank_account_localization: Mapped[dict[Language, BankAccountLocalization]] = relationship(
        BankAccountLocalization,
        collection_class=attribute_mapped_collection("language"),
        cascade="all, delete-orphan"
    )