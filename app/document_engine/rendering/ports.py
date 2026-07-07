from dataclasses import dataclass
from typing import Protocol


@dataclass(slots=True, frozen=True)
class Asset:
    data: bytes
    mime: str


class AssetProvider(Protocol):
    def get(self, asset_id: str) -> Asset | None:
        ...