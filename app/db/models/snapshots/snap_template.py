from sqlalchemy.orm import Mapped, mapped_column


from app.db.base import Base

class SnapTemplate(Base):
    __tablename__ = "snap_templates"

    id: Mapped[int] = mapped_column(
        primary_key=True,
    )