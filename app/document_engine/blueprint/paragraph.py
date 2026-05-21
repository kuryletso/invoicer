from typing import Literal

from app.document_engine.blueprint.blueprint_node import BlueprintNode
from app.document_engine.blueprint.styles import ParagraphStyle
from app.document_engine.blueprint.unions import Segment

class ParagraphBlueprint(BlueprintNode):
    type: Literal["paragraph"] = "paragraph"
    style: ParagraphStyle
    segments: list[Segment]