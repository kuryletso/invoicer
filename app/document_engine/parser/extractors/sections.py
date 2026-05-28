from lxml.etree import _Element

from app.document_engine.parser.models.blocks import SectionBreakNode
from app.document_engine.parser.namespaces import NS

WORD_NAMESPACE = NS["w"]


def get_attr(node: _Element, attr_name: str) -> str | None:
    return node.get(f"{{{WORD_NAMESPACE}}}{attr_name}")


def parse_section(section: _Element) -> SectionBreakNode:
    section_type = None
    orientation = None
    page_width = None
    page_height = None
    margin_header = None
    margin_footer = None
    margin_top = None
    margin_bottom = None
    margin_left = None
    margin_right = None

    type_node = section.find("w:type", NS)
    if type_node is not None:
        section_type = get_attr(type_node, "val")

    page_size = section.find("w:pgSz", NS)
    if page_size is not None:
        orientation = get_attr(page_size, "orient")
        page_width = get_attr(page_size, "w")
        page_height = get_attr(page_size, "h")

    page_margins = section.find("w:pgMar", NS)
    if page_margins is not None:
        margin_header = get_attr(page_margins, "header")
        margin_footer = get_attr(page_margins, "footer")
        margin_top = get_attr(page_margins, "top")
        margin_bottom = get_attr(page_margins, "bottom")
        margin_left = get_attr(page_margins, "left")
        margin_right = get_attr(page_margins, "right")


    return SectionBreakNode(
        section_type=section_type,
        orientation=orientation,
        page_width=page_width,
        page_height=page_height,
        margin_header=margin_header,
        margin_footer=margin_footer,
        margin_top=margin_top,
        margin_bottom=margin_bottom,
        margin_left=margin_left,
        margin_right=margin_right,
    )