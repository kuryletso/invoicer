from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.references.language import Language

if TYPE_CHECKING:
    from app.db.models.snapshots.snap_representative import SnapRepresentative


class SnapRepresentativeLocalization(Base):
    __tablename__ = "snap_representative_localizations"

    representative_id: Mapped[int] = mapped_column(
        ForeignKey("snap_representatives.id"),
        primary_key=True
    )

    language_code: Mapped[str] = mapped_column(
        ForeignKey("languages.code"),
        primary_key=True,
    )

    representative: Mapped[SnapRepresentative] = relationship(
        foreign_keys=[representative_id],
        back_populates="localizations"
    )

    language: Mapped[Language] = relationship(
        foreign_keys=[language_code],
    )

    name: Mapped[str] = mapped_column(
        String(120),
    )

    title: Mapped[str | None] = mapped_column(
        String(120),
    )