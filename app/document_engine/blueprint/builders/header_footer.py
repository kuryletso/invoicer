from app.document_engine.blueprint.models.header_footer import HeaderFooterGroupBlueprint, HeaderFooterBlueprint

from app.document_engine.normalization.models.header_footer import NormalizedHeaderFooterGroup, NormalizedHeaderFooter
from app.document_engine.normalization.models.blocks import NormalizedParagraph, NormalizedTable


def hf_bp_from_bormalized(
    header_footer: NormalizedHeaderFooter | None,
) -> HeaderFooterBlueprint | None:
    
    if header_footer is None:
        return None

    blocks = []
    for block in header_footer.blocks:
        if isinstance(block, NormalizedParagraph):
            blocks.append(
                paragraph_bp_from_normalized(block),
            )

        elif isinstance(block, NormalizedTable):
            blocks.append(
                table_bp_from_normalized(block),
            )

    return HeaderFooterBlueprint(
        type=header_footer.type,
        blocks=tuple(blocks),
    )


def hf_group_bp_from_normalized(
    hf_group: NormalizedHeaderFooterGroup,
) -> HeaderFooterGroupBlueprint:
    

    return HeaderFooterGroupBlueprint(
        default=hf_bp_from_bormalized(hf_group.default),
        first=hf_bp_from_bormalized(hf_group.first),
        even=hf_bp_from_bormalized(hf_group.even),
    )