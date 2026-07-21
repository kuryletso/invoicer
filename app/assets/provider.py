from sqlalchemy.orm import Session

from app.db.models.core.assets import Asset as AssetRow
from app.document_engine.rendering.ports import Asset


class DbAssetProvider:
    """Satisfies rendering.ports.AssetProvider, backed by the assets table."""

    def __init__(
            self,
            session: Session,
    ) -> None:
        
        self._session = session


    def get(
            self,
            asset_id: str,
    ) -> Asset | None:
        
        row = self._session.get(AssetRow, asset_id)
        if row is None:
            return None
        
        return Asset(
            data=row.data,
            mime=row.mime_type,
        )