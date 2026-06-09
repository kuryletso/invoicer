from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.core.organization import Organization

from sqlalchemy import ForeignKey, UniqueConstraint, String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.references.country import Country
from app.db.models.registries.tax_id_system import TaxIdSystemRegistry


class TaxId(Base):
    __tablename__ = "tax_ids"

    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "system",
            "country",
            name="unique_organization_tax_id_system"
        ),
        Index(
            "idx_country_system_value",
            "country",
            "system",
            "value"
        )
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
    )

    organization: Mapped[Organization] = relationship(
        foreign_keys=[organization_id],
        back_populates="tax_ids",
    )

    tax_id_system_code: Mapped[str] = mapped_column(
        ForeignKey("tax_id_system_registry.code"),
    )

    tax_id_system: Mapped[TaxIdSystemRegistry] = relationship()

    country_code: Mapped[str] = mapped_column(
        ForeignKey("countries.code"),
    )

    country: Mapped[Country] = relationship()

    value: Mapped[str] = mapped_column(
        String(17),
    )