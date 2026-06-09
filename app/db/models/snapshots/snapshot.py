from __future__ import annotations

from typing import TYPE_CHECKING
from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import String, Date, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.models.references.currency import Currency
from app.db.models.references.language import Language
from app.db.models.registries.document_type import DocumentTypeRegistry
from app.domain.constants import MONEY

if TYPE_CHECKING:
    from app.db.models.snapshots.snap_invoice_line import SnapInvoiceLine
    from app.db.models.snapshots.snap_organization import SnapOrganization
    from app.db.models.snapshots.snap_template import SnapTemplate


class Snapshot(Base):
    __tablename__ = "snapshots"
    __table_args__ = (
        Index(
            "idx_issue_date_serial_document_type",
            "issue_date",
            "serial",
            "document_type"
        ),
    )

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )

    serial: Mapped[str] = mapped_column(
        String(25),
        unique=True,
        index=True,
    )

    document_type_code: Mapped[str] = mapped_column(
        ForeignKey("document_type_registry.code"),
    )

    document_type: Mapped[DocumentTypeRegistry] = relationship()

    issue_date: Mapped[date] = mapped_column(
        Date,
        index=True,
    )

    due_date: Mapped[date | None] = mapped_column(
        Date,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True,
    )

    currency_code: Mapped[str] = mapped_column(
        ForeignKey("currencies.code"),
    )

    currency: Mapped[Currency] = relationship()

    primary_language_code: Mapped[str] = mapped_column(
        ForeignKey("languages.code"),
    )

    primary_language: Mapped[Language] = relationship(
        foreign_keys=[primary_language_code],
    )

    secondary_language_code: Mapped[str | None] = mapped_column(
        ForeignKey("languages.code"),
    )

    secondary_language: Mapped[Language | None]= relationship(
        foreign_keys=[secondary_language_code],
    )

    subtotal: Mapped[Decimal] = mapped_column(MONEY)

    tax_amount: Mapped[Decimal] = mapped_column(MONEY)

    total: Mapped[Decimal] = mapped_column(MONEY)

    invoice_lines: Mapped[list[SnapInvoiceLine]] = relationship(
        back_populates="snapshot",
        cascade="all, delete-orphan",
    )

    contractor_id: Mapped[int] = mapped_column(
        ForeignKey("snap_organizations.id"),
    )

    client_id: Mapped[int] = mapped_column(
        ForeignKey("snap_organizations.id"),
    )

    contractor: Mapped[SnapOrganization] = relationship(
        foreign_keys=[contractor_id],
    )

    client: Mapped[SnapOrganization] = relationship(
        foreign_keys=[client_id],
    )

    template_id: Mapped[int] = mapped_column(
        ForeignKey("snap_templates.id"),
    )

    template: Mapped[SnapTemplate] = relationship()