from sqlalchemy import String, ForeignKey, Enum as SQLEnum, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.domain.enums import Language

class ServiceLineLocalization(Base):
    __tablename__ = "service_line_localizations"
    __table_args__ = (
        UniqueConstraint(
            "service_line",
            "language",
            name="unique_service_line_language"
        ),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    service_line_id: Mapped[int] = mapped_column(
        ForeignKey("service_lines.id"),
        nullable=False
    )

    language: Mapped[Language] = mapped_column(
        SQLEnum(Language, name="language_enum")
    )

    description: Mapped[str] = mapped_column(
        String(255)
    )