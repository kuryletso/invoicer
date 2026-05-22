from decimal import Decimal

from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from app.db.base import Base
from app.db.models.invoice_line_localization import InvoiceLineLocalization
from app.db.types import MeasurementUnitEnum
from app.domain.enums import MeasurementUnit, Language
from app.domain.constants import MONEY, QUANTITY, RATE

class InvoiceLine(Base):
    __tablename__ = "invoice_lines"

    id: Mapped[int] = mapped_column(primary_key=True)
    
    localizations: Mapped[dict[Language,InvoiceLineLocalization]] = relationship(
        back_populates="invoice_line",
        collection_class=attribute_mapped_collection("language"),
        cascade="all, delete-orphan",
        lazy="joined"
    )

    quantity: Mapped[Decimal] = mapped_column(QUANTITY)

    unit: Mapped[MeasurementUnit] = mapped_column(MeasurementUnitEnum)

    unit_price: Mapped[Decimal] = mapped_column(MONEY)

    tax_rate: Mapped[Decimal] = mapped_column(RATE)