from typing import Literal

from app.document_engine.blueprint.blueprint_node import BlueprintNode
from app.document_engine.blueprint.styles import TextStyle

class TextSegment(BlueprintNode):
    type: Literal["text"] = "text"
    text: str
    style: TextStyle

class PlaceholderSegment(BlueprintNode):
    type: Literal["placeholder"] = "placeholder"
    key: str
    style: TextStyle

class ImageSegment(BlueprintNode):
    type: Literal["image"] = "image"
    asset_id: int
    width: int
    height: int