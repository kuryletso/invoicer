from app.assets.hashing import hash_bytes
from app.assets.id import generate_asset_id
from app.assets.mime import detect_mime_type
from app.assets.models import ImageAsset
from app.assets.storage import AssetStorage


class AssetService:

    def __init__(self) -> None:

        self.storage = AssetStorage()

        self.assets_by_hash: dict[str, ImageAsset] = {} # TODO: REPLACE WITH DB

    def create_image_asset(
        self,
        filename: str,
        data: bytes,
    ) -> ImageAsset:

        sha256_hash = hash_bytes(data)

        existing_asset = self.assets_by_hash.get(
            sha256_hash,
        )

        if existing_asset is not None:
            return existing_asset

        storage_path = self.storage.write(
            sha256_hash=sha256_hash,
            data=data,
        )

        asset = ImageAsset(
            id=generate_asset_id(),
            sha256=sha256_hash,
            mime_type=detect_mime_type(
                filename,
            ),
            storage_path=storage_path,
            size_bytes=len(data),
        )

        self.assets_by_hash[sha256_hash] = asset # TODO: REPLACE WITH DB

        return asset