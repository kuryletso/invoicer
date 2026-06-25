from lxml.etree import _Element

from app.document_engine.parser.context import ParserContext
from app.document_engine.parser.extractors.paragraphs import parse_paragraph
from app.document_engine.parser.models.blocks import BlockNode, TableCellNode, TableRowNode, TableNode
from app.document_engine.parser.namespaces import NS


def parse_table(table: _Element, context: ParserContext) -> TableNode:
    rows: list[TableRowNode] = []
    table_style=context.style_resolver.resolve_table_style(table)

    for row in table.findall("w:tr", NS):
        cells: list[TableCellNode] = []
        row_style = context.style_resolver.resolve_row_style(row, table_style)

        for cell in row.findall("w:tc", NS):
            blocks: list[BlockNode] = []
            cell_style = context.style_resolver.resolve_cell_style(cell, table_style, row_style)

            for child in cell:
                if child.tag == f"{{{NS['w']}}}p":
                    blocks.append(
                        parse_paragraph(child, context)
                    )
                elif child.tag == f"{{{NS['w']}}}tbl":
                    blocks.append(
                        parse_table(child, context)
                    )
                else:
                    continue

            cells.append(
                TableCellNode(
                    blocks=blocks,
                    style=cell_style,
                    
                )
            )

        rows.append(
            TableRowNode(
                cells=cells,
                style=row_style,
            )
        )

    return TableNode(
        rows=rows,
        style=table_style,
    )