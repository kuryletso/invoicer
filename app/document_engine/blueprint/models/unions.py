from __future__ import annotations

from typing import TYPE_CHECKING, Annotated

from pydantic import Field

if TYPE_CHECKING:
    from app.document_engine.blueprint.models.paragraph import ParagraphBlueprint
    from app.document_engine.blueprint.models.table import TableBlueprint
    from app.document_engine.blueprint.models.segment import (
        TextSegment,
        PlaceholderSegment,
        PlaceholderJoinSegment,
        PlaceholderGroupSegment,
        ImageSegment,
    )


BlueprintSegment = Annotated[
    TextSegment
    | PlaceholderSegment
    | PlaceholderJoinSegment
    | PlaceholderGroupSegment
    | ImageSegment,
    Field(discriminator="type")
]


BlueprintBlock = Annotated[
    ParagraphBlueprint
    | TableBlueprint,
    Field(discriminator="type")
]