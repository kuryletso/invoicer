from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.registries.measurement_unit import MeasurementUnitRegistry


class MeasurementUnitRegistryLocalization(Base):
    __tablename__ = "measurement_unit_registry_localizations"

    measurement_unit_code: Mapped[str] = mapped_column(
        ForeignKey("measurement_unit_registry.code"),
        primary_key=True,
    )

    language_code: Mapped[str] = mapped_column(
        ForeignKey("languages.code"),
        primary_key=True,
    )

    measurement_unit: Mapped[MeasurementUnitRegistry] = relationship(
        back_populates="localizations",
    )

    name: Mapped[str] = mapped_column(
        String(255),
    )