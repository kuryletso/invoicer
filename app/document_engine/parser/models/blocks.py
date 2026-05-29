from dataclasses import dataclass

from app.document_engine.enums.enums import HeaderFooterType
from app.document_engine.parser.models.inlines import RunNode, ImageNode
from app.document_engine.parser.models.header_footer import HeaderFooterNode
from app.document_engine.parser.models.styles import ParagraphStyle, TableCellStyle, TableRowStyle, TableStyle, SectionStyle

type ParsedInlineNode = RunNode | ImageNode


@dataclass(slots=True, frozen=True)
class ParagraphNode:
    inlines: list[ParsedInlineNode]
    style: ParagraphStyle


@dataclass(slots=True, frozen=True)
class TableCellNode:
    blocks: list[ParagraphNode]
    style: TableCellStyle

@dataclass(slots=True, frozen=True)
class TableRowNode:
    cells: list[TableCellNode]
    style: TableRowStyle


@dataclass(slots=True, frozen=True)
class TableNode:
    rows: list[TableRowNode]
    style: TableStyle


@dataclass(slots=True, frozen=True)
class SectionBreakNode:
    style: SectionStyle
    headers: dict[HeaderFooterType, HeaderFooterNode]
    footers: dict[HeaderFooterType, HeaderFooterNode]


type BlockNode = ParagraphNode | TableNode