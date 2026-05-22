from __future__ import annotations

from typing import TYPE_CHECKING, Optional

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.types import LanguageEnum
from app.domain.enums import Language

if TYPE_CHECKING:
    from app.db.models.snap_organization import SnapOrganization

class SnapOrganizationLocalization(Base):
    __tablename__ = "snap_organization_localizations"

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("snap_organizations.id"),
        primary_key=True
    )

    language: Mapped[Language] = mapped_column(
        LanguageEnum,
        primary_key=True
    )

    organization: Mapped[SnapOrganization] = relationship(
        back_populates="localizations"
    )

    legal_name: Mapped[str] = mapped_column(String(255))

    tax_id: Mapped[str] = mapped_column(String(100))

    address: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )