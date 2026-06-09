from decimal import Decimal

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship, attribute_keyed_dict

from app.db.base import Base
from app.db.models.core.invoice_line_localization import InvoiceLineLocalization
from app.db.models.references.language import Language
from app.db.models.registries.measurement_unit import MeasurementUnitRegistry
from app.domain.constants import MONEY, QUANTITY, RATE


class InvoiceLine(Base):
    __tablename__ = "invoice_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    localizations: Mapped[dict[Language,InvoiceLineLocalization]] = relationship(
        back_populates="invoice_line",
        collection_class=attribute_keyed_dict("language_code"),
        cascade="all, delete-orphan",
        lazy="joined",
    )

    quantity: Mapped[Decimal] = mapped_column(QUANTITY)

    measurement_unit_code: Mapped[str] = mapped_column(
        ForeignKey("measurement_unit_registry.code"),
    )

    measurement_unit: Mapped[MeasurementUnitRegistry] = relationship()

    unit_price: Mapped[Decimal] = mapped_column(MONEY)

    tax_rate: Mapped[Decimal] = mapped_column(RATE)