from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship, attribute_keyed_dict

from app.db.base import Base
from app.db.models.references.language import Language

if TYPE_CHECKING:
    from app.db.models.registries.document_type_localization import DocumentTypeRegistryLocalization


class DocumentTypeRegistry(Base):
    __tablename__ = "document_type_registry"

    code: Mapped[str] = mapped_column(
        String(30),
        primary_key=True,
    )

    localizations: Mapped[dict[Language, DocumentTypeRegistryLocalization]] = relationship(
        back_populates="document_type",
        collection_class=attribute_keyed_dict("language_code"),
        cascade="all, delete-orphan",
    )