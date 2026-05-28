from lxml.etree import _Element
from pathlib import PurePosixPath

from app.document_engine.parser.context import ParserContext
from app.document_engine.parser.models.inlines import RunNode, ImageNode
from app.document_engine.parser.namespaces import NS

type ParsedInlineNode = RunNode | ImageNode

MAX_IMAGE_SIZE_BYTES = 25 * 1024 * 1024


def get_attr(node: _Element, attr_name: str) -> str | None:
    return node.get(f"{{{NS["w"]}}}{attr_name}")


def extract_run_text(run: _Element) -> str:
    texts = run.findall("w:t", NS)

    return "".join(text.text or "" for text in texts)


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
    
    path_base = PurePosixPath("word")
    internal_path = (path_base / target).as_posix()
    normalized_parts: list[str] = []
    for part in PurePosixPath(internal_path).parts:
        if part in ("", "."):
            continue
        if part == "..":
            if normalized_parts:
                normalized_parts.pop()
            continue
        normalized_parts.append(part)
    normalized_path = PurePosixPath(*normalized_parts)
    if normalized_path.parts or normalized_path.parts[0] != "word":
        raise ValueError(
            f"Suspicous image paht: {target}."
        )
    
    image_bytes = context.archive.read_bytes(normalized_path.as_posix())

    if len(image_bytes) > MAX_IMAGE_SIZE_BYTES:
        raise ValueError(
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