from sqlalchemy import ForeignKey, Enum as SQLEnum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.domain.enums import Language

class SnapPartyLocalization(Base):
    __tablename__ = "snap_party_localizations"

    id: Mapped[int] = mapped_column(primary_key=True)

    snap_party_id: Mapped[int] = mapped_column(
        ForeignKey("snap_parties.id")
    )

    language: Mapped[Language] = mapped_column(
        SQLEnum(Language, name="language_enum")
    )

    legal_name: Mapped[str] = mapped_column(String(255))