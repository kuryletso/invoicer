from app.document_engine.blueprint.models.margins import MarginsBlueprint

from app.document_engine.normalization.models.shared import NormalizedMargins


def margins_bp_from_normalized(
    margins: NormalizedMargins,
) -> MarginsBlueprint:
    
    return MarginsBlueprint(
        top=margins.top,
        bottom=margins.bottom,
        left=margins.left,
        right=margins.right,
    )