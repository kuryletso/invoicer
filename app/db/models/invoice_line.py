from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.snapshot import Snapshot

from decimal import Decimal

from sqlalchemy import String, Enum as SQLEnum, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.domain.enums import MeasurenentUnit

class InvoiceLine(Base):
    __tablename__ = "invoice_lines"

    id: Mapped[int] = mapped_column(primary_key=True)

    snapshot: Mapped[Snapshot] 

    description: Mapped[str] = mapped_column(String(255))

    quantity: Mapped[int] = relationship(back_populates="invoice_lines")

    unit: Mapped[MeasurenentUnit] = mapped_column(
        SQLEnum(MeasurenentUnit, name="unit_enum")
    )

    unit_price: Mapped[Decimal] = mapped_column(Numeric(12,2))

    tax_rate: Mapped[Decimal] = mapped_column(Numeric(5,4))

    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12,2))

    line_total: Mapped[Decimal] = mapped_column(Numeric(12,2))