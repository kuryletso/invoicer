from __future__ import annotations

from typing import TYPE_CHECKING, Optional
from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import String, Date, DateTime, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.db.types import CurrencyEnum, LanguageEnum, DocumentTypeEnum
from app.domain.enums import Currency, Language, DocumentType
from app.domain.constants import MONEY

if TYPE_CHECKING:
    from app.db.models.snap_invoice_line import SnapInvoiceLine
    from app.db.models.snap_organization import SnapOrganization
    from app.db.models.snap_template import SnapTemplate

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

    id: Mapped[int] = mapped_column(primary_key=True)

    serial: Mapped[str] = mapped_column(
        String(25),
        unique=True,
        index=True
    )

    document_type: Mapped[DocumentType] = mapped_column(DocumentTypeEnum)

    issue_date: Mapped[date] = mapped_column(
        Date,
        index=True
    )

    due_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        index=True
    )

    currency: Mapped[Currency] = mapped_column(CurrencyEnum)

    primary_language: Mapped[Language] = mapped_column(LanguageEnum)

    secondary_language: Mapped[Optional[Language]]= mapped_column(
        LanguageEnum,
        nullable=True
    )

    subtotal: Mapped[Decimal] = mapped_column(MONEY)

    tax_amount: Mapped[Decimal] = mapped_column(MONEY)

    total: Mapped[Decimal] = mapped_column(MONEY)

    invoice_lines: Mapped[list[SnapInvoiceLine]] = relationship(
        back_populates="snapshot",
        cascade="all, delete-orphan"
    )

    contractor_id: Mapped[int] = mapped_column(ForeignKey("snap_organizations.id"))

    client_id: Mapped[int] = mapped_column(ForeignKey("snap_organizations.id"))

    contractor: Mapped[SnapOrganization] = relationship(foreign_keys=[contractor_id])

    client: Mapped[SnapOrganization] = relationship(foreign_keys=[client_id])

    template: Mapped[SnapTemplate] = relationship()