from typing import Optional
from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class RunNode:
    text: str
    bold: bool
    italic: bool
    underline: bool
    style_id: Optional[str]

@dataclass(slots=True, frozen=True)
class ImageNode:
    asset_id: str
    target_path: str | None = None