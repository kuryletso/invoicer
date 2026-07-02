from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.references.language import Language

if TYPE_CHECKING:
    from app.db.models.core.representative import Representative


class RepresentativeLocalization(Base):
    __tablename__ = "representative_localizations"

    representative_id: Mapped[int] = mapped_column(
        ForeignKey("representatives.id"),
        primary_key=True,
    )

    language_code: Mapped[str] = mapped_column(
        ForeignKey("languages.code"),
        primary_key=True,
    )

    representative: Mapped[Representative] = relationship(
        back_populates="localizations",
        foreign_keys=[representative_id],
    )

    language: Mapped[Language] = relationship(
        foreign_keys=[language_code],
    )

    name: Mapped[str] = mapped_column(
        String(255),
    )

    title: Mapped[str | None] = mapped_column(
        String(150),
    )