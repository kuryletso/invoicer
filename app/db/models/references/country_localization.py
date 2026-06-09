from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.references.language import Language

if TYPE_CHECKING:
    from app.db.models.references.country import Country


class CountryLocalization(Base):
    __tablename__ = "country_localizations"

    country_code: Mapped[str] = mapped_column(
        ForeignKey("countries.code"),
        primary_key=True,
    )

    language_code: Mapped[str] = mapped_column(
        ForeignKey("languages.code"),
        primary_key=True,
    )

    country: Mapped[Country] = relationship(
        foreign_keys=[country_code],
        back_populates="localizations",
    )

    language: Mapped[Language] = relationship(
        foreign_keys=[language_code],
    )

    name: Mapped[str] = mapped_column(
        String(120),
    )