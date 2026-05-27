from typing import Optional
from dataclasses import dataclass

from app.document_engine.normalization.models.inlines import NormalizedInlineNode

@dataclass(slots=True, frozen=True)
class NormalizedParagraphNode:
    inlines: tuple[NormalizedInlineNode, ...]
    style_id: Optional[str]


@dataclass(slots=True, frozen=True)
class NormalizedTableCellNode:
    blocks: tuple[NormalizedParagraphNode, ...]


@dataclass(slots=True, frozen=True)
class NormalizedTableRowNode:
    cells: tuple[NormalizedTableCellNode, ...]


@dataclass(slots=True, frozen=True)
class NormalizedTableNode:
    rows: tuple[NormalizedTableRowNode, ...]