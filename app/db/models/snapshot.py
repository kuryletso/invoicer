from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.db.models.invoice_line import InvoiceLine
    from app.db.models.snap_party import SnapParty
    from app.db.models.snap_template import SnapTemplate

from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import String, Date, DateTime, Enum as SQLEnum, Numeric, ForeignKey, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.domain.enums import Currency, Language, DocumentType

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

    document_type: Mapped[DocumentType] = mapped_column(
        SQLEnum(DocumentType, name="document_type_enum")
    )

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

    currency: Mapped[Currency] = mapped_column(
        SQLEnum(Currency, name="currency_enum")
    )

    primary_language: Mapped[Language] = mapped_column(
        SQLEnum(Language, name="language_enum")
    )

    secondary_language: Mapped[Optional[Language]]= mapped_column(
        SQLEnum(Language, name="language_enum"),
        nullable=True
    )

    subtotal: Mapped[Decimal] = mapped_column(Numeric(12,2))

    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12,2))

    total: Mapped[Decimal] = mapped_column(Numeric(12,2))

    invoice_lines: Mapped[list[InvoiceLine]] = relationship(
        back_populates="snapshot",
        cascade="all, delete-orphan"
    )

    contractor_id: Mapped[int] = mapped_column(ForeignKey("snap_parties.id"))

    client_id: Mapped[int] = mapped_column(ForeignKey("snap_parties.id"))

    contractor: Mapped[SnapParty] = relationship(foreign_keys=[contractor_id])

    client: Mapped[SnapParty] = relationship(foreign_keys=[client_id])

    snap_template: Mapped[SnapTemplate] = relationship()