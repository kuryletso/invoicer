from typing import Optional
from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class StyleNode:
    style_id: str
    style_type: str
    name: Optional[str]