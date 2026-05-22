from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.types import LanguageEnum
from app.domain.enums import Language

if TYPE_CHECKING:
    from app.db.models.representative import Representative

class RepresentativeLocalization(Base):
    __tablename__ = "representative_localizations"

    representative_id: Mapped[int] = mapped_column(
        ForeignKey("representatives.id"),
        primary_key=True,
    )

    language: Mapped[Language] = mapped_column(
        LanguageEnum,
        primary_key=True,
    )

    representative: Mapped[Representative] = relationship(
        back_populates="localizations",
    )

    name: Mapped[str] = mapped_column(String(255))

    title: Mapped[str] = mapped_column(String(150))