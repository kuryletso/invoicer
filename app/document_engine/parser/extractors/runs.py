from lxml.etree import _Element

from app.document_engine.parser.models.inlines import RunNode, ImageNode
from app.document_engine.parser.namespaces import NS

type ParsedInlineNode = RunNode | ImageNode

WORD_NAMESPACE = NS["w"]

def get_attr(node: _Element, attr_name: str) -> str | None:
    return node.get(f"{{{WORD_NAMESPACE}}}{attr_name}")

def extract_run_text(run: _Element) -> str:
    texts = run.findall("w:t", NS)

    return "".join(text.text or "" for text in texts)

def has_tag(node: _Element, tag: str) -> bool:
    return node.find(tag, NS) is not None

def extract_run_style_id(run_properties: _Element | None) -> str | None:
    if run_properties is None:
        return None
    
    style_node = run_properties.find("w:rStyle", NS)
    if style_node is None:
        return None
    
    return get_attr(style_node, "val")

def parse_image(run: _Element) -> ImageNode | None:
    blip = run.find(".//a:blip", NS)
    if blip is None:
        return None
    
    relationship_id = blip.get(f"{NS["r"]}embed")
    if relationship_id is None:
        return None
    
    return ImageNode(asset_id=relationship_id)

def parse_inline(run: _Element) -> list[ParsedInlineNode]:

    result = []

    image = parse_image(run)
    if image is not None:
        result.append(image)

    text = extract_run_text(run)
    if text:
        run_properties = run.find("w:rPr", NS)

        result.append(
            RunNode(
                text=extract_run_text(run),
                bold=has_tag(run_properties, "w:b") if run_properties is not None else False,
                italic=has_tag(run_properties, "w:i") if run_properties is not None else False,
                underline=has_tag(run_properties, "w:u") if run_properties is not None else False,
                style_id=extract_run_style_id(run_properties),
            )
        )

    return result