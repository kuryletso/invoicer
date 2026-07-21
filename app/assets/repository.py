from collections.abc import Mapping

from sqlalchemy.dialects.sqlite import insert
from sqlalchemy.orm import Session

from app.assets.service import AssetBlob
from app.db.models.core.assets import Asset


def save_assets(
        session: Session,
        bundle: Mapping[str, AssetBlob],
) -> None:
    
    for blob in bundle.values():
        stmt = insert(Asset).values(
            sha256=blob.sha256,
            mime_type=blob.mime_type,
            size_bytes=len(blob.data),
            data=blob.data,
        ).on_conflict_do_nothing(index_elements=["sha256"])

        session.execute(stmt)