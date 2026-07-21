from __future__ import annotations

from sqlalchemy import String, LargeBinary
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class Asset(Base):
    __tablename__ = "assets"

    sha256: Mapped[str] = mapped_column(
        String(64),
        primary_key=True,
    )

    mime_type: Mapped[str] = mapped_column(String(255))
    
    size_bytes: Mapped[int]

    data: Mapped[bytes] = mapped_column(LargeBinary)