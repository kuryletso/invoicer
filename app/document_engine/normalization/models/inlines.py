from dataclasses import dataclass

from app.document_engine.normalization.models.inline_style import NormalizedTextStyle


@dataclass(slots=True, frozen=True)
class NormalizedTextNode:
    text: str
    style: NormalizedTextStyle


@dataclass(slots=True, frozen=True)
class NormalizedImageNode:
    asset_id: str


type NormalizedInlineNode = NormalizedTextNode | NormalizedImageNode