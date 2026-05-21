from __future__ import annotations

from typing import TYPE_CHECKING, Annotated, Union
if TYPE_CHECKING:
    from app.document_engine.blueprint.paragraph import ParagraphBlueprint
    from app.document_engine.blueprint.table import TableBlueprint
    from app.document_engine.blueprint.segment import TextSegment, PlaceholderSegment, ImageSegment

from pydantic import Field

Segment = Annotated[
    Union[
        TextSegment,
        PlaceholderSegment,
        ImageSegment,
    ],
    Field(discriminator="type")
]

Block = Annotated[
    Union[
        ParagraphBlueprint,
        TableBlueprint,
    ],
    Field(discriminator="type")
]