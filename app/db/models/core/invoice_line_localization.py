from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.references.language import Language

if TYPE_CHECKING:
    from app.db.models.core.invoice_line import InvoiceLine


class InvoiceLineLocalization(Base):
    __tablename__ = "invoice_line_localizations"

    invoice_line_id: Mapped[int] = mapped_column(
        ForeignKey("invoice_lines.id"),
        primary_key=True,
    )

    language_code: Mapped[str] = mapped_column(
        ForeignKey("languages.code"),
        primary_key=True,
    )

    invoice_line: Mapped[InvoiceLine] = relationship(
        foreign_keys=[invoice_line_id],
        back_populates="localizations",
    )

    language: Mapped[Language] = relationship(
        foreign_keys=[language_code],
    )

    description: Mapped[str] = mapped_column(
        String(255),
    )