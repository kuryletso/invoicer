from typing import Optional

from dataclasses import dataclass

from app.document_engine.parser.models.inlines import RunStyle

@dataclass(slots=True, frozen=True)
class NormalizedTextStyle:
    bold: bool
    italic: bool
    underline: bool
    font_name: Optional[str]
    font_size: Optional[str]
    color: Optional[str]
    style_id: Optional[str]

    @classmethod
    def from_run_style(cls, run_style: RunStyle):        
        return cls(
            bold = run_style.bold,
            italic = run_style.italic,
            underline=run_style.underline,
            font_name=run_style.font_name,
            font_size=run_style.font_size,
            color=run_style.color,
            style_id=run_style.style_id,
        )