from dataclasses import dataclass
from typing import Optional


@dataclass(slots=True, frozen=True)
class InlineStyle:
    bold: bool
    italic: bool
    underline: bool
    style_id: Optional[str]