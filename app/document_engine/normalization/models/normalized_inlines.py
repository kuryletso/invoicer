from dataclasses import dataclass

from app.document_engine.normalization.models.inline_style import InlineStyle

@dataclass(slots=True, frozen=True)
class NormalizedTextNode:
    text: str
    style: InlineStyle

@dataclass(slots=True, frozen=True)
class NormalizedPlaceholderNode:
    key: str
    style: InlineStyle

@dataclass(slots=True, frozen=True)
class NormalizedPlaceholderGroupNode:
    items: list[str | NormalizedPlaceholderNode]
    separator: str


type NormalizedInlineNode = (
    NormalizedTextNode
    | NormalizedPlaceholderNode
    | NormalizedPlaceholderGroupNode
)