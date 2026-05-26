from lxml.etree import _Element

from app.document_engine.parser.context import ParserContext
from app.document_engine.parser.extractors.paragraphs import parse_paragraph
from app.document_engine.parser.models.blocks import ParagraphNode, TableCellNode, TableRowNode, TableNode
from app.document_engine.parser.namespaces import NS


def parse_table(table: _Element, context: ParserContext) -> TableNode:
    rows: list[TableRowNode] = []

    for row in table.findall("w:tr", NS):
        cells: list[TableCellNode] = []
        for cell in row.findall("w:tc", NS):
            paragraphs: list[ParagraphNode] = [
                parse_paragraph(paragraph, context)
                for paragraph in cell.findall("w:p", NS)
            ]

            cells.append(TableCellNode(blocks=paragraphs))

        rows.append(TableRowNode(cells=cells))

    return TableNode(rows=rows)