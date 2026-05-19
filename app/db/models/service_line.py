from decimal import Decimal

from sqlalchemy import Numeric, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.orm.collections import attribute_mapped_collection

from app.db.base import Base
from app.db.models.service_line_localization import ServiceLineLocalization
from app.domain.enums import MeasurementUnit, Language

class ServiceLine(Base):
    __tablename__ = "service_lines"
    __table_args__ = (
        UniqueConstraint(
            "service_line",
            "language",
            name="unique_service_line_language"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)
    
    quantity: Mapped[Decimal] = mapped_column(Numeric(12,3))

    unit: Mapped[MeasurementUnit] = mapped_column(
        SQLEnum(MeasurementUnit, name="unit_enum")
    )

    unit_price: Mapped[Decimal] = mapped_column(Numeric(12,2))

    tax_rate: Mapped[Decimal] = mapped_column(Numeric(6,5))

    localizations: Mapped[dict[Language,ServiceLineLocalization]] = relationship(
        ServiceLineLocalization,
        collection_class=attribute_mapped_collection("language"),
        cascade="all, delete-orphan",
        lazy="joined"
    )