from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from app.db.base import Base
from app.db.models.references.language import Language

if TYPE_CHECKING:
    from app.db.models.references.country_localization import CountryLocalization
    

class Country(Base):
    __tablename__ = "countries"

    code: Mapped[str] = mapped_column(
        String(3),
        primary_key=True,
    )

    localizations: Mapped[dict[Language, CountryLocalization]] = relationship(
        back_populates="country",
        collection_class=attribute_mapped_collection("language_code"),
        cascade="all, delete-orphan",
    )