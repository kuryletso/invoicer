from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship, attribute_keyed_dict

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.registries.measurement_unit_localization import MeasurementUnitRegistryLocalization


class MeasurementUnitRegistry(Base):
    __tablename__ = "measurement_unit_registry"

    code: Mapped[str] = mapped_column(
        String(30),
        primary_key=True,
    )

    localizations: Mapped[dict[str, MeasurementUnitRegistryLocalization]] = relationship(
        back_populates="measurement_unit",
        collection_class=attribute_keyed_dict("language_code"),
        cascade="all, delete-orphan",
    )