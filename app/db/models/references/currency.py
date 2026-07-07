from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship, attribute_keyed_dict

from app.db.base import Base

from app.document_engine.enums.enums import MoneySymbolPosition

if TYPE_CHECKING:
    from app.db.models.references.currency_localization import CurrencyLocalization


# SEEDING
class Currency(Base):
    __tablename__ = "currencies"

    code: Mapped[str] = mapped_column(
        String(3),
        primary_key=True,
    )

    decimal_places: Mapped[int]

    decimal_separator: Mapped[str] = mapped_column(String(1))       # "." or ","

    grouping_separator: Mapped[str] = mapped_column(String(1))      # "," or " "

    symbol_position: Mapped[MoneySymbolPosition] = mapped_column(SQLEnum(MoneySymbolPosition))

    symbol_spacing: Mapped[bool]

    localizations: Mapped[dict[str, CurrencyLocalization]] = relationship(
        back_populates="currency",
        collection_class=attribute_keyed_dict("language_code"),
        cascade="all, delete-orphan",
    )