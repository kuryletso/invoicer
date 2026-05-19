from sqlalchemy import String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.domain.enums import Language

class ServiceLineLocalization(Base):
    __tablename__ = "service_line_localizations"

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