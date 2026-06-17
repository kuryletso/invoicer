from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from pydantic import Field

if TYPE_CHECKING:
    from app.document_engine.blueprint.models.paragraph import ParagraphBlueprint
    from app.document_engine.blueprint.models.table import TableBlueprint, TablePlaceholder
    from app.document_engine.blueprint.models.segment import (
        TextSegment,
        PlaceholderSegment,
        JoinedPlaceholderSegment,
        GroupedPlaceholderSegment,
        ImageSegment,
    )


BlueprintSegment = Annotated[
    TextSegment
    | PlaceholderSegment
    | JoinedPlaceholderSegment
    | GroupedPlaceholderSegment
    | ImageSegment,
    Field(discriminator="type")
]


BlueprintBlock = Annotated[
    ParagraphBlueprint
    | TableBlueprint
    | TablePlaceholder,
    Field(discriminator="type")
]