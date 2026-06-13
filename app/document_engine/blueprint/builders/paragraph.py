from app.document_engine.blueprint.template_builder import TemplateBuilderContext
from app.document_engine.blueprint.builders.segments import image_segment_bp_from_normalized, extract_segments

from app.document_engine.blueprint.models.paragraph import ParagraphBlueprint, ParagraphStyleBlueprint

from app.document_engine.normalization.models.blocks import NormalizedParagraph, NormalizedParagraphStyle
from app.document_engine.normalization.models.inlines import NormalizedTextNode, NormalizedImageNode


def paragraph_style_bp_from_normalized(
    style: NormalizedParagraphStyle,
) -> ParagraphStyleBlueprint:
    
    return ParagraphStyleBlueprint(
        alignment=style.alignment,
        spacing_before=style.spacing_before,
        spacing_after=style.spacing_after,
        indent_left=style.indent_left,
        indent_right=style.indent_right,
        keep_next=style.keep_next,
    )


def paragraph_bp_from_normalized(
    paragraph: NormalizedParagraph,
    template_builder_context: TemplateBuilderContext,
) -> ParagraphBlueprint:
    
    segments = []
    for inline in paragraph.inlines:
        if isinstance(inline, NormalizedTextNode):
            segments.extend(
                extract_segments(inline, template_builder_context),
            )

        elif isinstance(inline, NormalizedImageNode):
            segments.append(
                image_segment_bp_from_normalized(inline),
            )

    style = paragraph_style_bp_from_normalized(paragraph.style)

    return ParagraphBlueprint(
        type="paragraph",
        segments=tuple(segments),
        style=style,
    )