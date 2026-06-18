from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from app.document_engine.enums.enums import HeaderFooterType

if TYPE_CHECKING:
    from app.document_engine.parser.models.blocks import BlockNode


@dataclass(slots=True, frozen=True)
class HeaderFooterNode:
    type: HeaderFooterType
    blocks: list[BlockNode]