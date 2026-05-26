from lxml.etree import _Element

from app.document_engine.parser.models.styles import StyleNode
from app.document_engine.parser.namespaces import NS

WORD_NAMESPACE = NS["w"]

def get_attr(node: _Element, attr_name: str) -> str | None:
    return node.get(f"{{{WORD_NAMESPACE}}}{attr_name}")

def parse_styles(styles_root: _Element) -> dict[str, StyleNode]:
    styles: dict[str, StyleNode] = {}

    for style in styles_root.findall("w:style", NS):
        style_id = get_attr(style, "styleId")
        style_type = get_attr(style, "type")

        if style_id is None or style_type is None:
            continue

        name_node = style.find("w:name", NS)
        name = None

        if name_node is not None:
            name = get_attr(name_node, "val")

        styles[style_id] = StyleNode(
            style_id=style_id,
            style_type=style_type,
            name=name,
        )

    return styles