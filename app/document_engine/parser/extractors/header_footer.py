from app.document_engine.parser.extractors.paragraphs import parse_paragraph 
from app.document_engine.parser.extractors.tables import parse_table 
from app.document_engine.parser.models.blocks import BlockNode
from app.document_engine.parser.models.header_footer import HeaderFooterType, HeaderFooterNode
from app.document_engine.parser.context import ParserContext
from app.document_engine.parser.namespaces import NS


def parse_header_footer_by_id(
    relationship_id: str,
    _type: HeaderFooterType,
    *,
    context: ParserContext,
) -> HeaderFooterNode | None:
    
    relationship = context.relationships.get(relationship_id)
    if relationship is None or relationship.target is None:
        return None
    
    try:
        root = context.archive.read_xml(relationship.target)
    except FileNotFoundError:
        return None
    
    blocks: list[BlockNode] = []

    for child in root:
        tag = child.tag

        if tag == f"{{{NS['w']}}}p":
            paragraph = parse_paragraph(child, context)
            if paragraph is not None:
                blocks.append(paragraph)

        elif tag == f"{{{NS['w']}}}tbl":
            table = parse_table(child, context)
            if table is not None:
                blocks.append(table)

    return HeaderFooterNode(
        type=_type,
        blocks=blocks,
    )