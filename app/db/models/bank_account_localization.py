from sqlalchemy import ForeignKey, Enum as SQLEnum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base
from app.domain.enums import Language

class BankAccountLocalization(Base):
    __tablename__ = "bank_account_localizations"

    id: Mapped[int] = mapped_column(primary_key=True)

    bank_account_id: Mapped[int] = mapped_column(
        ForeignKey("bank_accounts.id"),
        nullable=False
    )

    language: Mapped[Language] = mapped_column(
        SQLEnum(Language, name="language_enum")
    )

    bank_name: Mapped[str] = mapped_column(String(255))

    bank_info: Mapped[str] = mapped_column(String(255))