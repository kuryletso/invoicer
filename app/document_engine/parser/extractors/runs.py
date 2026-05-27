from lxml.etree import _Element

from app.document_engine.parser.context import ParserContext
from app.document_engine.parser.models.inlines import RunNode, ImageNode
from app.document_engine.parser.namespaces import NS

type ParsedInlineNode = RunNode | ImageNode


def get_attr(node: _Element, attr_name: str) -> str | None:
    return node.get(f"{{{NS["w"]}}}{attr_name}")


def extract_run_text(run: _Element) -> str:
    texts = run.findall("w:t", NS)

    return "".join(text.text or "" for text in texts)


def parse_image(run: _Element, context: ParserContext) -> ImageNode | None:
    blip = run.find(".//a:blip", NS)
    if blip is None:
        return None
    
    relationship_id = blip.get(f"{NS["r"]}embed")
    if relationship_id is None:
        return None
    
    target = context.relationships.resolve(relationship_id)
    if target is None:
        return None
    

    internal_path = f"word/{target}"    
    image_bytes = context.archive.read_bytes(internal_path)
    asset = context.asset_service.create_image_asset(
        filename=target,
        data=image_bytes,
    )

    return ImageNode(asset_id=asset.id)


def parse_inline(run: _Element, context: ParserContext) -> list[ParsedInlineNode]:

    result = []

    image = parse_image(run, context)
    if image is not None:
        result.append(image)

    text = extract_run_text(run)
    if text:
        result.append(
            RunNode(
                text=extract_run_text(run),
                style=context.style_resolver.resolve_run_style(run),
            )
        )

    return result