from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


# SEEDING
class Language(Base):
    __tablename__ = "languages"

    code: Mapped[str] = mapped_column(
        String(3),
        primary_key=True,
    )

    label_en: Mapped[str] = mapped_column(
        String(25),
    )

    label_uk: Mapped[str] = mapped_column(
        String(25),
    )