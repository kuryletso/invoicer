from pydantic import BaseModel
from typing import Optional

from app.document_engine.enums.enums import HorizontalAlignment, VerticalAlignment

class ParagraphStyle(BaseModel):
    style_name: Optional[str] = None
    alignment: Optional[HorizontalAlignment] = None
    left_indent: Optional[int] = None
    right_indent: Optional[int] = None
    line_spacing: Optional[float] = None
    space_before: Optional[float] = None
    space_after: Optional[float] = None

class TextStyle(BaseModel):
    bold: Optional[bool] = None
    italic: Optional[bool] = None
    underline: Optional[bool] = None
    strike: Optional[bool] = None
    font_name: Optional[str] = None
    font_size: Optional[float] = None
    color: Optional[str] = None
    highlight: Optional[str] = None
    all_caps: Optional[bool] = None
    small_caps: Optional[bool] = None

class TableStyle(BaseModel):
    autofit: Optional[bool] = None
    alignment: Optional[HorizontalAlignment] = None

class RowStyle(BaseModel):
    height: Optional[float] = None

class CellStyle(BaseModel):
    vertical_alignment: Optional[VerticalAlignment] = None