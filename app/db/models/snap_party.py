from __future__ import annotations

from typing import Optional, TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.snap_representative import SnapRepresentative
    from app.db.models.snap_bank_account import SnapBankAccount


from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from app.db.base import Base
from app.db.models.snap_party_localization import SnapPartyLocalization
from app.domain.enums import Language

class SnapParty(Base):
    __tablename__ = "snap_parties"

    id: Mapped[int] = mapped_column(primary_key=True)

    legal_name: Mapped[dict[Language,SnapPartyLocalization]] = relationship(
        SnapPartyLocalization,
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

    address: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )

    tax_id: Mapped[str] = mapped_column(String(100))

    snap_representative: Mapped[SnapRepresentative] = relationship(
        back_populates="party",
        uselist=False,
        cascade="all, delete-orphan"
    )

    snap_bank_account: Mapped[SnapBankAccount] = relationship(
        back_populates="party",
        uselist=False,
        cascade="all, delete-orphan"
    )