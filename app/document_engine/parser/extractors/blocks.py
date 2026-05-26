from collections.abc import Iterator
from lxml.etree import _Element

from app.document_engine.parser.namespaces import NS

BlockEvent = tuple[str, _Element]


def iter_blocks(body: _Element) -> Iterator[BlockEvent]:
    for child in body:
        tag = child.tag.split("}")[-1]

        match tag:
            case "p":
                yield "paragraph", child
                paragraph_properties = child.find("w:pPr", NS)

                if paragraph_properties is None:
                    continue

                section = paragraph_properties.find("w:sectPr", NS)

                if section is not None:
                    yield "section", section

            case "tbl":
                yield "table", child

            case "sectPr":
                yield "section", child