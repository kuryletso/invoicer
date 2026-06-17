from sqlalchemy import String, JSON, Enum as SQLEnum
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

from app.document_engine.enums.enums import PlaceholderType


class PlaceholderRegistry(Base):
    __tablename__ = "placeholder_registry"

    key: Mapped[str] = mapped_column(
        String(90),
        primary_key=True,
    )

    required: Mapped[bool]

    type: Mapped[PlaceholderType] = mapped_column(
        SQLEnum(PlaceholderType),
    )

    label: Mapped[str | None] = mapped_column(
        String(30),
    )

    description: Mapped[str | None] = mapped_column(
        String(120),
    )

    active: Mapped[bool]

    columns: Mapped[list[str] | None] = mapped_column(
        JSON,
    )