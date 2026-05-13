from typing import Optional

from sqlalchemy import String, ForeignKey, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.domain.enums import Language

class OrganizationLocalization(Base):
    __tablename__ = "organization_localizations"

    id: Mapped[int] = mapped_column(primary_key=True)

    organization_id: Mapped[int] = mapped_column(ForeignKey("organization.id"))

    language: Mapped[Language] = mapped_column(
        SQLEnum(Language, name="language_enum")
    )

    legal_name: Mapped[str] = mapped_column(String(255))

    address: Mapped[Optional[str]] = mapped_column(
        String(255),
        nullable=True
    )