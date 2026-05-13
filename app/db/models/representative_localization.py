from sqlalchemy import ForeignKey, Enum as SQLEnum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.domain.enums import Language

class RepresentativeLocalization(Base):
    __tablename__ = "representative_localizations"

    id: Mapped[int] = mapped_column(primary_key=True)

    representative_id: Mapped[int] = mapped_column(
        ForeignKey("representatives.id"),
        nullable=False
    )

    language: Mapped[Language] = mapped_column(
        SQLEnum(Language, name="language_enum")
    )

    name: Mapped[str] = mapped_column(String(255))

    title: Mapped[str] = mapped_column(String(150))