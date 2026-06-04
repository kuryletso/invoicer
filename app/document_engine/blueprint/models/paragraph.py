from typing import Literal

from app.document_engine.blueprint.models.blueprint_base import BlueprintBase
from app.document_engine.blueprint.models.unions import BlueprintSegment

from app.document_engine.enums.enums import ParagraphAlignment


class ParagraphStyleBlueprint(BlueprintBase):
    alignment: ParagraphAlignment
    spacing_before: int         # twips
    spacing_after: int          # twips
    indent_left: int            # twips
    indent_right: int           # twips
    keep_next: bool


class ParagraphBlueprint(BlueprintBase):
    type: Literal["paragraph"] = "paragraph"
    segments: list[BlueprintSegment]
    style: ParagraphStyleBlueprint