from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, attribute_keyed_dict

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.snapshots.snap_organization import SnapOrganization
    from app.db.models.snapshots.snap_representative_localization import SnapRepresentativeLocalization


class SnapRepresentative(Base):
    __tablename__ = "snap_representatives"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    localizations: Mapped[dict[str, SnapRepresentativeLocalization]] = relationship(
        back_populates="representative",
        collection_class=attribute_keyed_dict("language_code"),
        cascade="all, delete-orphan",
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("snap_organizations.id"),
    )

    organization: Mapped[SnapOrganization] = relationship(
        foreign_keys=[organization_id],
        back_populates="representative",
    )