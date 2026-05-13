from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.organization import Organization

from sqlalchemy import Enum as SQLEnum, ForeignKey, UniqueConstraint, String, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

from app.domain.enums import Country, TaxIdSystem

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

    id: Mapped[int] = mapped_column(primary_key=True)

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False
    )

    organization: Mapped[Organization] = relationship(
        back_populates="tax_ids"
    )

    system: Mapped[TaxIdSystem] = mapped_column(
        SQLEnum(TaxIdSystem, name="tax_id_system_enum"),
        nullable=False
    )

    country: Mapped[Country] = mapped_column(
        SQLEnum(Country, name="country_enum")
    )

    value: Mapped[str] = mapped_column(String(17))