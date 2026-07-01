from lxml import etree
from app.document_engine.rendering.docx.xml import qn, WORD_NSMAP


def build_header(
    blocks: list[etree._Element],
) -> etree._Element:
    
    hdr = etree.Element(qn("w:hdr"), nsmap=WORD_NSMAP)

    if blocks:
        for block in blocks:
            hdr.append(block)
    else:
        etree.SubElement(hdr, qn("w:p"))

    return hdr


def build_footer(
    blocks: list[etree._Element],
) -> etree._Element:
    
    ftr = etree.Element(qn("w:ftr"), nsmap=WORD_NSMAP)

    if blocks:
        for block in blocks:
            ftr.append(block)
    else:
        etree.SubElement(ftr, qn("w:p"))

    return ftr