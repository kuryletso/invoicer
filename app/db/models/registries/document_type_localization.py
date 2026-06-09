from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.references.language import Language

if TYPE_CHECKING:
    from app.db.models.registries.document_type import DocumentTypeRegistry


class DocumentTypeRegistryLocalization(Base):
    __tablename__ = "document_type_registry_localizations"

    document_type_code: Mapped[str] = mapped_column(
        ForeignKey("document_type_registry.code"),
        primary_key=True,
    )

    language_code: Mapped[str] = mapped_column(
        ForeignKey("languages.code"),
        primary_key=True,
    )

    document_type: Mapped[DocumentTypeRegistry] = relationship(
        foreign_keys=[document_type_code],
        back_populates="localizations",   
    )

    language: Mapped[Language] = relationship(
        foreign_keys=[language_code],
    )

    name: Mapped[str] = mapped_column(
        String(255),
    )

    description: Mapped[str | None] = mapped_column(
        String(255),
    )