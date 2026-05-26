from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from sqlalchemy import String, UniqueConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.types import DocumentTypeEnum
from app.domain.enums import DocumentType

if TYPE_CHECKING:
    from app.db.models.organization import Organization

class DocumentSequence(Base):
    __tablename__ = "document_sequences"
    __table_args__ = (
        UniqueConstraint(
            "organization_id",
            "document_type",
            "prefix",
            name="unique_organization_id_document_type_prefix"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    document_type: Mapped[DocumentType] = mapped_column(
        DocumentTypeEnum,
        nullable=False,
    ) 

    organization_id: Mapped[int] = mapped_column(
        ForeignKey("organizations.id"),
        nullable=False
    )

    organization: Mapped[Organization] = relationship(
        back_populates="sequences",
    )

    prefix: Mapped[Optional[str]] = mapped_column(
        String(32),
        nullable=False,
        default="",
    )

    counter: Mapped[int]