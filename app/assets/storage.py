from pathlib import Path

from app.assets.paths import ASSET_STORAGE_DIR

class AssetStorage:
    def __init__(self, root: Path = ASSET_STORAGE_DIR) -> None:
        self.root = root

    def build_storage_path(self, sha256_hash: str) -> Path:
        prefix = sha256_hash[:2]
        directory = self.root / prefix
        directory.mkdir(
            parents=True,
            exist_ok=True,
        )

        return directory / sha256_hash
    

    def exists(self, sha256_hash: str) -> bool:
        return self.build_storage_path(sha256_hash).exists()
    
    
    def write(self, sha256_hash: str, data: bytes) -> Path:
        path = self.build_storage_path(sha256_hash)

        if not path.exists():
            path.write_bytes(data)

        return path