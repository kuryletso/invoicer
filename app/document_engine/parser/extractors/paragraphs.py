from lxml.etree import _Element

from app.document_engine.parser.extractors.runs import parse_run
from app.document_engine.parser.models.blocks import ParagraphNode
from app.document_engine.parser.namespaces import NS

WORD_NAMESPACE = NS["w"]

def get_attr(node: _Element, attr_name: str) -> str | None:
    return node.get(f"{{{WORD_NAMESPACE}}}{attr_name}")

def extract_paragraph_style_id(paragraph_properties: _Element | None) -> str | None:
    if paragraph_properties is None:
        return None
    
    style_node = paragraph_properties.find("w:pStyle", NS)

    if style_node is None:
        return None
    
    return get_attr(style_node, "val")

def parse_paragraph(paragraph: _Element) -> ParagraphNode:
    paragraph_properties = paragraph.find("w:pPr", NS)

    runs = [
        parse_run(run)
        for run in paragraph.findall("w:r", NS)
    ]

    return ParagraphNode(
        runs=runs,
        style_id=extract_paragraph_style_id(paragraph_properties),
    )