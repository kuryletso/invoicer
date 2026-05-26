from typing import Optional
from dataclasses import dataclass

from app.document_engine.parser.models.inlines import RunNode, ImageNode

ParsedInlineNode = RunNode | ImageNode


@dataclass(slots=True, frozen=True)
class ParagraphNode:
    inlines: list[ParsedInlineNode]
    style_id: Optional[str]


@dataclass(slots=True, frozen=True)
class TableCellNode:
    blocks: list[ParagraphNode]


@dataclass(slots=True, frozen=True)
class TableRowNode:
    cells: list[TableCellNode]


@dataclass(slots=True, frozen=True)
class TableNode:
    rows: list[TableRowNode]


@dataclass(slots=True, frozen=True)
class SectionBreakNode:
    section_type: Optional[str]
    orientation: Optional[str]