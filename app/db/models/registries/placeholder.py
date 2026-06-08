from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class PlaceholderRegistry(Base):
    __tablename__ = "placeholder_registry"

    key: Mapped[str] = mapped_column(
        String(90),
        primary_key=True,
    )

    required: Mapped[bool]

    label: Mapped[str] = mapped_column(
        String(30),
        nullable=True,
    )

    description: Mapped[str] = mapped_column(
        String(120),
        nullable=True,
    )

    active: Mapped[bool]