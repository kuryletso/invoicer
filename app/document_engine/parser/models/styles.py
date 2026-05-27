from typing import Optional
from dataclasses import dataclass

@dataclass(slots=True, frozen=True)
class RunStyle:
    bold: Optional[bool] = None
    italic: Optional[bool] = None
    underline: Optional[bool] = None
    font_name: Optional[str] = None
    font_size: Optional[int] = None
    color: Optional[str] = None


@dataclass(slots=True, frozen=True)
class ParagraphStyle:
    alignment: Optional[str] = None
    spacing_before: Optional[int] = None
    spacing_after: Optional[int] = None
    indent_left: Optional[int] = None
    indent_right: Optional[int] = None
    keep_next: Optional[bool] = None


@dataclass(slots=True, frozen=True)
class Margins:
    top: int = 0
    bottom: int = 0
    left: int = 0
    right: int = 0

@dataclass(slots=True, frozen=True)
class TableCellStyle:
    shading: Optional[str] = None
    shading_fill: Optional[str] = None
    margins: Optional[Margins] = None
    grid_span: Optional[int] = None
    v_alignment: Optional[str] = None


@dataclass(slots=True, frozen=True)
class TableRowStyle:
    height: Optional[int] = None
    header: Optional[bool] = None


@dataclass(slots=True, frozen=True)
class TableBorderStyle:
    style: Optional[str] = None
    size: Optional[int] = None
    color: Optional[str] = None


@dataclass(slots=True, frozen=True)
class TableStyle:
    width: Optional[int] = None
    autofit: Optional[bool] = None
    border_top: Optional[TableBorderStyle] = None
    border_bottom: Optional[TableBorderStyle] = None
    border_left: Optional[TableBorderStyle] = None
    border_right: Optional[TableBorderStyle] = None
    border_inside_v: Optional[TableBorderStyle] = None
    border_inside_h: Optional[TableBorderStyle] = None
    margins: Optional[Margins] = None


@dataclass(slots=True, frozen=True)
class StyleNode:
    style_id: str
    style_type: str
    name: Optional[str] = None
    based_on: Optional[str] = None
    run_style: Optional[RunStyle] = None
    paragraph_style: Optional[ParagraphStyle] = None
    table_style: Optional[TableStyle] = None
    row_style: Optional[TableRowStyle] = None
    cell_style: Optional[TableCellStyle] = None