from app.document_engine.normalization.models.blocks import NormalizedParagraphNode
from app.document_engine.normalization.models.inlines import NormalizedTextNode, NormalizedImageNode, NormalizedInlineNode
from app.document_engine.normalization.models.inline_style import NormalizedTextStyle

from app.document_engine.parser.models.blocks import ParagraphNode
from app.document_engine.parser.models.inlines import RunNode, RunStyle, ImageNode


def normalize_text_style(run_style: RunStyle) -> NormalizedTextStyle:
    return NormalizedTextStyle(
        bold=run_style.bold,
        italic=run_style.italic,
        underline=run_style.underline,
        font_name=run_style.font_name,
        font_size=run_style.font_size,
        color=run_style.color,
        style_id=run_style.style_id,
    )


def normalize_paragraph(paragraph: ParagraphNode) -> NormalizedParagraphNode:
    normalized_inlines: list[NormalizedInlineNode] = []
    current_text = ""
    current_style: RunStyle | None = None

    def flush_text() -> None:
        nonlocal current_text, current_style

        if current_style is None or not current_text:
            return
        
        normalized_inlines.append(
            NormalizedTextNode(
                text=current_text,
                style=normalize_text_style(current_style),
            )
        )

        current_text = ""
        current_style = None

    for node in paragraph.inlines:
        if isinstance(node, RunNode):
            if current_style is not None and current_style == node.style:
                current_text += node.text
            else:
                flush_text()
                current_text = node.text
                current_style = node.style

        elif isinstance(node, ImageNode):
            flush_text()
            normalized_inlines.append(
                NormalizedImageNode(asset_id=node.asset_id)
            )

        else:
            raise TypeError(
                f"Unsupported inline node type: {type(node).__name__}."
            )
        
    flush_text()

    return NormalizedParagraphNode(
        inlines=tuple(normalized_inlines),
        style_id=paragraph.style_id,
    )