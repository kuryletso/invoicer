from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass

from app.assets.hashing import hash_bytes
from app.assets.mime import detect_mime_type


@dataclass(slots=True, frozen=True)
class AssetBlob:
    sha256: str
    mime_type: str
    data: bytes


class AssetCollector:
    """Accumulates image bytes during single parse, content-addressed by sha256."""

    def __init__(self) -> None:
        self._assets: dict[str, AssetBlob] = {}

    def add(
            self,
            filename: str,
            data: bytes,
    ) -> str:
        
        digest = hash_bytes(data)
        if digest not in self._assets:
            self._assets[digest] = AssetBlob(
                sha256=digest,
                mime_type=detect_mime_type(filename),
                data=data,
            )

        return digest       # serves as an asset_id
    

    @property
    def bundle(self) -> Mapping[str, AssetBlob]:
        return self._assets