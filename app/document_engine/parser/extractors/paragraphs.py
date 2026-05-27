from lxml.etree import _Element

from app.document_engine.parser.context import ParserContext
from app.document_engine.parser.extractors.runs import parse_inline
from app.document_engine.parser.models.blocks import ParagraphNode
from app.document_engine.parser.namespaces import NS

WORD_NAMESPACE = NS["w"]


def parse_paragraph(paragraph: _Element, context: ParserContext) -> ParagraphNode:
    inlines = []
    for run in paragraph.findall("w:r", NS):
        inlines.extend(parse_inline(run, context))

    return ParagraphNode(
        inlines=inlines,
        style=context.style_resolver.resolved_paragraph_style(paragraph),
    )