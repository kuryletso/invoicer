from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base

if TYPE_CHECKING:
    from app.db.models.registries.tax_id_sysyem import TaxIdSystemRegistry


class TaxIdSystemRegistryLocalization(Base):
    __tablename__ = "tax_id_system_registry_localizations"

    tax_id_system_code: Mapped[str] = mapped_column(
        ForeignKey("tax_id_system_registry.code"),
        primary_key=True,
    )

    language_code: Mapped[str] = mapped_column(
        ForeignKey("languages.code"),
        primary_key=True,
    )

    tax_id_system: Mapped[TaxIdSystemRegistry] = relationship(
        back_populates="localizations",
    )

    name: Mapped[str] = mapped_column(
        String(255),
    )