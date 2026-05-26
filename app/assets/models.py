from dataclasses import dataclass
from pathlib import Path


@dataclass(slots=True, frozen=True)
class ImageAsset:
    id: str
    sha256: str
    mime_type: str
    storage_path: Path
    size_bytes: int