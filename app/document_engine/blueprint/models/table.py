from __future__ import annotations

from typing import TYPE_CHECKING, Literal

from app.document_engine.blueprint.models.blueprint_base import BlueprintBase
from app.document_engine.blueprint.models.margins import MarginsBlueprint

from app.document_engine.enums.enums import TableCellShading, VerticalAlignment, TableWidthType, TableBorderStyleEnum

if TYPE_CHECKING:
    from app.document_engine.blueprint.models.unions import BlueprintBlock


class CellStyleBlueprint(BlueprintBase):
    shading: TableCellShading
    shading_fill: str
    margins: MarginsBlueprint
    grid_span: int
    v_alignment: VerticalAlignment


class RowStyleBlueprint(BlueprintBase):
    height: int
    header: bool


class TableWidthBlueprint(BlueprintBase):
    value: int | None
    type: TableWidthType


class TableBorderBlueprint(BlueprintBase):
    style: TableBorderStyleEnum
    size: int
    color: str


class TableStyleBlueprint(BlueprintBase):
    width: TableWidthBlueprint
    autofit: bool
    border_top: TableBorderBlueprint
    border_bottom: TableBorderBlueprint
    border_left: TableBorderBlueprint
    border_right: TableBorderBlueprint
    border_inside_v: TableBorderBlueprint
    border_inside_h: TableBorderBlueprint
    margins: MarginsBlueprint


class CellBlueprint(BlueprintBase):
    blocks: list[BlueprintBlock]
    style = CellStyleBlueprint


class RowBlueprint(BlueprintBase):
    cells: list[CellBlueprint]
    style = RowStyleBlueprint


class TableBlueprint(BlueprintBase):
    type: Literal["table"] = "table"
    rows: list[RowBlueprint]
    style: TableStyleBlueprint