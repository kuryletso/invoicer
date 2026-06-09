from __future__ import annotations

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from app.db.models.snapshots.snap_invoice_line import SnapInvoiceLine

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.references.language import Language


class SnapInvoiceLineLocalization(Base):
    __tablename__ = "snap_invoice_line_localizations"

    invoice_line_id: Mapped[int] = mapped_column(
        ForeignKey("snap_invoice_lines.id"),
        primary_key=True
    )

    language_code: Mapped[str] = mapped_column(
        ForeignKey("languages.code"),
        primary_key=True,
    )

    invoice_line: Mapped[SnapInvoiceLine] = relationship(
        foreign_keys=[invoice_line_id],
        back_populates="localizations",
    )

    language: Mapped[Language] = relationship(
        foreign_keys=[language_code],
    )

    description: Mapped[str] = mapped_column(
        String(255),
    )