from typing import Literal

from app.document_engine.blueprint.models.blueprint_base import BlueprintBase


class TextStyleBlueprint(BlueprintBase):
    bold: bool
    italic: bool
    underline: bool
    font_name: str
    font_size: int      # half-points
    color: str


class TextSegment(BlueprintBase):
    type: Literal["text"] = "text"
    text: str
    style: TextStyleBlueprint


class PlaceholderSegment(BlueprintBase):
    type: Literal["placeholder"] = "placeholder"
    key: str
    style: TextStyleBlueprint


class JoinedPlaceholderSegment(BlueprintBase):
    type: Literal["placeholder_join"] = "placeholder_join"
    items: tuple[TextSegment | PlaceholderSegment, ...]
    separator: str
    style: TextStyleBlueprint


class GroupedPlaceholderSegment(BlueprintBase):
    type: Literal["placeholder_group"] = "placeholder_group"
    items: tuple[tuple[TextSegment | PlaceholderSegment, ...], ...]
    separator: str
    style: TextStyleBlueprint


class ImageSegment(BlueprintBase):
    type: Literal["image"] = "image"
    asset_id: str