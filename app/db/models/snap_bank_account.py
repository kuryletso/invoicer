from __future__ import annotations

from typing import TYPE_CHECKING, Optional


from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from app.db.base import Base
from app.db.types import CurrencyEnum
from app.domain.enums import Currency, Language

if TYPE_CHECKING:
    from app.db.models.snap_organization import SnapOrganization
    from app.db.models.snap_bank_account_localization import SnapBankAccountLocalization

class SnapBankAccount(Base):
    __tablename__ = "snap_bank_accounts"

    id: Mapped[int] = mapped_column(primary_key=True)

    localizations: Mapped[dict[Language,SnapBankAccountLocalization]] = relationship(
        back_populates="bank_account",
        collection_class=attribute_mapped_collection("language"),
        cascade="all, delete-orphan",
    )

    iban: Mapped[str] = mapped_column(String(34))

    swift: Mapped[Optional[str]] = mapped_column(
        String(11),
        nullable=True
    )

    currency: Mapped[Currency] = mapped_column(
        CurrencyEnum,
    )

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("snap_organizations.id"),
        nullable=False
    )

    organization: Mapped[SnapOrganization] = relationship(
        back_populates="snap_bank_account"
    )