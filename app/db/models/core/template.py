from sqlalchemy import JSON
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Template(Base):
    __tablename__ = "templates"

    id: Mapped[int] = mapped_column(primary_key=True)

    sections: Mapped[list[str]] = mapped_column(
        JSON,
    )

    placeholders: Mapped[list[str]] = mapped_column(
        JSON,
    )

    config: Mapped[dict[str, str | int | None]] = mapped_column(
        JSON,
    )