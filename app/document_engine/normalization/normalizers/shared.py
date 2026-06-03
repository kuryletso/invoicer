from app.document_engine.normalization.models.shared import NormalizedMargins
from app.document_engine.normalization.errors import NormalizationFormatError

from app.document_engine.parser.models.styles import Margins

from app.document_engine.utils.overlay_dataclass import overlay_dataclass_strict


from typing import cast


def normalize_margins(
    margins: Margins | None,
    default: NormalizedMargins,
) -> NormalizedMargins:
    
    if margins is None:
        return default

    if isinstance(margins.top, int) and margins.top < 0:
        raise NormalizationFormatError(
            f"Margins can't be negative, {margins.top=}."
        )
    if isinstance(margins.bottom, int) and margins.bottom < 0:
        raise NormalizationFormatError(
            f"Margins can't be negative, {margins.bottom=}."
        )
    if isinstance(margins.left, int) and margins.left < 0:
        raise NormalizationFormatError(
            f"Margins can't be negative, {margins.left=}."
        )
    if isinstance(margins.right, int) and margins.right < 0:
        raise NormalizationFormatError(
            f"Margins can't be negative, {margins.right=}."
        )

    parsed_margins = NormalizedMargins(
        # Fields may be None here; overlay_dataclass_strict() immediately applies defaults.
        top=cast(int, margins.top),
        bottom=cast(int, margins.bottom),
        left=cast(int, margins.left),
        right=cast(int, margins.right),
    )

    return overlay_dataclass_strict(
        default,
        parsed_margins,
    )