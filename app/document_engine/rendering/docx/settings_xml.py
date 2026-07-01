from lxml import etree

from app.document_engine.rendering.docx.xml import qn, WORD_NSMAP


def build_settings(even_and_odd_headers: bool) -> etree._Element:

    settings = etree.Element(qn("w:settings"), nsmap=WORD_NSMAP)

    if even_and_odd_headers:
        etree.SubElement(settings, qn("w:evenAndOddHeaders"))
    
    return settings