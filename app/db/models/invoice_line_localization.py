from sqlalchemy import ForeignKey, Enum as SQLEnum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.domain.enums import Language

class InvoiceLineLocalization(Base):
    __tablename__ = "invoice_line_localizations"

    id: Mapped[int] = mapped_column(primary_key=True)

    invoice_line_id: Mapped[int] = mapped_column(
        ForeignKey("invoice_lines.id")
    )

    language: Mapped[Language] = mapped_column(
        SQLEnum(Language, name="language_enum")
    )

    description: Mapped[str] = mapped_column(String(255))