from __future__ import annotations

from typing import TYPE_CHECKING, Literal
if TYPE_CHECKING:
    from app.document_engine.blueprint.unions import Block

from pydantic import BaseModel

from app.document_engine.blueprint.blueprint_node import BlueprintNode 
from app.document_engine.blueprint.styles import TableStyle, RowStyle, CellStyle

class CellBlueprint(BaseModel):
    style = CellStyle
    blocks: list[Block]

class RowBlueprint(BaseModel):
    style = RowStyle
    cells: list[CellBlueprint]

class TableBlueprint(BlueprintNode):
    type: Literal["table"] = "table"
    style: TableStyle
    rows: list[RowBlueprint]