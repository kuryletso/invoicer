from typing import cast

from app.document_engine.normalization.models.header_footer import NormalizedHeaderFooter, NormalizedHeaderFooterGroup
from app.document_engine.normalization.models.blocks import NormalizedBlock
from app.document_engine.normalization.models.sections import NormalizedSection, NormalizedSectionStyle
from app.document_engine.normalization.normalizers.paragraphs import normalize_paragraph
from app.document_engine.normalization.normalizers.tables import normalize_table
from app.document_engine.normalization.normalizers.shared import normalize_margins
from app.document_engine.normalization.style_defaults import DEAFAULT_SECTION_STYLE
from app.document_engine.normalization.errors import NormalizationFormatError

from app.document_engine.parser.models.blocks import SectionBreakNode, ParagraphNode, TableNode
from app.document_engine.parser.models.header_footer import HeaderFooterNode

from app.document_engine.enums.enums import SectionType, PageOrientation, HeaderFooterType
from app.document_engine.utils.overlay_dataclass import overlay_dataclass_strict


def normalize_headers_footers(
    obj: dict[HeaderFooterType, HeaderFooterNode],
) -> NormalizedHeaderFooterGroup:

    preset = {}

    for t in (
        HeaderFooterType.DEFAULT,
        HeaderFooterType.EVEN,
        HeaderFooterType.FIRST,
    ):

        normalized = None
        parsed = obj.get(t)

        if parsed is not None:
            blocks = []
            for block in parsed.blocks:
                if isinstance(block, ParagraphNode):
                    blocks.append(
                        normalize_paragraph(block),
                    )

                elif isinstance(block, TableNode):
                    blocks.append(
                        normalize_table(block),
                    )

                else:
                    raise NormalizationFormatError(
                        f"Unknown item type in header/footer {parsed}: {type(block).__name__}."
                    )

            normalized = NormalizedHeaderFooter(
                type=t,
                blocks=tuple(blocks),
            )

        preset[t.value] = normalized
        
    return NormalizedHeaderFooterGroup(
        **preset,
    )


def normalize_section(
    ancestor: SectionBreakNode,
    blocks: list[NormalizedBlock],
) -> NormalizedSection:
    
    try:
        section_type = SectionType(ancestor.style.section_type) \
            if ancestor.style.section_type is not None \
            else None
    except ValueError as e:
        raise NormalizationFormatError(
            f"Invalid section type: {ancestor.style.section_type}."
        ) from e
    
    try:
        orientation = PageOrientation(ancestor.style.orientation) \
            if ancestor.style.orientation is not None \
            else None
    except ValueError as e:
        raise NormalizationFormatError(
            f"Invalid orientation type: {ancestor.style.orientation}."
        ) from e

    
    parsed_style = NormalizedSectionStyle(
        # Fields may be None here; overlay_dataclass_strict() immediately applies defaults.
        section_type=cast(SectionType, section_type),
        page_width=cast(int, ancestor.style.page_width),
        page_height=cast(int, ancestor.style.page_height),
        orientation=cast(PageOrientation, orientation),
        margin_header=cast(int, ancestor.style.margin_header),
        margin_footer=cast(int, ancestor.style.margin_footer),
        margins=normalize_margins(ancestor.style.margins),
    )

    normalized_style = overlay_dataclass_strict(
        DEAFAULT_SECTION_STYLE,
        parsed_style,
    )

    return NormalizedSection(
        blocks=tuple(blocks),
        headers=normalize_headers_footers(ancestor.headers),
        footers=normalize_headers_footers(ancestor.footers),
        style=normalized_style,
    )