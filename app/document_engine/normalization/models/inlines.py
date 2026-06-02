from dataclasses import dataclass


@dataclass(slots=True, frozen=True)
class NormalizedTextStyle:
    bold: bool
    italic: bool
    underline: bool
    font_name: str
    font_size: int      # half-points
    color: str


@dataclass(slots=True, frozen=True)
class NormalizedTextNode:
    text: str
    style: NormalizedTextStyle


@dataclass(slots=True, frozen=True)
class NormalizedImageNode:
    asset_id: str


type NormalizedInlineNode = NormalizedTextNode | NormalizedImageNode