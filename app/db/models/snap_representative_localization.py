from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.types import LanguageEnum
from app.domain.enums import Language

if TYPE_CHECKING:
    from app.db.models.snap_representative import SnapRepresentative

class SnapRepresentativeLocalization(Base):
    __tablename__ = "snap_representative_localizations"

    representative_id: Mapped[int] = mapped_column(
        ForeignKey("snap_representatives.id"),
        primary_key=True
    )

    language: Mapped[Language] = mapped_column(
        LanguageEnum,
        primary_key=True
    )

    representative: Mapped[SnapRepresentative] = relationship(
        back_populates="localizations"
    )

    name: Mapped[str] = mapped_column(String(120))

    title: Mapped[Optional[str]] = mapped_column(
        String(120),
        nullable=True
    )