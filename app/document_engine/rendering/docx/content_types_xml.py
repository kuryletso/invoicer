from lxml import etree

from app.document_engine.rendering.docx.constants import (
    CT_NS,
    CT_RELS,
    CT_XML,
)


def build_content_types(
    overrides: dict[str, str],
    extensions: dict[str, str]
) -> etree._Element:
    
    root = etree.Element(
        f"{{{CT_NS}}}Types",
        nsmap={None: CT_NS},
    )

    defaults = {"rels": CT_RELS, "xml": CT_XML, **extensions}

    for ext, ctype in defaults.items():
        d = etree.SubElement(root, f"{{{CT_NS}}}Default")
        d.set("Extension", ext)
        d.set("ContentType", ctype)

    for part_name, ctype in overrides.items():
        o = etree.SubElement(root, f"{{{CT_NS}}}Override")
        o.set("PartName", part_name)
        o.set("ContentType", ctype)

    return root