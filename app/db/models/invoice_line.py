from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.snapshot import Snapshot

from decimal import Decimal

from sqlalchemy import String, Enum as SQLEnum, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.domain.enums import MeasurenentUnit

class InvoiceLine(Base):
    __tablename__ = "invoice_lines"

    id: Mapped[int] = mapped_column(primary_key=True)

    snapshot_id: Mapped[int] = mapped_column(
        ForeignKey("snapshots.id"),
        nullable=False
    )

    snapshot: Mapped[Snapshot] = relationship(
        back_populates="invoice_lines"
    )

    description: Mapped[str] = mapped_column(String(255))

    quantity: Mapped[Decimal] = mapped_column(Numeric(12,3))

    unit: Mapped[MeasurenentUnit] = mapped_column(
        SQLEnum(MeasurenentUnit, name="unit_enum")
    )

    unit_price: Mapped[Decimal] = mapped_column(Numeric(12,2))

    tax_rate: Mapped[Decimal] = mapped_column(Numeric(6,5))

    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12,2))

    line_total: Mapped[Decimal] = mapped_column(Numeric(12,2))