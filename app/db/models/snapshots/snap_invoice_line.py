from __future__ import annotations

from typing import TYPE_CHECKING
from decimal import Decimal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, attribute_keyed_dict

from app.db.base import Base
from app.db.models.references.language import Language
from app.db.models.registries.measurement_unit import MeasurementUnitRegistry
from app.domain.constants import MONEY, QUANTITY, RATE

if TYPE_CHECKING:
    from app.db.models.snapshots.snap_invoice_line_localization import SnapInvoiceLineLocalization
    from app.db.models.snapshots.snapshot import Snapshot


class SnapInvoiceLine(Base):
    __tablename__ = "snap_invoice_lines"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    snapshot_id: Mapped[int] = mapped_column(
        ForeignKey("snapshots.id"),
    )

    snapshot: Mapped[Snapshot] = relationship(
        foreign_keys=[snapshot_id],
        back_populates="invoice_lines",
    )

    localizations: Mapped[dict[Language, SnapInvoiceLineLocalization]] = relationship(
        back_populates="invoice_line",
        collection_class=attribute_keyed_dict("language_code"),
        cascade="all, delete-orphan"
    )

    quantity: Mapped[Decimal] = mapped_column(QUANTITY)

    measurement_unit_code: Mapped[str] = mapped_column(
        ForeignKey("measurement_unit_registry.code"),
    )

    unit: Mapped[MeasurementUnitRegistry] = relationship()

    unit_price: Mapped[Decimal] = mapped_column(MONEY)

    tax_rate: Mapped[Decimal] = mapped_column(RATE)

    tax_amount: Mapped[Decimal] = mapped_column(MONEY)

    line_total: Mapped[Decimal] = mapped_column(MONEY)