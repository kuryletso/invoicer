from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from app.db.base import Base
from app.domain.enums import Language

if TYPE_CHECKING:
    from app.db.models.snap_organization import SnapOrganization
    from app.db.models.snap_representative_localization import SnapRepresentativeLocalization

class SnapRepresentative(Base):
    __tablename__ = "snap_representatives"

    id: Mapped[int] = mapped_column(primary_key=True)

    localizations: Mapped[dict[Language, SnapRepresentativeLocalization]] = relationship(
        back_populates="representative",
        collection_class=attribute_mapped_collection("language"),
        cascade="all, delete-orphan"
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("snap_organizations.id"),
        nullable=False
    )

    organization: Mapped[SnapOrganization] = relationship(
        back_populates="representative"
    )