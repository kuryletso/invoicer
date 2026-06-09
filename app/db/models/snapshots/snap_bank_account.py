from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, attribute_keyed_dict

from app.db.base import Base
from app.db.models.references.language import Language
from app.db.models.references.currency import Currency

if TYPE_CHECKING:
    from app.db.models.snapshots.snap_organization import SnapOrganization
    from app.db.models.snapshots.snap_bank_account_localization import SnapBankAccountLocalization


class SnapBankAccount(Base):
    __tablename__ = "snap_bank_accounts"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    localizations: Mapped[dict[Language,SnapBankAccountLocalization]] = relationship(
        back_populates="bank_account",
        collection_class=attribute_keyed_dict("language_code"),
        cascade="all, delete-orphan",
    )

    iban: Mapped[str] = mapped_column(
        String(34),
    )

    swift: Mapped[str | None] = mapped_column(
        String(11),
    )

    currency_code: Mapped[str] = mapped_column(
        ForeignKey("currencies.code"),
    )

    currency: Mapped[Currency] = relationship()

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("snap_organizations.id"),
    )

    organization: Mapped[SnapOrganization] = relationship(
        foreign_keys=[organization_id],
        back_populates="snap_bank_account",
    )