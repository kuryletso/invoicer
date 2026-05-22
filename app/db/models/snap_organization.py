from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from app.db.base import Base
from app.domain.enums import Language

if TYPE_CHECKING:
    from app.db.models.snap_organization_localization import SnapOrganizationLocalization
    from app.db.models.snap_representative import SnapRepresentative
    from app.db.models.snap_bank_account import SnapBankAccount

class SnapOrganization(Base):
    __tablename__ = "snap_organizations"

    id: Mapped[int] = mapped_column(primary_key=True)

    localizations: Mapped[dict[Language,SnapOrganizationLocalization]] = relationship(
        back_populates="organization",
        collection_class=attribute_mapped_collection("language"),
        cascade="all, delete-orphan",
    )

    email: Mapped[Optional[str]] = mapped_column(
        String(100),
        nullable=True
    )

    phone: Mapped[Optional[str]] = mapped_column(
        String(18),
        nullable=True
    )

    representative: Mapped[SnapRepresentative] = relationship(
        back_populates="organization",
        uselist=False,
        cascade="all, delete-orphan"
    )

    bank_account: Mapped[SnapBankAccount] = relationship(
        back_populates="organization",
        uselist=False,
        cascade="all, delete-orphan"
    )