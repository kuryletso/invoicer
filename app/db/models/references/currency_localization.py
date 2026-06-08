from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.references.currency import Currency


class CurrencyLocalization(Base):
    __tablename__ = "currency_localizations"

    currency_code: Mapped[str] = mapped_column(
        ForeignKey("currencies.code"),
        primary_key=True,
    )

    language_code: Mapped[str] = mapped_column(
        ForeignKey("languages.code"),
        primary_key=True,
    )

    currency: Mapped[Currency] = relationship(
        back_populates="localizations",
    )

    name: Mapped[str] = mapped_column(
        String(90),
    )