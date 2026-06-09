from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy.orm import Mapped, mapped_column, relationship, attribute_keyed_dict

from app.db.base import Base
from app.db.associations import organization_representative_m2m
from app.db.models.references.language import Language

if TYPE_CHECKING:
    from app.db.models.core.organization import Organization
    from app.db.models.core.representative_localization import RepresentativeLocalization


class Representative(Base):
    __tablename__ = "representatives"

    id: Mapped[int] = mapped_column(primary_key=True)

    organizations: Mapped[list[Organization]] = relationship(
        secondary=organization_representative_m2m,
        back_populates="representatives",
    )

    localizations: Mapped[dict[Language, RepresentativeLocalization]] = relationship(
        back_populates="representative",
        collection_class=attribute_keyed_dict("language_code"),
        cascade="all, delete-orphan",
    )