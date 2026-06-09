from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship, attribute_keyed_dict

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.snapshots.snap_organization_localization import SnapOrganizationLocalization
    from app.db.models.snapshots.snap_representative import SnapRepresentative
    from app.db.models.snapshots.snap_bank_account import SnapBankAccount


class SnapOrganization(Base):
    __tablename__ = "snap_organizations"

    id: Mapped[int] = mapped_column(primary_key=True)

    localizations: Mapped[dict[str, SnapOrganizationLocalization]] = relationship(
        back_populates="organization",
        collection_class=attribute_keyed_dict("language_code"),
        cascade="all, delete-orphan",
    )

    email: Mapped[str | None] = mapped_column(
        String(100),
    )

    phone: Mapped[str | None] = mapped_column(
        String(18),
    )

    representative: Mapped[SnapRepresentative] = relationship(
        back_populates="organization",
        uselist=False,
        cascade="all, delete-orphan",
    )

    bank_account: Mapped[SnapBankAccount] = relationship(
        back_populates="organization",
        uselist=False,
        cascade="all, delete-orphan",
    )