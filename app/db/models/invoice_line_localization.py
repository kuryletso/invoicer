from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.types import LanguageEnum
from app.domain.enums import Language

if TYPE_CHECKING:
    from app.db.models.invoice_line import InvoiceLine

class InvoiceLineLocalization(Base):
    __tablename__ = "invoice_line_localizations"

    invoice_line_id: Mapped[int] = mapped_column(
        ForeignKey("invoice_lines.id"),
        primary_key=True,
    )

    language: Mapped[Language] = mapped_column(
        LanguageEnum,
        primary_key=True,
    )

    invoice_line: Mapped[InvoiceLine] = relationship(
        back_populates="localizations"
    )

    description: Mapped[str] = mapped_column(
        String(255)
    )