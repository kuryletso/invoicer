from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, JSON, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column, relationship, attribute_keyed_dict

from app.db.base import Base

from app.document_engine.enums.enums import PlaceholderType

if TYPE_CHECKING:
    from app.db.models.registries.placeholder_localization import PlaceholderRegistryLocalization


class PlaceholderRegistry(Base):
    __tablename__ = "placeholder_registry"

    key: Mapped[str] = mapped_column(
        String(90),
        primary_key=True,
    )

    required: Mapped[bool]

    type: Mapped[PlaceholderType] = mapped_column(
        SQLEnum(PlaceholderType),
    )

    active: Mapped[bool]

    columns: Mapped[list[str] | None] = mapped_column(
        JSON,
    )

    localizations: Mapped[dict[str, PlaceholderRegistryLocalization]] = relationship(
        back_populates="placeholder",
        collection_class=attribute_keyed_dict("language_code"),
        cascade="all, delete-orphan",
    )