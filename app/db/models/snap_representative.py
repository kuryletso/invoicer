from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.db.models.snap_party import SnapParty

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

class SnapRepresentative(Base):
    __tablename__ = "snap_representatives"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(120))

    title: Mapped[Optional[str]] = mapped_column(
        String(120),
        nullable=True
    )

    party_id: Mapped[int] = mapped_column(
        ForeignKey("snap_parties.id"),
        nullable=False
    )

    party: Mapped[SnapParty] = relationship(
        back_populates="snap_representative"
    )