from __future__ import annotations

from typing import TYPE_CHECKING, Optional

if TYPE_CHECKING:
    from app.db.models.invoice_line import InvoiceLine
    from app.db.models.party import Party
    from app.db.models.snap_tamplate import SnapTemplate

from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import String, Date, DateTime, Enum as SQLEnum, Numeric, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.db.base import Base
from app.domain.enums import Currency, Language

class Snapshot(Base):
    __tablename__ = "snapshots"

    id: Mapped[int] = mapped_column(primary_key=True)

    serial: Mapped[str] = mapped_column(
        String(25),
        unique=True
    )

    document_type: Mapped[str] = mapped_column(String(25))

    issue_date: Mapped[date] = mapped_column(Date)

    due_date: Mapped[Optional[date]] = mapped_column(
        Date,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    currency: Mapped[Currency] = mapped_column(
        SQLEnum(Currency, name="currency_enum")
    )

    languages: Mapped[list[Language]] = mapped_column(
        SQLEnum(Language, name="language_enum")
    )

    subtotal: Mapped[Decimal] = mapped_column(Numeric(12,2))

    tax_amount: Mapped[Decimal] = mapped_column(Numeric(12,2))

    total: Mapped[Decimal] = mapped_column(Numeric(12,2))

    invoice_lines: Mapped[list[InvoiceLine]] = relationship(
        back_populates="snapshot",
        cascade="all, delete-orphan"
    )

    contractor_id: Mapped[int] = mapped_column(ForeignKey("parties.id"))

    client_id: Mapped[int] = mapped_column(ForeignKey("parties.id"))

    contractor: Mapped[Party] = relationship(foreign_keys=[contractor_id])

    client: Mapped[Party] = relationship(foreign_keys=[client_id])

    snap_template: Mapped[SnapTemplate] = relationship()