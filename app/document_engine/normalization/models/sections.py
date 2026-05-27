from typing import Optional

from dataclasses import dataclass

from app.document_engine.normalization.models.blocks import NormalizedParagraphNode, NormalizedTableNode
from app.document_engine.normalization.models.section_style import NormalizedSectionStyle

type NormalizedBlock = NormalizedParagraphNode | NormalizedTableNode


@dataclass(slots=True, frozen=True)
class NormalizedSection:
    blocks: tuple[NormalizedBlock]
    style: NormalizedSectionStyle


@dataclass(slots=True)
class NormalizedSectionBuilder:
    blocks: list[NormalizedBlock] = []
    page_width: Optional[int] = None
    page_height: Optional[int] = None
    orientation: Optional[int] = None
    margin_header: Optional[int] = None
    margin_footer: Optional[int] = None
    margin_top: Optional[int] = None
    margin_bottom: Optional[int] = None
    margin_left: Optional[int] = None
    margin_right: Optional[int] = None