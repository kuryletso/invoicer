from sqlalchemy import Table, Column, ForeignKey

from app.db.base import Base

organization_representative_m2m = Table(
    "organization_representative_association",
    Base.metadata,
    Column(
        "organization_id",
        ForeignKey("organizations.id"),
        primary_key=True
    ),
    Column(
        "representative_id",
        ForeignKey("representatives.id"),
        primary_key=True
    )
)