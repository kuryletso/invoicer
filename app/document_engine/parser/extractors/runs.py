from lxml.etree import _Element
from pathlib import PurePosixPath

from app.document_engine.parser.context import ParserContext
from app.document_engine.parser.models.inlines import RunNode, ImageNode
from app.document_engine.parser.namespaces import NS
from app.document_engine.parser.errors import ParserSecurityError, ParserAssetError

type ParsedInlineNode = RunNode | ImageNode

MAX_IMAGE_SIZE_BYTES = 25 * 1024 * 1024


def get_attr(node: _Element, attr_name: str) -> str | None:
    return node.get(f"{{{NS["w"]}}}{attr_name}")


def extract_run_text(run: _Element) -> str:
    parts: list[str] = []

    for child in run:
        tag = child.tag

        if tag == f"{{{NS["w"]}}}t":
            if child.text:
                text = child.text or ""
                parts.append(text)

        elif tag == f"{{{NS["w"]}}}tab":
            parts.append("\t")

        elif tag == f"{{{NS["w"]}}}cr":
            parts.append("\n")

        elif tag == f"{{{NS["w"]}}}br":
            br_type = child.get(f"{{{NS["w"]}}}type")
            if br_type in (None, "textWrapping"):
                parts.append("\n")

    return "".join(parts)


def parse_image(run: _Element, context: ParserContext) -> ImageNode | None:
    blip = run.find(".//a:blip", NS)
    if blip is None:
        return None
    
    relationship_id = blip.get(f"{{{NS["r"]}}}embed")
    if relationship_id is None:
        return None
    
    target = context.relationships.resolve(relationship_id)
    if target is None:
        return None
    
    normalized_path = PurePosixPath(target)

    image_bytes = None
    try:
        image_bytes = context.archive.read_bytes(normalized_path.as_posix())
    except KeyError as e:
        raise ParserAssetError(
            f"Invalid image reference {target}."
        ) from e

    if image_bytes and len(image_bytes) > MAX_IMAGE_SIZE_BYTES:
        raise ParserSecurityError(
            f"Image exceeds maximum allowed size:"
            f"{len(image_bytes)} bytes."
        )

    asset = context.asset_service.create_image_asset(
        filename=PurePosixPath(target).name,
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
                text=text,
                style=context.style_resolver.resolve_run_style(run),
            )
        )

    return result