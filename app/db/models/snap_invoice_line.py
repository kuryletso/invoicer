from __future__ import annotations

from typing import TYPE_CHECKING
from decimal import Decimal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from app.db.base import Base
from app.db.types import MeasurementUnitEnum
from app.domain.enums import MeasurementUnit, Language
from app.domain.constants import MONEY, QUANTITY, RATE

if TYPE_CHECKING:
    from app.db.models.snap_invoice_line_localization import SnapInvoiceLineLocalization
    from app.db.models.snapshot import Snapshot

class SnapInvoiceLine(Base):
    __tablename__ = "snap_invoice_lines"

    id: Mapped[int] = mapped_column(primary_key=True)

    snapshot_id: Mapped[int] = mapped_column(
        ForeignKey("snapshots.id"),
        nullable=False
    )

    snapshot: Mapped[Snapshot] = relationship(
        back_populates="invoice_lines"
    )

    localizations: Mapped[dict[Language, SnapInvoiceLineLocalization]] = relationship(
        back_populates="invoice_line",
        collection_class=attribute_mapped_collection("language"),
        cascade="all, delete-orphan"
    )

    quantity: Mapped[Decimal] = mapped_column(QUANTITY)

    unit: Mapped[MeasurementUnit] = mapped_column(MeasurementUnitEnum)

    unit_price: Mapped[Decimal] = mapped_column(MONEY)

    tax_rate: Mapped[Decimal] = mapped_column(RATE)

    tax_amount: Mapped[Decimal] = mapped_column(MONEY)

    line_total: Mapped[Decimal] = mapped_column(MONEY)