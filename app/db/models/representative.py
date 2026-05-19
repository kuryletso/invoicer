from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.organization import Organization

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from app.db.base import Base
from app.db.associations import organization_representative_m2m
from app.domain.enums import Language
from app.db.models.representative_localization import RepresentativeLocalization

class Representative(Base):
    __tablename__ = "representatives"

    id: Mapped[int] = mapped_column(primary_key=True)

    organizations: Mapped[list[Organization]] = relationship(
        secondary=organization_representative_m2m,
        back_populates="representatives"
    )

    localizations: Mapped[dict[Language, RepresentativeLocalization]] = relationship(
        collection_class=attribute_mapped_collection("language"),
        cascade="all, delete-orphan"
    )