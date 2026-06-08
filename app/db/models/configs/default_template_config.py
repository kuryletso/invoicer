from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.references.language import Language
from app.db.models.registries.document_type import DocumentTypeRegistry


class DefaultTemplateConfig(Base):
    __tablename__ = "default_template_config"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    primary_language_code: Mapped[str] = mapped_column(
        ForeignKey("languages.code"),
        nullable=False,
    )

    primary_language: Mapped[Language] = relationship(
        foreign_keys=[primary_language_code]
    )

    secondary_language_code: Mapped[str] = mapped_column(
        ForeignKey("languages.code"),
        nullable=True,
    )

    secondary_language: Mapped[Language] = relationship(
        foreign_keys=[secondary_language_code]
    )

    type_id: Mapped[int] = mapped_column(
        ForeignKey("document_types.id"),
        nullable=False,
    )

    type: Mapped[DocumentTypeRegistry] = relationship(
        foreign_keys=[type_id]
    )

    name: Mapped[str] = mapped_column(
        String(255),
    )

    description: Mapped[str] = mapped_column(
        String(255),
    )