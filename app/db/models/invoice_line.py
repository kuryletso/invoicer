from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from app.db.models.snapshot import Snapshot

from decimal import Decimal

from sqlalchemy import Enum as SQLEnum, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from app.db.base import Base
from app.db.models.invoice_line_localization import InvoiceLineLocalization
from app.domain.enums import MeasurementUnit, Language

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

    description: Mapped[dict[Language, InvoiceLineLocalization]] = relationship(
        InvoiceLineLocalization,
        collection_class=attribute_mapped_collection("language"),
        cascade="all, delete-orphan"
    )

    quantity: Mapped[Decimal] = mapped_column(Numeric(12,3))

    unit: Mapped[MeasurementUnit] = mapped_column(
        SQLEnum(MeasurementUnit, name="unit_enum")
    )

    unit_price: Mapped[Decimal] = mapped_column(Numeric(12,2))

    tax_rate: Mapped[Decimal] = mapped_column(Numeric(6,5))

    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12,2))

    line_total: Mapped[Decimal] = mapped_column(Numeric(12,2))