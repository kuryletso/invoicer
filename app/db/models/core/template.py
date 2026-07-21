from datetime import datetime, timezone

from sqlalchemy import JSON, String, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base

class Template(Base):
    __tablename__ = "templates"

    id: Mapped[int] = mapped_column(primary_key=True)

    name: Mapped[str] = mapped_column(String(255))

    type: Mapped[str] = mapped_column(String(30))       # document_type code

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc)
    )

    sections: Mapped[list[str]] = mapped_column(
        JSON,
    )

    placeholders: Mapped[dict] = mapped_column(
        JSON,
    )

    config: Mapped[dict[str, str | int | None]] = mapped_column(
        JSON,
    )