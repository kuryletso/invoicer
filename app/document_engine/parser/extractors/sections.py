from lxml.etree import _Element

from app.document_engine.parser.models.blocks import SectionBreakNode
from app.document_engine.parser.namespaces import NS

WORD_NAMESPACE = NS["w"]

def get_attr(node: _Element, attr_name: str) -> str | None:
    return node.get(f"{{{WORD_NAMESPACE}}}{attr_name}")

def parse_section(section: _Element) -> SectionBreakNode:
    section_type = None
    orientation = None

    type_node = section.find("w:type", NS)
    if type_node is not None:
        section_type = get_attr(type_node, "val")

    page_size = section.find("w:pgSz", NS)

    if page_size is not None:
        orientation = get_attr(page_size, "orient")

    return SectionBreakNode(
        section_type=section_type,
        orientation=orientation,
    )