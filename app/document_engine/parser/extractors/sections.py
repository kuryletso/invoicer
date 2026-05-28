from lxml.etree import _Element

from app.document_engine.parser.models.blocks import SectionBreakNode
from app.document_engine.parser.models.styles import SectionStyle, Margins
from app.document_engine.parser.namespaces import NS

WORD_NAMESPACE = NS["w"]
RELATIONSHIP_NAMESPACE = NS["r"]


def get_attr(node: _Element, attr_name: str) -> str | None:
    return node.get(f"{{{WORD_NAMESPACE}}}{attr_name}")


def get_int_attr(node: _Element, attr_name: str) -> int | None:
    value = get_attr(node, attr_name)
    if value is None:
        return None
    
    try:
        return int(value)
    except ValueError:
        return None


def get_relationship_id(node: _Element) -> str | None:
    return node.get(f"{{{RELATIONSHIP_NAMESPACE}}}id")

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
    default_header_id = None
    even_header_id = None
    first_header_id = None
    default_footer_id = None
    even_footer_id = None
    first_footer_id = None

    type_node = section.find("w:type", NS)
    if type_node is not None:
        section_type = get_attr(type_node, "val")

    page_size = section.find("w:pgSz", NS)
    if page_size is not None:
        orientation = get_attr(page_size, "orient")
        page_width = get_int_attr(page_size, "w")
        page_height = get_int_attr(page_size, "h")

    page_margins = section.find("w:pgMar", NS)
    if page_margins is not None:
        margin_header = get_int_attr(page_margins, "header")
        margin_footer = get_int_attr(page_margins, "footer")
        margin_top = get_int_attr(page_margins, "top")
        margin_bottom = get_int_attr(page_margins, "bottom")
        margin_left = get_int_attr(page_margins, "left")
        margin_right = get_int_attr(page_margins, "right")

    for header_reference in section.findall("w:headerReference", NS):
        reference_type = get_attr(header_reference, "type")
        relationship_id = get_relationship_id(header_reference)

        if relationship_id is None:
            continue

        match reference_type:
            case "default":
                default_header_id = relationship_id
            case "even":
                even_header_id = relationship_id
            case "first":
                first_header_id = relationship_id

    for footer_rederence in section.findall("w:footerReference", NS):
        reference_type = get_attr(footer_rederence, "type")
        relationship_id = get_relationship_id(footer_rederence)

        if relationship_id is None:
            continue

        match reference_type:
            case "default":
                default_footer_id = relationship_id
            case "even":
                even_footer_id = relationship_id
            case "first":
                first_footer_id = relationship_id

    return SectionBreakNode(
        style=SectionStyle(
            section_type=section_type,
            page_width=page_width,
            page_height=page_height,
            orientation=orientation,
            margin_header=margin_header,
            margin_footer=margin_footer,
            margins=Margins(
                top=margin_top,
                bottom=margin_bottom,
                left=margin_left,
                right=margin_right,
            ),
            default_header_id=default_header_id,
            even_header_id=even_header_id,
            first_header_id=first_header_id,
            default_footer_id=default_footer_id,
            even_footer_id=even_footer_id,
            first_footer_id=first_footer_id,
        )
    )