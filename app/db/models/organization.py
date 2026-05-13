from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.db.models.organization_localization import OrganizationLocalization
    from app.db.models.representative import Representative
    from app.db.models.bank_account import BankAccount
    from app.db.models.tax_id import TaxId

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from app.db.base import Base
from app.domain.enums import Language
from app.db.associations import organization_representative_m2m

class Organization(Base):
    __tablename__ = "organizations"

    id: Mapped[int] = mapped_column(primary_key=True)

    email: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    phone: Mapped[Optional[str]] = mapped_column(
        String(16),
        nullable=True
    )

    organization_localization: Mapped[dict[Language,OrganizationLocalization]] = relationship(
        OrganizationLocalization,
        collection_class=attribute_mapped_collection("language"),
        cascade="all, delete-orphan"
    )

    representatives: Mapped[list[Representative]] = relationship(
        secondary=organization_representative_m2m,
        back_populates="organizations"
    )

    bank_accounts: Mapped[list[BankAccount]] = relationship(
        back_populates="organization"
    )

    tax_ids: Mapped[list[TaxId]] = relationship(
        back_populates="organization",
        cascade="all, delete-orphan"
    )