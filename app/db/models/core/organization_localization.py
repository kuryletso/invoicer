from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.references.language import Language

if TYPE_CHECKING:
    from app.db.models.core.organization import Organization


class OrganizationLocalization(Base):
    __tablename__ = "organization_localizations"

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        primary_key=True,
    )

    language_code: Mapped[str] = mapped_column(
        ForeignKey("languages.code"),
        primary_key=True,
    )

    organization: Mapped[Organization] = relationship(
        foreign_keys=[organization_id],
        back_populates="localizations",
    )

    language: Mapped[Language] = relationship(
        foreign_keys=[language_code],
    )

    legal_name: Mapped[str] = mapped_column(
        String(255),
    )

    address: Mapped[str | None] = mapped_column(
        String(255),
    )